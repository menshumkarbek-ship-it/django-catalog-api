from django.contrib import admin
from .models import Category, Product, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name", "slug"]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "created_at"]
    list_filter = ["category", "created_at"]
    search_fields = ["name", "description"]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["product", "author", "rating", "created_at"]
    list_filter = ["rating", "created_at"]
    search_fields = ["text", "author__username", "product__name"]
