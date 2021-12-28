import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_VANTAGE_API_KEY = "FJWEQ4X6LKA2QWNX"
NEWS_API_KEY = "16847859bb1e4f719d1e72a014862c7a"
ACCOUNT_SID = "ACda535cb235918e420d29b42c7deb39e8"
AUTH_TOKEN = "ec515758f2ae07ec57700a4f9f50762e"

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
change = None

if float(yesterday_data["4. close"]) > float(day_before_yesterday_data["4. close"]):
    difference = float(yesterday_data["4. close"]) - float(day_before_yesterday_data["4. close"])
    percentage = (difference / float(yesterday_data["4. close"])) * 100
    change = "🔺"
elif float(yesterday_data["4. close"]) < float(day_before_yesterday_data["4. close"]):
    difference = float(day_before_yesterday_data["4. close"]) - float(yesterday_data["4. close"])
    percentage = (difference / float(day_before_yesterday_data["4. close"])) * 100
    change = "🔻"
elif float(yesterday_data["4. close"]) == float(day_before_yesterday_data["4. close"]):
    percentage = 0

get_news = False

if percentage >= 5:
    get_news = True

parameters_2 = {
    "qInTitle": "Tesla",
    "apiKey": NEWS_API_KEY
}

stock_news = []

if get_news:
    response_2 = requests.get("https://newsapi.org/v2/everything", params=parameters_2)
    response_2.raise_for_status()
    news = response_2.json()["articles"]
    three_articles = news[:3]

    first_article = {
        "title": three_articles[0]["title"],
        "description": three_articles[0]["description"]
    }

    second_article = {
        "title": three_articles[1]["title"],
        "description": three_articles[1]["description"]
    }

    third_article = {
        "title": three_articles[2]["title"],
        "description": three_articles[2]["description"]
    }
    stock_news.append(first_article)
    stock_news.append(second_article)
    stock_news.append(third_article)

if get_news:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages \
        .create(
            body=f"TSLA: {change} {int(percentage)}%\n\n"
                 f"Headline: {stock_news[0]['title']}\n"
                 f"Brief: {stock_news[0]['description']}\n\n"
                 f"Headline: {stock_news[1]['title']}\n"
                 f"Brief: {stock_news[1]['description']}\n\n"
                 f"Headline: {stock_news[2]['title']}\n"
                 f"Brief: {stock_news[2]['description']}\n\n",
            from_="+19564462998",
            to="+916379276131",
              )
    print(message.status)
