from django.contrib import admin
from .models import Category , Product , Variation

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name' , 'gender' , 'slug']
    prepopulated_fields = {'slug' : ('name' , )} # slug field will be prepopulated on populating name

admin.site.register(Category , CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name' , 'category' , 'price' , 'stock' , 'availible' , 'created' , 'updated']
    list_editable = ['price' , 'stock' , 'availible'] # can be edited
    prepopulated_fields = {'slug' : ('name' , )}
    list_per_page = 20

admin.site.register(Product , ProductAdmin)

class VariationAdmin(admin.ModelAdmin):
    list_display = ['title' , 'product' , 'stock' , 'active']
    list_editable = ['stock' , 'active']


admin.site.register(Variation , VariationAdmin)
