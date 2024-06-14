from django.contrib import admin
from store.models import Coupons, Product, Categorie, Taille, ProductTaille, CartItem, Cart
from django.db.models import Sum  

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug', 'price', 'get_stock', 'long_description',
        'short_description', 'thumbnails1', 'thumbnails2',
        'thumbnails3', 'thumbnails4', 'promo', 'percent_promo',
        'product_stripe_id', 'updated_at'
    )

    def get_stock(self, obj):
        return ProductTaille.objects.filter(product=obj).aggregate(total_stock=Sum('stock'))['total_stock']
    get_stock.short_description = 'Stock'

@admin.register(Taille)
class TailleAdmin(admin.ModelAdmin): 
    list_display = ('taille',)

@admin.register(ProductTaille)
class ProductTailleAdmin(admin.ModelAdmin):  
    list_display = ('product', 'taille', 'stock')  

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):  
    list_display = ('user', 'product', 'quantity', 'ordered', 'ordered_date', 'subtotal')

@admin.register(Coupons)
class CouponsAdmin(admin.ModelAdmin): 
    list_display = ('code', 'discount', 'is_active', 'created_at', 'expires_at')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):  
    list_display = ('ordered', 'ordered_date', 'totaux', 'all_quantity', 'get_coupons')

    def get_coupons(self, obj):
        return ", ".join([coupon.code for coupon in obj.coupons.all()])
    get_coupons.short_description = 'Coupons'
