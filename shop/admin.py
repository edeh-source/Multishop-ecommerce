from django.contrib import admin
from .models import Category, ProductImage, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_filter = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10
    
    
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    list_per_page = 10
    
    
@admin.register(Product)    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'quantity', 'active', 'created', 'special', 'updated']
    list_filter = ['category','active', 'price', 'quantity']    
    prepopulated_fields = {'slug':('name',)}
    list_per_page = 10
    
    
@admin.register(Review)  
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'polartity']
    list_filter = ['rating', 'polartity', 'user']  
    
    
    
    
