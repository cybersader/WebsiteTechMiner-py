import re
import csv
from enum import Enum
from pathlib import Path
import getopt, sys
import math
import json
from colorama import init, Fore, Back, Style
import argparse
import time
from progress.bar import ShadyBar
from progress.spinner import Spinner
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

'''
WebsiteTechMiner-py (CLI)
Developed by - CyberSader
Version - 0.0.1

TODO:
- Stop WTM if you run out of API credits for all tools
- Error fidelity on error prints
- Multiple API tokens in config file or some csv file
- More fields from APIs to csv
- Ability to use flags for fields
- Unlimited domains on command line
- http and https flags
- Default command with domains after
'''

tool_desc="""'WebsiteTechMiner-py' aggregates technographic data on websites by using the APIs
			of website profiling tools.  The tools currently used in WebsiteTechMiner-py include:
			 (Wappalyzer, BuiltWith)"""

#makes color works
init(convert=True)
#good = f"{Fore.GREEN}"
#error = f"{Fore.RED}"

#greate command line parser and command line arguments
parser = argparse.ArgumentParser(description =tool_desc, epilog='Developed by CyberSader - v0.0.1')

parser.add_argument('-s', '--single', type=str,
                    help ='(DOMAIN NAME) - processes the given domain name')

parser.add_argument('-b','--bulk', type=str,
					help="""(Domain List CSV file) - give the file path of a """
					+ """CSV file with a list of domain names in it (site1.com, site2.com, ...)""")
					
'''parser.add_argument('--verbose', action="store_true", default=False,
					help='Show all of the processing in the CLI as it happens')'''

#requests Wappalyzer API with api key and domain name and returns JSON
def Wappalyzer_API_request(domain, api_key):
	spinner_text_wapp='Requesting Wappalyzer tech lookup for -> ' + domain
	spinner_wapp = Spinner(spinner_text_wapp)
	spinner_wapp.next()
	wapp_tech_lookup_url="https://api.wappalyzer.com/v2/lookup/"
	wapp_api_query={'urls':domain}
	wapp_request_headers={'x-api-key':api_key}
	wappalyzer_response= requests.request("GET", wapp_tech_lookup_url, params=wapp_api_query, headers=wapp_request_headers, verify = False)
	if(wappalyzer_response.status_code==200):
		spinner_wapp.finish()
	else:
		spinner_wapp.finish()
		print(f"{Fore.RED} [REST API FAIL] {Fore.WHITE} Wappalyzer API returned code - ", wappalyzer_response.status_code)
		if(wappalyzer_response.status_code==403):
			print(f"{Fore.RED} [REST API FAIL] {Fore.WHITE} Either incorrect API key or you ran out of API credits to use on Wappalyzer.")
	return wappalyzer_response.json()

#requests BuiltWith API with api key and domain name and returns JSON
def BuiltWith_API_request(domain, api_key):
	spinner_text_bw='Requesting BuiltWith tech lookup for -> '+domain
	spinner_bw = Spinner(spinner_text_bw)
	spinner_bw.next()
	builtwith_tech_lookup_url="https://api.builtwith.com/v20/api.json?KEY="+api_key+"&LOOKUP="+domain
	bw_response= requests.request("GET", builtwith_tech_lookup_url, verify = False)
	if(bw_response.status_code==200):
		spinner_bw.finish()
	else:
		spinner_bw.finish()
		print(f"{Fore.RED} [REST API FAIL] {Fore.WHITE} BuiltWith API returned code - ", bw_response.status_code)
		exit()
	return bw_response.json()

def SingleDomainMiner( domain_name, config ):
	#techmining_data list
	tech_mining_data = []
	
	builtwith_key = config['builtwith-API-key']
	wappalyzer_key = config['wappalyzer-API-key']
	output_file_name = config['output-file-name']
	is_verbose = config['is_verbose']
	
	WAPP_API_CREDIT_ERROR = False
	BW_API_CREDIT_ERROR = False
	
	#parse URL - add "https://" if it isn't there
	if(not re.search("https://",domain_name)):
		domain_name="https://"+domain_name
	
	#Load Wappalyzer for domain
	wapp_response_json = Wappalyzer_API_request(domain_name, wappalyzer_key)
	if is_verbose:
		print(json.dumps(wapp_response_json, indent=4, sort_keys=True))
	
	#Load Builtwith
	bw_response_json = BuiltWith_API_request(domain_name, builtwith_key)
	if is_verbose:
		print(json.dumps(bw_response_json, indent=4, sort_keys=True))
	
	if(not bw_response_json['Errors']):
		pass
	else:
		if(bw_response_json['Errors'][-1]['Code']==-4):
			BW_API_CREDIT_ERROR = True
			print(f"{Fore.RED} [OUT OF API CREDITS] {Fore.WHITE} You ran out of BuiltWith API credits")
	
	if(not bw_response_json['Errors']):
		pass
	else:
		if(bw_response_json['Errors'][-1]['Code']==-4):
			BW_API_CREDIT_ERROR = True
			print(f"{Fore.RED} [OUT OF API CREDITS] {Fore.WHITE} You ran out of BuiltWith API credits")
	
	#used to make row for each technology found
	tech_row = []
	
	##wappalyzer processing
	if not WAPP_API_CREDIT_ERROR:
		#parse JSON
		count=0
		for wapp_domain_object in wapp_response_json:
			#CATCHES WAPPALYZER API ERROR //TODO
			try:
				wapp_domain_name = wapp_domain_object['url']
			except:
				exit()
			wapp_techs = wapp_domain_object['technologies']
			count+=1
			bar_wapp_tech_text = 'Parsing Wappalyzer Technologies - '+str(count)+"/"+str(len(wapp_response_json))
			bar_wapp_techs = ShadyBar(bar_wapp_tech_text, max=len(wapp_techs))
			for wapp_tech in wapp_techs:
				wapp_tech_name = wapp_tech['name']
				wapp_tech_categories = wapp_tech['categories']
				bar_wapp_techs.next()
				for wapp_tech_category in wapp_tech_categories:
					wapp_tech_category_name = wapp_tech_category['name']
					tech_row = [wapp_domain_name,'Wappalyzer',wapp_tech_category_name,wapp_tech_name,"NO DESC"]
					tech_mining_data.append(tech_row)
					if is_verbose:
						print(tech_row)
			bar_wapp_techs.finish()
				
	##builtwith processing
	if not BW_API_CREDIT_ERROR:
		count=0
		#TODO:check for cases where results are empty
		#TODO:check for type of error and return print based on the error code in response
		if bw_response_json['Results'] and not bw_response_json['Errors']:
			bw_domains = bw_response_json['Results'][0]['Result']['Paths']
			for bw_domain in bw_domains:
				if bw_domain['SubDomain']:
					bw_domain_name = bw_domain['SubDomain']+"."+bw_domain['Domain']
				else:
					bw_domain_name = bw_domain['Domain']
				count+=1
				bw_techs = bw_domain['Technologies']
				bar_bw_tech_text = 'Parsing BuiltWith Technologies - '+str(count)+"/"+str(len(bw_domains))
				bar_bw = ShadyBar(bar_bw_tech_text, max=len(bw_techs))
				for bw_tech in bw_techs:
					bar_bw.next()
					bw_tech_name = bw_tech['Name']
					bw_tech_category_name = bw_tech['Tag']
					bw_tech_desc = bw_tech['Description']
					tech_row = [bw_domain_name,'BuiltWith',bw_tech_category_name,bw_tech_name,bw_tech_desc]
					tech_mining_data.append(tech_row)
					if is_verbose:
							print(tech_row)
				bar_bw.finish()
			else:
				pass
	
	return tech_mining_data

def BulkDomainMiner(domain_list_csv, config ):
	#bulk techmining_data list
	bulk_tech_mining_data = []
	is_verbose = config['is_verbose']
	
	#open csv file
	with open(domain_list_csv, 'r') as file:
		print(f"\n{Fore.GREEN} [+] {Fore.WHITE} Opened bulk domain list (CSV)")
		#read csv file
		reader=csv.reader(file, delimiter=',')
		domain_list = list(reader)
		domain_num=len(domain_list)
		if is_verbose:
			print(domain_list)
		print(f"\n{Fore.GREEN} [+] {Fore.WHITE} "+str(domain_num)+" domains found in CSV file.")
		#mine each domain/subdomain listed in the csv file
		domains_bar = ShadyBar('Processing Domains from list ', max=domain_num)
		for domain_row in domain_list:
			for domain_name in domain_row:
				#Run SingleDomainMiner on current domain in list
				domains_bar.next()
				if(domain_name):
					tech_mining_data = SingleDomainMiner(domain_name, config)
					bulk_tech_mining_data.append(tech_mining_data)
		domains_bar.finish()
	return bulk_tech_mining_data

#Parse "WebTechMiner_setup.json"
'''
EXAMPLE JSON FILE
{
	"builtwith-API-key":"SOME API KEY",
	"wappalyzer-API-key":"SOME API KEY",
	"output-file-name":"website_technology_miner_results.csv"
}
'''

######    RUN MINER:   #########
#Parse arguments -> mine websites via APIs
args = parser.parse_args()
if not len(sys.argv) > 1:
	print(f"{Fore.RED} [+] {Fore.WHITE} No arguments given... Use '-h' for help menu.")
	exit()

print("")
print("")
print(f"{Fore.GREEN} [+] {Fore.WHITE} ARGUMENTS PARSED")

#load setup data form JSON file
setup_file = open('WebTechMiner_setup.json',"r")
config = json.load(setup_file)
print("")
print(f"{Fore.GREEN} [+] {Fore.WHITE} LOADED CONFIG FILE")
print("")

#config file checks and loading
builtwith_key = config['builtwith-API-key']
wappalyzer_key = config['wappalyzer-API-key']
output_file_name = config['output-file-name']

ERROR_BW=False
ERROR_WPLZ=False
ERROR_NO_OUTPUT_FILE=False

if(builtwith_key ==""):
	ERROR_BW=True
	print(f"{Fore.RED} [CONFIG FILE ERROR] {Fore.WHITE} No BuiltWith API Key")
if(wappalyzer_key ==""):
	ERROR_WPLZ=True
	print(f"{Fore.RED} [CONFIG FILE ERROR] {Fore.WHITE} No Wappalyzer API Key")
if(output_file_name ==""):
	ERROR_NO_OUTPUT_FILE=True
	print(f"{Fore.RED} [CONFIG FILE ERROR] {Fore.WHITE} No Output File Name Given")
if(ERROR_BW or ERROR_WPLZ or ERROR_NO_OUTPUT_FILE):
	print(f"{Fore.RED} [ERROR] {Fore.WHITE} Fix config file")
	quit()
print("")
print("CONFIG File Settings ('WebTechMiner_setup.json')")
print("")
print("--------------------------------------")
print("builtwith-API-key ->",builtwith_key)
print("wappalyzer-API-key ->",wappalyzer_key)
print("builtwith-API-key ->",output_file_name)
print("--------------------------------------")
print("")
print(f"{Fore.GREEN} [+] {Fore.WHITE} Config File Parsed")
print("")
print(f"{Fore.GREEN} [+] {Fore.WHITE} Initializing Technographic Miner ")
time.sleep(1)

#RUN WebsiteTechMiner Functions based on arguments from user
miner_results_list = []
if args.single:
	miner_results_list = SingleDomainMiner(args.single, config)
elif args.bulk:
	miner_results_list = BulkDomainMiner(args.bulk, config)
else:
	print("error")
print(f"\n{Fore.GREEN} [+] {Fore.WHITE} Opening output CSV file. ")

#Output to miner results to CSV file
fields = ['subdomain','tech_profiler_tool_used','category','technology_name','description']
csv_filename = config['output-file-name']
csvfile = open(csv_filename, 'w+')
#csvwriter = csv.writer(csvfile, dialect='excel-tab', newline='')
csvwriter = csv.writer(csvfile, dialect='excel', lineterminator='\n')
csvwriter.writerow(fields)

print(f"\n{Fore.GREEN} [+] {Fore.WHITE} Opened output CSV file for Results")
print(f"\n{Fore.GREEN} [+] {Fore.WHITE} Writing results to CSV file  ")
for row in miner_results_list:
	csvwriter.writerow(row)
print("")
print(f"{Fore.GREEN}:::::: [FINISHED] ::::::{Fore.WHITE} Results written to CSV!!!")