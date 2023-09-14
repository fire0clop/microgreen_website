from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.urls import reverse_lazy
from ordering.models import Order
from .forms import UserRegisterForm
from .models import Profile
from django.contrib.auth.views import LogoutView


def mainlog(request):
    return render(request, 'myaccount/base.html')

class UserListView(ListView):
    model = User
    template_name = 'myaccount/user_list.html'
    context_object_name = 'users'



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone = form.cleaned_data.get('phone')
            company_name = form.cleaned_data.get('company_name')
            Profile.objects.create(user=user, phone=phone, company_name=company_name)
            return redirect('user_login') # замените 'login' на адрес своей страницы входа
    else:
        form = UserRegisterForm()
    return render(request, 'myaccount/user_create.html', {'form': form})

class DetailsUserView(DetailView):
    template_name = 'myaccount/user_detail.html'
    model = Profile
    context_object_name = 'users'

class UpdateUserView(UpdateView):
    template_name = 'myaccount/user_update.html'
    model = Profile
    fields = ['email', 'phone']
    success_url = reverse_lazy('user_list')



def login_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/admin/')
        return render (request, 'myaccount/base.html')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/admin/')
    return render(request, 'myaccount/base.html', {'error': 'Invalid login credentials'})

class LogoutView(LogoutView):
    next_page = reverse_lazy('main_page')

def myaccount(request):
    user = request.user  # Получаем текущего пользователя

    # Получаем активные заказы пользователя с статусами 1 или 2
    active_orders = Order.objects.filter(user=user, status__in=[1, 2])

    # Получаем завершенные заказы пользователя с статусом 3
    completed_orders = Order.objects.filter(user=user, status=3)

    return render(request, 'myaccount/my_account.html', {'active_orders': active_orders, 'completed_orders': completed_orders})