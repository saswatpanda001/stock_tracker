

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from yahoo_fin import stock_info as si 
import pandas as pd
import requests 
import time
import queue
from django.http import HttpResponse
from threading import Thread
from main.models import StockCache,Stocks


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



@login_required
def home(request):
    return render(request,"home.html")


@login_required
def picker(request):
    
    stocks_all = si.tickers_nifty50()
    return render(request,"pick_stocks.html",{"stocks":stocks_all})



shared_data = []

@login_required
def trader(request):
    res_data = []
    
    if request.POST:
        if request.POST.getlist('stock_list'):
            
            start = time.time
            stocks_name = request.POST.getlist('stock_list')
            
            StockCache.objects.get(User1=request.user.id).stocks.set([])

            for each in stocks_name:
                st = Stocks.objects.filter(name=str(each)).first()

                print(st)
                StockCache.objects.get(User1=1).stocks.add(st)
                


            thread_list = []
            for each in stocks_name:
                th = Thread(target=get_quote_table,args=[each,res_data])
                thread_list.append(th)
                th.start()
            for each in thread_list:
                each.join()
            end = time.time()
            shared_data = res_data
            return render(request,"trade_stocks.html",{"data":res_data})
    else:
        return HttpResponse("No stocks picked")        
            
@login_required
def trade_data(request):
    return render(request,"trade_data.html",{"data":shared_data})
   
    
    