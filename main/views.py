from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "main/index.html")

def contacts(request):
    return render(request, "main/contacts.html")