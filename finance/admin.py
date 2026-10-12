from django.contrib import admin

from .models import (
    Account,
    Bill,
    Budget,
    Category,
    FinancialProfile,
    SavingsGoal,
    Transaction,
)


@admin.register(FinancialProfile)
class FinancialProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "monthly_income_target",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "profile",
        "account_type",
        "balance",
        "currency",
        "is_active",
    )

    list_filter = (
        "account_type",
        "is_active",
        "currency",
    )

    search_fields = (
        "name",
        "profile__user__username",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "profile",
        "category_type",
        "is_default",
    )

    list_filter = (
        "category_type",
        "is_default",
    )

    search_fields = (
        "name",
        "profile__user__username",
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "description",
        "profile",
        "transaction_type",
        "amount",
        "category",
        "account",
        "transaction_date",
    )

    list_filter = (
        "transaction_type",
        "payment_method",
        "transaction_date",
    )

    search_fields = (
        "description",
        "profile__user__username",
        "notes",
    )

    date_hierarchy = "transaction_date"


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = (
        "category",
        "profile",
        "amount",
        "month",
        "year",
    )

    list_filter = (
        "month",
        "year",
    )

    search_fields = (
        "category__name",
        "profile__user__username",
    )


@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "profile",
        "target_amount",
        "current_amount",
        "target_date",
        "completed",
    )

    list_filter = (
        "completed",
    )

    search_fields = (
        "name",
        "profile__user__username",
    )


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "profile",
        "amount",
        "due_date",
        "recurring",
        "paid",
    )

    list_filter = (
        "paid",
        "recurring",
        "frequency",
    )

    search_fields = (
        "name",
        "profile__user__username",
    )