# Send alert if significant portfolio drift occurs


# Imports
import csv
from yfinance import Ticker
from send_email import send_email


# Constants
INPUT_PATH = "dir/portfolio/"
INPUT_FILE_PORTFOLIO = "tickers.csv"
INPUT_FILE_CASH = "cash.txt"
PERCENT_DRIFT_TOLERANCE = 3.0


# Get and store important data
current_ticker_values = {}
current_cash_value = 0.0
current_ticker_total_values = {}
current_ticker_percentages = {}
current_ticker_amounts = {}
current_cash_percentage = 0.0
total_portfolio_value = 0.0
desired_ticker_percentages = {}
desired_cash_percentage = 100.0
email_receiver = "kagekowalski@gmail.com"
email_subject = "Significant Portfolio Drift Alert"
email_body = "Significant portfolio drift of > " + str(PERCENT_DRIFT_TOLERANCE) + '%' + \
             " has occurred.\nSee below for details.\n\n"

with open(INPUT_PATH + INPUT_FILE_PORTFOLIO, mode='r') as f:
    reader = csv.DictReader(f)

    for row in reader:
        current_ticker_values[row["Ticker"]] = float(Ticker(row["Ticker"]).info["regularMarketPrice"])
        current_ticker_total_values[row["Ticker"]] = \
            current_ticker_values[row["Ticker"]] * int(row["CurrentAmount"])
        total_portfolio_value = total_portfolio_value + current_ticker_total_values[row["Ticker"]]
        desired_cash_percentage = desired_cash_percentage - float(row["DesiredPercentage"])
        desired_ticker_percentages[row["Ticker"]] = float(row["DesiredPercentage"])
        current_ticker_amounts[row["Ticker"]] = int(row["CurrentAmount"])

with open(INPUT_PATH + INPUT_FILE_CASH, mode='r') as f:
    current_cash_value = float(f.read())
    total_portfolio_value = total_portfolio_value + current_cash_value
    current_cash_percentage = (current_cash_value / total_portfolio_value) * 100


for ticker in current_ticker_total_values.keys():
    current_ticker_percentages[ticker] = float((current_ticker_total_values[ticker] / total_portfolio_value) * 100)


# Detect whether significant portfolio drift has occurred
print("\nCHECKING DRIFT")
significant_drift = False
with open(INPUT_PATH + INPUT_FILE_PORTFOLIO, mode='r') as f:
    reader = csv.DictReader(f)

    for row in reader:
        if abs(float(row["DesiredPercentage"]) - current_ticker_percentages[row["Ticker"]]) > PERCENT_DRIFT_TOLERANCE:
            significant_drift = True
            print(row["Ticker"] + " has experienced significant drift.")
            print("abs(" + str(row["DesiredPercentage"]) + " - " + str(current_ticker_percentages[row["Ticker"]]) +
                  ") > " + str(PERCENT_DRIFT_TOLERANCE))
        else:
            print(row["Ticker"] + " has NOT experienced significant drift.")
            print("abs(" + str(row["DesiredPercentage"]) + " - " + str(current_ticker_percentages[row["Ticker"]]) +
                  ") < " + str(PERCENT_DRIFT_TOLERANCE))

if abs(desired_cash_percentage - current_cash_percentage) > PERCENT_DRIFT_TOLERANCE:
    significant_drift = True
    print("cash has experienced significant drift.")
    print("abs(" + str(desired_cash_percentage) + " - " + str(current_cash_percentage) +
          ") > " + str(PERCENT_DRIFT_TOLERANCE))
else:
    print("cash has NOT experienced significant drift.")
    print("abs(" + str(desired_cash_percentage) + " - " + str(current_cash_percentage) +
          ") < " + str(PERCENT_DRIFT_TOLERANCE))


# Get ideally balanced portfolio
ideal_portfolio = {}
for ticker in desired_ticker_percentages.keys():
    ideal_portfolio[ticker] = round((total_portfolio_value * (desired_ticker_percentages[ticker] / 100)) /
                                    current_ticker_values[ticker])

print("\nIDEAL PORTFOLIO")
print(ideal_portfolio)

print("\nIDEAL PORTFOLIO PERCENTAGES")
ideal_portfolio_percentages = {}
for ticker in ideal_portfolio.keys():
    ideal_portfolio_percentages[ticker] = ideal_portfolio[ticker] * current_ticker_values[ticker] / \
                                          total_portfolio_value * 100
    print(ticker + " - " + str(((ideal_portfolio[ticker] * current_ticker_values[ticker]) / total_portfolio_value) *
                               100))


# Send email if current percentage of any ticker is >3% away from its desired percentage
print("\nTO FIX DRIFT")
for ticker in current_ticker_amounts.keys():
    if current_ticker_amounts[ticker] > ideal_portfolio[ticker]:
        print("Sell " + str(current_ticker_amounts[ticker] - ideal_portfolio[ticker]) + " of " + ticker)
    else:
        print("Buy " + str(ideal_portfolio[ticker] - current_ticker_amounts[ticker]) + " of " + ticker)
if significant_drift:
    email_body = email_body + "CURRENT PORTFOLIO\n"
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

    send_email(email_receiver, email_subject, email_body)
