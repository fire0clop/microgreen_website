from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Product, ProductImage
from .forms import ProductForm, ProductImageForm
from myaccount.models import Profile
from django.contrib import messages
from django.http import HttpResponseRedirect
from ordering.forms import OrderForm
from ordering.models import OrderItem, Order, Status
class MainPage(ListView):
    model = Product
    template_name = 'product/main_page.html'
    context_object_name = 'products'
def toggle_favorite(request, product_id):
    # Получите текущую сессию пользователя
    session_key = request.session.session_key
    if not session_key:
        request.session.save()
        session_key = request.session.session_key

    # Получите список избранных продуктов из сессии (если есть)
    favorites = request.session.get('favorites', [])
    print(favorites)

    if product_id in favorites:
        # Если продукт уже в избранном, удалите его
        favorites.remove(product_id)
        messages.success(request, "Продукт удален из избранного.")
    else:
        # В противном случае, добавьте продукт в избранное
        favorites.append(product_id)
        messages.success(request, "Продукт добавлен в избранное.")

    # Обновите список избранных продуктов в сессии
    request.session['favorites'] = favorites

    # Вернитесь на предыдущую страницу
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
def favorite_products(request):
    # Получите текущую сессию пользователя
    session_key = request.session.session_key
    if not session_key:
        request.session.save()
        session_key = request.session.session_key

    # Получите список избранных продуктов из сессии (если есть)
    favorites = request.session.get('favorites', [])

    # Получите список продуктов из базы данных, которые находятся в избранном
    favorite_products = Product.objects.filter(id__in=favorites)

    return render(request, 'product/favorite_products.html', {'favorite_products': favorite_products})
def toggle_cart(request, product_id):
    # Получите текущую сессию пользователя
    session_key = request.session.session_key
    if not session_key:
        request.session.save()
        session_key = request.session.session_key

    # Получите список товаров в корзине из сессии (если есть)
    cart = request.session.get('cart', [])
    print(cart)

    if product_id in cart:
        # Если товар уже в корзине, удалите его
        cart.remove(product_id)
        messages.success(request, "Товар удален из корзины.")
    else:
        # В противном случае, добавьте товар в корзину
        cart.append(product_id)
        messages.success(request, "Товар добавлен в корзину.")

    # Обновите список товаров в корзине в сессии
    request.session['cart'] = cart

    # Вернитесь на предыдущую страницу
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
@login_required
def cart_products(request):
    if request.method == 'POST':
        # Получите данные из формы
        company_name = request.POST.get('company_name')
        delivery_date = request.POST.get('delivery_date')
        user = request.user  # Текущий пользователь
        print(user)
        status = Status.objects.get(id=1)  # Замените на соответствующий статус

        # Создайте новый заказ
        order = Order.objects.create(
            user=user,
            company_name=company_name,
            delivery_date=delivery_date,
            status=status
        )

        # Обработайте товары в корзине и создайте записи в OrderItem
        cart = request.session.get('cart', [])
        for product_id in cart:
            product = Product.objects.get(id=product_id)
            quantity = int(request.POST.get(f'quantity_{product_id}', 1))
            if quantity > 0:
                OrderItem.objects.create(order=order, product=product, quantity=quantity)

        # Очистите корзину
        request.session['cart'] = []


        return redirect('main_page')  # Замените 'success_page' на URL страницы успешного оформления заказа

    # Если это не POST-запрос, продолжайте отображать корзину
    cart = request.session.get('cart', [])
    cart_products = Product.objects.filter(id__in=cart)

    return render(request, 'product/cart_products.html', {'cart_products': cart_products})


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            images = request.FILES.getlist('images')  # Получаем список дополнительных изображений
            for image in images:
                ProductImage.objects.create(product=product, image=image)
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product/product_create.html', {'form': form})
class ProductList(ListView):
    template_name = 'product/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        search_query = self.request.GET.get('search')

        if search_query:
            # Если есть параметр поиска, фильтруем по названию продукта и атрибуту archived
            queryset = Product.objects.filter(name__icontains=search_query, archived=True)
        else:
            # Иначе показываем все продукты с атрибутом archived=True
            queryset = Product.objects.filter(archived=True)

        return queryset
class ProductDetailView(DetailView):
    queryset = Product.objects.prefetch_related('images')
    template_name = 'product/product_detail.html'
    context_object_name = 'products'
def delete_image(request, pk):
    image = get_object_or_404(ProductImage, pk=pk)
    product = image.product
    image.delete()
    return redirect('product_update', pk=product.pk)
class ProductEditView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_update.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_images'] = ProductImage.objects.filter(product=self.object)
        context['product_image_form'] = ProductImageForm()
        return context

    def form_valid(self, form):
        if 'add_image' in self.request.POST:
            # Если нажата кнопка "Add Image", обрабатываем загрузку изображения
            image_form = ProductImageForm(self.request.POST, self.request.FILES)
            if image_form.is_valid():
                new_image = image_form.save(commit=False)
                new_image.product = self.object
                new_image.save()
                return self.render_to_response(self.get_context_data(form=form))
        else:
            # Если нажата кнопка "Save Changes", сохраняем изменения в продукте
            form.save()
        return super().form_valid(form)
class ProductDeleteView(DeleteView):
    template_name = 'product/product_delete.html'
    model = Product
    success_url = reverse_lazy('product_list')
class ProductCatalog(ListView):
    template_name = 'product/product_catalog.html'
    model = Product
    context_object_name = 'products'


