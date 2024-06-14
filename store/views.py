from typing import Any
from urllib import request
from django.db.models.query import QuerySet
from django.forms import modelformset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import requests
from accounts.models import ShippingAddress
from store.models import CartItem, Product, Categorie, ProductTaille, Cart, Coupons
from django.contrib import messages
from store.forms import RechercheProduitForm, CartItemForm
from django.views.generic.list import ListView
from django.utils.translation import gettext as _ 
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_POST
from django.utils import translation
from django.conf import settings
import json
import os
import stripe
stripe.api_key = settings.STRIPE_API_KEY
simtao_api_key = settings.SIMTAO_API_KEY

# Create your views here.

# HomePage
def index(request):
    categories = Categorie.objects.all()
    latest_products = Product.objects.all().order_by('-updated_at')[:6] 
    return render(request, 'store/index.html', context={"categories" : categories , 'latest_products': latest_products})

# # Filtre par categorie
# def products_by_category(request, category_slug):
#     category = get_object_or_404(Categorie, slug=category_slug)
#     products = Product.objects.filter(categorie=category)
#     categories = Categorie.objects.all()  
#     return render(request, 'store/products_by_category.html', context={"products": products, "category": category, "categories": categories})


def category_view(request, category_slug):
    # if category.parent == 'Homme' :
    # print(category_slug)
    products = Product.objects.filter(genre = category_slug)
    for product in products:
        print(product.name)
        
    # print('3ème print', products)
    # elif category.parent == 15 :
        # products_femme = Product.objects.filter(categorie=category)
   
       
    return render(request, 'store/category.html', {
        'products': products, 
        'category_slug': category_slug
        # 'products_femme': products_femme,
    })

    
# Page Shop : listing produits
def products(request):
    products = Product.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'store/products.html', context={"products" : products,
                                                           "categories" : categories 
                                                           })
# details produits
def product_detail(request, slug):
    product = get_object_or_404(Product, slug = slug)
    product_tailles = ProductTaille.objects.filter(product=product).order_by('taille__taille')
    return render(request, 'store/details.html', context={"product" : product,
                                                          "product_tailles": product_tailles})
# Filtre de recherche : -100€
class ProductUnder100View(ListView):
    model = Product 
    template_name = 'store/under_100.html'
    
    
    def get_queryset(self):
        return Product.objects.filter(price__lt=100)  

# Filtre de recherche : entre 100€ et 200€
class ProductsBetween100And200View(ListView):
    model = Product
    template_name = 'store/between_100_and_200.html'

    def get_queryset(self):
        return Product.objects.filter(price__gte=100, price__lte=200)
    
    

# Filtre de recherche : + de 200€
class ProductsAbove200View(ListView):
    model = Product
    template_name = 'store/above_200.html'

    def get_queryset(self):
        return Product.objects.filter(price__gt=200)

# Filtre de recherche : Produit en promotion -50%  
class Products50PercentOffView(ListView):
    model = Product
    template_name = 'store/50_percent_off.html'

    def get_queryset(self):
        return Product.objects.filter(promo=True, percent_promo=50)
    
# Filtre de recherche : Produit par taille
class ProductsBySizeView(ListView):
    model = Product
    template_name = 'store/templates/store/products_by_size.html'
    context_object_name = 'products'

    def get_queryset(self):
        size = self.kwargs.get('size')
        return Product.objects.filter(sizes__contains=size)
    
def add_to_cart(request, slug): 
    user = request.user

    # Vérifie l'authentification du user 
    if not user.is_authenticated:
        messages.add_message(request, messages.ERROR, "Veuillez vous connecter afin d'ajouter des produits au panier.")
        return redirect('login')

    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = CartItem.objects.get_or_create(
        user=user,
        ordered=False,
        product=product
    )
    
    if created:
        cart.orders.add(order)
        cart.all_quantity += 1
    else:
        order.quantity += 1
        cart.all_quantity += 1
        cart.save()
        order.save()
    
    return redirect(reverse("product", kwargs={'slug': slug}))

def recherche_produit(request):
    form = RechercheProduitForm()
    resultats = []
    if request.method == 'GET':
        form = RechercheProduitForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            resultats = Product.objects.filter(nom__icontains=query)
    return render(request, 'store/recherche.html', context={'form': form, 'resultats': resultats})

def cart(request):
    # commande de l'utilisateur en cours  = request.user
    orders = CartItem.objects.filter(user = request.user)
    # Si le panier et vide 
    # et que l'utilisateur cherche a aller sur panier redirect index
    if orders.count() == 0:
        return redirect('index') 
    
    # Création d'un OrderFormSet qui est unensemble de formulaire 
    # basé sur le model Order
    CartItemFormSet = modelformset_factory(CartItem, form=CartItemForm, extra=0)
    
    #  queryset -> les instances de commandes passée par le user
    formset = CartItemFormSet(queryset=orders )
    
    return render(request, 'store/cart.html', context={"forms" : formset, "orders" : orders})

def update_quantities(request):
     if request.method == 'POST':
    # commande de l'utilisateur en cours  = request.user
        orders = CartItem.objects.filter(user = request.user)
        
        # Création d'un CartItemFormSet qui est un ensemble de formulaire 
        # basé sur le model CartItem
        CartItemFormSet = modelformset_factory(CartItem, form=CartItemForm, extra = 0)
        
        #  queryset -> les instances de commandes passée par le user
        formset = CartItemFormSet(request.POST, queryset =orders)
        
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data.get('delete'):
                    form.instance.delete()
                else:
                    form.save()
            
        # recalcule du total panier
        if orders.count() != 0:
            request.user.cart.calc_totaux()
            print("Votre panier a été mis à jour.")
            # messages.success(request, 'Votre panier a été mis à jour.')
        else:
            print('Erreur lors de la mise à jour du panier.')
            # messages.error(request, 'Erreur lors de la mise à jour du panier.')
        return redirect('cart')
        
     return redirect('cart')

def delete_order(request, name):
    
    if cart := request.user.cart:
        cart.delete_order(name)
        cart.calc_totaux()
        
        # if cart.all_quantity == 0:
        #     print('test')
            
        if cart.orders.count() == 0:
            cart.delete()
        # return redirect('index')

    return redirect('cart')
    
@login_required
def update_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    orders = cart.orders.all()
    
    if request.method == "POST":
        code = request.POST.get('code')
        coupon = Coupons.objects.filter(code=code, is_active=True).first()
        
        if coupon:
            if coupon in cart.coupons.all():
                messages.warning(request, "Ce coupon a déjà été utilisé.")
            else:
                cart.coupons.add(coupon)
                cart.calc_totaux()
                cart.save()
                messages.success(request, "Coupon activé !")
        else:
            messages.warning(request, "Ce coupon n'est pas valide !")

        return redirect('cart')

    context = {
        "cart": cart,
    }
    return render(request, 'store/cart.html', context)

@login_required
def calculate_shipping_fees(request):
    print("TEST")
    # Récupérer l'adresse de livraison par défaut de l'utilisateur
    address = get_object_or_404(ShippingAddress, user=request.user)
    
    # Récupérer les informations des colis de la commande
    # Assurez-vous que l'utilisateur a une commande en cours, par exemple :
    order = request.user.cart.orders.all()  
    print(order)
    
    packages = []
    for order_item in order:
        package = {
            "weight": order_item.product.weight,  
            "dimensions": {
                "length": order_item.product.length,
                "width": order_item.product.width,
                "height": order_item.product.height,
            },
        }
        packages.append(package)
    print(packages)
    # Configurer les informations pour l'API SIMTao de La Poste
   
    
    data={
        "effectiveDate": "06/12/2023",
        "offerCode": "3125",
        "majorFunctionalVersion": 1,
        "contractNumber": "D-811755-1",
        "customerNumber": "295417",
        "customerMarketingTypeCode": "B2C",
        "customerEstablishZoneCode": "01",
        "criteria": {
            "DT_APPLI_TAR": "06/12/2023",
            "ZON_DPAR": "96",
            "ZON_DESTN": "96",
            "contract_requestedType": "APILSP005",
            "contract_complexTypeManagement": "1",
            "ZON_INFO": "titre:Détail de la prestation choisie@@texte:L'API d'affranchissement Courrier suivi permet aux clients d'affranchir leurs courriers depuis leur environnement de travail ; l'intégration de cette API nécessite la signature d'un contrat ; les consommations sont facturées en fin de mois au client signataire du contrat.@@space@@interlocuteur:ITL_OPE@@space@@adresse:ADR_FAC",
            "offerType": "AAC001",
            "offerSubType": "AAC001"
        },
        "cases": packages
    }

    headers = {
        "Accept": "application/json",
        "X-Okapi-Key": simtao_api_key,
    }
    api_url = "https://api.laposte.fr/sim-tao/v1/public/sto/api/v1/pricing/sto" 

    response = requests.post(api_url, json=data, headers=headers,)
    print(response)

    if response.status_code == 200:
        shipping_info = response.json()
        print(shipping_info)
        return render(request, 'store/shipping_info.html', context={ 'shipping_infos': shipping_info} )


    return redirect('cart')


@xframe_options_exempt           
def create_checkout_session(request):
    print("TEST")
    cart = request.user.cart

    line_items = []
    for order in cart.orders.all():
        price = order.product.price_promo if order.product.promo else order.product.price
        line_data = {
            'price_data': {
                'unit_amount': int(price*100),
                'currency': 'eur',
                'product_data': {
                    'name':order.product.name,
                    'description':order.product.short_description or "",

                },
            },
            'quantity': order.quantity
        }
          
        line_items.append(line_data)
    

    checkout_data = {
        "line_items":line_items,
        "mode":"payment",
        "shipping_address_collection": {"allowed_countries" :["FR", "US", "CA"]},
        "payment_intent_data" : {"metadata" : {"infos" : 'le client est dispo de 8h à 12h'}}, 
        "success_url":request.build_absolute_uri(reverse('index')),
        "cancel_url":request.build_absolute_uri(reverse('index')),
        "shipping_options": [{"shipping_rate" : 'shr_1PNxe205fBSSfTICnOhgg62e'}],
    }

    if request.user.stripe_id:
        checkout_data["customer"] = request.user.stripe_id
    else:
        checkout_data["customer_email"] = request.user.email
        # "always" : option de creation automatoique du compte stripe 
        checkout_data["customer_creation"] = "always"   
        # checkout_data["invoice_creation"] = {
        #     "enabled" : True,
        #     "invoice_data":{
        #         "description" : "test"
        #     }
        # }     
    try :
        checkout_session = stripe.checkout.Session.create(**checkout_data)
    # Gestion des erreurs
    except Exception as e:
        # erreur 500 : erreur coté serveur 
        return JsonResponse({'error' : str(e)}, status=500)    
        
    # Genere la page de redirection stripe
    return redirect(checkout_session.url, code= 303)

# Ecouteur d'evenements stripes
@csrf_exempt
def stripe_webhook(request):
    # contenu de requete
    payload = request.body
    # en-tete de la requete
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    endpoint_secret = env("ENDPOINT_SECRET")


    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # convertit l'erreur en str
        print('Error verifying webhook signature :{}'.format(str(e)) )
        # print('Error verifying webhook signature :{0} {1}'.format([str(e), sig_header]) )
        # Gère l'erreur et redirige vers l'erreur 400 
        return HttpResponse(status=400)
    # listes des type d'event sur la doc
    # checkout.session.completed : le paiment a étét effectuer 
    if event.type == 'checkout.session.completed':
        # Récupération de l'objet de data.event
        payment_intent = event.data.object
        try:
            # Récupération des infos du webhook et de la class Shopper ->>> voir terminal CLI
            # R2cupere le bon user
            user = get_object_or_404(stripe.Customer, email=payment_intent["customer_details"]["email"])
            
        except KeyError:
            return HttpResponse("invalid user", status=404)
        
       
        # supprime le panier après le paiment
        complete_order(data=payment_intent, user=user)
        save_shipping_address(data = payment_intent, user=user)

        # print(payment_intent)
        # pprint(payment_intent)
        return HttpResponse(status=200)
    elif event.type == "payment_intent.succeeded":
        payment_intent = event.data.object
        print(payment_intent)
    
    return HttpResponse(status=200)

def complete_order(data, user):
    # Déclarer dans tableau data['customer'] ou attribut une str vide et pas null 
    user.stripe_id = data['customer'] or ''
    user.cart.delete()
    user.save()
    return HttpResponse(status=200)

def save_shipping_address(data, user):
    try:
        address = data["shipping_details"]["address"]
        name = data["shipping_details"]["name"]
        city = address["city"]
        country = address["country"]
        line1 = address["line1"]
        line2 = address["line2"]
        postal_code = address["postal_code"]
    except KeyError:
        return HttpResponse(status=400)
    ShippingAddress.objects.get_or_create(user=user,
                                        name=name,
                                        city =city,
                                        country=country,
                                        address_1 = line1,
                                        address_2 = line2 or "",
                                        zip_code = postal_code)
    return HttpResponse(status=200)

def checkout_success(request):
 return render(request, 'store/success.html')


# Choix de langues
def change_language(request, lang_code):
    response = redirect('index')  
    print('La langue est :',lang_code)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response




def choose_relay(request):
    # commande de l'utilisateur en cours  = request.user
    orders = CartItem.objects.filter(user = request.user)
     # Création d'un OrderFormSet qui est unensemble de formulaire 
    # basé sur le model Order
    CartItemFormSet = modelformset_factory(CartItem, form=CartItemForm, extra=0)
    
    #  queryset -> les instances de commandes passée par le user
    formset = CartItemFormSet(queryset=orders )
    
    return render (request, 'store/choose_relay.html', context={"forms" : formset, "orders" : orders})