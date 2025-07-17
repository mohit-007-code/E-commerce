from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, TemplateView
from .models import Product, Cart, CartItem
from .forms import ProductForm

class HomeView(TemplateView):
    template_name = 'home.html'

class BuyNowProductView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, 'buy_now_product.html', {'product': product})
    
    def post(self, request, pk):
        return redirect('checkout-complete')

class CheckoutCompleteView(View):
    def get(self, request):
        return render(request, 'buy_now_product.html')
    
    def post(self, request):
        context = {
            'address': request.POST.get('address'),
            'phone': request.POST.get('phone'),
            'email': request.POST.get('email'),
            'payment_method': request.POST.get('payment_method'),
        }
        return render(request, 'endpoint.html', context)

class AddProductView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'add_product.html'
    success_url = reverse_lazy('product-list-page')

class ProductListView(ListView):
    model = Product
    template_name = 'list.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return Product.objects.filter(name__icontains=query) if query else Product.objects.all()

class ProductDetailView(DetailView):
    model = Product
    template_name = 'detail.html'
    context_object_name = 'product'

class CartPageView(View):
    def get(self, request):
        cart_id = request.session.get('cart_id')
        cart_items = []
        total_price = 0
        
        if cart_id:
            cart = get_object_or_404(Cart, id=cart_id)
            cart_items = CartItem.objects.filter(cart=cart)
            total_price = sum(item.total_price() for item in cart_items)
        
        return render(request, 'cart_page.html', {'cart_items': cart_items, 'total_price': total_price})

class AddToCartView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        cart_id = request.session.get('cart_id')
        
        if not cart_id:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
        else:
            cart = get_object_or_404(Cart, id=cart_id)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        return redirect('cart_page')

class RemoveFromCartView(View):
    def get(self, request, pk):
        cart_id = request.session.get('cart_id')
        
        if not cart_id:
            messages.error(request, 'No cart found.')
            return redirect('cart_page')
        
        cart = get_object_or_404(Cart, id=cart_id)
        
        try:
            cart_item = CartItem.objects.get(pk=pk, cart=cart)
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
        except CartItem.DoesNotExist:
            messages.error(request, 'Item not found in your cart.')
        
        return redirect('cart_page')

class DeleteProductView(DeleteView):
    model = Product
    success_url = reverse_lazy('product-list-page')
    template_name = 'confirm_delete.html'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Product deleted successfully.')
        return super().delete(request, *args, **kwargs)
