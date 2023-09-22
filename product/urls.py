from .views import (ProductList,
                    create_product,
                    ProductDetailView,
                    ProductEditView,
                    delete_image,
                    ProductDeleteView,
                    ProductCatalog,
                    toggle_favorite,
                    favorite_products,
                    toggle_cart,
                    cart_products)
from django.urls import path


urlpatterns = [
    path('product_list/', ProductList.as_view(), name = 'product_list'),
    path('product_create/', create_product, name = 'product_create'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name = 'product_detail'),
    path('product_update/<int:pk>/', ProductEditView.as_view(), name = 'product_update'),
    path('product/image/delete/<int:pk>/', delete_image, name='delete_image'),
    path('product_delete/<int:pk>/', ProductDeleteView.as_view(), name = 'product_delete'),
    path('product_catalog/', ProductCatalog.as_view(), name = 'product_catalog'),
    path('toggle_favorite/<int:product_id>/', toggle_favorite, name='toggle_favorite'),
    path('product_favorites/',favorite_products, name = 'favorite_products'),
    path('toggle_cart/<int:product_id>/', toggle_cart, name='toggle_cart'),
    path('product_cart/', cart_products, name = 'cart_products'),


]
