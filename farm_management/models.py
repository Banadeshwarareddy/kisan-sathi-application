from django.db import models
from django.conf import settings
from django.utils import timezone


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('seeds', 'Seeds'),
        ('fertilizer', 'Fertilizer'),
        ('pesticide', 'Pesticide'),
        ('irrigation', 'Irrigation'),
        ('labor', 'Labor'),
        ('equipment', 'Equipment'),
        ('fuel', 'Fuel'),
        ('electricity', 'Electricity'),
        ('transport', 'Transport'),
        ('storage', 'Storage'),
        ('maintenance', 'Maintenance'),
        ('veterinary', 'Veterinary'),
        ('feed', 'Animal Feed'),
        ('other', 'Other'),
    ]

    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.category} - ₹{self.amount} ({self.date})"

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()


class Income(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('quintal', 'Quintal'),
        ('ton', 'Ton'),
        ('piece', 'Piece'),
        ('dozen', 'Dozen'),
        ('liter', 'Liter'),
        ('bag', 'Bag'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('received', 'Received'),
        ('partial', 'Partial'),
    ]

    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='incomes'
    )
    crop = models.CharField(max_length=100)
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    unit = models.CharField(
        max_length=20, choices=UNIT_CHOICES,
        default='kg'
    )
    rate_per_unit = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True
    )
    buyer_name = models.CharField(max_length=200, blank=True)
    sale_date = models.DateField(default=timezone.now)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    notes = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-sale_date', '-created_at']

    def save(self, *args, **kwargs):
        # Auto calculate total if qty and rate given
        if self.quantity and self.rate_per_unit:
            self.total_amount = self.quantity * self.rate_per_unit
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.crop} - ₹{self.total_amount} ({self.sale_date})"

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()


class CropPlan(models.Model):
    CROP_CHOICES = [
        ('wheat', 'Wheat (Gehun)'),
        ('rice', 'Rice (Dhan)'),
        ('maize', 'Maize (Makka)'),
        ('cotton', 'Cotton (Kapas)'),
        ('sugarcane', 'Sugarcane (Ganna)'),
        ('mustard', 'Mustard (Sarso)'),
        ('soybean', 'Soybean'),
        ('chickpea', 'Chickpea (Chana)'),
        ('tomato', 'Tomato (Tamatar)'),
        ('potato', 'Potato (Aalu)'),
        ('onion', 'Onion (Pyaz)'),
        ('groundnut', 'Groundnut (Moongfali)'),
        ('sunflower', 'Sunflower'),
        ('turmeric', 'Turmeric (Haldi)'),
        ('ginger', 'Ginger (Adrak)'),
        ('banana', 'Banana (Kela)'),
        ('mango', 'Mango (Aam)'),
        ('arhar', 'Arhar Dal'),
        ('moong', 'Moong Dal'),
        ('bajra', 'Bajra'),
        ('jowar', 'Jowar'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('sowing', 'Sowing'),
        ('growing', 'Growing'),
        ('harvesting', 'Harvesting'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='crop_plans'
    )
    crop = models.CharField(max_length=50, choices=CROP_CHOICES)
    area_acres = models.DecimalField(max_digits=8, decimal_places=2)
    planting_date = models.DateField()
    expected_harvest = models.DateField(null=True, blank=True)
    estimated_cost = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True
    )
    expected_revenue = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned'
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-planting_date']

    def __str__(self):
        return f"{self.get_crop_display()} - {self.area_acres} acres"

    @property
    def expected_profit(self):
        if self.expected_revenue and self.estimated_cost:
            return self.expected_revenue - self.estimated_cost
        return None


class Livestock(models.Model):
    ANIMAL_CHOICES = [
        ('cow', 'Cow (Gaay)'),
        ('buffalo', 'Buffalo (Bhains)'),
        ('goat', 'Goat (Bakri)'),
        ('sheep', 'Sheep (Bhed)'),
        ('pig', 'Pig (Suar)'),
        ('chicken', 'Chicken (Murgi)'),
        ('duck', 'Duck (Batakh)'),
        ('horse', 'Horse (Ghoda)'),
        ('donkey', 'Donkey (Gadha)'),
        ('camel', 'Camel (Oont)'),
        ('rabbit', 'Rabbit (Khargosh)'),
        ('other', 'Other'),
    ]

    HEALTH_CHOICES = [
        ('healthy', 'Healthy'),
        ('sick', 'Sick'),
        ('recovering', 'Recovering'),
        ('quarantine', 'Quarantine'),
        ('deceased', 'Deceased'),
    ]

    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='livestock'
    )
    animal_type = models.CharField(max_length=50, choices=ANIMAL_CHOICES)
    tag_number = models.CharField(max_length=100)
    age_months = models.IntegerField(null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True
    )
    health_status = models.CharField(
        max_length=20,
        choices=HEALTH_CHOICES,
        default='healthy'
    )
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_animal_type_display()} - {self.tag_number}"


class Loan(models.Model):
    LOAN_TYPE_CHOICES = [
        ('crop_loan', 'Crop Loan'),
        ('kcc', 'Kisan Credit Card'),
        ('equipment', 'Equipment Loan'),
        ('land', 'Land Purchase Loan'),
        ('personal', 'Personal Loan'),
        ('cooperative', 'Cooperative Loan'),
        ('microfinance', 'Microfinance'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('overdue', 'Overdue'),
        ('restructured', 'Restructured'),
    ]

    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='loans'
    )
    lender_name = models.CharField(max_length=200)
    loan_type = models.CharField(
        max_length=50, choices=LOAN_TYPE_CHOICES,
        default='crop_loan'
    )
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    tenure_months = models.IntegerField()
    emi_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default='active'
    )
    purpose = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.lender_name} - ₹{self.loan_amount}"

    @property
    def total_payable(self):
        return self.emi_amount * self.tenure_months

    @property
    def total_interest(self):
        return self.total_payable - self.loan_amount
