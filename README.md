# Kickoff
Simple automation and enumeration script for CTF environments.



Simple Python script to kickoff a few basic commands in a CTF environment.

Requires Rustscan to be installed in a docker container, nmap, gobuster, and dirb/big.txt.

Specifically, run Rustscan:1.10.0 or change to accomodate.

Example Usage: python3 kickoff.py 10.10.10.10 8000 OR python3 kickoff.py 10.10.10.10
