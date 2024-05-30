# imports ....
import datetime
import json
import xmlrpc.client
from .models import OrderItem
import requests as r
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator



# api url 
URL = 'http://127.0.0.1:8000/api'
def str_to_dict(data:str,args:list):
    """
    elle aide à convertir une chaine de caractères en un dictionnaire 
    data : la chaine de caractères à convertir 
    args: les clés de dictionnaire à retourner 
    """
    result= {}
    for key in args:
        index = data.find(key)
        # removing all character before the the key
        data = data[index + len(key) : ]
        value = data[data.find(':')+1:data.find(',')]
        result[str(key)]= value.replace('"','')

    return result


def index(request):
    
    if request.method =='GET':
        try:
            CLIENT_ID = request.COOKIES['visitor_uuid']
        except KeyError:    
            try :
                CLIENT_ID = request.COOKIES['session_id']
            except KeyError:
                CLIENT_ID = request.COOKIES['sessionid']
            
        
        order_items = OrderItem.objects.filter(client_id=CLIENT_ID)
        total = 0
        nb_items = 0
        for item in order_items:
            total += item.total
            nb_items += item.quantity
        

        # pour afficher la liste des catégories dans cette page !
        list_catg = r.get(f'{URL}/catg/').json()

        product = r.get(f'{URL}/produits/').json()
        # Set up Pagination
               

        catg_prod_list = zip(list_catg,product)
        

        context = {'total':total,
                    'nb_items':nb_items,
                    'list_catg':list_catg,
                    'product':product,
                    'catg_prod_list':catg_prod_list,
                    }

        return render(request,'pages/index.html',context)

def contact(request):

    try:
        CLIENT_ID = request.COOKIES['visitor_uuid']
    except KeyError:    
        try :
            CLIENT_ID = request.COOKIES['session_id']
        except KeyError:
            CLIENT_ID = request.COOKIES['sessionid']

    order_items = OrderItem.objects.filter(client_id=CLIENT_ID)
    total = 0
    nb_items = 0
    for item in order_items:
        total += item.total
        nb_items += item.quantity

    # pour afficher la liste des catégories dans cette page !
    list_catg = r.get(f'{URL}/catg/').json()

    return render(request,'pages/contact.html',{'list_catg':list_catg,'total':total,'nb_items':nb_items})
def checkout(request):

    try:
        clientId = request.COOKIES['visitor_uuid']
    except KeyError:    
        try :
            clientId = request.COOKIES['session_id']
        except KeyError:
            clientId = request.COOKIES['sessionid']    


    order_items = OrderItem.objects.filter(client_id=clientId)
    nb_items = 0
    total = 0
    for item in order_items:
        total += item.total
        nb_items += item.quantity


    

    # pour afficher la liste des catégories dans cette page !
    list_catg = r.get(f'{URL}/catg/').json()

    return render(request,'pages/checkout.html',{'list_catg':list_catg,'order_items':order_items,'total':total,'nb_items':nb_items})

def shop_details(request,id):
    
    try:
        CLIENT_ID = request.COOKIES['visitor_uuid']
    except KeyError:    
        try :
            CLIENT_ID = request.COOKIES['session_id']
        except KeyError:
            CLIENT_ID = request.COOKIES['sessionid']



    order_items = OrderItem.objects.filter(client_id=CLIENT_ID)
    total = 0
    nb_items = 0
    for item in order_items:
        total += item.total
        nb_items += item.quantity

    # pour afficher la liste des catégories dans cette page !
    list_catg = r.get(f'{URL}/catg').json()
    
    #selectionner les informations du produit (id)
    response_produit = r.get(f'{URL}/produit/{id}/').json()
    response_related_produit = r.get(f'{URL}/related_prod/{id}/').json()
    # importer 5 elements seulement 
    response_related_produit = response_related_produit[:4]
    
 
    


    return render(request,'pages/shop-details.html',{'item':response_produit,'related_product':response_related_produit,'list_catg':list_catg
    ,'total':total,'nb_items':nb_items})





def shop_grid(request,id_catg=None,safe=False):
 
    if request.method =='GET':
        
        CLIENT_ID = request.COOKIES['visitor_uuid']
        
        order_items = OrderItem.objects.filter(client_id=CLIENT_ID)
        total = 0
        nb_items = 0
        for item in order_items:
            total += item.total
            nb_items += item.quantity        
        # pour afficher la liste des catégories dans cette page !
        list_catg = r.get(f'{URL}/catg/').json()
        products = r.get(f'{URL}/produits/').json()
        p =Paginator(products,15)
        page= request.GET.get('page')
        product_paginate = p.get_page(page) 
        #response = response[:12]
        if id_catg == None:
            return render(request,'pages/shop-grid.html',{'products':products,'list_catg':list_catg,'total':total,'nb_items':nb_items,'product_paginate':product_paginate})
        else:
            # filtrer le sproduits selon l'id d'une catégorie
            produit_selon_catg = r.get(f'{URL}/prod_catg/{id_catg}').json()
            return render(request,'pages/shop-grid.html',{'model':products,'list_catg':list_catg,'produit_selon_catg':produit_selon_catg,'total':total,'nb_items':nb_items})






def shop_cart(request):
    try:
        CLIENT_ID = request.COOKIES['visitor_uuid']
    except KeyError:    
        try :
            CLIENT_ID = request.COOKIES['session_id']
        except KeyError:
            CLIENT_ID = request.COOKIES['sessionid']
    order_items = OrderItem.objects.filter(client_id=CLIENT_ID)
    total = 0
    nb_items = 0
    for item in order_items:
        total += item.total
        nb_items += item.quantity

    list_catg = r.get(f'{URL}/catg/').json()
    return render(request,'pages/shoping-cart.html',{'list_catg':list_catg,'order_items':order_items,'total':total,'nb_items':nb_items})

def blog(request):
    list_catg = r.get(f'{URL}/catg/').json()
    return render(request,'pages/blog.html',{'list_catg':list_catg})

def blog_details(request):
    list_catg = r.get(f'{URL}/catg/').json()
    return render(request,'pages/blog-details.html',{'list_catg':list_catg})

def updateItem(request):

    DATA=''
    message=''
   

    try:
        CLIENT_ID = request.COOKIES['visitor_uuid']
    except KeyError:    
        try :
            CLIENT_ID = request.COOKIES['session_id']
        except KeyError:
            CLIENT_ID = request.COOKIES['sessionid']

    try:
        DATA=request.read().decode('utf-8') 
        DATA = str_to_dict(DATA,['productId','action','user'])
        
    except json.decoder.JSONDecodeError:
        print('json.decoder.JSONDecodeError problem has been detected !')

    except r.exceptions.JSONDecodeError:
        print('JSONDecodeError problem has been detected !')
    except:
        print('ERROR ')

    

    if DATA:
        PRODUCT_ID = DATA['productId']
        
        Action = DATA['action']


        if Action == 'add':
            try:    
                product = OrderItem.objects.get(client_id=CLIENT_ID,product_id=PRODUCT_ID)
                product.quantity +=1
                product.save()
            except OrderItem.DoesNotExist:
                
                DATA = r.get(f'{URL}/produit/{PRODUCT_ID}/').json()
                product = OrderItem()
                product.product_id = PRODUCT_ID
                product.client_id = CLIENT_ID
                product.name = DATA['name']
                product.price = DATA['list_price']
                product.save()

        elif Action == 'remove':
            product = OrderItem.objects.get(client_id=CLIENT_ID,product_id=PRODUCT_ID)
            if product.quantity ==1:    
                product.delete()
            else:
                product.quantity -=1
        elif Action == 'delete':
            OrderItem.objects.get(client_id=CLIENT_ID,product_id=PRODUCT_ID).delete()
            try:
                product = OrderItem.objects.get(client_id=CLIENT_ID,product_id=PRODUCT_ID)
            except OrderItem.DoesNotExist:
                message='item deleted !'
                print('item deleted !')
                

    

        message ='item added '


    return JsonResponse(message,safe=False)


def create_order(request):
    print('Creating order ..........')
    try:
        user = request.COOKIES['visitor_uuid']
    except KeyError:    
        try :
            user = request.COOKIES['session_id']
        except KeyError:
            user = request.COOKIES['sessionid']
    print('USER : ',user)
    

    MONTANT_PAYER =True
    CONFIRMER_COMMANDE =False


 
    # établir la connection avec serveur odoo
    URL_ODOO = 'http://127.0.0.1:8069'
    db = 'marketplace'
    username = 'azizjlassi498@gmail.com'
    password = 'azizjlassi'
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(URL_ODOO))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(URL_ODOO))
    DATA=request.read().decode('utf-8') 
    DATA = str_to_dict(DATA,['first_name','last_name','country','address_1','address_2','city','state','postcode','phone','email','acc'])
    print('DATA :',DATA)
    if request.method == 'POST':
        order_data = {
                
                "state": "draft",
                "date_order": str(datetime.date.today()), # Date du devis
                "user_id": 2,
                "partner_id": 42,
                "partner_invoice_id":41, #Adresse de facturation
                "partner_shipping_id": 42, # Adresse de livraison
                "picking_policy": "direct",
                "pricelist_id": 5, #  Liste de prix
                "note": "note",
            }
        order = models.execute_kw(db, uid, password, 'sale.order', 'create', [order_data]) # création d'un order 
        print('création order N° : ',order)
        total = 0
        data = OrderItem.objects.filter(client_id=user)
        for item in data:
            try:
                total += item.total
                order_line = models.execute_kw(db, uid, password, 'sale.order', 'write',[[order], {'order_line': [(0, '_', {"product_id": item.product_id, "product_uom_qty": item.quantity,'price_unit':item.price})]}],{})
            except   xmlrpc.client.Fault:
                print(f'Record id :{item.product_id} :  { item.name } does not exist or has been deleted !')
                print(user)
                print(OrderItem.objects.filter(product_id=item.product_id))
                print(f'Record id :{item.product_id} :   { item.name }  has been deleted !')

        if MONTANT_PAYER:
            # traitement de payement 
            models.execute_kw(db, uid, password, 'sale.order', 'write', [[order], {'state': "sent"}])
            print('Devis envoyé ......')

        if MONTANT_PAYER and CONFIRMER_COMMANDE:
            # confirmation de commande 
            models.execute_kw(db, uid, password, 'sale.order', 'write', [[order], {'state': "sale"}])
            print('Commande confirmé ......')

        # création facture 



        print(f'items for order {order} added !')
        OrderItem.objects.filter(client_id=id).delete()
        return redirect('mysite:index')
    return JsonResponse('order added !',safe=False)


def clear(request):
    """
    Cette fonction efface tous les enregistrements
    situés dans la base de données
    """
    OrderItem.objects.all().delete()
    print(OrderItem.objects.all())
    return JsonResponse('data base clear',safe=False)









