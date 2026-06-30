from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Sum, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Expense, Income, CropPlan, Livestock, Loan
from .pdf_generator import (
    generate_expense_pdf, generate_income_pdf,
    generate_full_report_pdf
)
from .excel_generator import (
    generate_expense_excel, generate_income_excel,
    generate_full_report_excel
)
from decimal import Decimal
from datetime import date
from calendar import month_name


class FarmManagementView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'farm_management/home.html', {'active_page': 'farm_management'})


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        farmer = request.user
        year = request.GET.get('year', timezone.now().year)

        # Totals
        total_expenses = Expense.objects.filter(
            farmer=farmer, is_deleted=False
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        total_income = Income.objects.filter(
            farmer=farmer, is_deleted=False
        ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')

        # Monthly data for chart
        monthly_data = []
        for month_num in range(1, 13):
            m_expense = Expense.objects.filter(
                farmer=farmer, is_deleted=False,
                date__year=year, date__month=month_num
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            m_income = Income.objects.filter(
                farmer=farmer, is_deleted=False,
                sale_date__year=year, sale_date__month=month_num
            ).aggregate(total=Sum('total_amount'))['total'] or 0
            
            monthly_data.append({
                'month': month_name[month_num],
                'income': float(m_income),
                'expense': float(m_expense),
                'profit': float(m_income) - float(m_expense),
            })

        # Expense by category
        exp_by_cat = Expense.objects.filter(
            farmer=farmer, is_deleted=False
        ).values('category').annotate(
            total=Sum('amount')
        ).order_by('-total')

        # Income by crop
        inc_by_crop = Income.objects.filter(
            farmer=farmer, is_deleted=False
        ).values('crop').annotate(
            total=Sum('total_amount')
        ).order_by('-total')

        # Recent records
        recent_expenses = list(Expense.objects.filter(
            farmer=farmer, is_deleted=False
        ).values('id', 'category', 'amount', 'date', 'notes')[:5])
        
        recent_income = list(Income.objects.filter(
            farmer=farmer, is_deleted=False
        ).values('id', 'crop', 'total_amount', 'sale_date',
                 'payment_status', 'buyer_name')[:5])
        
        recent_crops = list(CropPlan.objects.filter(
            farmer=farmer
        ).values('id', 'crop', 'area_acres', 'status',
                 'planting_date', 'expected_harvest')[:3])
        
        recent_livestock = list(Livestock.objects.filter(
            farmer=farmer, is_active=True
        ).values('id', 'animal_type', 'tag_number',
                 'health_status', 'age_months')[:3])

        # Loan summary
        active_loans = Loan.objects.filter(farmer=farmer, status='active')
        total_loan = active_loans.aggregate(
            total=Sum('loan_amount')
        )['total'] or 0

        return Response({
            'total_expenses': float(total_expenses),
            'total_income': float(total_income),
            'net_profit': float(total_income - total_expenses),
            'active_expense_records': Expense.objects.filter(
                farmer=farmer, is_deleted=False
            ).count(),
            'deleted_expense_records': Expense.objects.filter(
                farmer=farmer, is_deleted=True
            ).count(),
            'active_income_records': Income.objects.filter(
                farmer=farmer, is_deleted=False
            ).count(),
            'deleted_income_records': Income.objects.filter(
                farmer=farmer, is_deleted=True
            ).count(),
            'active_crop_plans': CropPlan.objects.filter(farmer=farmer).count(),
            'total_livestock': Livestock.objects.filter(
                farmer=farmer, is_active=True
            ).count(),
            'active_loans': active_loans.count(),
            'total_loan_amount': float(total_loan),
            'monthly_data': monthly_data,
            'expense_by_category': [
                {'category': e['category'], 'amount': float(e['total'])}
                for e in exp_by_cat
            ],
            'income_by_crop': [
                {'crop': i['crop'], 'amount': float(i['total'])}
                for i in inc_by_crop
            ],
            'recent_expenses': [
                {**e, 'amount': float(e['amount']), 'date': str(e['date'])}
                for e in recent_expenses
            ],
            'recent_income': [
                {**i, 'total_amount': float(i['total_amount'] or 0),
                 'sale_date': str(i['sale_date'])}
                for i in recent_income
            ],
            'recent_crop_plans': [
                {**c, 'area_acres': float(c['area_acres']),
                 'planting_date': str(c['planting_date']),
                 'expected_harvest': str(c['expected_harvest'])
                 if c['expected_harvest'] else None}
                for c in recent_crops
            ],
            'recent_livestock': recent_livestock,
        })


# ── EXPENSE VIEWS ──────────────────────────────
class ExpenseListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(farmer=request.user, is_deleted=False)
        data = [{
            'id': e.id,
            'category': e.category,
            'category_display': e.get_category_display(),
            'amount': float(e.amount),
            'date': str(e.date),
            'notes': e.notes,
            'created_at': e.created_at.isoformat(),
        } for e in expenses]
        return Response({'expenses': data, 'count': len(data)})

    def post(self, request):
        category = request.data.get('category')
        amount = request.data.get('amount')
        date_str = request.data.get('date')
        notes = request.data.get('notes', '')

        if not category or not amount:
            return Response(
                {'error': 'Category and amount are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            expense = Expense.objects.create(
                farmer=request.user,
                category=category,
                amount=Decimal(str(amount)),
                date=date_str or date.today(),
                notes=notes
            )
            return Response({
                'id': expense.id,
                'category': expense.category,
                'category_display': expense.get_category_display(),
                'amount': float(expense.amount),
                'date': str(expense.date),
                'notes': expense.notes,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ExpenseDeletedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(farmer=request.user, is_deleted=True)
        data = [{
            'id': e.id,
            'category': e.category,
            'category_display': e.get_category_display(),
            'amount': float(e.amount),
            'date': str(e.date),
            'notes': e.notes,
        } for e in expenses]
        return Response({'expenses': data, 'count': len(data)})


class ExpenseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            expense = Expense.objects.get(pk=pk, farmer=request.user)
            expense.soft_delete()
            return Response(
                {'message': 'Expense moved to history'},
                status=status.HTTP_200_OK
            )
        except Expense.DoesNotExist:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class ExpenseRestoreView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            expense = Expense.objects.get(
                pk=pk, farmer=request.user, is_deleted=True
            )
            expense.restore()
            return Response({'message': 'Expense restored'})
        except Expense.DoesNotExist:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class ExpensePermanentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            expense = Expense.objects.get(
                pk=pk, farmer=request.user, is_deleted=True
            )
            expense.delete()  # Permanent deletion
            return Response(
                {'message': 'Expense permanently deleted'},
                status=status.HTTP_200_OK
            )
        except Expense.DoesNotExist:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class ExpensePDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(farmer=request.user, is_deleted=False)
        pdf_buffer = generate_expense_pdf(expenses, request.user)
        response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="kisan_sathi_expenses.pdf"'
        return response


class ExpenseExcelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(farmer=request.user, is_deleted=False)
        excel_buffer = generate_expense_excel(expenses, request.user)
        response = HttpResponse(
            excel_buffer.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="kisan_sathi_expenses.xlsx"'
        return response


# ── INCOME VIEWS ──────────────────────────────
class IncomeListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        incomes = Income.objects.filter(farmer=request.user, is_deleted=False)
        data = [{
            'id': i.id,
            'crop': i.crop,
            'quantity': float(i.quantity) if i.quantity else None,
            'unit': i.unit,
            'rate_per_unit': float(i.rate_per_unit) if i.rate_per_unit else None,
            'total_amount': float(i.total_amount) if i.total_amount else 0,
            'buyer_name': i.buyer_name,
            'sale_date': str(i.sale_date),
            'payment_status': i.payment_status,
            'notes': i.notes,
        } for i in incomes]
        return Response({'incomes': data, 'count': len(data)})

    def post(self, request):
        crop = request.data.get('crop')
        quantity = request.data.get('quantity')
        unit = request.data.get('unit', 'kg')
        rate_per_unit = request.data.get('rate_per_unit')
        buyer_name = request.data.get('buyer_name', '')
        sale_date = request.data.get('sale_date')
        payment_status = request.data.get('payment_status', 'pending')
        notes = request.data.get('notes', '')

        if not crop:
            return Response(
                {'error': 'Crop is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            income = Income.objects.create(
                farmer=request.user,
                crop=crop,
                quantity=Decimal(str(quantity)) if quantity else None,
                unit=unit,
                rate_per_unit=Decimal(str(rate_per_unit)) if rate_per_unit else None,
                buyer_name=buyer_name,
                sale_date=sale_date or date.today(),
                payment_status=payment_status,
                notes=notes
            )
            return Response({
                'id': income.id,
                'crop': income.crop,
                'total_amount': float(income.total_amount or 0),
                'sale_date': str(income.sale_date),
                'payment_status': income.payment_status,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class IncomeDeletedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        incomes = Income.objects.filter(farmer=request.user, is_deleted=True)
        data = [{
            'id': i.id,
            'crop': i.crop,
            'total_amount': float(i.total_amount or 0),
            'sale_date': str(i.sale_date),
            'payment_status': i.payment_status,
        } for i in incomes]
        return Response({'incomes': data, 'count': len(data)})


class IncomeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            income = Income.objects.get(pk=pk, farmer=request.user)
            income.soft_delete()
            return Response({'message': 'Income moved to history'})
        except Income.DoesNotExist:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class IncomeRestoreView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            income = Income.objects.get(
                pk=pk, farmer=request.user, is_deleted=True
            )
            income.restore()
            return Response({'message': 'Income restored'})
        except Income.DoesNotExist:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class IncomePermanentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            income = Income.objects.get(
                pk=pk, farmer=request.user, is_deleted=True
            )
            income.delete()  # Permanent deletion
            return Response(
                {'message': 'Income permanently deleted'},
                status=status.HTTP_200_OK
            )
        except Income.DoesNotExist:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class IncomePDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        incomes = Income.objects.filter(farmer=request.user, is_deleted=False)
        pdf_buffer = generate_income_pdf(incomes, request.user)
        response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="kisan_sathi_income.pdf"'
        return response


class IncomeExcelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        incomes = Income.objects.filter(farmer=request.user, is_deleted=False)
        excel_buffer = generate_income_excel(incomes, request.user)
        response = HttpResponse(
            excel_buffer.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="kisan_sathi_income.xlsx"'
        return response


# ── CROP PLAN VIEWS ───────────────────────────
class CropPlanListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        crops = CropPlan.objects.filter(farmer=request.user)
        data = [{
            'id': c.id,
            'crop': c.crop,
            'crop_display': c.get_crop_display(),
            'area_acres': float(c.area_acres),
            'planting_date': str(c.planting_date),
            'expected_harvest': str(c.expected_harvest) if c.expected_harvest else None,
            'estimated_cost': float(c.estimated_cost) if c.estimated_cost else None,
            'expected_revenue': float(c.expected_revenue) if c.expected_revenue else None,
            'expected_profit': float(c.expected_profit) if c.expected_profit else None,
            'status': c.status,
            'notes': c.notes,
        } for c in crops]
        return Response({'crops': data, 'count': len(data)})

    def post(self, request):
        try:
            crop = CropPlan.objects.create(
                farmer=request.user,
                crop=request.data.get('crop'),
                area_acres=Decimal(str(request.data.get('area_acres'))),
                planting_date=request.data.get('planting_date'),
                expected_harvest=request.data.get('expected_harvest') or None,
                estimated_cost=Decimal(str(request.data.get('estimated_cost')))
                if request.data.get('estimated_cost') else None,
                expected_revenue=Decimal(str(request.data.get('expected_revenue')))
                if request.data.get('expected_revenue') else None,
                status=request.data.get('status', 'planned'),
                notes=request.data.get('notes', ''),
            )
            return Response({
                'id': crop.id,
                'crop': crop.crop,
                'crop_display': crop.get_crop_display(),
                'status': crop.status,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class CropPlanDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            crop = CropPlan.objects.get(pk=pk, farmer=request.user)
            crop.status = request.data.get('status', crop.status)
            crop.notes = request.data.get('notes', crop.notes)
            crop.save()
            return Response({'message': 'Updated', 'status': crop.status})
        except CropPlan.DoesNotExist:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            crop = CropPlan.objects.get(pk=pk, farmer=request.user)
            crop.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CropPlan.DoesNotExist:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )


# ── LIVESTOCK VIEWS ───────────────────────────
class LivestockListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        animals = Livestock.objects.filter(farmer=request.user, is_active=True)
        data = [{
            'id': a.id,
            'animal_type': a.animal_type,
            'animal_display': a.get_animal_type_display(),
            'tag_number': a.tag_number,
            'age_months': a.age_months,
            'purchase_date': str(a.purchase_date) if a.purchase_date else None,
            'purchase_price': float(a.purchase_price) if a.purchase_price else None,
            'health_status': a.health_status,
            'notes': a.notes,
        } for a in animals]
        return Response({'livestock': data, 'count': len(data)})

    def post(self, request):
        try:
            animal = Livestock.objects.create(
                farmer=request.user,
                animal_type=request.data.get('animal_type'),
                tag_number=request.data.get('tag_number'),
                age_months=request.data.get('age_months') or None,
                purchase_date=request.data.get('purchase_date') or None,
                purchase_price=Decimal(str(request.data.get('purchase_price')))
                if request.data.get('purchase_price') else None,
                health_status=request.data.get('health_status', 'healthy'),
                notes=request.data.get('notes', ''),
            )
            return Response({
                'id': animal.id,
                'animal_type': animal.animal_type,
                'tag_number': animal.tag_number,
                'health_status': animal.health_status,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class LivestockDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            animal = Livestock.objects.get(pk=pk, farmer=request.user)
            animal.health_status = request.data.get('health_status', animal.health_status)
            animal.notes = request.data.get('notes', animal.notes)
            animal.save()
            return Response({'message': 'Updated'})
        except Livestock.DoesNotExist:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            animal = Livestock.objects.get(pk=pk, farmer=request.user)
            animal.is_active = False
            animal.save()
            return Response({'message': 'Removed'})
        except Livestock.DoesNotExist:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )


# ── LOAN VIEWS ────────────────────────────────
class LoanListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        loans = Loan.objects.filter(farmer=request.user)
        data = [{
            'id': l.id,
            'lender_name': l.lender_name,
            'loan_type': l.loan_type,
            'loan_type_display': l.get_loan_type_display(),
            'loan_amount': float(l.loan_amount),
            'interest_rate': float(l.interest_rate),
            'start_date': str(l.start_date),
            'tenure_months': l.tenure_months,
            'emi_amount': float(l.emi_amount),
            'status': l.status,
            'purpose': l.purpose,
            'total_payable': float(l.total_payable),
            'total_interest': float(l.total_interest),
        } for l in loans]
        return Response({'loans': data, 'count': len(data)})

    def post(self, request):
        try:
            loan = Loan.objects.create(
                farmer=request.user,
                lender_name=request.data.get('lender_name'),
                loan_type=request.data.get('loan_type', 'crop_loan'),
                loan_amount=Decimal(str(request.data.get('loan_amount'))),
                interest_rate=Decimal(str(request.data.get('interest_rate'))),
                start_date=request.data.get('start_date'),
                tenure_months=int(request.data.get('tenure_months')),
                emi_amount=Decimal(str(request.data.get('emi_amount'))),
                status=request.data.get('status', 'active'),
                purpose=request.data.get('purpose', ''),
            )
            return Response({
                'id': loan.id,
                'lender_name': loan.lender_name,
                'loan_amount': float(loan.loan_amount),
                'status': loan.status,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class LoanDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            loan = Loan.objects.get(pk=pk, farmer=request.user)
            loan.status = request.data.get('status', loan.status)
            loan.save()
            return Response({'message': 'Updated'})
        except Loan.DoesNotExist:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            loan = Loan.objects.get(pk=pk, farmer=request.user)
            loan.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Loan.DoesNotExist:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )


# ── FULL REPORT VIEWS ─────────────────────────
class FullReportPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pdf_buffer = generate_full_report_pdf(request.user)
        response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="kisan_sathi_farm_report.pdf"'
        return response


class FullReportExcelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        excel_buffer = generate_full_report_excel(request.user)
        response = HttpResponse(
            excel_buffer.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="kisan_sathi_farm_report.xlsx"'
        return response
