from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'instock_items', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'instock_items']
    search_fields = ['name', 'description']
    list_editable = ['price', 'instock_items']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'image')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'instock_items')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
