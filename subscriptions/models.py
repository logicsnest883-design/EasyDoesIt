from django.conf import settings
from django.db import models


class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("successful", "Successful"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscription_payments",
    )

    reference = models.CharField(max_length=100, unique=True)

    airtel_transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    phone_number = models.CharField(max_length=20)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    currency = models.CharField(
        max_length=10,
        default="ZMW",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reference} - {self.status}"


class Subscription(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscription",
    )

    start_date = models.DateTimeField()
    expiry_date = models.DateTimeField()

    downloads_allowed = models.PositiveIntegerField(default=5)
    downloads_used = models.PositiveIntegerField(default=0)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def downloads_remaining(self):
        return max(
            self.downloads_allowed - self.downloads_used,
            0,
        )

    def __str__(self):
        return f"{self.user} - {self.expiry_date}"