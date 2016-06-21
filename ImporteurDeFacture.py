
import xmlrpc.client
import configureEnvironnement
import django
django.setup()


from easyPoS.models import Facture,LigneFacture,Client


class Connection:
    def __init__(self,url,db,username,password):
        self.url=url
        self.db=db
        self.username=username
        self.password=password
        self.uid=None
        self.models=None
        self.hasModel=False

    def getUid(self):
        if not self.uid:
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
            self.uid = common.authenticate(self.db, self.username, self.password, {})
        return self.uid

    def getModels(self):
        if not self.hasModel:
            self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            self.hasModel=True
        return self.models




c=Connection('http://localhost:8069','w',"w","w")
#print(c.getUid())
#print(c.getModels())
#models=c.getModels()

class ProductTemplate:
    nom="product.template"
    requiredFields=['uom_id', 'name', 'categ_id', 'type', 'product_variant_ids', 'product_tmpl_id', 'uom_po_id']
    def __init__(self):
        self.uom_po_id = 5
        self.name = "product"
        self.product_variant_ids = []
        self.categ_id = 4
        self.name_template = "product"
        self.uom_id = 5
        self.type = "service"
        self.display_name = "product"


class Product:
    nom="product.product"
    requiredFields=['uom_id', 'name', 'categ_id', 'type', 'product_variant_ids', 'product_tmpl_id', 'uom_po_id']
    def __init__(self):
        self.uom_po_id = 5
        self.name = "product"
        self.product_tmpl_id = 1
        self.product_variant_ids = []
        self.categ_id = 4
        self.name_template = "product"
        self.uom_id = 5
        self.type = "service"
        self.display_name = "product"


class Client2:
    nom="res.partner"
    requiredFields=["notify_email","property_account_payable_id","property_account_receivable_id","name","display_name"]
    def __init__(self):
        self.display_name = "anonyme"
        self.name = "anonyme"
        self.property_account_receivable_id = 277
        self.notify_email = "always"
        self.parent_name = False
        self.property_account_payable_id = 263



class Facture2:
    nom="account.invoice"
    requiredFields = ["reference_type", 'partner_id', "reference_type", "account_id", "currency_id", "journal_id",
                      "company_id"]
    def __init__(self):
        self.company_id=1
        self.currency_id=1
        self.partner_id=44
        self.reference_type= "none"
        self.journal_id=1
        self.account_id=277
    #    self.lignes=[]
     #   self.clients=[]

class LigneFacture2:
    nom="account.invoice.line"
    requiredFields=["account_id","price_unit","quantity","name","invoice_line_tax_ids"]

    def __init__(self):
        self.display_name = "fromage"
        self.invoice_line_tax_ids = [3]
        self.price_unit = 4.0
        self.account_id = 624
        self.quantity = 1.0
        self.name = "fromage"
        pass

def convertisseur_d_instance_en_dico(instance):
 #   print("HOHO",instance.__dict__.keys())
    dico={}
    for k in instance.__dict__.keys():
        dico[k]=getattr(instance,k)
    return (dico)


#res=models.execute_kw(db, uid, password,     'account.invoice', 'check_access_rights',    ['write'], {'raise_exception': False})

#res=c.getModels().execute_kw(c.db, c.getUid(), c.password,    'account.invoice', 'search',    [ [] ] )
#print(res)


def trouveRequiredFields(c,classe):
    r = c.getModels().execute_kw(c.db, c.getUid(), c.password, classe.nom, 'fields_get', [], {})
    liste=[]
    for rr, vv in r.items():
  #      print(rr,vv)
        if vv["required"]:
            liste.append(rr)
            print(rr)
    return liste

#
#print("ZOZO")
#print(trouveRequiredFields(c,Product))

def lisLaDonnee(c,classe,id):
    print(classe.nom)
    record=c.getModels().execute_kw(c.db,c.getUid(),c.password,classe.nom,"read",[id])
    print("hi on a lu",classe.nom,record)
    toCreate = {}
    for k, v in record.items():
        if "name" in k:

            print ("self."+str(k),"=", v)

        if k in classe.requiredFields:
   #         print(k,v)
            v1=v
            if type(v) is list and len(v) == 2:
                v1 = v[0]
   #         print ("self."+str(k),"=", v)
            toCreate[k] = v1
            print(k,"=",v,"00000000000000000000")
        else:
            print(k,"=",v)
    return toCreate

def ecrisLaDonnee(db,uid,password,models,classe):
    pass
if False:
    toCreate=lisLaDonnee(c,Facture2,1602)
    print()
    toCreate=lisLaDonnee(c,LigneFacture2,1279)
    print()
    print()
    toCreate=lisLaDonnee(c,Product,835)


#print(toCreate)


#def creerObjet()

def creerClient(c,nom):
    f=Client2()
    d=convertisseur_d_instance_en_dico(f)
    d['name']=nom
    d['display_name'] = nom
    id=c.getModels().execute_kw(c.db,c.getUid(),c.password,"res.partner","create",[d])
    print(id,"client a ete cree")
    return id

def creerFacture(c,facture):
    f=Facture2()
    l=LigneFacture2()


    idLignes = []
    dicoLigne = convertisseur_d_instance_en_dico(l)
    for ligne in facture.lignefacture_set.all():
        if ligne.libelle or not ligne.produit:
            continue;
        dicoLigne["name"]=ligne.produit.nom
        dicoLigne["display_name"] = ligne.produit.nom


        dicoLigne["quantity"]=ligne.quantite
        dicoLigne["price_unit"] = float(ligne.prixUnitaireFinal)
        pp=Product()
        dicoProd=convertisseur_d_instance_en_dico(pp)
        dicoProd["name"]=ligne.produit.nom
        dicoProd["name_template"] = ligne.produit.nom
        dicoProd["display_name"] = ligne.produit.nom

        temp = c.getModels().execute_kw(c.db, c.getUid(), c.password, "product.template", "create", [dicoProd])
        dicoProd["product_tmpl_id"]=temp
        print(dicoProd)
        prod = c.getModels().execute_kw(c.db, c.getUid(), c.password, "product.product", "create", [dicoProd])

        dicoLigne["product_id"] = prod


        print(ligne)
        print("le dico:",dicoLigne)


        nid = c.getModels().execute_kw(c.db, c.getUid(), c.password, "account.invoice.line", "create", [dicoLigne])
        print(nid,"a été creeEEEEE")
        idLignes.append(nid)

    d=convertisseur_d_instance_en_dico(f)
    cli=creerClient(c,facture.clientNomFinal)

    d["partner_id"]=cli
    d["invoice_line_ids"]=[idLignes]

    print("before",d)
    id=c.getModels().execute_kw(c.db,c.getUid(),c.password,"account.invoice","create",[d])
    print("after")

    print(id," a ete cree")

#pp=Product()
#dicoProd = convertisseur_d_instance_en_dico(pp)
#print("PPPPPPPPPPP",dicoProd)
#prod = c.getModels().execute_kw(c.db, c.getUid(), c.password, "product.product", "create", [dicoProd])

fs=Facture.objects.all()
#creerFacture(c,fs[1])
for f in fs:
    if f.client and f.client.nom:
        creerFacture(c,f)
#for i in range(10):
 #   id = c.getModels().execute_kw(c.db, c.getUid(), c.password, 'account.invoice', 'create', [toCreate])