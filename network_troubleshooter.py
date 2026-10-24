
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


def test_multiple_ports(host, ports):
    """Test TCP connectivity to a selected list of ports."""
    print("\nMultiple-Port Test")
    print("-" * 30)
    print(f"Host: {host}\n")

    for port in ports:
        start = time.perf_counter()

        try:
            with socket.create_connection((host, port), timeout=3):
                elapsed = (time.perf_counter() - start) * 1000
                print(
                    f"[OPEN] Port {port}: connection successful "
                    f"({elapsed:.2f} ms)"
                )

        except socket.timeout:
            print(f"[TIMEOUT] Port {port}: connection timed out")

        except OSError as error:
            print(f"[CLOSED/UNREACHABLE] Port {port}: {error}")

    print("\nMultiple-port test complete.")


def main():
    host = input("Enter a hostname (e.g. example.com): ").strip()

    if not host or "://" in host or "/" in host:
        print("Please enter a hostname only, without a URL path.")
        return

    print("\nChoose a test:")
    print("1. Test a single TCP port")
    print("2. Test multiple TCP ports")

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
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

    elif choice == "2":
        ports_text = input(
            "Enter ports separated by commas (e.g. 80,443): "
        ).strip()

        try:
            ports = [int(item.strip()) for item in ports_text.split(",")]
        except ValueError:
            print("Ports must be numbers separated by commas.")
            return

        if not ports or any(not 1 <= port <= 65535 for port in ports):
            print("Each port must be between 1 and 65535.")
            return

        if len(ports) > 20:
            print("Please test no more than 20 ports at a time.")
            return

        if len(set(ports)) != len(ports):
            print("Please do not enter duplicate ports.")
            return

        test_multiple_ports(host, ports)

    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()

