from django.contrib import admin
from .models import Food, TableReservation, KitchenOrder,Payment, Feedback


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    search_fields = ('name', 'category')


@admin.register(TableReservation)
class TableReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'date', 'time', 'guests')


@admin.register(KitchenOrder)
class KitchenOrderAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'quantity', 'status')
    list_filter = ('status',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'comment']
    search_fields = ['name']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'method', 'amount', 'status']
    list_filter = ['method', 'status']
    search_fields = ['method']    