from . import views
from django.urls import path

app_name ='accounts'

urlpatterns = [
    path('login_user/',views.login_user,name='login'),
    path('logout_user/',views.logout_user,name='logout'),
    path('signup/',views.signup,name='signup'),
    
]
