from django.shortcuts import render, get_object_or_404
from .models import Good, Category
from django.core.paginator import Paginator
from .latest_products import LatestProducts
from cart.cart import Cart
# Create your views here.

def good_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    goods = Good.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        goods = goods.filter(category=category)
    paginator = Paginator(goods, 6)
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    latest_products = LatestProducts(request).get()

    cart = Cart(request)

    

    return render(request,
                  "shop/product_list.html",
                  context={"category": category,
                           "categories": categories,
                           "goods": goods,
                           "page_obj": page_obj,
                           "latest_products": latest_products,
                           "cart": list(cart),
                           'cart_total_price': cart.get_total_price(),
                           "cart_len": len(cart)})
    
def good_detail(request, pk, slug):
                  
    good = get_object_or_404(Good,
                                id=pk,
                                slug=slug,
                                available=True)
    latest_products = LatestProducts(request)
    latest_products.add(good)

    cart = Cart(request)
    
    return render(request,
                  'shop/product_detail.html',
                  {'good': good,
                   'cart': list(cart),
                   'cart_total_price': cart.get_total_price(),
                   "cart_len": len(cart)})
