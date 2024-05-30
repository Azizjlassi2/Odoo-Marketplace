
from django.db import models



class OrderItem(models.Model):
    client_id = models.CharField(max_length=200,null=True,blank=True)
    product_id = models.IntegerField(null=True,blank=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    price = models.FloatField(null=True,blank=True)
    quantity = models.IntegerField(default=1,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' product name : {self.name} , client id { self.client_id }'

    @property
    def total(self):
        return self.price * self.quantity

    
    

