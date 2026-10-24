
# Mini Network Troubleshooter

A beginner-friendly Python project for diagnosing basic network connectivity issues.

## Features

- Resolves hostnames using DNS.
- Displays resolved IP addresses.
- Tests TCP connectivity to a specified port.
- Measures TCP connection establishment time.
- Handles common DNS and connection errors.

## Requirements

- Python 3.8 or newer
- Network access to the target host
- No third-party Python packages required

## How to Run

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

   ```bash
   python network_troubleshooter.py
   ```

4. Enter a hostname, such as `example.com`.
5. Enter a TCP port, or press Enter to use port `443` (HTTPS).

## Example Output

```text
Mini Network Troubleshooter
------------------------------
Host: example.com
TCP port: 443

[PASS] DNS resolution successful
       IP address: example IP address

Checking TCP port 443...
[PASS] TCP connection successful
       Connection time: 25.00 ms

Troubleshooting complete.
```

*Example output is illustrative; actual results will vary.*

## What I Learned

- DNS resolution
- TCP connections and port numbers
- Connection timeouts
- Python exception handling
- Basic network troubleshooting

## Limitations

A failed connection does not always mean a server is down. Firewalls, blocked ports, routing problems, and other network settings can cause failures. Connection time measures TCP connection establishment, not full webpage loading time.

## License

No license has been specified yet.
