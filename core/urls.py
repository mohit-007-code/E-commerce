from django.urls import path
from .views import (
    HomeView, ProductListView, ProductDetailView, AddProductView, BuyNowProductView,
    CheckoutCompleteView, DeleteProductView, CartPageView, AddToCartView, RemoveFromCartView
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name='home-page'),
    path('product-list/', ProductListView.as_view(), name='product-list-page'),
    path('product-detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail-page'),
    path('add/', AddProductView.as_view(), name='add-product'),
    path('buy-now/<int:pk>/', BuyNowProductView.as_view(), name='buy-now-product'),
    path('checkout-complete/', CheckoutCompleteView.as_view(), name='checkout-complete'),
    path('delete-product/<int:pk>/', DeleteProductView.as_view(), name='delete-product'),
    path('cart/', CartPageView.as_view(), name='cart_page'),
    path('add-to-cart/<int:pk>/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove-from-cart/<int:pk>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)