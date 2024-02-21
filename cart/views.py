from django.shortcuts import render, get_object_or_404
from .cart import Cart
from shop.models import Good
from django.http import JsonResponse
# Create your views here.

def cart_detail(request):
    cart = Cart(request)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'total_price': cart.get_total_price()})
    return render(request, "cart/cart_detail.html", {"cart": list(cart), "total_price": cart.get_total_price()})

def cart_add(request):
    if request.method == 'POST':

        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')

        cart = Cart(request)
        product = get_object_or_404(Good, id=int(product_id))
        cart.add(product, quantity)

        return JsonResponse({'success': True})


def cart_remove(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = Cart(request)
        product = get_object_or_404(Good, id=int(product_id))
        cart.remove(product)
        return JsonResponse({'success': True})

