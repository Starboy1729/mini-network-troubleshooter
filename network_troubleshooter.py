
import socket
import time


def troubleshoot(host, port):
    print("\nMini Network Troubleshooter")
    print("-" * 30)
    print(f"Host: {host}")
    print(f"TCP port: {port}\n")

    # Step 1: DNS lookup
    try:
        addresses = socket.getaddrinfo(host, None)
        unique_ips = sorted({item[4][0] for item in addresses})

        print("[PASS] DNS resolution successful")
        for ip in unique_ips:
            print(f"       IP address: {ip}")

    except socket.gaierror:
        print("[FAIL] DNS resolution failed")
        print("       Check the hostname or DNS settings.")
        return

    # Step 2: TCP connectivity test
    print(f"\nChecking TCP port {port}...")
    start = time.perf_counter()

    try:
        with socket.create_connection(
            (host, port), timeout=5
        ):
            elapsed = (time.perf_counter() - start) * 1000
            print("[PASS] TCP connection successful")
            print(f"       Connection time: {elapsed:.2f} ms")

    except socket.timeout:
        print("[FAIL] Connection timed out")
        print("       The host may be unreachable or filtering traffic.")

    except OSError as error:
        print("[FAIL] TCP connection failed")
        print(f"       Reason: {error}")

    print("\nTroubleshooting complete.")


def main():
    host = input("Enter a hostname (e.g. example.com): ").strip()

    if not host or "://" in host or "/" in host:
        print("Please enter a hostname only, without a URL path.")
        return

    port_text = input("Enter TCP port (default 443): ").strip()

    try:
        port = int(port_text) if port_text else 443
    except ValueError:
        print("Port must be a number.")
        return

    if not 1 <= port <= 65535:
        print("Port must be between 1 and 65535.")
        return

    troubleshoot(host, port)


if __name__ == "__main__":
    main()
