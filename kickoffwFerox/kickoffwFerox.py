#!/usr/bin/env python3

#Simple python script to kickoff a few basic commands in a CTF environment.
#Stores contents in robots.txt, webPageScrape.txt, owaspzapscan.html, portScan.txt, zapoutput.txt
#and directBruteForce.txt.
#Requires espeak, rustscan and OWASP Zap proxy in a container, nmap, and feroxbuster in docker container.
#For script to run correctly, I cloned with the github repository for ZAP proxy to /opt directory.
#For script to run correctly, I used rustscan v 2.1.1
#The above can be changed to adapt to your environment
#Rustscan starts the scanning analysis. Next,OWASP ZAP will run followed by feroxbuster at the end.
#Sed command will kick off in another terminal window and exit when finished. This is clearing the portScan file of
#unwanted lines. Additionally, this is used to clean up the directBruteForce file as well.
#To grab feroxbuster with docker do: sudo docker pull epi052/feroxbuster:latest
#To grab Rustscan with docker do: sudo docker pull rustscan/ruscan:x.x.x
#Rustscan Link: https://github.com/RustScan/RustScan.git
#OWASP Zap Link: https://github.com/zaproxy/zaproxy.git
#Feroxbuster Link: https://epi052.github.io/feroxbuster-docs/docs/
#To grab zaproxy do: cd /opt; sudo git clone https://github.com/zaproxy/zaproxy.git
#To grab espeak do: sudo apt install espeak alsa-utils
#To grab python3 requirements: sudo pip3 install pyfiglet pyttsx3
#Example Usage:
#              "python3 kickoff.py 10.10.10.10"
#               OR "python3 kickoff.py"

import sys, os, pyfiglet, pyttsx3, re

#Initialize variables
secureHTTP = "443"
regHTTP = "80"
#Bake in variables here
starting = "Your analysis has started"
pAnalysis = "Port Analysis is now complete"
finished = "Scanning is now complete"
# input what you like your directory depth set to:
dirDepth = ""
#dirDepth= "1"

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
		match = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", machine)
		while machine == "" or bool(match) == False:
			machine = input('Please input a valid victim machine IP: ')
			match = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", machine)

		return machine
	else:
		machine = sys.argv[1]
		match = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", machine)
		while bool(match) == False:
			machine = input('Please input a valid victim machine IP: ')
			match = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", machine)
		return machine

#Find what web server ports may be available
def rustPortScan(machine):
	#Lets scan with rust baby
									#Change below to line up with your rustscan version
	portScanCMD = "docker run -it --rm --name rustscan rustscan/rustscan:2.1.1 -a " + machine + " --ulimit 7500 -- -sC -sV -A | tee portScan"

	sed = "sleep 2; sed '1,45d' portScan > portScan.txt; rm -rf portScan; exit"#Close Me When Finished!!!

	sedCMD= "gnome-terminal -- bash -c " + sed

	cmds = portScanCMD, sedCMD

	for x in cmds:

		print("")
		os.system(x)
		print("")

#Assign listener a port
def wsPort(pAnalysis):
	addAudioAlert(pAnalysis)
	#Look above to gather your port information and find out whether to pursue HTTP or HTTPS
	listener = input("Please input the web server port: ")
	match = re.match(r"^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$", listener)
	while listener == "" or bool(match) == False:
		listener = input("Please input a valid web server port: ")
		match = re.match(r"^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$", listener)
	print('')
	if listener == regHTTP:
		listener = ""
		return listener
	else:
		return listener

#tell whether this is non-standard HTTPS
def wsPortHTTPS(listener):
	nonStandard = input("The above port, is it a non-standard HTTPS port? (y/n/q): ")
	print('')
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

def checKDirDepth(dirDepth):
	if not dirDepth:
		dirDepth = input("Please input the directory depth for Feroxbuster (1-5): \n")
		match = re.match(r"^([1-5])$", dirDepth)
		while dirDepth == "" or bool(match) == False:
			dirDepth = input("Please input the directory depth for Feroxbuster (1-5): \n")
			match = re.match(r"^([1-5])$", dirDepth)
		return dirDepth
	else:

		return dirDepth

#Function to run kickoff script with IP only. This assuming that port 80 is open for http
def kickoff(machine,dirDepth):
	#List of Commands to run

	owaspzapCMD = "python3 /opt/zaproxy/docker/zap-full-scan.py -t http://" + machine + " -s -r owaspzapscan.html | tee zapoutput.txt"

	robotsCMD = "curl -s http://" + machine + "/robots.txt | tee robots.txt"

	pageScrapeCMD = "curl -s http://" + machine + " | tee webPageScrape.txt"

	feroxCMD = "docker run --init -it epi052/feroxbuster -u http://" + machine + " -d " + dirDepth + " -x js,html,php,txt > directBruteForce"

	showDirCMD = "cat directBruteForce"

	sed = "sleep 2; sed '1,15d' directBruteForce > directBruteForce.txt; rm -rf directBruteForce; exit"#Close Me When Finished!!!

	sedCMD= "gnome-terminal -- bash -c " + sed

	cmds = robotsCMD, pageScrapeCMD, owaspzapCMD, feroxCMD, showDirCMD, sedCMD

	for x in cmds:

		print("")
		os.system(x)
		print("")

#Function to run kickoff script with IP and Port
def kickoffwPort(machine,port,dirDepth):
	#List of Commands to run

	owaspzapCMD = "python3 /opt/zaproxy/docker/zap-full-scan.py -t http://" + machine + ":" + port + " -s -r owaspzapscan.html | tee zapoutput.txt"

	robotsCMD = "curl -s http://" + machine + ":" + port + "/robots.txt | tee robots.txt"

	pageScrapeCMD = "curl -s http://" + machine + ":" + port + " | tee webPageScrape.txt"

	feroxCMD = "docker run --init -it epi052/feroxbuster -u http://" + machine + ":" + port + " -d " + dirDepth + " -x js,html,php,txt > directBruteForce"

	showDirCMD = "cat directBruteForce"

	sed = "sleep 2; sed '1,15d' directBruteForce > directBruteForce.txt; rm -rf directBruteForce; exit"#Close Me When Finished!!!

	sedCMD= "gnome-terminal -- bash -c " + sed

	cmds = robotsCMD, pageScrapeCMD, owaspzapCMD, feroxCMD, showDirCMD, sedCMD

	for x in cmds:

		print("")
		os.system(x)
		print("")

#Function to run kickoff script with with SSL mode
def kickoffwSSL(machine,port,dirDepth):

	print("Now running in SSL Mode!")

	#List of Commands to run

	owaspzapCMD = "python3 /opt/zaproxy/docker/zap-full-scan.py -t https://" + machine + ":" + port + " -s -r owaspzapscan.html | tee zapoutput.txt"

	robotsCMD = "curl -k -s https://" + machine + ":" + port + "/robots.txt | tee robots.txt"

	pageScrapeCMD = "curl -k -s https://" + machine + ":" + port + " | tee webPageScrape.txt"

	feroxCMD = "docker run --init -it epi052/feroxbuster -k -u https://" + machine + ":" + port + " -d " + dirDepth + " -x js,html,php,txt > directBruteForce"

	showDirCMD = "cat directBruteForce"

	sed = "sleep 2; sed '1,15d' directBruteForce > directBruteForce.txt; rm -rf directBruteForce; exit"#Close Me When Finished!!!

	sedCMD= "gnome-terminal -- bash -c " + sed

	cmds = robotsCMD, pageScrapeCMD, owaspzapCMD, feroxCMD, showDirCMD, sedCMD

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
	listener = wsPort(pAnalysis)
	nonStandardSSL = wsPortHTTPS(listener)
	depthNum = checKDirDepth(dirDepth)

	#If no port was provided then run assuming webserver is hosted on port 80
	if not listener:

		kickoff(vic,depthNum)
	#Run in ssl mode whether it is standard or non-standard https port
	elif listener == secureHTTP or nonStandardSSL == True:

		kickoffwSSL(vic,listener,depthNum)
	#Run assuming webserver is running on non-standard http port
	else:

		kickoffwPort(vic,listener,depthNum)

	addAudioAlert(finished)
