# 1. Check whether significant portfolio drift has occurred
# 2. Create a message including all information on how to correct portfolio drift
# 3. If significant portfolio drift has occurred, send the message as an email alert
#
# Relies on TICKERS_FILE and CASH_FILE from env_var.py as input data, which represent the portfolio being checked
# TICKERS_FILE is a csv file containing information on tickers in the portfolio, with headers...
# ["Ticker", "DesiredPercentage", "CurrentAmount"]
# CASH_FILE is a txt file containing the amount of cash in the portfolio
# TICKERS_FILE and CASH_FILE must be updated manually


# Imports
import env_var
import csv
from yfinance import Ticker
from send_email import send_email


# Constants
PERCENT_DRIFT_TOLERANCE = 3.0


# Get and store useful info
current_ticker_values = {}
current_ticker_total_values = {}
current_ticker_percentages = {}
current_ticker_amounts = {}
desired_ticker_percentages = {}
current_cash_value = 0.0
current_cash_percentage = 0.0
total_portfolio_value = 0.0
desired_cash_percentage = 100.0

with open(env_var.PORTFOLIO_PATH + env_var.TICKERS_FILE, mode='r') as f:
    reader = csv.DictReader(f)

    for row in reader:
        current_ticker_values[row["Ticker"]] = float(Ticker(row["Ticker"]).info["regularMarketPrice"])
        current_ticker_total_values[row["Ticker"]] = \
            current_ticker_values[row["Ticker"]] * int(row["CurrentAmount"])
        total_portfolio_value = total_portfolio_value + current_ticker_total_values[row["Ticker"]]
        desired_cash_percentage = desired_cash_percentage - float(row["DesiredPercentage"])
        desired_ticker_percentages[row["Ticker"]] = float(row["DesiredPercentage"])
        current_ticker_amounts[row["Ticker"]] = int(row["CurrentAmount"])

with open(env_var.PORTFOLIO_PATH + env_var.CASH_FILE, mode='r') as f:
    current_cash_value = float(f.read())
    total_portfolio_value = total_portfolio_value + current_cash_value
    current_cash_percentage = (current_cash_value / total_portfolio_value) * 100

for ticker in current_ticker_total_values.keys():
    current_ticker_percentages[ticker] = float((current_ticker_total_values[ticker] / total_portfolio_value) * 100)


# Get ideally balanced portfolio amounts
ideal_portfolio = {}
for ticker in desired_ticker_percentages.keys():
    ideal_portfolio[ticker] = round((total_portfolio_value * (desired_ticker_percentages[ticker] / 100)) /
                                    current_ticker_values[ticker])


# Get ideally balanced portfolio percentages
ideal_portfolio_percentages = {}
for ticker in ideal_portfolio.keys():
    ideal_portfolio_percentages[ticker] = ideal_portfolio[ticker] * current_ticker_values[ticker] / \
                                          total_portfolio_value * 100


# Detect whether significant portfolio drift has occurred for any ticker
significant_drift = False
with open(env_var.PORTFOLIO_PATH + env_var.TICKERS_FILE, mode='r') as f:
    reader = csv.DictReader(f)

    for row in reader:
        if abs(float(row["DesiredPercentage"]) - current_ticker_percentages[row["Ticker"]]) > PERCENT_DRIFT_TOLERANCE:
            significant_drift = True


# Detect whether significant portfolio drift has occurred for cash
if abs(desired_cash_percentage - current_cash_percentage) > PERCENT_DRIFT_TOLERANCE:
    significant_drift = True


# Construct email
email_receiver = "kagekowalski@gmail.com"
email_subject = "Significant Portfolio Drift Alert"
email_body = "Significant portfolio drift of > " + str(PERCENT_DRIFT_TOLERANCE) + '%' + \
             " has occurred.\nSee below for details.\n"

email_body = email_body + "\nCURRENT PORTFOLIO\n"
for ticker in current_ticker_amounts.keys():
    email_body = email_body + "Ticker: " + ticker + \
                 " | Amount Owned: " + str(current_ticker_amounts[ticker]) + \
                 " | Percentage of Portfolio: " + "{:.2%}".format(current_ticker_percentages[ticker] / 100) + \
                 " @ " + '$' + str(current_ticker_values[ticker]) + "/share" + '\n'

email_body = email_body + "\nDESIRED PERCENTAGES\n"
for ticker in desired_ticker_percentages.keys():
    email_body = email_body + "Ticker: " + ticker + " | Desired Percentage of Portfolio: " + \
                 "{:.2%}".format(desired_ticker_percentages[ticker] / 100) + '\n'

email_body = email_body + "\nIDEAL PORTFOLIO\n"
for ticker in ideal_portfolio.keys():
    email_body = email_body + "Ticker: " + ticker + \
                 " | Amount Owned: " + str(ideal_portfolio[ticker]) + \
                 " | Percentage of Portfolio: " + "{:.2%}".format(ideal_portfolio_percentages[ticker] / 100) + '\n'

email_body = email_body + "\nACTIONS TO CORRECT DRIFT\n"
for ticker in current_ticker_amounts.keys():
    if current_ticker_amounts[ticker] > ideal_portfolio[ticker]:
        email_body = email_body + "Sell " + str(current_ticker_amounts[ticker] - ideal_portfolio[ticker]) + \
                     " of " + ticker
    else:
        email_body = email_body + "Buy " + str(ideal_portfolio[ticker] - current_ticker_amounts[ticker]) + \
                     " of " + ticker
    email_body = email_body + '\n'

print("EMAIL TO SEND")
print("receiver: " + email_receiver)
print("subject: " + email_subject)
print("body-\n" + email_body)

# If significant drift has occurred, send email
if significant_drift:
    print("\nSignificant portfolio drift detected. Email will be sent.")
    send_email(email_receiver, email_subject, email_body)
    print("Email sent successfully.")
else:
    print("\nNo significant portfolio drift detected. Email will not be sent.")
