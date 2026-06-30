from django.urls import path
from . import views

app_name = 'farm_management'

urlpatterns = [
    # Page
    path('', views.FarmManagementView.as_view(), name='home'),

    # Dashboard
    path('api/v1/farm/dashboard/', views.DashboardAPIView.as_view()),

    # Expenses
    path('api/v1/farm/expenses/', views.ExpenseListCreateView.as_view()),
    path('api/v1/farm/expenses/deleted/', views.ExpenseDeletedView.as_view()),
    path('api/v1/farm/expenses/<int:pk>/', views.ExpenseDetailView.as_view()),
    path('api/v1/farm/expenses/<int:pk>/restore/', views.ExpenseRestoreView.as_view()),
    path('api/v1/farm/expenses/<int:pk>/permanent/', views.ExpensePermanentDeleteView.as_view()),
    path('api/v1/farm/expenses/pdf/', views.ExpensePDFView.as_view()),
    path('api/v1/farm/expenses/excel/', views.ExpenseExcelView.as_view()),

    # Income
    path('api/v1/farm/income/', views.IncomeListCreateView.as_view()),
    path('api/v1/farm/income/deleted/', views.IncomeDeletedView.as_view()),
    path('api/v1/farm/income/<int:pk>/', views.IncomeDetailView.as_view()),
    path('api/v1/farm/income/<int:pk>/restore/', views.IncomeRestoreView.as_view()),
    path('api/v1/farm/income/<int:pk>/permanent/', views.IncomePermanentDeleteView.as_view()),
    path('api/v1/farm/income/pdf/', views.IncomePDFView.as_view()),
    path('api/v1/farm/income/excel/', views.IncomeExcelView.as_view()),

    # Crops
    path('api/v1/farm/crops/', views.CropPlanListCreateView.as_view()),
    path('api/v1/farm/crops/<int:pk>/', views.CropPlanDetailView.as_view()),

    # Livestock
    path('api/v1/farm/livestock/', views.LivestockListCreateView.as_view()),
    path('api/v1/farm/livestock/<int:pk>/', views.LivestockDetailView.as_view()),

    # Loans
    path('api/v1/farm/loans/', views.LoanListCreateView.as_view()),
    path('api/v1/farm/loans/<int:pk>/', views.LoanDetailView.as_view()),

    # Full Reports
    path('api/v1/farm/report/pdf/', views.FullReportPDFView.as_view()),
    path('api/v1/farm/report/excel/', views.FullReportExcelView.as_view()),
]
