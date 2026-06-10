from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tag)
admin.site.register(UserProfile)
admin.site.register(Collection)
admin.site.register(CollectionItem)