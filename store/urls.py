from django.urls import path
from store.views import (
    calculate_shipping_fees, category_view, checkout_success, choose_relay, create_checkout_session, index, products, product_detail, recherche_produit, add_to_cart, 
    cart, stripe_webhook, update_cart, update_quantities, delete_order, ProductsBySizeView, ProductUnder100View, ProductsBetween100And200View, 
    ProductsAbove200View, Products50PercentOffView
)

urlpatterns = [
    path('products/size/<str:size>/', ProductsBySizeView.as_view(), name='products-by-size'),
    path('products/under-100/', ProductUnder100View.as_view(), name='products-under-100'),
    path('products/100-200/', ProductsBetween100And200View.as_view(), name='products-between-100-and-200'),
    path('products/above-200/', ProductsAbove200View.as_view(), name='products-above-200'),
    path('products/50-percent-off/', Products50PercentOffView.as_view(), name='products-50-percent-off'),
    path("products/", products, name="products"),
    path("product/<str:slug>/", product_detail, name="product"),
    path('categorie/<slug:parent_slug>/<slug:category_slug>/', category_view, name='subcategory'),
    path('categorie/<slug:category_slug>/', category_view, name='category'),
    
    path('stripe-webhook/', stripe_webhook, name="stripe-webhook"),
    path('cart/create-checkout-session', create_checkout_session, name='create-checkout-session'),
    path("cart/success", checkout_success, name="checkout_success"),
    
    path('choose-relay', choose_relay, name="choose-relay"),
    path("product/<str:slug>/add-to-cart", add_to_cart, name="add-to-cart"),
    path("cart/update-quantities", update_quantities, name="update-quantities"),
    path('cart/update-cart/', update_cart, name='update_cart'),
    path('cart/calculate-shipping-fees', calculate_shipping_fees, name='calculate-shipping-fees'),
    path("cart/<str:name>", delete_order, name="delete_order"),
    path("recherche/", recherche_produit, name="recherche_produit"),
    path("cart/", cart, name="cart"),
]
