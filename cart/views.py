from django.shortcuts import render, get_object_or_404
from .cart import Cart
from shop.models import Good
from django.http import JsonResponse
# Create your views here.

def cart_detail(request):
    cart = Cart(request)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'total_price': cart.get_total_price(),
                             'len': len(cart)})
    return render(request, "cart/cart_detail.html", {"cart": list(cart), "total_price": cart.get_total_price(),
                                                     "cart_len": len(cart), "current_url": request.path})

def cart_add(request):
    if request.method == 'POST':
        print(request.POST)
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        update_quantity = None
        if request.POST.get('update_quantity'):
            update_quantity = request.POST.get("update_quantity")

        cart = Cart(request)
        product = get_object_or_404(Good, id=int(product_id))
        if update_quantity:
            cart.add(product, quantity, update_quantity)
        else:
            cart.add(product, quantity)
        for i in list(cart):
            if i['product']['id'] == int(product_id):
                product = i


        return JsonResponse({'success': True,
                             'product': product,
                             'total_price': cart.get_total_price()})


def cart_remove(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = Cart(request)
        product = get_object_or_404(Good, id=int(product_id))
        cart.remove(product)
        return JsonResponse({'success': True})

