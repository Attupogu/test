STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "4W2V1055U0TJSIF4"
NEWS_API_KEY= "d2b56313973b4056a1092b9c7ef08fb9"
STOCK_FUNCTION="TIME_SERIES_DAILY_ADJUSTED"

import requests
from datetime import datetime, timedelta
from twilio.rest import Client

today = datetime.now().date()

yesterday = today - timedelta(days=1)
day_before_yesterday = yesterday-timedelta(days=1)




stock_params= {
  "function": STOCK_FUNCTION,
  "symbol":STOCK_NAME,
  "apikey":STOCK_API_KEY,
}
response_stock= requests.get(url=STOCK_ENDPOINT,params=stock_params)

stock_data= response_stock.json()['Time Series (Daily)']
stock_data_list = [value for (key, value) in stock_data.items()]
yesterday_data= stock_data_list[0]
yesterday_close= float(yesterday_data['4. close'])


print(yesterday_close)


day_before_yesterday_data = stock_data_list[1]
day_before_yesterday_close= float(day_before_yesterday_data['4. close'])

print(day_before_yesterday_close)


stock_price_change= (yesterday_close- day_before_yesterday_close)
percentage_stock_price_change = round(abs(stock_price_change)*100/ yesterday_close,2)

print(percentage_stock_price_change)

up_down= None
if stock_price_change<0:
  up_down = "🔻"
else:
  up_down="🔺"


if percentage_stock_price_change> 4:

  news_params={
    "q":COMPANY_NAME,
    "from": yesterday,
    "apiKey":NEWS_API_KEY
  }
  response_news= requests.get(url=NEWS_ENDPOINT, params=news_params)

  result_news= response_news.json()
  articles= result_news['articles']
  first_three_articles= articles[:3]




formatted_articles = [f"{STOCK_NAME}: {up_down} {percentage_stock_price_change}% \n Headline: {article['title']},\nBrief: {article['description']}" for article in first_three_articles]


account_sid = 'ACb702f990a893265a3ea991b26d9d86b0'
auth_token = '4c0b4412ceeeb151915579b8cd8c1233'
client = Client(account_sid, auth_token)

for article in formatted_articles:
  message = client.messages.create(
    from_='+13156934153',
      body= article ,
      to='+919679838331'
)

print(message.sid)


#Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""



#from twilio.rest import Client
#
#account_sid = 'ACb702f990a893265a3ea991b26d9d86b0'
#auth_token = '4c0b4412ceeeb151915579b8cd8c1233'
#client = Client(account_sid, auth_token)
#
#message = client.messages.create(
#  from_='+13156934153',
#  body='Message goes here',
#  to='+919679838331'
#)
#
#print(message.sid)