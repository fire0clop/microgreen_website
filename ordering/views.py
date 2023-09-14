from django.shortcuts import render, redirect
from .models import Product, Order, OrderItem
from .forms import OrderForm

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Получите данные из формы
            company_name = form.cleaned_data['company_name']
            delivery_date = form.cleaned_data['delivery_date']

            # Создайте заказ
            order = Order(user=request.user, company_name=company_name, delivery_date=delivery_date)
            order.save()

            # Получите товары из корзины
            cart_products = Product.objects.filter(id__in=request.session.get('cart', []))

            # Добавьте товары в заказ
            for product in cart_products:
                quantity = request.POST.get('quantity_' + str(product.id))
                order_item = OrderItem(order=order, product=product, quantity=quantity)
                order_item.save()

            # Очистите корзину
            request.session['cart'] = []

            # Верните пользователю страницу подтверждения заказа или другую нужную вам страницу
            return redirect('order_confirmation')  # Замените 'order_confirmation' на имя нужного представления

    else:
        form = OrderForm()

    # Получите товары из корзины для отображения
    cart_product_ids = request.session.get('cart', [])
    cart_products = Product.objects.filter(id__in=cart_product_ids)

    # Рассчитайте общую стоимость заказа
    total_price = sum(product.price * int(request.POST.get('quantity_' + str(product.id))) for product in cart_products)

    return render(request, 'product/create_order.html', {'form': form, 'cart_products': cart_products, 'total_price': total_price})