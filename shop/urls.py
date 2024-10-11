from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.GoodListView.as_view(), name="good_list"),
    path("<slug:category_slug>", views.GoodListView.as_view(), name="good_list_by_category"),
    path("good/<int:pk>/<slug:slug>", views.GoodDetailView.as_view(), name="good_detail")
    
] 

