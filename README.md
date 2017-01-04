# What is it?
New Year resolutions app using Google forms and sheets for data entry/storage and SparkPost for sending emails.

# Why did you do this?
Fun? Demo of Sparkpost and google apps integration because I hadn't done that before. Also M asked me very nicely for help

# Prerequisites

A google sheet with all of your data. We used a Google form to collect it, so
it was a natural location to center our project data.

Service account credentials file for that spreadsheet

A SparkPost account, with your sending domain set up and verified, and your API
key in-hand

A google apps service account with access to your spreadsheets
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



