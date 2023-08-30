#!/usr/bin/env python3

#Simple python script to kickoff a few basic commands in a CTF environment.
#Stores contents in robots.txt, webPageScrape.txt, owaspzapscan.html, portScan.txt, and directBruteForce.txt.
#Requires espeak, xterm, rustscan, OWASP Zap proxy in a container, nmap, gobuster, and dirb/big.txt file.
#For script to run correctly, big.txt must be stored in directory: /usr/share/wordlists/dirb/
#For script to run correctly, I cloned with the github repository for ZAP proxy to /opt directory.
#For script to run correctly, I used rustscan v 2.1.1
#The above can be changed to adapt to your environment
#OWASP ZAP will run at the end of the script.
#Sed command will kick off in another xterm window and exit when finished. This is clearing the portScan file of
#unwanted lines.
#To grab Rustscan with docker do: docker pull rustscan/ruscan:x.x.x
#Rustscan Link: https://github.com/RustScan/RustScan.git
#OWASP Zap Link: https://github.com/zaproxy/zaproxy.git
#To grab zaproxy do: cd /opt; sudo git clone https://github.com/zaproxy/zaproxy.git
#To grab espeak do: sudo apt install espeak xterm gobuster alsa-utils
#To grab python3 requirements: sudo pip3 install pyfiglet pyttsx3
#Example Usage:
#              "python3 kickoff.py 10.10.10.10"
#               OR "python3 kickoff.py"

import sys, os, pyfiglet, pyttsx3

#Initialize variables
secureHTTP = "443"
regHTTP = "80"
starting = "Your analysis has started"
finished = "Scanning is now complete"

#Sound off
def addAudioAlert(someString):

	engine = pyttsx3.init()
	engine.setProperty('rate', 150)
	engine.say(someString)
	engine.runAndWait()

#Print my art
def art():

	ascii_banner = pyfiglet.figlet_format("Kickoff \n Simple Upfront Enumeration")
	print(ascii_banner)
	print("")
	print("")

#if no ip is provided ask
def checkIp():

	if not len(sys.argv) > 1:

		machine = input('Please input the victim machine IP: ')

		return machine
	else:
		machine = sys.argv[1]
		return machine

#Find what web server ports may be available
def rustPortScan(machine):
	#Lets scan with rust baby
									#Change below to line up with your rustscan version
	portScanCMD = "docker run -it --rm --name rustscan rustscan/rustscan:2.1.1 -a " + machine + " --ulimit 7500 -- -sC -sV -A | tee portScan"

	sed = "sleep 2; sed '1,9d' portScan > portScan.txt; rm -rf portScan; exit"#Close Me When Finished!!!

	sedCMD= "xterm -e " + sed

	cmds = portScanCMD, sedCMD

	for x in cmds:

		print("")
		os.system(x)
		print("")

#Assign listener a port
def wsPort():
	#Look above to gather your port information and find out whether to pursue HTTP or HTTPS
	listener = input("Please input the web server port: ")
	print('')
	if listener == regHTTP:
		listener = ""
		return listener
	elif not listener:
		listener = input("Please input the web server port: ")
		if listener == regHTTP:
			listener = ""
			return listener
		else:
			return listener
	else:
		return listener

#tell whether this is non-standard HTTPS
def wsPortHTTPS(listener):
	nonStandard = input("The above port, was it a non-standard HTTPS port? (y/n/q): ")

	#Take user input and determine yes, no, quit, or undecided input
	if nonStandard.lower() == 'y' or nonStandard.lower() == 'n' or nonStandard.lower() == 'q' or nonStandard.lower() == 'yes' or nonStandard.lower() == 'no' or nonStandard.lower() == 'quit':

		if nonStandard.lower() == 'y' or nonStandard.lower() == 'yes':
			nonStandardSSL = True
			return nonStandardSSL

		elif nonStandard.lower() == 'n' or nonStandard.lower() == 'no':

			if listener == secureHTTP:

				print('')
				print('Script will be ran on regular HTTPS')
				nonStandardSSL = False
				return nonStandardSSL
			else:
				nonStandardSSL = False
				return nonStandardSSL

		else:

			print('Bye!')
			exit()

	else:

		print('Your input for the non-standard port was taken incorrectly. Exiting!')

		exit()

#Function to run kickoff script with IP only. This assuming that port 80 is open for http
def kickoff(machine):
	#List of Commands to run

	owaspzapCMD = "python3 /opt/zaproxy/docker/zap-full-scan.py -t http://" + machine + " -r owaspzapscan.html"

	robotsCMD = "curl -s http://" + machine + "/robots.txt | tee robots.txt"

	pageScrapeCMD = "curl -s http://" + machine + " | tee webPageScrape.txt"

	gobusterCMD = "gobuster dir -u http://" + machine + " -w /usr/share/wordlists/dirb/big.txt -t 25 -x html,php,txt | tee directBruteForce.txt"

	cmds = robotsCMD, pageScrapeCMD, gobusterCMD, owaspzapCMD

	for x in cmds:

		print("")
		os.system(x)
		print("")

#Function to run kickoff script with IP and Port
def kickoffwPort(machine, port):
	#List of Commands to run

	owaspzapCMD = "python3 /opt/zaproxy/docker/zap-full-scan.py -t http://" + machine + ":" + port + " -r owaspzapscan.html"

	robotsCMD = "curl -s http://" + machine + ":" + port + "/robots.txt | tee robots.txt"

	pageScrapeCMD = "curl -s http://" + machine + ":" + port + " | tee webPageScrape.txt"

	gobusterCMD = "gobuster dir -u http://" + machine + ":" + port + " -w /usr/share/wordlists/dirb/big.txt -t 25 -x html,php,txt | tee directBruteForce.txt"

	cmds = robotsCMD, pageScrapeCMD, gobusterCMD, owaspzapCMD

	for x in cmds:

		print("")
		os.system(x)
		print("")

#Function to run kickoff script with with SSL mode
def kickoffwSSL(machine, port):

	print("Now running in SSL Mode!")

	#List of Commands to run

	owaspzapCMD = "python3 /opt/zaproxy/docker/zap-full-scan.py -t https://" + machine + ":" + port + " -r owaspzapscan.html"

	robotsCMD = "curl -k -s https://" + machine + ":" + port + "/robots.txt | tee robots.txt"

	pageScrapeCMD = "curl -k -s https://" + machine + ":" + port + " | tee webPageScrape.txt"

	gobusterCMD = "gobuster dir -k -u https://" + machine + ":" + port + " -w /usr/share/wordlists/dirb/big.txt -t 25 -x html,php,txt | tee directBruteForce.txt"

	cmds = robotsCMD, pageScrapeCMD, gobusterCMD, owaspzapCMD

	for x in cmds:

		print("")
		os.system(x)
		print("")

#Calling in the Main
if __name__ == "__main__":

	addAudioAlert(starting)
	art()
	vic = checkIp()
	rustPortScan(vic)
	listener = wsPort()
	nonStandardSSL = wsPortHTTPS(listener)

	#If no port was provided then run assuming webserver is hosted on port 80
	if not listener:

		kickoff(vic)
	#Run in ssl mode whether it is standard or non-standard https port
	elif listener == secureHTTP or nonStandardSSL == True:

		kickoffwSSL(vic,listener)
	#Run assuming webserver is running on non-standard http port
	else:

		kickoffwPort(vic, listener)

	addAudioAlert(finished)
