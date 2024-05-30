from . import views
from django.urls import path
app_name ='payment'



urlpatterns = [
    path('',views.paypal,name='paypal'),
]