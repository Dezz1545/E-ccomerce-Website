"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .import views

urlpatterns = [
    path("",views.index,name="index.html"),
    path("blog.html/",views.blog,name="blog.html"),
    path("check-out.html/",views.checkout,name="check-out.html"),
    path("contact/",views.contact,name="contact.html"),
    path("faq.html/",views.faq,name="faq.html"),
    path("login.html/",views.logIn,name="login.html"),
    path("register.html/",views.register,name="register.html"),
    path("logOut.html/",views.register,name="logOut.html"),
    path("main.html/",views.main,name="main.html"),
    path("product.html/",views.product,name="product.html"),
    path("shop.html/",views.shop,name="shop.html"),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('create_comment/<int:id>/', views.create_comment, name='create_comment'),
    path("shopping-cart.html/",views.shoppingcart,name="shopping-cart.html"),
]