# 1. Check whether significant portfolio drift has occurred
# 2. Create a message including all information on how to correct portfolio drift
# 3. If significant portfolio drift has occurred, send the message as an email alert
#
# Relies on TICKERS_FILE and CASH_FILE, which represent the portfolio being checked
# Relies on EMAIL_CRED_FILE, which contains the credentials of the sender's email account
#
# TICKERS_FILE is a csv file containing information on tickers in the portfolio, with headers...
# ["Ticker", "DesiredPercentage", "CurrentAmount"]
#
# CASH_FILE is a csv file containing information on cash in the portfolio, with headers...
# ["DesiredPercentage", "CurrentAmount"]
# CASH_File must contain exactly one line, excluding the header line
#
# EMAIL_CRED_FILE is a txt file containing the sender's email address on the first line and their password on the
# second line
#
# All DesiredPercentage fields from TICKERS_FILE and CASH_FILE must add up to 100
# TICKERS_FILE and CASH_FILE must be updated manually


# Imports
import env_var
import csv
from yfinance import Ticker
from os_util import send_email


# Constants
PERCENT_DRIFT_TOLERANCE = 3.0
EMAIL_RECEIVER = "kagekowalski@gmail.com"
EMAIL_SUBJECT = "Significant Portfolio Drift Alert"
PORTFOLIO_PATH = env_var.DIR_PATH + "portfolio/"
TICKERS_FILE = PORTFOLIO_PATH + "tickers.csv"
CASH_FILE = PORTFOLIO_PATH + "cash.csv"
EMAIL_CRED_FILE = env_var.CRED_PATH + "email_credentials.txt"


# Get input data from TICKERS_FILE, and get online data from yfinance.Ticker
ticker_info = {}
total_ticker_value = 0.0
with open(TICKERS_FILE, mode='r') as f:
    reader = csv.DictReader(f)

    for row in reader:
        current_ticker_value = float(Ticker(row["Ticker"]).info["regularMarketPrice"])
        current_ticker_amount = int(row["CurrentAmount"])
        ticker_info[row["Ticker"]] = {"DesiredPercentage": float(row["DesiredPercentage"]),
                                      "CurrentAmount": current_ticker_amount,
                                      "CurrentValue": current_ticker_value}
        total_ticker_value = total_ticker_value + (current_ticker_value * current_ticker_amount)


# Get input data from CASH_FILE
cash_info = {}
total_portfolio_value = 0.0
with open(CASH_FILE, mode='r') as f:
    reader = csv.DictReader(f)

    for row in reader:
        cash_info["DesiredPercentage"] = float(row["DesiredPercentage"])
        cash_info["CurrentAmount"] = float(row["CurrentAmount"])

    total_portfolio_value = total_ticker_value + cash_info["CurrentAmount"]


# Calculate CurrentPercentage, IdealAmount, and IdealPercentage of each ticker
# Also, detect whether significant portfolio drift has occurred for any ticker
significant_drift = False
for ticker in ticker_info:
    ticker_info[ticker]["CurrentPercentage"] = \
        (ticker_info[ticker]["CurrentAmount"] * ticker_info[ticker]["CurrentValue"]) / total_portfolio_value * 100

    ticker_info[ticker]["IdealAmount"] = \
        round((total_portfolio_value * (ticker_info[ticker]["DesiredPercentage"] / 100)) /
              ticker_info[ticker]["CurrentValue"])

    ticker_info[ticker]["IdealPercentage"] = \
        ticker_info[ticker]["IdealAmount"] * ticker_info[ticker]["CurrentValue"] / total_portfolio_value * 100

    if abs(ticker_info[ticker]["DesiredPercentage"] - ticker_info[ticker]["CurrentPercentage"]) > \
            PERCENT_DRIFT_TOLERANCE:
        significant_drift = True


# Calculate CurrentPercentage, IdealAmount, and IdealPercentage of cash
# Also, detect whether significant portfolio drift has occurred for cash
cash_info["CurrentPercentage"] = cash_info["CurrentAmount"] / total_portfolio_value * 100
cash_info["IdealAmount"] = round(total_portfolio_value * (cash_info["DesiredPercentage"] / 100))
cash_info["IdealPercentage"] = cash_info["IdealAmount"] / total_portfolio_value * 100
if abs(cash_info["DesiredPercentage"] - cash_info["CurrentPercentage"]) > PERCENT_DRIFT_TOLERANCE:
    significant_drift = True


# Construct email body
email_body = "Significant portfolio drift of > " + str(PERCENT_DRIFT_TOLERANCE) + '%' + \
             " has occurred.\nSee below for details.\n\n"

for ticker in ticker_info:
    email_body = email_body + "Analyzing: " + ticker + '\n'
    email_body = email_body + "Current: " + str(ticker_info[ticker]["CurrentAmount"]) + " owned @ $" + \
                 str(ticker_info[ticker]["CurrentValue"]) + "/share, totaling $" + \
                 str(round(ticker_info[ticker]["CurrentAmount"] * ticker_info[ticker]["CurrentValue"], 2)) + \
                 ", making up " + str(round(ticker_info[ticker]["CurrentPercentage"], 2)) + "% of portfolio.\n"
    email_body = email_body + "Ideal: " + str(ticker_info[ticker]["IdealAmount"]) + " owned @ $" + \
                 str(ticker_info[ticker]["CurrentValue"]) + "/share, totaling $" + \
                 str(round(ticker_info[ticker]["IdealAmount"] * ticker_info[ticker]["CurrentValue"], 2)) + \
                 ", making up " + str(round(ticker_info[ticker]["IdealPercentage"], 2)) + "% of portfolio.\n"
    if ticker_info[ticker]["CurrentAmount"] > ticker_info[ticker]["IdealAmount"]:
        email_body = email_body + "To Correct Drift: Sell " + \
                     str(ticker_info[ticker]["CurrentAmount"] - ticker_info[ticker]["IdealAmount"]) + " shares\n\n"
    else:
        email_body = email_body + "To Correct Drift: Buy " + \
                     str(ticker_info[ticker]["IdealAmount"] - ticker_info[ticker]["CurrentAmount"]) + " shares\n\n"

print("START EMAIL BODY AS CONSTRUCTED--------------------------------------------------------------------------------")
print(email_body)
print("END EMAIL BODY AS CONSTRUCTED----------------------------------------------------------------------------------")
print()


# If significant drift has occurred, send email
if significant_drift:
    print("Significant portfolio drift detected: sending email.")
    with open(EMAIL_CRED_FILE) as f:
        SENDER_USERNAME = f.readline()
        SENDER_PASSWORD = f.readline()
    send_email(EMAIL_RECEIVER, EMAIL_SUBJECT, email_body, SENDER_USERNAME, SENDER_PASSWORD)
    print("Email sent successfully.")
else:
    print("No significant portfolio drift detected. Email will not be sent.")
