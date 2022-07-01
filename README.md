# WebsiteTechMiner-py ⛏

A little Python project to automate gathering website profiling data from "BuiltWith" & "Wappalyzer" for tech stack information, technographic data, website reports, website tech lookups, website architecture lookups, etc.

### Uses of WebsiteTechMiner
- 👁️ Data Privacy Activities
    - Vendor Discovery for Websites
    - Risk Management
    - Data Privacy Read-Ahead Material for Privacy Assessments
- 🖥️ Cyber Security Activities
    - Reconnaissance
    - OSINT
- 🗺️ Other Discovery Activities
    - Business Intelligence
    - Marketing Activities
    - Competition Analysis
#### Generated Data Fields: 

##### All data is exported into the CSV file designated in the config file.

- ***[ domain , tech_profiler_tool_used , category , technology_name , description (if one exists) ]***

<img src="https://user-images.githubusercontent.com/106132469/176921390-9b6c36c1-a97c-4bf8-9362-7eb356013238.png" width="100">

## Getting Started

### ⬇ Installation
- Use Git or download this repo
- Git
    - Open `cmd` or your terminal of choice
    - `cd` to the folder you want to `git clone` to
    - ```git clone https://github.com/cybersader/WebsiteTechMiner-py.git```
- Download
    - Simply download this repo, as is.

### Requirements
- Python dependencies:
    - Make sure you've installed the project
    - `cd` into the project
    - If you don't have Python, then you're going to need it to use pip https://www.python.org/downloads/
    - `pip install -r requirements.txt`

### ✉ TempMail for Accounts
- Make an email with https://temp-mail.org/en/
- No need to use your real email for short-term discovery projects.

### DO NOT be fradulent
- I'm not going to design any automated fradulent solutions to automatically generate temporary accounts and emails.
- If you are trying to process very large amounts of URLs, then please purchase plans from these tech lookup services.

### Setting up Wappalyzer
- Create a Wappalyzer Account - https://www.wappalyzer.com/
- Go to https://www.wappalyzer.com/apikey/
- Create and copy the API key into the `WebTechMinerNG_setup.json` file using a notepad or editor
- Make sure to put it in the quotes after `wappalyzer-API-key` 

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

## 💎 Future Developments

### API Functionalities
- Ability to choose from more fields
   - connected websites, location, recursive search, etc.
- Add in multiple successive API keys
   - CLI or in config
- Default without flags
- Unlimited domains in command

### 🌐 Discovery 
- Recursive Subdomain discovery option
- Connected website discovery
- PI Discovery

