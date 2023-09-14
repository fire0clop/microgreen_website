from django.urls import path
from .views import create_order

urlpatterns = [
    # ... другие URL-маршруты ...
    path('create_order/', create_order, name='create_order'),
    # ... другие URL-маршруты ...
]