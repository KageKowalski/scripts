# Contains environment variables to be imported by scripts
# Naming paradigm: <DESCRIPTOR>_<PATH OR FILE>


# Imports
from os import environ


# Global vars
SCRIPTS_PATH = environ["SCRIPTS"]
CRED_PATH = SCRIPTS_PATH + ".cred/"
DIR_PATH = SCRIPTS_PATH + "dir/"


# check_portfolio_drift.py vars
PORTFOLIO_PATH = DIR_PATH + "portfolio/"
TICKERS_FILE = "tickers.csv"
CASH_FILE = "cash.csv"


# send_email.py vars
EMAIL_CRED_FILE = "email_credentials.txt"
