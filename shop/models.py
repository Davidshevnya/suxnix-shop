from django.db import models
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ("name", )
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("shop:good_list_by_category", args=[self.slug])
    


class Good(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="goods")
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='goods/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=64)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        
    def get_absolute_url(self):
        return reverse("shop:good_detail", args=[self.id, self.slug])
    

    def __str__(self):
        return self.name



    