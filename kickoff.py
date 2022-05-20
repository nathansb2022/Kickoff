#!/usr/bin/env python3

#Simple python script to kickoff a few basic commands in a CTF environment.
#Requires Rustscan to be installed in a docker container, nmap, gobuster, and dirb/big.txt.
#Specifically, I am running Rustscan:1.10.0 or change to accomodate.
#To grab Rustscan with docker do: docker pull rustscan/ruscan:vx.x.x
#Link: https://github.com/RustScan/RustScan.git
#Feel free to edit the directory of your wordlist and file below.
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

	linuxCMD1 = "curl http://" + machine + "/robots.txt"

	linuxCMD2 = "curl http://" + machine
									#Change below to line up with your rustscan version
	linuxCMD3 = "docker run -it --rm --name rustscan rustscan/rustscan:1.10.0 " + machine + " --ulimit 7500 -- -sC -sV -A -v"
                                                   #Change to match your wordlist directory and file.
	linuxCMD4 = "gobuster dir -u http://" + machine + " -w /usr/share/wordlists/dirb/big.txt -t 25 -x html,php,txt"

	cmds = linuxCMD1, linuxCMD2, linuxCMD3, linuxCMD4

	for x in cmds:

		print("")
		os.system(x)
		print("")

#Function to run kickoff script with IP and Port
def kickoffwPort(machine, port):

	linuxCMD1 = "curl http://" + machine + ":" + port + "/robots.txt"

	linuxCMD2 = "curl http://" + machine + ":" + port
                
	linuxCMD3 = "docker run -it --rm --name rustscan rustscan/rustscan:1.10.0 " + machine + " --ulimit 7500 -- -sC -sV -A -v"
                                                                    #Change to match your wordlist directory and file.
	linuxCMD4 = "gobuster dir -u http://" + machine + ":" + port + " -w /usr/share/wordlists/dirb/big.txt -t 25 -x html,php,txt"

	cmds = linuxCMD1, linuxCMD2, linuxCMD3, linuxCMD4

	for x in cmds:

		print("")
		os.system(x)
		print("")

#Calling in the Main
if __name__ == "__main__":

	ascii_banner = pyfiglet.figlet_format("Kickoff \n Simple Upfront Enumeration")
	print(ascii_banner)
	print("")
	print("")

	if not listener:

		kickoff(vic)

	elif listener:

		kickoffwPort(vic, listener)	
