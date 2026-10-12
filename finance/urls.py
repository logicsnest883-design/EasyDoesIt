from django.urls import path

from .views import (
    account_add,
    account_close,
    account_edit,
    accounts,
    dashboard,
    transaction_add,
    transaction_delete,
    transaction_edit,
    transactions,
    savings_goals,
    savings_goal_add,
    savings_goal_edit,
    savings_goal_delete,
    savings_goal_contribute,
    bills,
    bill_add,
    bill_edit,
    bill_mark_paid,
)

app_name = "finance"

urlpatterns = [
    path("", dashboard, name="dashboard"),

    path("accounts/", accounts, name="accounts"),
    path("accounts/add/", account_add, name="account_add"),
    path("accounts/<int:pk>/edit/", account_edit, name="account_edit"),
    path("accounts/<int:pk>/close/", account_close, name="account_close"),

    path("transactions/", transactions, name="transactions"),
    path(
        "transactions/income/add/",
        transaction_add,
        {"transaction_type": "income"},
        name="transaction_add_income",
    ),
    path(
        "transactions/expense/add/",
        transaction_add,
        {"transaction_type": "expense"},
        name="transaction_add_expense",
    ),
    path(
        "transactions/<int:pk>/edit/",
        transaction_edit,
        name="transaction_edit",
    ),
    path(
        "transactions/<int:pk>/delete/",
        transaction_delete,
        name="transaction_delete",
    ),

    path("savings/", savings_goals, name="savings_goals"),
    path("savings/add/", savings_goal_add, name="savings_goal_add"),
    path(
        "savings/<int:pk>/edit/",
        savings_goal_edit,
        name="savings_goal_edit",
    ),
    path(
        "savings/<int:pk>/contribute/",
        savings_goal_contribute,
        name="savings_goal_contribute",
    ),
    path(
        "savings/<int:pk>/delete/",
        savings_goal_delete,
        name="savings_goal_delete",
    ),
    path("bills/", bills, name="bills"),
    path("bills/", bills, name="bills"),
    path("bills/add/", bill_add, name="bill_add"),
    path("bills/<int:pk>/edit/", bill_edit, name="bill_edit"),
    path("bills/<int:pk>/mark-paid/", bill_mark_paid, name="bill_mark_paid"),
]