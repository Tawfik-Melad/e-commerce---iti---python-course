from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    categories_input = forms.CharField(
        required=False,
        help_text="Enter categories separated by commas (e.g., Electronics, Smartphones, Accessories)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter categories separated by commas'
        })
    )
    
    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'instock_items', 'description']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'instock_items': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter product description'}),
        } 