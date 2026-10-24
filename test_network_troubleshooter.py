
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from contextlib import redirect_stdout

import network_troubleshooter as nt


class TestNetworkTroubleshooter(unittest.TestCase):

    @patch("network_troubleshooter.socket.getaddrinfo")
    @patch("network_troubleshooter.socket.create_connection")
    def test_successful_connection(self, mock_connection, mock_dns):
        mock_dns.return_value = [
            (None, None, None, None, ("93.184.216.34", 0))
        ]

        mock_connection.return_value.__enter__.return_value = MagicMock()

        output = StringIO()
        with redirect_stdout(output):
            nt.troubleshoot("example.com", 443)

        self.assertIn("DNS resolution successful", output.getvalue())
        self.assertIn("TCP connection successful", output.getvalue())

    @patch("network_troubleshooter.socket.getaddrinfo")
    def test_dns_failure(self, mock_dns):
        mock_dns.side_effect = nt.socket.gaierror("DNS failed")

        output = StringIO()
        with redirect_stdout(output):
            nt.troubleshoot("invalid.example", 443)

        self.assertIn("DNS resolution failed", output.getvalue())

    @patch("network_troubleshooter.socket.getaddrinfo")
    @patch("network_troubleshooter.socket.create_connection")
    def test_connection_timeout(self, mock_connection, mock_dns):
        mock_dns.return_value = [
            (None, None, None, None, ("93.184.216.34", 0))
        ]
        mock_connection.side_effect = nt.socket.timeout("Timed out")

        output = StringIO()
        with redirect_stdout(output):
            nt.troubleshoot("example.com", 443)

        self.assertIn("Connection timed out", output.getvalue())

    @patch("network_troubleshooter.socket.getaddrinfo")
    @patch("network_troubleshooter.socket.create_connection")
    def test_connection_os_error(self, mock_connection, mock_dns):
        mock_dns.return_value = [
            (None, None, None, None, ("93.184.216.34", 0))
        ]
        mock_connection.side_effect = OSError("Connection refused")

        output = StringIO()
        with redirect_stdout(output):
            nt.troubleshoot("example.com", 443)

        self.assertIn("TCP connection failed", output.getvalue())

    @patch("builtins.input", side_effect=["", "443"])
    @patch("builtins.print")
    def test_empty_hostname_rejected(self, mock_print, mock_input):
        nt.main()

        printed_text = " ".join(
            str(call) for call in mock_print.call_args_list
        )
        self.assertIn("hostname only", printed_text)

    @patch("builtins.input", side_effect=["example.com", "abc"])
    @patch("builtins.print")
    def test_non_numeric_port_rejected(self, mock_print, mock_input):
        nt.main()

        printed_text = " ".join(
            str(call) for call in mock_print.call_args_list
        )
        self.assertIn("Port must be a number", printed_text)

    @patch("builtins.input", side_effect=["example.com", "70000"])
    @patch("builtins.print")
    def test_out_of_range_port_rejected(self, mock_print, mock_input):
        nt.main()

        printed_text = " ".join(
            str(call) for call in mock_print.call_args_list
        )
        self.assertIn("Port must be between 1 and 65535", printed_text)


if __name__ == "__main__":
    unittest.main()
