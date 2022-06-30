
# WebsiteTechMiner-py ⛏

A little Python project to automate gathering website profiling data from "BuiltWith" & "Wappalyzer" for tech stack information, technographic data, website reports, website tech lookups, website architecture lookups, etc.

### Uses of WebsiteTechMiner
- 🔒 Data Privacy Activities
    - Vendor Discovery
    - Risk Management
    - Data Privacy Assessments
- 🖥️ Cyber Security Activities
    - Reconnaissance
    - OSINT
    - Risk Management
- 🗺️ Other Discovery Activities
    - Business Intelligence
    - Marketing Activities
    - Competition Analysis
#### Generated Data Fields: 
- ***[ domain , tech_profiler_tool_used , category , technology_name , description (if one exists) ]***

## Getting Started

### ⬇ Installation
- Use Git or download this repo
- Git
    - Open `cmd` or your terminal of choice
    - `cd` to the folder you want to `git clone` to
    - ```git clone https://github.com/cybersader/WebsiteTechMiner-py.git```
- Download
    - Simply download this repo, as is.

### ✉ TempMail for Accounts
- Make an email with https://temp-mail.org/en/
- No need to use your real email since this is temporary.

### Setting up Wappalyzer
- Create a Wappalyzer Account - https://www.wappalyzer.com/
- Go to https://www.wappalyzer.com/apikey/
- Create and copy the API key into the `WebTechMinerNG_setup.json` file using a notepad or editor
- Make sure to put it in the quotes after `wappalyzer-API-key` 
### Requirements
- Python dependencies:
    - Make sure you've installed the project
    - `cd` into the project
    - If you don't have Python, then you're going to need that use pip https://www.python.org/downloads/
    - `pip install -r requirements.txt`

### Setting up BuiltWith
- Create a BuiltWith Account - https://builtwith.com/
- Go to https://api.builtwith.com/
- Create and copy the API key into the `WebTechMiner_setup.json` file using a notepad or editor
- Make sure to put it in the quotes after `builtwith-API-key` 

## Usage

###### ***WebsiteTechMiner-py currently has 2 options:***
- -s, "single" (analyze a single domain)
- -b, "bulk" (analyze a list of domains using a CSV file)
    - put them into rows, columns, or a combination of the two in Excel (it doesn't matter).

### Single Website Lookup
#### command:
```python WebsiteTechMiner.py -s example.com```

### Bulk Website Lookup

#### ⚠🛑⚠🛑⚠🛑⚠🛑
- ***Be careful running this***:
    - if you don't have a paid plan, then you will quickly go over your limits
    - This is not recommended unless you have a high limit for API credits with:
        - Wappalyzer, Builtwith

#### command:
```python WebsiteTechMiner.py -b example_website_list.csv```


