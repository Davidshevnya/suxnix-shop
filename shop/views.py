from django.shortcuts import render, get_object_or_404
from .models import Good, Category
# Create your views here.

def good_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    goods = Good.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        goods = goods.filter(category=category)
    return render(request,
                  "shop/product_list.html",
                  context={"category": category,
                           "categories": categories,
                           "goods": goods})
    
def good_detail(request, pk, slug):
    good = get_object_or_404(Good,
                                id=pk,
                                slug=slug,
                                available=True)
    return render(request,
                  'shop/product_detail.html',
                  {'good': good})
