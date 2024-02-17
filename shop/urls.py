from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.good_list, name="good_list"),
    path("<slug:category_slug>", views.good_list, name="good_list_by_category"),
    path("good/<int:pk>/<slug:slug>", views.good_detail, name="good_detail")
    
] 

