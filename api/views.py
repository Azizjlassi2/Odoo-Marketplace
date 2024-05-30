
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import xmlrpc.client as xc




url = 'http://127.0.0.1:8069'
db = 'marketplace'
username ='azizjlassi498@gmail.com'
password = 'azizjlassi'


"""
Create = POST
Retrieve = GET
Update = PUT
Delete = DELETE

"""

# création du lien avec le serveur 
common = xc.ServerProxy(f'{url}/xmlrpc/2/common')

#création du user id 
uid = common.authenticate(db, username,password,{})

# création le lien avec le schéma 'res' de la bd
models = xc.ServerProxy(f'{url}/xmlrpc/2/object')


# Create your views here.

# api produits 

@api_view(['GET','PUT'])
def products(request,format=None):
    # lire les enregistrements 
    if request.method == 'GET':

        list_products = models.execute_kw(db,uid,password,'product.template','search_read',[[]])
        # on va retourner tout les détails des produits 
        return Response(list_products)
    
    # création d'un enregistrement
    elif request.method == 'PUT':
        models.execute_kw(db,uid,password,'product.template','create',[request.data])
        return Response(request.data,status=status.HTTP_201_CREATED)


@api_view(['GET','POST','DELETE'])
def produit(request,id , format=None):
    # lire un enregistrement (id)
    if request.method == 'GET':
        product_rec = models.execute_kw(db,uid,password,'product.template','search',[[['id', '=',id]]])
        if product_rec == []:
            return Response("aucun record trouvé",status= status.HTTP_404_NOT_FOUND)
        # si la liste n'est pas vide
        product_rec = models.execute_kw(db,uid,password,'product.template','read',[id])
        return Response(product_rec[0])

    # modifier un enregistrement (id)
    elif request.method == 'POST':
        product_rec = models.execute_kw(db,uid,password,'product.template','search',[[['id', '=',id]]])
        if product_rec == []:
            return Response("aucun record trouvé",status= status.HTTP_400_BAD_REQUEST)

        models.execute_kw(db,uid,password,'product.template','write',[[id],request.data])
        return Response(request.data,status=status.HTTP_201_CREATED)
    # supprimer un enregistrement (id)
    elif request.method == 'DELETE':
        product_rec = models.execute_kw(db,uid,password,'product.template','search',[[['id', '=',id]]])
        if product_rec == []:
            return Response("aucun record trouvé",status= status.HTTP_404_NOT_FOUND)

        models.execute_kw(db, uid, password, 'product.template', 'unlink', [[id]])
        # check if the deleted record is still in the database
        models.execute_kw(db, uid, password, 'product.template', 'search', [[['id', '=', id]]])
        return Response("record suppimé !")

# api for Categories

@api_view(['GET'])
def categories(request,format=None):
    if request.method == 'GET':
        categories_list = models.execute_kw(db,uid,password,"product.category",'search_read',[[]])
        return Response(categories_list) 


@api_view(['GET'])
def related_product(request,id):
    # fetchinig the principale  product (id)
    if request.method == 'GET':
        record_id_product = models.execute_kw(db,uid,password,'product.template','search_read',[[['id','=',id]]])
        categ_id_for_id_product = record_id_product[0]["categ_id"][0]
        record_related_product = models.execute_kw(db,uid,password,'product.template','search_read',[[['categ_id', '=',categ_id_for_id_product]]])
        
    return Response(record_related_product)


@api_view(['GET'])
def prod_selon_catg(request,id_catg,format=None):
    if request.method == 'GET':
        catg = models.execute_kw(db,uid,password,'product.category','search_read',[[['id','=',id_catg]]])
        catg_name = catg[0]['name']
        catg_id = [str(id_catg),str(catg_name)]
        list_prod = models.execute_kw(db,uid,password,'product.template','search_read',[[['categ_id','=',catg_id]]])
        return Response(list_prod)

@api_view(['GET'])
def catg_id(request,id,format=None):
    if request.method == 'GET':
        catg = models.execute_kw(db,uid,password,'product.category','search_read',[[['id','=',id]]])
        return Response([id,catg[0]['name']])


# latest product 

@api_view(['GET','PUT'])
def users(request,format=None):
    if request.method == 'GET':
        
        users = models.execute_kw(db,uid,password,'res.users','search_read',[[]])
        return Response(users)

    if request.method =='PUT':
        models.execute_kw(db,uid,password,'res.users','create',[request.data])
        return Response(request.data,status=status.HTTP_201_CREATED)
    

@api_view(['GET','POST','DELETE'])
def user(request,email=None,pwd=None,format=None):
    if email != None or pwd != None :
        if request.method == 'GET':
            uid = common.authenticate(db,username,password,{})
            user = models.execute_kw(db,uid,password,'res.users','search_read',[[['email','=',email],['password','=',pwd]]])
            if user == []:
                return Response("aucun utilisateur trouvé",status= status.HTTP_404_NOT_FOUND)
            
            return Response(user[0])
        
        
        if request.method =='POST':
            if email != None:
                models.execute_kw(db,uid,password,'res.users','write',[[email],request.data])
                return Response('utilisateur modifié !',status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            
            user_rec = models.execute_kw(db,uid,password,'res.users','search',[[['email', '=',email],['password','=',password]]])
            if user_rec == []:
                return Response("aucun utilisateur trouvé",status= status.HTTP_404_NOT_FOUND)
            
            models.execute_kw(db, uid, password, 'res.users', 'unlink', [[email]])
            return Response("utilisateur suppimé !")


@api_view(['GET','POST'])
def commande(request,id=None):
    if request.method == 'GET':
        if id==None:
            commandes = models.execute_kw(db,uid,password,'sale.order','search_read',[[]])
            return Response(commandes)
        else:
            commandes = models.execute_kw(db,uid,password,'sale.order','search_read',[[['id','=',id]]])
            return Response(commandes)



@api_view(['GET'])
def saleorderfields(request):
    if request.method =='GET':
       fields =  models.execute_kw(db, uid, password, 'sale.order', 'fields_get', [], {'attributes': ['string', 'help', 'type']})    
       return Response(fields)



@api_view(['GET','PUT'])
def respartner(request,name=None):
    """
    name = None  : retoune tous les contacts 
    name != None : retorune le contact correspondant au name 
    """
    if name == None:
        partners = models.execute_kw(db,uid,password,'res.partner','search_read',[[]])
        return Response(partners)   
    else:
        partners = models.execute_kw(db,uid,password,'res.partner','search_read',[[['name','=',name]]])
        return Response(partners)   
   
@api_view(['GET','POST'])
def devis(request,rate=None,id=None,symbol=None):
    if request.method == 'GET':
        if symbol !=None:
            devislist = models.execute_kw(db,uid,password,'res.currency','search_read',[[['symbol','=',symbol]]])
            return Response(devislist)
        elif id != None:
            devislist = models.execute_kw(db,uid,password,'res.currency','search_read',[[['id','=',id]]])
            return Response(devislist)
        else:
            devislist = models.execute_kw(db,uid,password,'res.currency','search_read',[[]])
            return Response(devislist)





    if request.method == 'POST':
        # rate est la valeur de la monnie par rapport au dollar
        devislist = models.execute_kw(db,uid,password,'res.currency','write',[[id],{'rate': rate}])
        devis = models.execute_kw(db,uid,password,'res.currency','search_read',[[['id','=',id]]])

        return Response(devis)


@api_view(['GET'])
def pricelist(request):
    pricelist = models.execute_kw(db,uid,password,'product.pricelist','search_read',[[]])
    return Response(pricelist)

    
@api_view(['GET'])
def paimentLinkWizard(request,id=None):
    if id == None:
        paimentLinkWizardList = models.execute_kw(db,uid,password,'payment.link.wizard','fields_get', [], {'attributes': ['string', 'help', 'type']})
        return Response(paimentLinkWizardList)
    else:
        paimentLinkWizardList = models.execute_kw(db,uid,password,'payment.link.wizard','search_read',[[['id','=',id]]])
        return Response(paimentLinkWizardList)



@api_view(['GET'])
def saleordertemplatefields(request):
    """
    
    elle retoune les champs du model 'sale.order' """
    if request.method =='GET':
       fields =  models.execute_kw(db, uid, password, 'sale.order.template', 'fields_get', [], {'attributes': ['string', 'help', 'type']})    
       return Response(fields)

@api_view(['GET'])
def stockpicking(request,id=None):
    """
    parmetre id = None  : elle retorune tous les commandes qui ont un état  'bon de commande' 
    parmetre id != None : elle retourne la commande correspondant
    """
    if request.method == 'GET':
        if id ==None:
            response = models.execute_kw(db,uid,password,'stock.picking','search_read',[[]])
            return Response(response)        
        # modifier  pour quelle a une realtion avec sale.order
        if id!=None:
            try :
                res = models.execute_kw(db,uid,password,'sale.order','search_read',[[['id','=',id]]])[0] # the first element 
            except IndexError:
                return Response(f'la commande {id} n\'existe pas !')
            name = res['name']
            sale_id = [str(id),str(name) ]
            try:
                response = models.execute_kw(db,uid,password,'stock.picking','search_read',[[['sale_id','=',sale_id]]])[0]
            except IndexError:
                return Response(f'cette commande : (id : {id} , name : {name}) n\'est pas validé comme une bon de commande ,    \
                vous devez la valider d\'abort ! ')
            return Response(response)


# sale.order (id) => stock.picking([id,name])  => account.move (invoice_origin= name(stock.picking) )

@api_view(['POST'])
def changerPolitiqueExpédition(request,id=None,format=None):


    """
    Parametre id : prend l'identificateur d'une instance de la classe stock.picking !
    
    elle change la politique d'expédition en 'Lorsque tous les articles sont prèts !

    elle retourne 1 si le changement a eté effetué sinon -1

    """
    if request.method == 'POST':
        if id==None:
            raise MissingParameter
        elif id != None:
            try:
                models.execute_kw(db,uid,password,'stock.picking','write',[[id],{'move_type':'one'}])
                return Response(1)
            except :
                return Response(-1)


@api_view(['GET','PUT'])
def factures(request,name=None,format=None):

    """
    le parametre name correspond a l'identificateur d'une instance sale.order
    """
    
    if request.method == 'GET' and name ==None:
        """
        retourne tous les factures de type Factures Client ('move_type','=','out_invoice')
        """
        res = models.execute_kw(db,uid,password,'account.move','search_read',[[['move_type','=','out_invoice']]])
        return Response(res)
    
    elif request.method == 'GET' and name !=None: 
        """
        retourne la facture qui correspond au nom de la commande (sale.order)
        """
        res = models.execute_kw(db,uid,password,'account.move','search_read',[[['move_type','=','out_invoice'],['invoice_origin','=',name]]])[0]
        return Response(res)
    
    elif request.method == 'PUT' and name !=None:
        # recupérer les informations nécessaires pour remplir la facture correctement ! avec le paramètre 'name' 

        res = models.execute_kw(db,uid,password,'account.move','search_read',[[['move_type','=','out_invoice'],['invoice_origin','=',name]]])[0]
        print('RES: ',res)
        data =    {
        
        "name":"FAC/2023/"+name+"T",

        "state":"draft",
        "move_type":"out_invoice",
        "journal_id":1,
        "user_id":[2,"Mitchell Admin"],
        "date":"2023-09-08",
        "currency_id":129,
        "partner_id":[41,"aziz jlassi"],
        "commercial_partner_id": [41,"aziz jlassi"],}
        facture = models.execute_kw(db, uid, password,'account.move', 'create',[data])
        print('FACTURE: ',facture)
        for item in res['line_ids']:
            invoice_line_ids = models.execute_kw(db, uid, password, 'account.move', 'write',[[facture], {'invoice_line_ids': [(0, '_', {"product_id": item, "quantity": 2,'price_unit':10})]}],{})
            print(invoice_line_ids)
        return Response(facture)



@api_view(['GET','POST'])
def facture(request ,id=None):
    """
    GET : pour rechercher une facture selon l'id
    POST : pour confirmer une facture ! (brouillon -> comptabilisé )
    """
    if request.method == 'GET'  and id !=None:
        res = models.execute_kw(db,uid,password,'account.move','search_read',[[['id','=',id]]])
        return Response(res)
    elif request.method == 'POST':
        res = models.execute_kw(db,uid,password,'account.move','write',[[id],{'state':'posted'}])
        return Response(res)




@api_view(['GET'])
def purchase_order(request):
    if request.method =='GET':
        res = models.execute_kw(db,uid,password,'purchase.order','search_read',[[]])
        return Response(res)
        
@api_view(['POST'])
def products_qty_available(request):
    if request.method == 'POST':
        print('Selecting all the products ...')

        products = models.execute_kw(db,uid,password,'product.template','search_read',[[]])

        print('{} products found !'.format(len(products)))

        for product in products:
            print('id : ',product['id'],' : ',product['name'])
            last_quantity = product['qty_available']
            print('Quantity avant le changement :',product['qty_available'])

            models.execute_kw(db,uid,password,'product.template','write',[[product['id']],{"qty_available" : 200.0}])
            print('Quantity après le changement :',product['qty_available'],'\n')

            if  product['qty_available'] == last_quantity:
                print('Aucun changement est effectué ! \n')
            else:
                print('changement est effectué ! \n')

    return Response('Done')
