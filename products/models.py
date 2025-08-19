from django.db import models
from django.contrib.auth.models import User
from category.models import Category

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # example: 99999999.99
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # optional
    instock_items = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # set when created
    updated_at = models.DateTimeField(auto_now=True)      # set whenever updated
    id = models.AutoField(primary_key=True)  # auto-incrementing ID
    description = models.TextField(blank=True, null=True) # long text allowed
    categories = models.ManyToManyField(Category, related_name="products")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products' , null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} (ID: {self.id})"
    
    def get_owner(self):
        return self.owner.username if self.owner else "No Owner"

    class Meta:
        ordering = ['-created_at']
