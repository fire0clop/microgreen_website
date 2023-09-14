from django.urls import path
from django.contrib.auth.views import LoginView
from .views import mainlog, UserListView, DetailsUserView, UpdateUserView, login_view, register, LogoutView, myaccount

urlpatterns = [
    path('', mainlog, name = 'main_login'),
    path('user_list/', UserListView.as_view(), name = 'user_list'),
    path('user_create/', register, name = 'user_create'),
    path('user_detail/<int:pk>/', DetailsUserView.as_view(), name = 'user_details'),
    path('user_update/<int:pk>/', UpdateUserView.as_view(), name = 'user_update'),
    path('user_login/', LoginView.as_view(template_name ='myaccount/login.html', redirect_authenticated_user=True, ), name ='user_login'),
    path('user_logout/', LogoutView.as_view(), name = 'user_logout'),
    path('user/myaccount/', myaccount, name='my_account')
]