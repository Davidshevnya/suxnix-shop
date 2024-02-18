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
    
class Tag(models.Model):
    name = models.CharField(max_length=200, db_index=True)

    class Meta:
        ordering = ("name", )
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        
    def __str__(self):
        return self.name

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

class Protein(models.Model):
    good = models.OneToOneField(Good, on_delete=models.CASCADE, related_name='protein_info')
    calories = models.DecimalField(max_digits=6, decimal_places=2)
    total_fat = models.CharField(max_length=20)
    saturated_fat = models.CharField(max_length=20)
    cholesterol = models.CharField(max_length=20)
    total_carbohydrate = models.CharField(max_length=20)
    protein = models.CharField(max_length=20)
    total_sugars = models.CharField(max_length=20)
    sodium = models.CharField(max_length=20)
    calcium = models.CharField(max_length=20)
    potassium = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Protein'
        verbose_name_plural = 'Proteins'

    def __str__(self):
        return f"{self.good.name} - Protein Info"

    