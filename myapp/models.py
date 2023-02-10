from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Statut(models.Model):
    name = models.CharField(max_length=100)
        #Standards
    status= models.BooleanField(default=True)
    date_add= models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)
        #Standards
    status= models.BooleanField(default=True)
    date_add= models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=100)
        #Standards
    status= models.BooleanField(default=True)
    date_add= models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
        #Standards
    status= models.BooleanField(default=True)
    date_add= models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.name                

class Categorie(models.Model):
    name = models.CharField(max_length=100)
   
    #Standards
    status= models.BooleanField(default=True)
    date_add= models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.name

class Post(models.Model):
    image = models.ImageField(upload_to="Post")
    categorie = models.ManyToManyField(Categorie, related_name="categorie1")
    description = models.TextField(blank=True)


    #Standards
    status= models.BooleanField(default=True)
    date_add= models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)



class Product(models.Model):
    statut = models.ManyToManyField(Statut, related_name="statut")
    categorie = models.ManyToManyField(Categorie, related_name="categorie")
    brand = models.ManyToManyField(Brand, related_name="brand")
    color = models.ManyToManyField(Color, related_name="color")
    tag = models.ManyToManyField(Tag, related_name="tag")
    nom = models.CharField(max_length=150)
    price = models.FloatField(default=0.00)
    stock =models.IntegerField(default=0)
    description = models.TextField(blank=True) # (blank=True) pour créer le produit sans forcément mettre une description
    image = models.ImageField(upload_to="products")
   
    #Standards
    status= models.BooleanField(default=True)
    date_add= models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.nom
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

        #Standards
    status= models.BooleanField(default=True)
    date_add= models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.nom

class Cart(models.Model):
    created = models.DateTimeField(auto_now_add=None)

    #Standards
    status= models.BooleanField(default=True)
    date_add= models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.created

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
        
    #Standards
    status= models.BooleanField(default=True)
    date_add= models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)
    
    def __str__(self) :
        return self.cart

class Contact(models.Model):
    nom = models.CharField(max_length=100)
    email =models.EmailField(max_length=100)
    objet =models.CharField(max_length=100)
    message =models.TextField()

    #Standards
    status= models.BooleanField(default=True)
    date_add= models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.nom


