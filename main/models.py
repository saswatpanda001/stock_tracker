


from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()




class Stocks(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name
    

class StockCache(models.Model):
    User1 = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True,related_name="user_model")
    stocks = models.ManyToManyField(Stocks,related_name="stocks_model")

    def __str__(self):
        return self.User1.username

