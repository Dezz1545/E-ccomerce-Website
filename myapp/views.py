from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from . token import generateToken
from django.http import JsonResponse


from django.core.mail import send_mail, EmailMessage
from myproject import settings
from django.shortcuts import render,redirect,get_object_or_404

#Les different Models
from .models import Statut
from .models import Brand
from .models import Color
from .models import Tag
from .models import Product
from .models import Cart
from .models import CartItem
from .models import Categorie
from .models import Post
from .forms import Contactform 
#Fin des models

from django.urls import reverse
from . import views
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout

#Serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import myproject
from .serializers import myprojectSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


#fin Serializers







# Create your views here.

class myprojectListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        todos = myproject.objects.filter(user = request.user.id)
        serializer = myprojectSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = myprojectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def blog(request):
    posts = Post.objects.all()
    categories = Categorie.objects.all()
    datas = {'categories': categories, 'posts': posts}

    return render(request,"blog.html",datas)   

def checkout(request):
    datas = {}

    return render(request,"check-out.html",datas)
   

def contact(request):
    form = Contactform()
    return render(request, 'contact.html', {'form': form})   

def faq(request):
    datas = {}

    return render(request,"faq.html",datas)
    

def index(request):
    # Récupérer tous les produits de la catégorie "Women"
    women_products = Product.objects.filter(categorie__name='Women')

    # Récupérer tous les produits de la catégorie "Men"
    men_products = Product.objects.filter(categorie__name='Men')

    tags = Tag.objects.all()

    datas = {
        'women_products': women_products,
        'men_products': men_products,
        'tags': tags,
    }

    return render(request, 'index.html', datas)

#formulaire d'inscription 
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà attribué à un compte.")
            return redirect('register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà attribué à un compte.")
            return redirect('register.html') 

        if not username.isalnum():
            messages.error(request, "Votre nom d'utilisateur doit contenir uniquement des caractères alphanumériques.")
            return redirect('register.html')  

        if len(password) < 8:
            messages.error(request, "Le mot de passe doit contenir au moins 8 caractères.")
            return redirect('register.html')

        if password != password2:
            messages.error(request, "Les deux mots de passe ne sont pas identiques.")
            return redirect('register.html')           

        mon_utilisateur = User.objects.create_user(username, email, password)
        messages.success(request, "Votre compte a été créé avec succès. Vous pouvez maintenant vous connecter.")
        return redirect('login.html')

    return render(request, "register.html")   

def logIn(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue {username}, vous êtes maintenant connecté.")
            return redirect('index.html')
        else:
            messages.error(request, 'Mauvaise authentification. Veuillez vérifier vos informations.')
            return redirect('login.html')

    return render(request, "login.html")      


#formulaire de déconnexion
def logOut(request):
    datas = {}
    products = Product.objects.all()
    logout(request)
    messages.success(request, 'Vous avez été déconnecter avec succès')

    return render(request,"index.html", {'products': products})


    

def main(request):
    datas = {}

    return render(request,"main.html",datas)

def blog_details(request, pk):
    post = Post.objects.get(id=pk)
    categories = Categorie.objects.all()
    datas = {'categories': categories, 'post': post}

    return render(request, "blog-details.html", datas)


def add_to_cart(request, product_id):
   cart, created = Cart.objects.get_or_create(user=request.user)
   product = get_object_or_404(Product, id=product_id)
   cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
   cart_item.quantity += 1
   cart_item.save()
   return redirect(request,'cart_detail.html')

def cart_detail(request):
   cart = Cart.objects.get(user=request.user)
   items = cart.cartitem_set.all()
   return render(request, 'cart/detail.html', {'items': items})

def product(request, pk):
    statuts = Statut.objects.all()
    brands = Brand.objects.all()
    colors = Color.objects.all()
    tags = Tag.objects.all()
    # Utilisez filter() pour filtrer les objets par leur ID
    products = Product.objects.filter(id=pk)
    categories = Categorie.objects.all()
    carts = Cart.objects.all()
    cartItems = CartItem.objects.all()
    datas = {
        'products': products, 
        'categories': categories, 
        'statuts': statuts, 
        'brands': brands, 
        'colors': colors, 
        'tags': tags, 
        'carts': carts,
        'cartItems': cartItems 
    }
    return render(request, "product.html", datas)


def shop(request):
    # Récupérer toutes les données nécessaires pour la page shop
    statuts = Statut.objects.all()
    brands = Brand.objects.all()
    colors = Color.objects.all()
    tags = Tag.objects.all()
    categories = Categorie.objects.all()

    # Filtres sélectionnés par l'utilisateur (initialisé à None)
    selected_color = request.GET.get('color')
    selected_tag = request.GET.get('tag')
    selected_categorie = request.GET.get('categorie')  # Correction du nom de la variable
    selected_brand = request.GET.get('brand')

    # Filtrage des produits en fonction des filtres sélectionnés
    products = Product.objects.all().order_by('-date_add')  # Tri par date d'ajout décroissante

    if selected_color:
        products = products.filter(color__name=selected_color)
    if selected_tag:
        products = products.filter(tag__name=selected_tag)
    if selected_categorie:
        # Assurez-vous que le champ pour la catégorie est correctement référencé dans votre modèle Product
        products = products.filter(categorie__name=selected_categorie)  # Correction du champ de filtre
    if selected_brand:
        products = products.filter(brand__name=selected_brand)

    # Pagination
    paginator = Paginator(products, 9)  # 9 produits par page
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # Si la page n'est pas un entier, afficher la première page
        products = paginator.page(1)
    except EmptyPage:
        # Si la page est en dehors de la plage de pagination, afficher la dernière page
        products = paginator.page(paginator.num_pages)

    # Récupérer les paniers et articles de panier
    carts = Cart.objects.all()
    cartItems = CartItem.objects.all()

    # Données à passer au template
    datas = {
        'products': products,
        'categories': categories,
        'statuts': statuts,
        'brands': brands,
        'colors': colors,
        'tags': tags,
        'carts': carts,
        'cartItems': cartItems,
        'selected_color': selected_color,
        'selected_tag': selected_tag,
        'selected_categorie': selected_categorie,
        'selected_brand': selected_brand,
    }

    return render(request, 'shop.html', datas)





def shoppingcart(request):
    datas = {}

    return render(request,"shopping-cart.html",datas)        



def activate(request, uid64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid64))    
        user =User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generateToken.check_token(user, token):
       user.is_active = True
       user.save()
       messages.success(request, "Votre compte a été activé félicitation connectez vous maintenant")
       return redirect('login.html')
    else:
        messages.error(request, "activation echoué !!")  
        return redirect('index.html') 

