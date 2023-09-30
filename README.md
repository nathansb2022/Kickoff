# Kickoff
Simple automation and enumeration script for CTF environments. Focus is on one host at a time.

Stores contents in robots.txt, webPageScrape.txt, owaspzapscan.html, portScan.txt, and directBruteForce.txt. Requires xterm, rustscan, OWASP Zap proxy in a container, nmap, gobuster, and dirb/big.txt file. There is audio notifications to alert you when starting and completing.  

# IMPORTANT

Completely enhanced this tool. Just added chatGPT to the mix as a helper with the scan results. See kickoffwAI folder for python3 script. Read comments in header of the py file that has required packages. When prompted on how you would like your scan data to be reviewed by chatGPT with model="gpt-4", try "Take the following input and generate a vulnerability report in markdown". Furthermore, I have incorporated a version with Feroxbuster (See kickoffwFerox folder).

# Terminal Output

First, the terminal starts off with Rustscan output showing ports and services. Next, a curl request will be made to the robots.txt file of a website and another request to page scrape the site itself. Gobuster will start with some directory brute forcing. All of the command outputs will be stored in txt files for further review.

Sed command will kick off in another xterm window and exit when finished. This is clearing the portScan file of unwanted lines. OWASP ZAP will run at the end of the script and results will be stored in the respective html file.

# Remember

First, remember to change the version of Rustscan in your script if needed. For script to run correctly, big.txt must be stored in directory: /usr/share/wordlists/dirb/ and ZAP proxy to be cloned with the github repository for ZAP proxy to /opt directory. If you choose different paths for files called, remember to change them in the script.

Links below:

[Rustscan](https://github.com/RustScan/RustScan.git)

[OWASP ZAP Proxy](https://github.com/zaproxy/zaproxy.git)

[Gobuster](https://github.com/OJ/gobuster)

[Feroxbuster](https://epi052.github.io/feroxbuster-docs/docs/)

[ChatGPT](https://chat.openai.com/auth/login)

# How to Use

Example Usage:

Add IP as argument
```bash
python3 kickoff.py 10.10.10.10
```
Or without
```bash
python3 kickoff.py
```
# Install Requirements

To grab Rustscan with docker do:
```bash
sudo docker pull rustscan/rustcan:2.1.1
```
To grab zaproxy do:
```bash
cd /opt; sudo git clone https://github.com/zaproxy/zaproxy.git
```
To grab Feroxbuster with docker do:
```bash
sudo docker pull epi052/feroxbuster:latest
```
To grab additional software:
```bash
sudo apt install espeak xterm gobuster alsa-utils
```
To grab python requirements do:
```bash
sudo pip3 install pyfiglet pyttsx3
```
