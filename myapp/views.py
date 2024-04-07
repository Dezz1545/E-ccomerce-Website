from django.core.mail import send_mail
from myproject import settings
from django.shortcuts import render,redirect,get_object_or_404
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
from django.urls import reverse
from . import views
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login





# Create your views here.


def blog(request):
    posts = Post.objects.all()
    categories = Categorie.objects.all()
    datas = {'categories': categories, 'posts': posts}

    return render(request,"blog.html",datas)   

def checkout(request):
    datas = {}

    return render(request,"check-out.html",datas)
   

def contact(request):    
    datas = {}

    return render(request,"contact.html",datas)   

def faq(request):
    datas = {}

    return render(request,"faq.html",datas)
    

def index(request):
    products = Product.objects.all()
    datas = {}

    return render(request, 'index.html', {'products': products})

def register(request):
    if request.method == "POST":
        #Traiter le formulaire
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if User.objects.filter(username=username):
            messages.error(request, "Ce nom d'utilisateur est déja attribuer a un compte.")
            return redirect('register.html')

        if User.objects.filter(email=email):
            messages.error(request, "Cet Email est déja attribuer a un compte.")
            return redirect('register.html') 

        if not username.isalnum():
            messages.error(request, "Votre nom doit contenir que des caractère alphanumeric.")
            return redirect('register.html')  

        if len(password) < 8:
            messages.error(request, "Le mot de passe doit contenir au moins 8 caractères.")
            return redirect('register.html')

        if password != password2:
            messages.error(request, "les deux mot de passe ne sont pas identique.")
            return redirect('register.html')           

        mon_utilisateur = User.objects.create_user(username, email, password)
        mon_utilisateur.save()
        messages.success(request, "Votre compte a été crée avec succès")
        #Envoie Email de bienvenue
        subject = "Bienvenue sur Fashi"
        message = "Bienvenu "+ mon_utilisateur.username + "\ Nous somme heureux de vous comptez parmis nos utilisateur"
        from_email =  settings.EMAIL_HOST_USER
        to_list = [mon_utilisateur.email]
        send_email(subject, message, from_email, to_list, fail_silently=False)
        return redirect('login.html')

    return render(request,"register.html")      

def logIn(request):
    datas = {}
    products = Product.objects.all()
    if request.method == "POST":
        #Traiter le formulaire
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate( username=username, password=password)
        if user is not None:
            login(request, user)
            username= user.username
            return render(request,"index.html" )
        else:
            messages.error(request, 'Mauvaise Authentification')
            return redirect('login.html')



    return render(request,"login.html", {'products': products})          

def logOut(request):
    datas = {}
    products = Product.objects.all()
    logout(request)
    messages.success(request, 'Vous avez été déconnecter avec succès')

    return render(request,"index.html", {'products': products})


    

def main(request):
    datas = {}

    return render(request,"main.html",datas)

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

def product(request):
    datas = {}

    return render(request,"product.html",datas)   


def shop(request):
    statuts = Statut.objects.all()
    brands = Brand.objects.all()
    colors = Color.objects.all()
    tags = Tag.objects.all()
    products = Product.objects.all()
    categories = Categorie.objects.all()
    carts =Cart.objects.all()
    cartItems =CartItem.objects.all()
    datas = {'products': products, 'categories': categories, 'statuts': statuts, 'brands': brands, 'colors': colors, 'tags': tags, 'carts': carts,'cartItems': cartItems }

    return render(request, 'shop.html',datas)

def shoppingcart(request):
    datas = {}

    return render(request,"shopping-cart.html",datas)        


def create_comment(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == 'POST':
        comment = Comment(article=article, author=request.user, content=request.POST['content'])
        comment.save()
        return redirect('shop_detail', id=id)
    return render(request, 'create_comment.html', {'article': article})


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    article = comment.article
    if request.user.is_authenticated and comment.author == request.user:
        comment.delete()
        return redirect('shop_detail', id=article.id)
    else:
        # Rediriger vers une page d'erreur ou u
        
        return redirect('shop_detail', id=article.id)