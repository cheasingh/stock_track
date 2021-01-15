from newsapi import NewsApiClient
from twilio.rest import Client
import json
import requests
import os


def get_news(query):
    '''
    query news from well knowns source, get 2 inputs mark ask required
    query=string, topic name
    count=int, number of query 
    '''
    newsapi = NewsApiClient(api_key=os.environ["NEWSAPI"])
    get_news = newsapi.get_everything(q=query)

    # j_to_string = json.dumps(get_news, indent=4)

    use_article = get_news["articles"][0]
    return [use_article["title"], use_article["author"]]


def get_stock(query):
    endpoint = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY"
    query = {
        "symbol": query,
        "apikey": os.environ["ALPHA_VINTAGE"]
    }

    return requests.get(endpoint, query).json()["Time Series (Daily)"]


def cal_dif(n):
    query = get_stock(query="TSLA")
    close_one = float(query[n[0]]["4. close"])
    close_two = float(query[n[1]]["4. close"])

    result = close_one - close_two
    result_percent = (abs(result) / close_one) * 100

    print(result_percent)
    # result = 200 - 10

    if result_percent > 5:
        return True
    else:
        return False


def send_message(data):
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=data,
        from_='+18705282420',
        to='+85511702696'
    )
    print(message.status)


    # convert dict to list, using its key
    # get 2 lists value from stock result
stock = list(get_stock(query="TSLA").keys())[:2]

if cal_dif(stock) == True:
    news = get_news("tsla")
    body = f"{news[0]} by {news[1]}"
    send_message(body)
else:
    send_message("everything look normal")
