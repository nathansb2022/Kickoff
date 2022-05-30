#!/usr/bin/env python3

#Simple python script to kickoff a few basic commands in a CTF environment.
#Stores contents in robots.txt, webPageScrape.txt, portScan.txt, and directBruteForce.txt.
#Requires xterm, terminator, nikto, nmap, gobuster, and dirb/big.txt file.
#Nikto will run in parallel with the remainder of the script.
#Sed command will kick off in another xterm window and exit when finished. This is clearing the portScan file of
#unwanted lines.
#Additionally, requires Rustscan to be installed in a docker container.
#Specifically, I am running Rustscan:1.10.0 or change to accomodate.
#To grab Rustscan with docker do: docker pull rustscan/ruscan:vx.x.x
#Link: https://github.com/RustScan/RustScan.git
#Example Usage: python3 kickoff.py 10.10.10.10 8000 OR python3 kickoff.py 10.10.10.10

import sys, os, pyfiglet

#Initialize host and port variables
vic = sys.argv[1]
listener = ""

#Assign listener a port number if the value is present from the command line
if len(sys.argv) == 3:

	listener = sys.argv[2]

#Function to run kickoff script with IP only
def kickoff(machine):
	#List of Commands to run
	nikto = "nikto -h http://" + machine + "/"
	#Send job to another xterm window to run in parrallel
	niktoCMD = "terminator -x " + nikto

	robotsCMD = "curl -s http://" + machine + "/robots.txt | tee robots.txt"

	pageScrapeCMD = "curl http://" + machine + " | tee webPageScrape.txt"
									#Change below to line up with your rustscan version
	portScanCMD = "docker run -it --rm --name rustscan rustscan/rustscan:1.10.0 " + machine + " --ulimit 7500 -- -sC -sV -A | tee portScan"

	sed = "sleep 2; sed '1,9d' portScan > portScan.txt; rm -rf portScan; exit"#Close Me When Finished!!!

	sedCMD= "xterm -e " + sed

	gobusterCMD = "gobuster dir -u http://" + machine + " -w /usr/share/wordlists/dirb/big.txt -t 25 -x html,php,txt | tee directBruteForce.txt"

	cmds = niktoCMD, robotsCMD, pageScrapeCMD, portScanCMD, sedCMD, gobusterCMD

	for x in cmds:

		print("")
		os.system(x)
		print("")

#Function to run kickoff script with IP and Port
def kickoffwPort(machine, port):
	#List of Commands to run
	nikto = "nikto -h http://" + machine + ":" + port + "/"
	#Send job to another terminator window to run in parrallel
	niktoCMD = "terminator -x " + nikto

	robotsCMD = "curl -s http://" + machine + ":" + port + "/robots.txt | tee robots.txt"

	pageScrapeCMD = "curl http://" + machine + ":" + port + " | tee webPageScrape.txt"

	portScanCMD = "docker run -it --rm --name rustscan rustscan/rustscan:1.10.0 " + machine + " --ulimit 7500 -- -sC -sV -A | tee portScan"

	sed = "sleep 2; sed '1,9d' portScan > portScan.txt; rm -rf portScan; exit"#Close Me When Finished!!!

	sedCMD = "xterm -e " + sed

	gobusterCMD = "gobuster dir -u http://" + machine + ":" + port + " -w /usr/share/wordlists/dirb/big.txt -t 25 -x html,php,txt | tee directBruteForce.txt"

	cmds = niktoCMD, robotsCMD, pageScrapeCMD, portScanCMD, sedCMD, gobusterCMD

	for x in cmds:

		print("")
		os.system(x)
		print("")

#Calling in the Main
if __name__ == "__main__":

	ascii_banner = pyfiglet.figlet_format("Kickoff2 \n Simple Upfront Enumeration")
	print(ascii_banner)
	print("")
	print("")

	#If no port was provided then run assuming webserver is hosted on port 80
	if not listener:

		kickoff(vic)

	elif listener:

		kickoffwPort(vic,listener)
		
