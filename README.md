
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


## Troubleshooting Tips

### DNS Resolution Failed
- Check that the hostname is spelled correctly.
- Verify that DNS resolution is available on your network.
- Try another known hostname to compare results.

### Connection Timed Out
- The destination may be unreachable or filtering traffic.
- A firewall or network policy may be blocking the connection.
- Check whether the selected TCP port is accessible.

### Connection Failed
- Verify that the hostname and port are correct.
- The destination service may be unavailable.
- A connection refusal can indicate that no service is accepting connections on that port.

## Example Test Cases

| Hostname | Port | What it tests |
|---|---:|---|
| example.com | 443 | DNS and HTTPS-port connectivity |
| google.com | 443 | DNS and HTTPS-port connectivity |
| localhost | 1 | A local connection attempt that may fail |

Results depend on network conditions, DNS responses, and firewall policies.

## Project Status

The tool has been tested in GitHub Codespaces with successful DNS resolution and TCP connectivity checks.

## Future Improvements

- Add command-line arguments for hostnames and ports.
- Export diagnostic results to a text file.
- Add an option to test multiple hosts.
- Improve the summary of common network errors.
