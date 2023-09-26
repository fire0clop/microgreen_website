from django.urls import path
from django.contrib.auth.views import LoginView
from .views import (mainlog,
                    UserListView,
                    DetailsUserView,
                    UpdateUserView, MyLoginView, register, LogoutView, myaccount,OrderListView, UserDeleteView)

urlpatterns = [
    path('', mainlog, name = 'main_login'),
    path('user_list/', UserListView.as_view(), name = 'user_list'),
    path('user_create/', register, name = 'user_create'),
    path('user_detail/<int:pk>/', DetailsUserView.as_view(), name = 'user_details'),
    path('user_update/<int:pk>/', UpdateUserView.as_view(), name = 'user_update'),
    path('user_login/', MyLoginView.as_view(), name ='user_login'),
    path('user_logout/', LogoutView.as_view(), name = 'user_logout'),
    path('user/myaccount/', myaccount, name='my_account'),
    path('user/myaccount_admin/', OrderListView.as_view(), name='admin_account'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
]