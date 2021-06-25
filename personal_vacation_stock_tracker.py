from datetime import datetime
import yfinance as yf
import FinNews as fn
from pytz import timezone
import smtplib, time, json

tickers = ["fcel", "nok", "ride", "amc", "gme", "clne"]
stock_times = ["18:33:50", "12:00:00", "15:55:00"]

with open("gmail.json") as file: #opens a json file for my email credentials
    config= json.load(file)
    file.close()

def stock_information():
    #get empty deictionary for my stock news and for the stock price 
    stock_dict = {}
    stock_news = {}
    for i in tickers:
        news_link = []#make an empty list used later to added it into a list and from there, add it into a dictionary
        stock_ticker_list = [] #Make an empty list 
        stocks = yf.Ticker(i) #gets the stock tickers from the list per above
        stock_data = stocks.info #use the yfinance library to pull information about the ticker
        price = round(((stock_data["bid"] + stock_data["ask"])/2), 2) #calculating the stock price
        stock_dict[i] = price #Creates a dictionary of stock tickers and their respective stock price
        ticker_news  = fn.Yahoo(topics =['financial', f'${i}'], save_feeds=True).get_news() # gets news

        # appends the stock news for each ticker into a list and then into a dictionary 
        stock_ticker_list.append(i)
        stock_news_1 = ticker_news[0]["link"]
        news_link.append(stock_news_1)
        stock_news_2 = ticker_news[1]["link"]
        news_link.append(stock_news_2)
        stock_news_3 = ticker_news[2]["link"]
        news_link.append(stock_news_3)
        stock_news[i]= news_link
        print("done")
    #email the stock news and the stock price 
    smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(config["username"], config["password"])
    smtpObj.sendmail("kazushiemailbot@gmail.com", "kaznater@gmail.com", f"Subject: Stock Prices on {(datetime.now()).strftime('%m/%d/%y')}\n\nThe Price for Fuel Cell Energy is {stock_dict['fcel']}\n Here are some news articles on it\n {stock_news['fcel'][0]}\n\n{stock_news['fcel'][1]}\n\n{stock_news['fcel'][2]}\n\nThe price for Nokia is {stock_dict['nok']}\n Here are some news articles on it\n {stock_news['nok'][0]}\n\n{stock_news['nok'][1]}\n\n{stock_news['nok'][2]}\n\nThe price for Lordstown Motors('RIDE') is {stock_dict['ride']}\n Here are some news articles on it\n {stock_news['ride'][0]}\\n\n{stock_news['ride'][1]}\n\n{stock_news['ride'][2]}\n\nThe price for AMC is {stock_dict['amc']}\n Here are some news articles on it\n {stock_news['amc'][0]}\n\n{stock_news['amc'][1]}\n\n{stock_news['amc'][2]}\n\n\nThe price for Gamestop is {stock_dict['gme']}\n Here are some news articles on it\n {stock_news['gme'][0]}\n\n{stock_news['gme'][1]}\n\n{stock_news['gme'][2]}\n\nThe price for Clean Energy Corp is {stock_dict['clne']}\n Here are some news articles on it\n {stock_news['clne'][0]}\n\n{stock_news['clne'][1]}\n\n{stock_news['clne'][2]}")
    smtpObj.quit()
    print("done!")
        
        
def morning_time(time):
    #goes to the list above for stock times and confirms when to execute the script
    for i in stock_times:
        if i == time:
            print("working on this")
            stock_information()
            
    else:
        print("it is not time")

while True:
    #executes the above morning_time script and puts the time into eastern timezone to base off the stock market opening and closing times
    time.sleep(1)
    eastern = timezone("US/Eastern")
    eastern_now = datetime.now(eastern)
    eastern_zone = eastern_now.strftime("%H:%M:%S")
    print(eastern_zone)
    morning_time(eastern_zone)
    
  
