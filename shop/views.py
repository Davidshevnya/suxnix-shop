from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator

from .latest_products import LatestProducts
from .models import Good, Category


class GoodListView(ListView):
    model = Good
    template_name = "shop/product_list.html"
    context_object_name = "goods"
    paginate_by = 6

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        queryset = Good.objects.filter(available=True)

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)

        return queryset
    

    def get_context_data(self, **kwargs) -> dict[str, any]:
        category_slug = self.kwargs.get('category_slug')
        goods = self.object_list
        paginator = Paginator(goods, self.paginate_by)
        
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=category_slug) if category_slug else None
        context['categories'] = Category.objects.all()
        context['latest_products'] = LatestProducts(self.request).get()
        context['page_obj'] = paginator.get_page(self.request.GET.get("page"))
        
        return context
    
    



class GoodDetailView(DetailView):

    model = Good
    template_name = 'shop/product_detail.html'
    context_object_name = 'good'
    
                  
    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Good, id=self.kwargs.get('pk'), slug=slug, available=True)

                                
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_products = LatestProducts(self.request)
        latest_products.add(self.object)  
        context['latest_products'] = latest_products  
        return context
