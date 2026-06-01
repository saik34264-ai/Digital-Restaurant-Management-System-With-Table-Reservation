from django.urls import path
from . import views

urlpatterns = [
    path('',            views.welcome,           name='welcome'),
    path('menu/',       views.menu,              name='menu'),
    path('cart/',       views.view_cart,         name='view_cart'),

  
    path('add/<int:item_id>/',      views.add_to_cart,      name='add_to_cart'),
    path('increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove/<int:item_id>/',   views.remove_from_cart,  name='remove_from_cart'),

    path('place-order/', views.place_order,       name='place_order'),
    path('kitchen/',     views.kitchen_dashboard, name='kitchen'),
    path('reserve/',     views.reserve_table,     name='reserve_table'),

    path('payment/', views.payment_page, name='payment'),
    path('confirm-payment/', views.confirm_payment, name='confirm_payment'),

    path('track-order/', views.track_order, name='track_order'),

    path('feedback/', views.feedback, name='feedback'),
]

