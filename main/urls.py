
from django.urls import path,include
from main import views

app_name = "main_app"

urlpatterns = [
    path('', views.home,name="home"),
    path('main/pick_stocks', views.picker,name="pick_stocks"),
    path('main/trade', views.trader, name="trade_stocks"),
    path('main/trade_data', views.trade_data, name="trade_stocksdata")
]


