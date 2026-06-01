from django.shortcuts import render, redirect, get_object_or_404
from .models import Food, KitchenOrder, TableReservation, Payment, Feedback


# ───────────────── PAYMENT MODULE ─────────────────

def payment_page(request):
    cart = request.session.get('cart', {})
    total = 0

    for item_id, data in cart.items():
        total += data['price'] * data['quantity']

    return render(request, 'app1/payment.html', {'total': total})


def confirm_payment(request):
    if request.method == 'POST':
        method = request.POST.get('method')

        cart = request.session.get('cart', {})
        total = 0

        for item_id, data in cart.items():
            total += data['price'] * data['quantity']

            KitchenOrder.objects.create(
                food_name=data['name'],
                quantity=data['quantity'],
                status='Pending'
            )

        Payment.objects.create(
            method=method,
            amount=total,
            status='Paid'
        )

        request.session['cart'] = {}
        request.session.modified = True

        return render(request, 'app1/success.html')

    return redirect('view_cart')


# ───────────────── FEEDBACK MODULE ─────────────────

def feedback(request):
    if request.method == 'POST':
        Feedback.objects.create(
            name=request.POST.get('name'),
            rating=request.POST.get('rating'),
            comment=request.POST.get('comment')
        )
        return render(request, 'app1/feedback_success.html')

    return render(request, 'app1/feedback.html')


# ───────────────── ORDER TRACKING ─────────────────

def track_order(request):
    orders = KitchenOrder.objects.all().order_by('-id')
    return render(request, 'app1/track_order.html', {'orders': orders})


# ───────────────── WELCOME PAGE ─────────────────

def welcome(request):
    return render(request, 'app1/index.html')


# ───────────────── MENU PAGE ─────────────────

def menu(request):
    items = Food.objects.all()
    return render(request, 'app1/menu.html', {'items': items})


# ───────────────── ADD TO CART ─────────────────

def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    key = str(item_id)

    if key in cart:
        cart[key]['quantity'] += 1
    else:
        food = get_object_or_404(Food, id=item_id)

        cart[key] = {
            'name': food.name,
            'price': food.price,
            'quantity': 1,
        }

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('menu')


# ───────────────── VIEW CART ─────────────────

def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for item_id, data in cart.items():
        total_price = data['price'] * data['quantity']
        total += total_price

        items.append({
            'id': item_id,
            'name': data['name'],
            'price': data['price'],
            'quantity': data['quantity'],
            'total_price': total_price,
        })

    return render(request, 'app1/cart.html', {
        'items': items,
        'total': total
    })


# ───────────────── INCREASE QUANTITY ─────────────────

def increase_quantity(request, item_id):
    cart = request.session.get('cart', {})
    key = str(item_id)

    if key in cart:
        cart[key]['quantity'] += 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('view_cart')


# ───────────────── DECREASE QUANTITY ─────────────────

def decrease_quantity(request, item_id):
    cart = request.session.get('cart', {})
    key = str(item_id)

    if key in cart:
        if cart[key]['quantity'] > 1:
            cart[key]['quantity'] -= 1
        else:
            del cart[key]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('view_cart')


# ───────────────── REMOVE ITEM ─────────────────

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    key = str(item_id)

    if key in cart:
        del cart[key]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('view_cart')


# ───────────────── PLACE ORDER ─────────────────

def place_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        if not cart:
            return redirect('view_cart')

        for item_id, data in cart.items():
            KitchenOrder.objects.create(
                food_name=data['name'],
                quantity=data['quantity'],
                status='Pending'
            )

        request.session['cart'] = {}
        request.session.modified = True

        return render(request, 'app1/success.html')

    return redirect('view_cart')


# ───────────────── KITCHEN DASHBOARD ─────────────────

def kitchen_dashboard(request):

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')

        order = get_object_or_404(KitchenOrder, id=order_id)
        order.status = new_status
        order.save()

        return redirect('kitchen')

    pending = KitchenOrder.objects.filter(status='Pending').order_by('-id')
    preparing = KitchenOrder.objects.filter(status='Preparing').order_by('-id')
    ready = KitchenOrder.objects.filter(status='Ready').order_by('-id')
    served = KitchenOrder.objects.filter(status='Served').order_by('-id')

    return render(request, 'app1/kitchen.html', {
        'pending': pending,
        'preparing': preparing,
        'ready': ready,
        'served': served,
    })


# ───────────────── TABLE RESERVATION ─────────────────

def reserve_table(request):
    if request.method == 'POST':

        TableReservation.objects.create(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            date=request.POST.get('date'),
            time=request.POST.get('time'),
            guests=request.POST.get('guests'),
        )

        return render(request, 'app1/reservation_success.html')

    return render(request, 'app1/reserve_table.html')


# ───────────────── EDIT ITEM ─────────────────

def edit_item(request, id):
    item = get_object_or_404(Food, id=id)

    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.price = request.POST.get('price')
        item.category = request.POST.get('category')

        if request.FILES.get('image'):
            item.image = request.FILES['image']

        item.save()
        return redirect('menu')

    return render(request, 'app1/edit_item.html', {'item': item})


# ───────────────── DELETE ITEM ─────────────────

def delete_item(request, id):
    item = get_object_or_404(Food, id=id)

    if request.method == 'POST':
        item.delete()
        return redirect('menu')

    return render(request, 'app1/confirm_delete.html', {'item': item})