from django.urls import include, path
from . import views
app_name ='mysite'


urlpatterns = [
    path('',views.index,name='index',),

    path('shop-details/<int:id>/',views.shop_details,name='shop-details'),
    path('contact/',views.contact,name='contact'),
    path('checkout/',views.checkout,name='checkout'),

    path('shop-grid/',views.shop_grid,name='shop-grid'),

    path('shop-grid/<int:id_catg>/',views.shop_grid,name='shop-grid-catg'),
    path('shop-cart/',views.shop_cart,name='shop-cart'),
    path('blog/',views.blog,name='blog'),
    path('blog-details/',views.blog_details,name='blog-details'),



    path('shop-grid/update_item/',views.updateItem,name='update_item'),
    path('checkout/create_order/',views.create_order),
    
    path('clear/',views.clear)

    
    ]
    