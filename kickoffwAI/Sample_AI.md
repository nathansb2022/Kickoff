# Sample

Generated from tryhackme.com's box wonderland

# Vulnerability Report

## Summary

The target system at IP address 10.10.90.216 was scanned for vulnerabilities. The system appears to be running a Linux operating system with an OpenSSH server and a Golang net/http server. The scan revealed several potential vulnerabilities and areas of concern.

## Detailed Findings

### Open Ports

The following ports were found to be open:

- Port 22: OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
- Port 80: Golang net/http server (Go-IPFS json-rpc or InfluxDB API)

### SSH Vulnerabilities

The OpenSSH server on port 22 may be vulnerable due to the use of potentially weak RSA, ECDSA, and ED25519 keys.

### HTTP Vulnerabilities

The Golang net/http server on port 80 may be vulnerable due to the following issues:

- The server supports the GET, HEAD, POST, and OPTIONS methods, which could potentially be exploited.
- The server's HTTP title is "Follow the white rabbit." This could potentially be a clue or hint for further exploitation.

### Web Application Vulnerabilities

The web application hosted on the server may be vulnerable due to the following issues:

- Missing Anti-clickjacking Header
- X-Content-Type-Options Header Missing
- Content Security Policy (CSP) Header Not Set
- Permissions Policy Header Not Set
- HTTP Only Site

### Directory Enumeration

The following directories were found on the server:

- /img
- /index.html
- /poem
- /r

These directories could potentially contain sensitive information or further attack vectors.

## Recommendations

- Update the OpenSSH server to the latest version and consider using stronger key algorithms.
- Limit the methods supported by the Golang net/http server and ensure that it is updated to the latest version.
- Implement the missing headers in the web application to mitigate potential attacks.
- Review the contents of the discovered directories for sensitive information and remove or secure as necessary.
