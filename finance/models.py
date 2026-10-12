from django.conf import settings
from django.db import models
from django.utils import timezone


class FinancialProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="financial_profile",
    )

    monthly_income_target = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - Financial Profile"


class Account(models.Model):
    ACCOUNT_TYPES = [
    ("cash", "Cash"),
    ("bank", "Bank Account"),
    ("airtel_money", "Airtel Money"),
    ("mtn_money", "MTN Money"),
    ("zamtel_money", "Zamtel Money"),
    ("savings", "Savings"),
    ("other", "Other"),
]

    profile = models.ForeignKey(
        FinancialProfile,
        on_delete=models.CASCADE,
        related_name="accounts",
    )

    name = models.CharField(max_length=100)

    account_type = models.CharField(
        max_length=30,
        choices=ACCOUNT_TYPES,
        default="cash",
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    currency = models.CharField(
        max_length=10,
        default="ZMW",
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    CATEGORY_TYPES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    profile = models.ForeignKey(
        FinancialProfile,
        on_delete=models.CASCADE,
        related_name="categories",
    )

    name = models.CharField(max_length=100)

    category_type = models.CharField(
        max_length=20,
        choices=CATEGORY_TYPES,
    )

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    PAYMENT_METHODS = [
        ("cash", "Cash"),
        ("bank", "Bank"),
        ("airtel_money", "Airtel Money"),
        ("mtn_money", "MTN Mobile Money"),
        ("zamtel_money", "Zamtel Money"),
        ("card", "Card"),
        ("other", "Other"),
    ]

    profile = models.ForeignKey(
        FinancialProfile,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="transactions",
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    description = models.CharField(max_length=255)

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHODS,
        default="cash",
    )

    transaction_date = models.DateField(
        default=timezone.now,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description} - K{self.amount}"


class Budget(models.Model):
    profile = models.ForeignKey(
        FinancialProfile,
        on_delete=models.CASCADE,
        related_name="budgets",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="budgets",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "category", "month", "year"],
                name="unique_monthly_budget",
            )
        ]

    def __str__(self):
        return f"{self.category} - {self.month}/{self.year}"


class SavingsGoal(models.Model):
    profile = models.ForeignKey(
        FinancialProfile,
        on_delete=models.CASCADE,
        related_name="savings_goals",
    )

    name = models.CharField(max_length=150)

    target_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    current_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    target_date = models.DateField(
        blank=True,
        null=True,
    )

    notes = models.TextField(
        blank=True,
    )

    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def progress_percentage(self):
        if self.target_amount <= 0:
            return 0

        percentage = (
            self.current_amount / self.target_amount
        ) * 100

        return min(percentage, 100)

    def __str__(self):
        return self.name




    @property
    def remaining_amount(self):
        remaining = self.target_amount - self.current_amount
        return max(remaining, 0)


class Bill(models.Model):
    profile = models.ForeignKey(
        FinancialProfile,
        on_delete=models.CASCADE,
        related_name="bills",
    )

    name = models.CharField(max_length=150)

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    due_date = models.DateField()

    recurring = models.BooleanField(default=False)

    frequency = models.CharField(
        max_length=30,
        blank=True,
        choices=[
            ("weekly", "Weekly"),
            ("monthly", "Monthly"),
            ("yearly", "Yearly"),
        ],
    )

    paid = models.BooleanField(default=False)

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name