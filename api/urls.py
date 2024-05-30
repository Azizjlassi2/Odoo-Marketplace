from django.urls import path, register_converter
from . import views ,converts
from rest_framework.urlpatterns import format_suffix_patterns

register_converter(converts.FloatUrlParameterConverter, 'float')

urlpatterns = [
    path('produits/',views.products),
    path('products_qty_available/',views.products_qty_available),
    path('produit/<int:id>/',views.produit),
    path('catg/',views.categories),
    path('related_prod/<int:id>/',views.related_product),
    path('prod_catg/<int:id_catg>/',views.prod_selon_catg),
    path('catg/<int:id>/',views.catg_id),
    path('users/',views.users),
    path('user/<str:email>/<str:pwd>',views.user),
    path('commandes/',views.commande),
    path('commande/<int:id>/',views.commande),
    path('saleorderFields/',views.saleorderfields),
    path('saleordertemplatefields/',views.saleordertemplatefields),
    path('respartner/',views.respartner),
    path('respartner/<str:name>/',views.respartner),
    path('devis/',views.devis),
    path('devis/<int:id>/',views.devis),
    path('devis/<str:symbol>/',views.devis),
    path('devis/<int:id>/<float:rate>/',views.devis),
    path('pricelist/',views.pricelist),
    path('pricelist/<int:id>',views.pricelist),
    path('paiment_link_wizard/',views.paimentLinkWizard),
    path('paiment_link_wizard/<str:id>/',views.paimentLinkWizard),
    path('stockpicking/',views.stockpicking),
    path('stockpicking/<int:id>/',views.stockpicking),
    path('upadtepolitique/<int:id>/',views.changerPolitiqueExpédition),
    path('factures/',views.factures),
    path('facture/<str:name>/',views.factures),
    path('facture/<int:id>',views.facture),
    path('purchase-order/',views.purchase_order)

]

urlpatterns = format_suffix_patterns(urlpatterns)
