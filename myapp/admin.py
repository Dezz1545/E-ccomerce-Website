from django.contrib import admin
from .models import Statut
from .models import Brand
from .models import Color
from .models import Tag
from .models import Categorie
from .models import Product
from .models import Post
from .models import Comment

from .models import Cart
from .models import CartItem
from .models import Contact





# Register your models here.
admin.site.register(Statut)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Tag)
admin.site.register(Categorie)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Contact)
admin.site.register(Post)
admin.site.register(Comment)




