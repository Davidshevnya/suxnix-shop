
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("contacts/", views.contacts, name="contacts")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
