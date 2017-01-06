# What is it?
New Year resolutions app using Google forms and sheets for data entry/storage and SparkPost for sending emails.

It periodically sends emails reminding people of their resolution and encouraging them to keep going.

# Why did you do this?
It was a fun project that [mary-grace](https://github.com/mary-grace) asked for help with. It was also a great way to learn, as I hadn't previously worked on a SparkPost & Google Apps integration.

# Prerequisites

* A Google Sheet with all of your data. We used a Google Form to collect it, so it was a natural location to center our project data.

* A service account with access to the spreadsheet, and the credentials file for the account. (Easy information on how to set this up can be found [here](https://www.sparkpost.com/blog/google-apps-and-sparkpost-notification/), thanks to [colestrode](https://github.com/colestrode))

* A [SparkPost account](https://app.sparkpost.com/sign-up?src=Dev-Website&sfdcid=70160000000pqBb), with your sending domain [set up](https://support.sparkpost.com/customer/en/portal/articles/1933318-creating-sending-domains?_ga=1.8114224.367117918.1448915879) and [verified](https://support.sparkpost.com/customer/en/portal/articles/1933360-verify-sending-domains), and an [API key](https://support.sparkpost.com/customer/portal/articles/1933377) with Transmission Read/Write permissions.

* pip > 8
```
pip install -U pip>=8.1.2
```
Not required, but recommended:
```
pip install -U virtualenv mkvirtualenv
```

# Setup

* Clone this repo
```
git clone

* Run the following:
```
cd resolutions
mkvirtualenv resolutions
pip install -r reqiurements.txt

export RES_SPREADSHEET_ID="xxMYxxSHEETxxID"
export SPARKPOST_API_KEY="xkred47mvemjsunpejot"
export RES_CREDS_FILENAME='gapps_service_account_creds.json'
```

* [Read this blogpost](https://sparkpo.st/pk1ig) for more info about what, how, and why we did what we did.
