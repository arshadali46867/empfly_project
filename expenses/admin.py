from django.contrib import admin

# Register your models here.

from .models import User, Expense


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'is_admin', 'created_at')
    search_fields = ('email', 'name')
    # list_filter = ('is_admin', 'is_active')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'category', 'date', 'created_at')
    search_fields = ('category', 'description')
    list_filter = ('category', 'date')
