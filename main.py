import requests

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_VANTAGE_API_KEY = "FJWEQ4X6LKA2QWNX"
NEWS_API_KEY = "16847859bb1e4f719d1e72a014862c7a"

# Change the date to today.

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

# STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file
 by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
 coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file
 by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
 coronavirus market crash.
"""


parameters_1 = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "outputsize": "compact",
    "apikey": ALPHA_VANTAGE_API_KEY
}

response = requests.get("https://www.alphavantage.co/query", params=parameters_1)
response.raise_for_status()
hundred_day_data = response.json()
yesterday_data = None
day_before_yesterday_data = None

times_running = 0

for thing in hundred_day_data["Time Series (Daily)"]:
    times_running += 1
    if times_running == 1:
        yesterday_data = hundred_day_data["Time Series (Daily)"][thing]
    elif times_running == 2:
        day_before_yesterday_data = hundred_day_data["Time Series (Daily)"][thing]

percentage = None

if float(yesterday_data["4. close"]) > float(day_before_yesterday_data["4. close"]):
    difference = float(yesterday_data["4. close"]) - float(day_before_yesterday_data["4. close"])
    percentage = (difference / float(yesterday_data["4. close"])) * 100
elif float(yesterday_data["4. close"]) < float(day_before_yesterday_data["4. close"]):
    difference = float(day_before_yesterday_data["4. close"]) - float(yesterday_data["4. close"])
    percentage = (difference / float(day_before_yesterday_data["4. close"])) * 100
elif float(yesterday_data["4. close"]) == float(day_before_yesterday_data["4. close"]):
    percentage = 0


get_news = False

if percentage >= 5:
    get_news = True

parameters_2 = {
    "qInTitle": "Tesla",
    "apiKey": NEWS_API_KEY
}

if get_news:
    response_2 = requests.get("https://newsapi.org/v2/everything", params=parameters_2)
    response_2.raise_for_status()
    news = response_2.json()["articles"]
    three_articles = news[:3]
    print(three_articles)
