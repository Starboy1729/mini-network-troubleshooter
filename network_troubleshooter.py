import concurrent.futures
import socket
import time


def troubleshoot(host, port):
    """Test connectivity to a single TCP port with detailed diagnostics."""
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
        with socket.create_connection((host, port), timeout=5):
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


def test_single_port_worker(host, port, timeout=3):
    """Helper worker function to test a single port inside a thread."""
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            elapsed = (time.perf_counter() - start) * 1000
            return port, "OPEN", f"connection successful ({elapsed:.2f} ms)"
    except socket.timeout:
        return port, "TIMEOUT", "connection timed out"
    except OSError as error:
        return port, "CLOSED/UNREACHABLE", str(error)


def test_multiple_ports(host, ports):
    """Test TCP connectivity to a list of ports concurrently (all at once)."""
    print("\nMultiple-Port Concurrent Scan")
    print("-" * 30)
    print(f"Host: {host}")
    print(f"Scanning {len(ports)} port(s) simultaneously...\n")

    start_total = time.perf_counter()

    # ThreadPoolExecutor launches background threads to check all ports at once.
    # max_workers=len(ports) ensures every port gets its own thread instantly.
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=len(ports)
    ) as executor:
        # Submit all tasks to the thread pool
        futures = {
            executor.submit(test_single_port_worker, host, port): port
            for port in ports
        }

        # Print results as each thread finishes (faster ports print first)
        for future in concurrent.futures.as_completed(futures):
            port, status, message = future.result()
            print(f"[{status}] Port {port}: {message}")

    elapsed_total = (time.perf_counter() - start_total) * 1000
    print(f"\nScan complete in {elapsed_total:.2f} ms total.")


def main():
    host = input("Enter a hostname or IP (e.g. example.com): ").strip()

    if not host or "://" in host or "/" in host:
        print("Please enter a valid hostname or IP only, without URL paths.")
        return

    print("\nChoose a test:")
    print("1. Test a single TCP port")
    print("2. Test multiple TCP ports (Concurrent)")

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
            "Enter ports separated by commas (e.g. 80,443,8080): "
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
