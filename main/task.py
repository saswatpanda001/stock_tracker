import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_tracker.settings")

django.setup()



from celery import shared_task
from main.views import shared_data

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from yahoo_fin import stock_info as si 
import pandas as pd
import requests 
import time
import queue
from django.http import HttpResponse
from threading import Thread




def get_quote_table(stock_name,res_data):
    headers = {'User-agent': 'Mozilla/5.0'} 
    site = "https://finance.yahoo.com/quote/" + stock_name + "?p=" + stock_name
    tables = pd.read_html(requests.get(site, headers=headers,verify=False).text)
    data = pd.concat([tables[0], tables[1]])
    data.columns = ["attribute" , "value"]
    quote_price = pd.DataFrame(["Quote Price", si.get_live_price(stock_name)]).transpose()
    quote_price.columns = data.columns.copy()
    data = pd.concat([data, quote_price])
    data = data.drop_duplicates().reset_index(drop = True)
    # data["value"] = data.value.map(force_float)
    result = {key : val for key,val in zip(data.attribute , data.value)}
    st_data = {}
    st_data["price"] = format(result["Quote Price"],".2f")
    st_data["pe_ratio"] = result["PE Ratio (TTM)"]
    st_data["stock_name"] = stock_name
    st_data["52_week_range"] = result["52 Week Range"]
    st_data["market_cap"] = result["Market Cap"]
    st_data["eps"] = result["EPS (TTM)"]
    st_data["volume"] = result["Volume"]
    st_data["prev_close"] = result["Previous Close"]
    res_data.append(st_data)

## when user1 has picked up 5 stocks then celery will update it every n seconds
## if user2 has also picked up 3 common stocks that user1 has, then we will only add the extra 2 stocks to celery task list
## so that no extra process is created
# if there is no user in website then all process will be deleted
## when celery will request data from yahoo, the frontend will be updated using websockets, database is not updated here
       
            

@shared_task(bind=True)
def update_stock(stock_list):
    stocks_name= ['RELAIANCE.NS','BAJAJFINSV.NS']
    res_data = []
    start = time.time()
    thread_list = []

    for each in stocks_name:    
        th = Thread(target=get_quote_table,args=[each,res_data])
        thread_list.append(th)
        th.start()
        
    for each in thread_list:
        each.join()
               
    end = time.time()
    return 'Done'















