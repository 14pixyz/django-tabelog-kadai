from django.contrib import admin
from .models import CustomUser, Category, Store, Review, Reservation, Favarit
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


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'star' , 'is_publish')


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'store' , 'date', 'time')

class FavaritAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'store' , 'create_datetime')


admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Favarit, FavaritAdmin)