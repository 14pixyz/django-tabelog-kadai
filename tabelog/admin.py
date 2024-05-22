from django.contrib import admin
from .models import CustomUser, Category, Store

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Store)