from django import forms
from .models import Product, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'category', 'weight', 'main_image']
        labels = {
            'name': 'Название',  # Здесь укажите переводы для каждого поля
            'price': 'Цена',
            'description': 'Описание',
            'category': 'Категория',
            'weight' : 'Вес',
            'main_image': 'Основное изображение',
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']
        labels = {
            'image': 'Изображение',
        }