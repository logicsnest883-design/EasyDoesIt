from decimal import Decimal

from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from django.utils import timezone
from .forms import BillForm
from django.views.decorators.http import require_POST

from .forms import AccountForm
from .models import Account, FinancialProfile
from .forms import AccountForm, TransactionForm
from .models import Account, Category, FinancialProfile, Transaction, Bill

from .models import (
    Account,
    Bill,
    Category,
    FinancialProfile,
    SavingsGoal,
    Transaction,
)
from .forms import (
    AccountForm,
    TransactionForm,
    SavingsGoalForm,
    SavingsContributionForm,
)

from .models import (
    Account,
    Category,
    FinancialProfile,
    Transaction,
    SavingsGoal,
)

def dashboard(request):

    if not request.user.is_authenticated:
        return render(
            request,
            "finance/dashboard.html",
            {
                "is_finance_user": False,
            },
        )

    profile, created = FinancialProfile.objects.get_or_create(
        user=request.user
    )

    if not Category.objects.filter(profile=profile).exists():
        default_categories = [
            ("Salary", "income"),
            ("Business", "income"),
            ("Freelance", "income"),
            ("Other Income", "income"),
            ("Food", "expense"),
            ("Transport", "expense"),
            ("Rent", "expense"),
            ("Electricity", "expense"),
            ("Airtime & Data", "expense"),
            ("Education", "expense"),
            ("Health", "expense"),
            ("Entertainment", "expense"),
            ("Shopping", "expense"),
            ("Other Expense", "expense"),
        ]

        Category.objects.bulk_create(
            [
                Category(
                    profile=profile,
                    name=name,
                    category_type=category_type,
                    is_default=True,
                )
                for name, category_type in default_categories
            ]
        )

    today = timezone.now().date()

    current_month = today.month
    current_year = today.year

    transactions = Transaction.objects.filter(
        profile=profile
    )

    monthly_transactions = transactions.filter(
        transaction_date__year=current_year,
        transaction_date__month=current_month,
    )

    income = (
        monthly_transactions.filter(
            transaction_type="income"
        ).aggregate(
            total=Sum("amount")
        )["total"]
        or Decimal("0.00")
    )

    expenses = (
        monthly_transactions.filter(
            transaction_type="expense"
        ).aggregate(
            total=Sum("amount")
        )["total"]
        or Decimal("0.00")
    )

    total_balance = (
        Account.objects.filter(
            profile=profile,
            is_active=True,
        ).aggregate(
            total=Sum("balance")
        )["total"]
        or Decimal("0.00")
    )

    available = income - expenses

    recent_transactions = (
        transactions
        .select_related(
            "account",
            "category",
        )
        .order_by(
            "-transaction_date",
            "-created_at",
        )[:8]
    )

    accounts = Account.objects.filter(
        profile=profile,
        is_active=True,
    ).order_by("name")

    savings_goals = SavingsGoal.objects.filter(
        profile=profile,
        completed=False,
    ).order_by("target_date")[:4]

    upcoming_bills = Bill.objects.filter(
        profile=profile,
        paid=False,
        due_date__gte=today,
    ).order_by("due_date")[:5]

    overdue_bills = Bill.objects.filter(
        profile=profile,
        paid=False,
        due_date__lt=today,
    ).order_by("due_date")

    context = {
        "is_finance_user": True,
        "profile": profile,
        "total_balance": total_balance,
        "income": income,
        "expenses": expenses,
        "available": available,
        "recent_transactions": recent_transactions,
        "accounts": accounts,
        "savings_goals": savings_goals,
        "upcoming_bills": upcoming_bills,
        "overdue_bills": overdue_bills,
        "current_month": today.strftime("%B"),
        "current_year": current_year,
    }

    return render(
        request,
        "finance/dashboard.html",
        context,
    )




@login_required
def accounts(request):
    profile, created = FinancialProfile.objects.get_or_create(
        user=request.user
    )

    account_list = profile.accounts.filter(
        is_active=True
    ).order_by("name")

    closed_accounts = profile.accounts.filter(
        is_active=False
    ).order_by("-updated_at")

    total_balance = sum(
        account.balance
        for account in account_list
    )

    return render(
        request,
        "finance/accounts.html",
        {
            "accounts": account_list,
            "closed_accounts": closed_accounts,
            "total_balance": total_balance,
        },
    )


@login_required
def account_add(request):
    profile, created = FinancialProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = AccountForm(request.POST)

        if form.is_valid():
            account = form.save(commit=False)
            account.profile = profile
            account.is_active = True
            account.save()

            messages.success(
                request,
                f"{account.name} has been added successfully.",
            )

            return redirect("finance:accounts")

    else:
        form = AccountForm(
            initial={
                "currency": "ZMW",
            }
        )

    return render(
        request,
        "finance/account_form.html",
        {
            "form": form,
            "page_title": "Add Account",
            "submit_text": "Add Account",
        },
    )


@login_required
def account_edit(request, pk):
    profile, created = FinancialProfile.objects.get_or_create(
        user=request.user
    )

    account = get_object_or_404(
        Account,
        pk=pk,
        profile=profile,
        is_active=True,
    )

    if request.method == "POST":
        form = AccountForm(
            request.POST,
            instance=account,
        )

        if form.is_valid():
            account = form.save()

            messages.success(
                request,
                f"{account.name} has been updated.",
            )

            return redirect("finance:accounts")

    else:
        form = AccountForm(instance=account)

    return render(
        request,
        "finance/account_form.html",
        {
            "form": form,
            "page_title": "Edit Account",
            "submit_text": "Save Changes",
            "account": account,
        },
    )


@login_required
def account_close(request, pk):
    if request.method != "POST":
        return redirect("finance:accounts")

    profile, created = FinancialProfile.objects.get_or_create(
        user=request.user
    )

    account = get_object_or_404(
        Account,
        pk=pk,
        profile=profile,
        is_active=True,
    )

    account.is_active = False
    account.save(update_fields=["is_active", "updated_at"])

    messages.success(
        request,
        f"{account.name} has been closed.",
    )

    return redirect("finance:accounts")










@login_required
def transactions(request):
    profile, created = FinancialProfile.objects.get_or_create(
        user=request.user
    )

    transaction_list = (
        profile.transactions
        .select_related("account", "category")
        .order_by("-transaction_date", "-created_at")
    )

    return render(
        request,
        "finance/transactions.html",
        {
            "transactions": transaction_list,
        },
    )


@login_required
def transaction_add(request, transaction_type):
    if transaction_type not in ["income", "expense"]:
        return redirect("finance:dashboard")

    profile, created = FinancialProfile.objects.get_or_create(
        user=request.user
    )

    categories = Category.objects.filter(
        profile=profile,
        category_type=transaction_type,
    )

    if not categories.exists():
        messages.error(
            request,
            "No categories are available for this transaction type.",
        )

        return redirect("finance:dashboard")

    if request.method == "POST":

        form = TransactionForm(
            request.POST,
            profile=profile,
            transaction_type=transaction_type,
        )

        if form.is_valid():

            with transaction.atomic():

                account = (
                    Account.objects
                    .select_for_update()
                    .get(
                        pk=form.cleaned_data["account"].pk,
                        profile=profile,
                        is_active=True,
                    )
                )

                transaction_obj = form.save(commit=False)

                transaction_obj.profile = profile
                transaction_obj.transaction_type = transaction_type
                transaction_obj.account = account

                if transaction_type == "income":
                    account.balance += transaction_obj.amount
                else:
                    account.balance -= transaction_obj.amount

                account.save(
                    update_fields=[
                        "balance",
                        "updated_at",
                    ]
                )

                transaction_obj.save()

            if transaction_type == "income":
                messages.success(
                    request,
                    f"Income of K{transaction_obj.amount:,.2f} was added successfully.",
                )
            else:
                messages.success(
                    request,
                    f"Expense of K{transaction_obj.amount:,.2f} was added successfully.",
                )

            return redirect("finance:transactions")

    else:
        form = TransactionForm(
            profile=profile,
            transaction_type=transaction_type,
            initial={
                "transaction_date": timezone.localdate(),
            },
        )

    page_title = (
        "Add Income"
        if transaction_type == "income"
        else "Add Expense"
    )

    submit_text = (
        "Add Income"
        if transaction_type == "income"
        else "Add Expense"
    )

    return render(
        request,
        "finance/transaction_form.html",
        {
            "form": form,
            "page_title": page_title,
            "submit_text": submit_text,
            "transaction_type": transaction_type,
        },
    )


@login_required
def transaction_edit(request, pk):
    profile, created = FinancialProfile.objects.get_or_create(
        user=request.user
    )

    existing_transaction = get_object_or_404(
        Transaction.objects.select_related(
            "account",
            "category",
        ),
        pk=pk,
        profile=profile,
    )

    transaction_type = existing_transaction.transaction_type

    if request.method == "POST":

        form = TransactionForm(
            request.POST,
            profile=profile,
            transaction_type=transaction_type,
            instance=existing_transaction,
        )

        if form.is_valid():

            with transaction.atomic():

                old_account = (
                    Account.objects
                    .select_for_update()
                    .get(
                        pk=existing_transaction.account.pk,
                        profile=profile,
                    )
                )

                old_amount = existing_transaction.amount
                old_type = existing_transaction.transaction_type

                if old_type == "income":
                    old_account.balance -= old_amount
                else:
                    old_account.balance += old_amount

                old_account.save(
                    update_fields=[
                        "balance",
                        "updated_at",
                    ]
                )

                updated_transaction = form.save(
                    commit=False
                )

                new_account = (
                    Account.objects
                    .select_for_update()
                    .get(
                        pk=form.cleaned_data["account"].pk,
                        profile=profile,
                        is_active=True,
                    )
                )

                updated_transaction.profile = profile
                updated_transaction.transaction_type = transaction_type
                updated_transaction.account = new_account

                if transaction_type == "income":
                    new_account.balance += updated_transaction.amount
                else:
                    new_account.balance -= updated_transaction.amount

                new_account.save(
                    update_fields=[
                        "balance",
                        "updated_at",
                    ]
                )

                updated_transaction.save()

            messages.success(
                request,
                "Transaction updated successfully.",
            )

            return redirect("finance:transactions")

    else:

        form = TransactionForm(
            profile=profile,
            transaction_type=transaction_type,
            instance=existing_transaction,
        )

    page_title = (
        "Edit Income"
        if transaction_type == "income"
        else "Edit Expense"
    )

    return render(
        request,
        "finance/transaction_form.html",
        {
            "form": form,
            "page_title": page_title,
            "submit_text": "Save Changes",
            "transaction_type": transaction_type,
            "transaction": existing_transaction,
        },
    )


@login_required
def transaction_delete(request, pk):

    if request.method != "POST":
        return redirect("finance:transactions")

    profile, created = FinancialProfile.objects.get_or_create(
        user=request.user
    )

    transaction_obj = get_object_or_404(
        Transaction,
        pk=pk,
        profile=profile,
    )

    with transaction.atomic():

        account = (
            Account.objects
            .select_for_update()
            .get(
                pk=transaction_obj.account.pk,
                profile=profile,
            )
        )

        if transaction_obj.transaction_type == "income":
            account.balance -= transaction_obj.amount
        else:
            account.balance += transaction_obj.amount

        account.save(
            update_fields=[
                "balance",
                "updated_at",
            ]
        )

        transaction_obj.delete()

    messages.success(
        request,
        "Transaction deleted successfully.",
    )

    return redirect("finance:transactions")









@login_required
def savings_goals(request):
    profile, created = FinancialProfile.objects.get_or_create(
        user=request.user
    )

    goals = profile.savings_goals.order_by(
        "completed",
        "target_date",
        "-created_at",
    )

    return render(
        request,
        "finance/savings_goals.html",
        {
            "goals": goals,
        },
    )


@login_required
def savings_goal_add(request):
    profile, created = FinancialProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = SavingsGoalForm(request.POST)

        if form.is_valid():
            goal = form.save(commit=False)
            goal.profile = profile
            goal.current_amount = 0
            goal.completed = False
            goal.save()

            messages.success(
                request,
                f"{goal.name} has been created successfully.",
            )

            return redirect("finance:savings_goals")

    else:
        form = SavingsGoalForm()

    return render(
        request,
        "finance/savings_goal_form.html",
        {
            "form": form,
            "page_title": "Create Savings Goal",
            "submit_text": "Create Goal",
        },
    )


@login_required
def savings_goal_edit(request, pk):
    profile, created = FinancialProfile.objects.get_or_create(
        user=request.user
    )

    goal = get_object_or_404(
        SavingsGoal,
        pk=pk,
        profile=profile,
    )

    if request.method == "POST":
        form = SavingsGoalForm(
            request.POST,
            instance=goal,
        )

        if form.is_valid():
            goal = form.save(commit=False)

            if goal.current_amount >= goal.target_amount:
                goal.current_amount = goal.target_amount
                goal.completed = True
            else:
                goal.completed = False

            goal.save()

            messages.success(
                request,
                f"{goal.name} has been updated.",
            )

            return redirect("finance:savings_goals")

    else:
        form = SavingsGoalForm(instance=goal)

    return render(
        request,
        "finance/savings_goal_form.html",
        {
            "form": form,
            "page_title": "Edit Savings Goal",
            "submit_text": "Save Changes",
            "goal": goal,
        },
    )


@login_required
def savings_goal_contribute(request, pk):
    profile, created = FinancialProfile.objects.get_or_create(
        user=request.user
    )

    goal = get_object_or_404(
        SavingsGoal,
        pk=pk,
        profile=profile,
    )

    if request.method == "POST":
        form = SavingsContributionForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data["amount"]

            remaining = goal.target_amount - goal.current_amount

            if amount > remaining:
                amount = remaining

            goal.current_amount += amount

            if goal.current_amount >= goal.target_amount:
                goal.current_amount = goal.target_amount
                goal.completed = True

            goal.save(
                update_fields=[
                    "current_amount",
                    "completed",
                    "updated_at",
                ]
            )

            if goal.completed:
                messages.success(
                    request,
                    f"Congratulations! You completed your {goal.name} savings goal.",
                )
            else:
                messages.success(
                    request,
                    f"K{amount:,.2f} has been added to {goal.name}.",
                )

            return redirect("finance:savings_goals")

    else:
        form = SavingsContributionForm()

    return render(
        request,
        "finance/savings_contribute.html",
        {
            "form": form,
            "goal": goal,
        },
    )


@login_required
def savings_goal_delete(request, pk):
    if request.method != "POST":
        return redirect("finance:savings_goals")

    profile, created = FinancialProfile.objects.get_or_create(
        user=request.user
    )

    goal = get_object_or_404(
        SavingsGoal,
        pk=pk,
        profile=profile,
    )

    goal_name = goal.name
    goal.delete()

    messages.success(
        request,
        f"{goal_name} has been deleted.",
    )

    return redirect("finance:savings_goals")








@login_required
def bills(request):
    profile, created = FinancialProfile.objects.get_or_create(
        user=request.user
    )

    today = timezone.localdate()

    upcoming_bills = (
        profile.bills
        .filter(paid=False, due_date__gte=today)
        .order_by("due_date", "name")
    )

    overdue_bills = (
        profile.bills
        .filter(paid=False, due_date__lt=today)
        .order_by("due_date", "name")
    )

    paid_bills = (
        profile.bills
        .filter(paid=True)
        .order_by("-due_date", "-updated_at")
    )

    return render(
        request,
        "finance/bills.html",
        {
            "upcoming_bills": upcoming_bills,
            "overdue_bills": overdue_bills,
            "paid_bills": paid_bills,
            "today": today,
        },
    )








@login_required
def bill_add(request):
    profile, created = FinancialProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.profile = profile
            bill.paid = False
            bill.save()
            return redirect("finance:bills")
    else:
        form = BillForm()

    return render(
        request,
        "finance/bill_form.html",
        {
            "form": form,
            "page_title": "Add a bill",
            "submit_label": "Save bill",
        },
    )


@login_required
def bill_edit(request, pk):
    profile, created = FinancialProfile.objects.get_or_create(
        user=request.user
    )
    bill = get_object_or_404(profile.bills, pk=pk)

    if request.method == "POST":
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect("finance:bills")
    else:
        form = BillForm(instance=bill)

    return render(
        request,
        "finance/bill_form.html",
        {
            "form": form,
            "bill": bill,
            "page_title": "Edit bill",
            "submit_label": "Save changes",
        },
    )


@login_required
@require_POST
def bill_mark_paid(request, pk):
    profile, created = FinancialProfile.objects.get_or_create(
        user=request.user
    )
    bill = get_object_or_404(profile.bills, pk=pk)

    if not bill.paid:
        bill.paid = True
        bill.save(update_fields=["paid", "updated_at"])

    return redirect("finance:bills")