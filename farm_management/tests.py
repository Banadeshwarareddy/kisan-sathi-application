from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from datetime import date
from farm_management.models import Expense, Income, CropPlan, Livestock, Loan

User = get_user_model()


class FarmManagementAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testfarmer',
            password='testpassword123',
            first_name='Test',
            last_name='Farmer'
        )
        self.other_user = User.objects.create_user(
            username='otherfarmer',
            password='testpassword123'
        )
        # Authenticate the client
        self.client.login(username='testfarmer', password='testpassword123')

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get('/farm-management/api/v1/farm/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_dashboard_api(self):
        # Create some test records
        Expense.objects.create(
            farmer=self.user,
            category='seeds',
            amount=Decimal('1500.00'),
            date=date.today(),
            notes='Bought wheat seeds'
        )
        Income.objects.create(
            farmer=self.user,
            crop='Wheat',
            quantity=Decimal('10.00'),
            unit='kg',
            rate_per_unit=Decimal('200.00'),
            total_amount=Decimal('2000.00'),
            payment_status='received',
            sale_date=date.today()
        )
        CropPlan.objects.create(
            farmer=self.user,
            crop='wheat',
            area_acres=Decimal('2.50'),
            planting_date=date.today(),
            status='sowing'
        )
        Livestock.objects.create(
            farmer=self.user,
            animal_type='cow',
            tag_number='COW-001',
            health_status='healthy'
        )
        Loan.objects.create(
            farmer=self.user,
            lender_name='Cooperative Bank',
            loan_type='crop_loan',
            loan_amount=Decimal('50000.00'),
            interest_rate=Decimal('4.50'),
            start_date=date.today(),
            tenure_months=12,
            emi_amount=Decimal('4300.00'),
            status='active'
        )

        response = self.client.get('/farm-management/api/v1/farm/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['total_expenses'], 1500.00)
        self.assertEqual(data['total_income'], 2000.00)
        self.assertEqual(data['net_profit'], 500.00)
        self.assertEqual(data['active_crop_plans'], 1)
        self.assertEqual(data['total_livestock'], 1)
        self.assertEqual(data['active_loans'], 1)

    def test_expense_crud(self):
        # 1. Create Expense
        post_data = {
            'category': 'fertilizer',
            'amount': 2500.50,
            'date': str(date.today()),
            'notes': 'Organic fertilizer'
        }
        response = self.client.post('/farm-management/api/v1/farm/expenses/', post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.filter(farmer=self.user).count(), 1)
        expense_id = response.json()['id']

        # 2. Get active expenses
        response = self.client.get('/farm-management/api/v1/farm/expenses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['expenses']), 1)

        # 3. Soft delete expense
        response = self.client.delete(f'/farm-management/api/v1/farm/expenses/{expense_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Expense.objects.get(id=expense_id).is_deleted)

        # 4. Get deleted expenses
        response = self.client.get('/farm-management/api/v1/farm/expenses/deleted/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['expenses']), 1)

        # 5. Restore expense
        response = self.client.post(f'/farm-management/api/v1/farm/expenses/{expense_id}/restore/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Expense.objects.get(id=expense_id).is_deleted)

    def test_income_crud(self):
        # 1. Create Income
        post_data = {
            'crop': 'Tomato',
            'quantity': 50.00,
            'unit': 'kg',
            'rate_per_unit': 30.00,
            'buyer_name': 'Local Market',
            'sale_date': str(date.today()),
            'payment_status': 'pending',
            'notes': 'Fresh harvest'
        }
        response = self.client.post('/farm-management/api/v1/farm/income/', post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Income.objects.filter(farmer=self.user).count(), 1)
        income_id = response.json()['id']

        # 2. Get active income
        response = self.client.get('/farm-management/api/v1/farm/income/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['incomes']), 1)

        # 3. Soft delete
        response = self.client.delete(f'/farm-management/api/v1/farm/income/{income_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Income.objects.get(id=income_id).is_deleted)

        # 4. Get deleted income
        response = self.client.get('/farm-management/api/v1/farm/income/deleted/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['incomes']), 1)

        # 5. Restore income
        response = self.client.post(f'/farm-management/api/v1/farm/income/{income_id}/restore/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Income.objects.get(id=income_id).is_deleted)

    def test_crop_plans(self):
        # 1. Create Crop Plan
        post_data = {
            'crop': 'maize',
            'area_acres': 1.5,
            'planting_date': str(date.today()),
            'expected_harvest': str(date.today()),
            'estimated_cost': 5000.00,
            'expected_revenue': 12000.00,
            'status': 'planned',
            'notes': 'Monsoon crop'
        }
        response = self.client.post('/farm-management/api/v1/farm/crops/', post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        crop_id = response.json()['id']

        # 2. Update Crop Plan
        response = self.client.put(f'/farm-management/api/v1/farm/crops/{crop_id}/', {'status': 'growing'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CropPlan.objects.get(id=crop_id).status, 'growing')

        # 3. Delete Crop Plan
        response = self.client.delete(f'/farm-management/api/v1/farm/crops/{crop_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CropPlan.objects.filter(id=crop_id).count(), 0)

    def test_livestock(self):
        # 1. Create Livestock
        post_data = {
            'animal_type': 'goat',
            'tag_number': 'GOAT-002',
            'age_months': 6,
            'purchase_date': str(date.today()),
            'purchase_price': 8000.00,
            'health_status': 'healthy',
            'notes': 'Breeding stock'
        }
        response = self.client.post('/farm-management/api/v1/farm/livestock/', post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        animal_id = response.json()['id']

        # 2. Update Livestock
        response = self.client.put(f'/farm-management/api/v1/farm/livestock/{animal_id}/', {'health_status': 'sick'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Livestock.objects.get(id=animal_id).health_status, 'sick')

        # 3. Delete (soft-deactivates by setting is_active=False)
        response = self.client.delete(f'/farm-management/api/v1/farm/livestock/{animal_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Livestock.objects.get(id=animal_id).is_active)

    def test_loans(self):
        # 1. Create Loan
        post_data = {
            'lender_name': 'SBI Bank',
            'loan_type': 'kcc',
            'loan_amount': 150000.00,
            'interest_rate': 7.00,
            'start_date': str(date.today()),
            'tenure_months': 36,
            'emi_amount': 4600.00,
            'status': 'active',
            'purpose': 'Buy tractors'
        }
        response = self.client.post('/farm-management/api/v1/farm/loans/', post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        loan_id = response.json()['id']

        # 2. Update Loan status
        response = self.client.put(f'/farm-management/api/v1/farm/loans/{loan_id}/', {'status': 'closed'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Loan.objects.get(id=loan_id).status, 'closed')

        # 3. Delete Loan
        response = self.client.delete(f'/farm-management/api/v1/farm/loans/{loan_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Loan.objects.filter(id=loan_id).count(), 0)

    def test_report_downloads(self):
        # Seed records for reports
        Expense.objects.create(farmer=self.user, category='seeds', amount=100.00, date=date.today())
        Income.objects.create(farmer=self.user, crop='Wheat', quantity=5, total_amount=500.00, sale_date=date.today())

        # Test full report PDF
        response = self.client.get('/farm-management/api/v1/farm/report/pdf/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')

        # Test full report Excel
        response = self.client.get('/farm-management/api/v1/farm/report/excel/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
