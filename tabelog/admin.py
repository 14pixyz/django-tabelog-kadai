from django.contrib import admin
from .models import CustomUser, Category, Store
from django.utils.safestring import mark_safe

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    search_fields = ('email',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')
    search_fields = ('name',)

    def image(self, obj):
        return mark_safe('<img src="{}" style="width:100px height:auto;">'.format(obj.img.url))

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Store, StoreAdmin)