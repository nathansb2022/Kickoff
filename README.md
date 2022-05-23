# Kickoff
Simple automation and enumeration script for CTF environments.


Python script to kickoff a few basic commands in a CTF environment. It requires Rustscan to be installed in a docker container, nmap, gobuster, and dirb/big.txt. Specifically, run Rustscan:1.10.0 or change to accomodate.

Curl robots.txt, curl the webpage, RustScan the IP, and a little directory Brute Forcing with GoBuster are included.

Output is at the command line.

# Remember

First, remember to change the version of Rustscan in your script.To grab Rustscan with docker do: docker pull rustscan/rustcan:vX.X.X

Link: https://github.com/RustScan/RustScan.git

Change command line Args to match your wordlist directory and file.

# How to Use

python3 kickoff.py 10.10.10.10 8000 OR python3 kickoff.py 10.10.10.10
