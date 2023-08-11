
from __future__ import absolute_import,unicode_literals
import os 
from celery import Celery
import json
from django.conf import Settings
# import django
# django.setup() 


# from celery.schedules import crontab
# use to schedule task at particular time
# from main.task import update_stock
# from main.models import StockCache



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_tracker.settings")



# stocks_data = StockCache.objects.get(User1=1).stocks.all()
# stocks_name = []
# for each in stocks_data:
#     stocks_name.append(each.name)



app = Celery("stock_tracker")
app.conf.enable_utc = False
app.conf.update(timezone="Asia/Kolkata")
app.config_from_object(Settings,namespace='CELERY')
# app.conf.beat_schedule = {
#     'every-20-seconds':{
#         'task': update_stock,
#         'schedule':20,
#         'args': (stocks_name)
#     }
# }



app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print("errors: ",self.request)
