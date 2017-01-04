# What is it?
New Year resolutions app using Fgoogle forms and sheets for data entry/storage and Sparkpost for sending emails. 

# Why did you do this?
Fun? Demo of Sparkpost and google apps integration because I hadn't done that before. Also M asked me very nicely for help

# Prerequisites
pip > 8
```
pip install -U pip>=8.1.2
```
Not required, but recommended
```
pip install -U virtualenv mkvirtualenv
```

# Setup

clone this repo
```
cd resolutions
mkvirtualenv resolutions
pip install -r reqiurements.txt

export RES_SPREADSHEET_ID="xxMYxxSHEETxxID"
export SPARKPOST_API_KEY="xkred47mvemjsunpejot"
export RES_CREDS_FILENAME='gapps_service_account_creds.json'
```

Set up your google spreadsheets like:


