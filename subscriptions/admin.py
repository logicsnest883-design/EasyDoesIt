from django.contrib import admin
from .models import Payment, Subscription


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "user",
        "phone_number",
        "amount",
        "currency",
        "status",
        "created_at",
    )

    list_filter = ("status", "currency")
    search_fields = (
        "reference",
        "airtel_transaction_id",
        "phone_number",
        "user__username",
    )

    readonly_fields = (
        "reference",
        "airtel_transaction_id",
        "created_at",
        "updated_at",
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "start_date",
        "expiry_date",
        "downloads_allowed",
        "downloads_used",
        "active",
    )

    list_filter = ("active",)
    search_fields = ("user__username",)