from django.urls import URLPattern, path

from . import views

app_name = 'cart'


urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart_detail'),
    path('add/', views.CartAddView.as_view(), name="cart_add"),
    path('remove/', views.CartRemoveView.as_view(), name='cart_remove')
]
