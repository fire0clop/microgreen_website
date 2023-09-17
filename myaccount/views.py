from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse_lazy, reverse
from ordering.models import Order, Status
from .forms import UserRegisterForm
from .models import Profile
from django.contrib.auth.views import LogoutView, LoginView


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



class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'myaccount/login.html'  # Ваш шаблон для входа

    def get_success_url(self):
        # Проверяем, является ли пользователь администратором
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return reverse_lazy('admin_account')  # URL-адрес для администраторов
        return reverse_lazy('my_account')  # URL-адрес для обычных пользователей

class LogoutView(LogoutView):
    next_page = reverse_lazy('main_page')

def myaccount(request):
    user = request.user  # Получаем текущего пользователя

    # Получаем активные заказы пользователя с статусами 1 или 2
    active_orders = Order.objects.filter(user=user, status__in=[1, 2])

    # Получаем завершенные заказы пользователя с статусом 3
    completed_orders = Order.objects.filter(user=user, status=3)
    try:
        profile = Profile.objects.get(user=user)
        company_name = profile.company_name
    except Profile.DoesNotExist:
        company_name = None

    return render(request, 'myaccount/my_account.html', {'active_orders': active_orders, 'completed_orders': completed_orders, 'company_name': company_name})


class OrderListView(View):
    template_name = 'myaccount/my_account_admin.html'

    def get(self, request):
        scroll_position = request.session.get('scroll_position', '0')

        # Инициализируйте пустой словарь для хранения профилей заказов
        order_profiles = {}

        # Получите все заказы и их связанные профили
        orders = Order.objects.all().order_by('status__id')
        for order in orders:
            try:
                profile = Profile.objects.get(user=order.user)
                order_profiles[order] = profile
            except Profile.DoesNotExist:
                # Обработка случая, если объект Profile не существует для пользователя
                pass

        statuses = Status.objects.all()

        return render(request, self.template_name, {
            'orders': order_profiles,
            'statuses': statuses,
            'scroll_position': scroll_position,
        })

    def post(self, request):
        order_id = request.POST.get('order_id')
        status_id = request.POST.get('status_id')
        try:
            order = Order.objects.get(pk=order_id)
            order.status_id = status_id
            order.save()

            # Перенаправьте пользователя на текущую страницу
            return redirect('admin_account')
        except Order.DoesNotExist:
            # Обработка ошибки, если заказ не найден
            pass
        finally:
            request.session['scroll_position'] = request.POST.get('scroll_position', '0')
