#!/usr/bin/env python3

#Simple python script to kickoff a few basic commands in a CTF environment.
#Stores contents in robots.txt, webPageScrape.txt, owaspzapscan.html, zapoutput.txt,
#portScan.txt, and directBruteForce.txt.
#Requires espeak, python3-pyaudio, alsa-utils, gobuster, rustscan, and OWASP Zap proxy in a container, and nmap.
#For script to run correctly, I cloned with the github repository for ZAP proxy to /opt directory.
#For script to run correctly, I used rustscan v 2.1.1
#The above can be changed to adapt to your environment
#A port scan and some site recon starts the initial phases of scanning.
#OWASP ZAP will be ran next. Lastly, a directory brute force will bring up the rear.
#The results gathered from the scans will be sent to chatGPT. The following files will be consolidated
#and sent to the chatGPT prompt: robot.txt, webPageScrape.txt, portScan.txt, zapoutput.txt, and directBruteForce.txt.
#If not baked into the script, you will be prompted with how you would your scan data to be viewed by chatGPT.
#Next, the A.I. results will be output in red.
#Sed command will kick off in another terminal window and exit when finished. This is clearing the portScan file of
#unwanted lines. Additionally, this will be done with the directBruteForce file as well.
#Running chatGPT 4, can be changed below.
#To grab Rustscan with docker do: sudo docker pull rustscan/ruscan:x.x.x
#Rustscan Link: https://github.com/RustScan/RustScan.git
#OWASP Zap Link: https://github.com/zaproxy/zaproxy.git
#To grab zaproxy do: cd /opt; sudo git clone https://github.com/zaproxy/zaproxy.git
#To grab espeak do: sudo apt install espeak alsa-utils jackd2 python3-pyaudio gobuster
#To grab python3 requirements: sudo pip3 install pyfiglet pyttsx3 openai pandas tenacity nltk
#Example Usage:
#              "python3 kickoffwAI.py 10.10.10.10"
#               OR "python3 kickoffwAI.py"
#BAKE IN VARIABLES Below
import sys, os, pyfiglet, pyttsx3, openai, pandas as pd, re, time, nltk
from colorama import Fore
from tenacity import (
	retry,
	stop_after_attempt,
	wait_random_exponential,
)  # for exponential backoff
#Timer
start = time.time()
# Initialize basic variables
secureHTTP = "443"
regHTTP = "80"
# These can be modified if needed to enhance audio
starting = "Your analysis has started"
pAnalysis = "Port Analysis is complete"
finished = "Scanning is now complete"
# input your Open AI API key here
OKEY = "" # or add as env variable Below and uncomment
OKEY = os.environ.get('OKEY')
# input what you would like to ask about your scan data from chatGPT
gptInput = "" #Example Below
gptInput = "Provide the best path of exploitation from greatest to least given the information below. Be sure to write this as a vulnerability report in markdown with supporting web links if plausible. "
# input what model you would like to use
flavorGPT = ""
flavorGPT = "gpt-4"
#Calculate Time
def calculateTime(start):
	end = time.time()
	elapsed = end - start                        # 15186 s
	whatTime = time.strftime("%Hh%Mm%Ss", time.gmtime(elapsed))   # '04h13m06s'
	print(Fore.CYAN + "Your analysis took this long " + whatTime + "\n")
#Sound off
def addAudioAlert(someString):
	engine = pyttsx3.init()
	engine.setProperty('rate', 150)
	engine.say(someString)
	engine.runAndWait()
#Print my art
def art():
	ascii_banner = pyfiglet.figlet_format("Kickoff \n Simple Upfront Enumeration")
	print(Fore.CYAN + ascii_banner)
	print("")
	print("")
# check if the api has been input
def checKAPIKey(OKEY):
	if not OKEY:
		OKEY = input("Please input the OpenAI API key: \n")
		while OKEY == "":
			OKEY = input("Please input the OpenAI API key: \n")
		return OKEY
	else:
		return OKEY
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
	#Lets scan with rust baby								#Change below to line up with your rustscan version
	portScanCMD = "docker run -it --rm --name rustscan rustscan/rustscan:2.1.1 -a " + machine + " --ulimit 7500 -- -sC -sV -A | tee portScan"
	sed = "sleep 2; sed '1,56d' portScan > portScan1;  head -n -17 portScan1 > portScan.txt; rm -rf portScan portScan1; exit"#Close Me When Finished!!!
	sedCMD= "gnome-terminal -- bash -c " + sed
	cmds = portScanCMD, sedCMD
	for x in cmds:
		print("")
		os.system(x)
		print("")
#Assign listener a port number
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
#Function to run kickoff script with IP only. This assuming that port 80 is open for http
def kickoff(machine):
	#List of Commands to run
	owaspzapCMD = "python3 /opt/zaproxy/docker/zap-full-scan.py -t http://" + machine + " -s -r owaspzapscan.html | tee zapoutput.txt"
	robotsCMD = "curl -s http://" + machine + "/robots.txt | tee robots.txt"
	pageScrapeCMD = "curl -s http://" + machine + " | tee webPageScrape.txt"
	gobusterCMD = "gobuster dir -u http://" + machine + " -w /usr/share/wordlists/dirb/big.txt -t 25 -x html,php,txt | tee directBruteForce"
	sed = "sleep 2; sed '1,14d' directBruteForce > directBruteForce.txt; rm -rf directBruteForce; exit"#Close Me When Finished!!!
	sedCMD= "gnome-terminal -- bash -c " + sed
	cmds = robotsCMD, pageScrapeCMD, owaspzapCMD, gobusterCMD, sedCMD
	for x in cmds:
		print("")
		os.system(x)
		print("")
#Function to run kickoff script with IP and Port
def kickoffwPort(machine,port):
	#List of Commands to run
	owaspzapCMD = "python3 /opt/zaproxy/docker/zap-full-scan.py -t http://" + machine + ":" + port + " -s -r owaspzapscan.html | tee zapoutput.txt"
	robotsCMD = "curl -s http://" + machine + ":" + port + "/robots.txt | tee robots.txt"
	pageScrapeCMD = "curl -s http://" + machine + ":" + port + " | tee webPageScrape.txt"
	gobusterCMD = "gobuster dir -u http://" + machine + ":" + port + " -w /usr/share/wordlists/dirb/big.txt -t 25 -x html,php,txt | tee directBruteForce"
	sed = "sleep 2; sed '1,14d' directBruteForce > directBruteForce.txt; rm -rf directBruteForce; exit"#Close Me When Finished!!!
	sedCMD= "gnome-terminal -- bash -c " + sed
	cmds = robotsCMD, pageScrapeCMD, owaspzapCMD, gobusterCMD, sedCMD
	for x in cmds:
		print("")
		os.system(x)
		print("")
#Function to run kickoff script with with SSL mode
def kickoffwSSL(machine,port):
	print("Now running in SSL Mode!")
	#List of Commands to run
	owaspzapCMD = "python3 /opt/zaproxy/docker/zap-full-scan.py -t https://" + machine + ":" + port + " -s -r owaspzapscan.html | tee zapoutput.txt"
	robotsCMD = "curl -k -s https://" + machine + ":" + port + "/robots.txt | tee robots.txt"
	pageScrapeCMD = "curl -k -s https://" + machine + ":" + port + " | tee webPageScrape.txt"
	gobusterCMD = "gobuster dir -k -u https://" + machine + ":" + port + " -w /usr/share/wordlists/dirb/big.txt -t 25 -x html,php,txt | tee directBruteForce"
	sed = "sleep 2; sed '1,14d' directBruteForce > directBruteForce.txt; rm -rf directBruteForce; exit"#Close Me When Finished!!!
	sedCMD= "gnome-terminal -- bash -c " + sed
	cmds = robotsCMD, pageScrapeCMD, owaspzapCMD, gobusterCMD, sedCMD
	for x in cmds:
		print("")
		os.system(x)
		print("")
#See if the following text files were generated by the tools utilized: robot.txt,
#webPageScrape.txt, portScan.txt, zapoutput.txt, and directBruteForce.txt
def checkFile():
	f1txt = ""
	f2txt = ""
	f3txt = ""
	f4txt = ""
	f5txt = ""
	if os.path.isfile("portScan.txt"):
		f1 = "portScan.txt"
		with open(f1, 'r') as f:
			f1txt = f.read()
			f.close()
	if os.path.isfile("robots.txt"):
		f2 = "robots.txt"
		with open(f2, 'r') as f:
			f2txt = f.read()
			f.close()
	if os.path.isfile("webPageScrape.txt"):
		f3 = "webPageScrape.txt"
		with open(f3, 'r') as f:
			f3txt = f.read()
			f.close()
	if os.path.isfile("directBruteForce.txt"):
		f4 = "directBruteForce.txt"
		with open(f4, 'r') as f:
			f4txt = f.read()
			f.close()
	if os.path.isfile("zapoutput.txt"):
		f5 = "zapoutput.txt"
		with open(f5, 'r') as f:
			f5txt = f.read()
			f.close()
	nltk_tokens = nltk.word_tokenize(f3txt)
	if len(nltk_tokens) >= 4001:
		return f1txt + f2txt + f4txt + f5txt
	else:
		return f1txt + f2txt + f3txt + f4txt + f5txt
#Add in your model if you have not baked it in
def checKAIModel(flavor):
	if not flavor:
		flavor = input("Please input the model of your AI, i.e. gpt-4 : \n")
		while flavor == "":
			flavor = input("Please input an actual AI Model, i.e. gpt-4 : \n")
		return flavor
	else:
		return flavor
#Add variables to get the response from chatGPT
def gather(prompt, OKEY, flavorGPT):
	openai.api_key = OKEY
	print('')
	prompt = prompt
	print(Fore.GREEN + "Please wait while we ask chatGPT about this host.\n")
	response = get_completion(prompt, flavorGPT)
	print(Fore.RED + response)
#Reach out to chatGPT with the results from scanning
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(10))
def get_completion(prompt, flavor):
	messages = [{"role": "user", "content": prompt}]
	response = openai.ChatCompletion.create(
		model=flavor,
		messages=messages,
		temperature=0,
		)
	return response.choices[0].message["content"]
# check for the beginning input to chat gpt
def checkGPTInput(gptInput):
	if not gptInput:
		gptInput = input("Please input how you would like your scan data to be reviewed by chatGPT: \n")
		while gptInput == "":
			gptInput = input("Please input how you would like your scan data to be reviewed by chatGPT: \n")
		return gptInput
	else:
		return gptInput
#tell whether to run chatGPT request again if failed
def errorGPT(prompt, OKEY, flavorGPT):
	nonStandard = input("Would you like to reach out to chatGPT again with your analysis? (y/n/q): ")
	print('')
	#Take user input and determine yes, no, quit, or undecided input
	if nonStandard.lower() == 'y' or nonStandard.lower() == 'n' or nonStandard.lower() == 'q' or nonStandard.lower() == 'yes' or nonStandard.lower() == 'no' or nonStandard.lower() == 'quit':
		if nonStandard.lower() == 'y' or nonStandard.lower() == 'yes':
			gather(prompt, OKEY, flavorGPT)
		elif nonStandard.lower() == 'n' or nonStandard.lower() == 'no':
			exit()
		else:
			print('Bye!')
			exit()
	else:
		print('Your input for chatGPT request was taken incorrectly. Exiting!')
		exit()
#Calling in the Main
if __name__ == "__main__":
	try:
		art()
		addAudioAlert(starting)
		vic = checkIp()
		# input put your api key below if not set above
		OKEY = checKAPIKey(OKEY)
		rustPortScan(vic)
		listener = wsPort(pAnalysis)
		nonStandardSSL = wsPortHTTPS(listener)
		#If no port was provided then run assuming webserver is hosted on port 80
		if not listener:
			kickoff(vic)
		#Run in ssl mode whether it is standard or non-standard https port
		elif listener == secureHTTP or nonStandardSSL == True:
			kickoffwSSL(vic,listener)
		#Run assuming webserver is running on non-standard http port
		else:
			kickoffwPort(vic,listener)
		#Send the results gathered from the text files to be summarized by chatGPT robot.txt,
		#webPageScrape.txt, portScan.txt, zapoutput.txt, and directBruteForce.txt
		addAudioAlert(finished)
		calculateTime(start)
		flavorGPT = checKAIModel(flavorGPT)
		gptInput = checkGPTInput(gptInput)
		#nltk needs punkt
		nltk.download('punkt')
		print('')
		print('')
		scanData = checkFile()
		prompt = gptInput + scanData
		gather(prompt, OKEY, flavorGPT)
	except Exception as err:
		print(f"Unexpected {err=}, {type(err)=}")
		errorGPT(prompt, OKEY, flavorGPT)
