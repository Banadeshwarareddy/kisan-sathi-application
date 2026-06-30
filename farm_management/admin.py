from django.contrib import admin
from .models import Expense, Income, CropPlan, Livestock, Loan

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['category', 'amount', 'date', 'farmer', 'is_deleted']
    list_filter = ['category', 'is_deleted', 'date']
    search_fields = ['notes', 'farmer__username']

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['crop', 'total_amount', 'sale_date', 'payment_status', 'farmer']
    list_filter = ['payment_status', 'is_deleted', 'sale_date']
    search_fields = ['crop', 'buyer_name', 'farmer__username']

@admin.register(CropPlan)
class CropPlanAdmin(admin.ModelAdmin):
    list_display = ['crop', 'area_acres', 'planting_date', 'status', 'farmer']
    list_filter = ['status', 'crop']
    search_fields = ['farmer__username']

@admin.register(Livestock)
class LivestockAdmin(admin.ModelAdmin):
    list_display = ['animal_type', 'tag_number', 'health_status', 'is_active', 'farmer']
    list_filter = ['animal_type', 'health_status', 'is_active']
    search_fields = ['tag_number', 'farmer__username']

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['lender_name', 'loan_amount', 'interest_rate', 'status', 'farmer']
    list_filter = ['status', 'loan_type']
    search_fields = ['lender_name', 'farmer__username']
