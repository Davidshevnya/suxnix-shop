from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse


from .cart import Cart
from shop.models import Good
# Create your views here.

class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'total_price': cart.get_total_price(),
                'len': len(cart)
            })

        return render(request, "cart/cart_detail.html", {
            "cart": list(cart),
            "total_price": cart.get_total_price(),
            "cart_len": len(cart),
            "current_url": request.path
        })

class CartAddView(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        update_quantity = request.POST.get('update_quantity')

        cart = Cart(request)
        product = get_object_or_404(Good, id=int(product_id))

        if update_quantity:
            cart.add(product, quantity, update_quantity)
        else:
            cart.add(product, quantity)

        for item in list(cart):
            if item['product']['id'] == int(product_id):
                product = item

        return JsonResponse({
            'success': True,
            'product': product,
            'total_price': cart.get_total_price()
        })
    
        

class CartRemoveView(View):
    def post(self, request):
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Good, id=int(product_id))
       
        
        cart.remove(product)
        
        return JsonResponse({'success': True})

