from django import forms

from .models import Account, Category, Transaction
from django.views.decorators.http import require_POST




class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            "name",
            "account_type",
            "balance",
            "currency",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100",
                    "placeholder": "e.g. Airtel Money",
                }
            ),
            "account_type": forms.Select(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100",
                }
            ),
            "balance": forms.NumberInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "0.00",
                }
            ),
            "currency": forms.TextInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100",
                    "placeholder": "ZMW",
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if not name:
            raise forms.ValidationError("Account name is required.")

        return name

    def clean_currency(self):
        currency = self.cleaned_data["currency"].strip().upper()

        if not currency:
            raise forms.ValidationError("Currency is required.")

        return currency


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "account",
            "category",
            "amount",
            "description",
            "payment_method",
            "transaction_date",
            "notes",
        ]

        widgets = {
            "account": forms.Select(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100",
                }
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100",
                    "step": "0.01",
                    "min": "0.01",
                    "placeholder": "0.00",
                }
            ),
            "description": forms.TextInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100",
                    "placeholder": "e.g. Monthly salary",
                }
            ),
            "payment_method": forms.Select(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100",
                }
            ),
            "transaction_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100",
                    "placeholder": "Optional notes",
                }
            ),
        }

    def __init__(
        self,
        *args,
        profile=None,
        transaction_type=None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.profile = profile
        self.transaction_type = transaction_type

        if profile is not None:
            self.fields["account"].queryset = (
                Account.objects.filter(
                    profile=profile,
                    is_active=True,
                )
                .order_by("name")
            )

            categories = Category.objects.filter(
                profile=profile,
                category_type=transaction_type,
            ).order_by("name")

            self.fields["category"].queryset = categories

    def clean_amount(self):
        amount = self.cleaned_data["amount"]

        if amount <= 0:
            raise forms.ValidationError(
                "Transaction amount must be greater than zero."
            )

        return amount

    def clean(self):
        cleaned_data = super().clean()

        account = cleaned_data.get("account")
        category = cleaned_data.get("category")

        if account and self.profile:
            if account.profile_id != self.profile.id:
                self.add_error(
                    "account",
                    "Invalid account.",
                )

            if not account.is_active:
                self.add_error(
                    "account",
                    "This account is closed.",
                )

        if category and self.profile:
            if category.profile_id != self.profile.id:
                self.add_error(
                    "category",
                    "Invalid category.",
                )

            if category.category_type != self.transaction_type:
                self.add_error(
                    "category",
                    "Invalid category for this transaction type.",
                )

        return cleaned_data






from django import forms

from .models import Account, Category, Transaction, SavingsGoal


class SavingsGoalForm(forms.ModelForm):

    class Meta:
        model = SavingsGoal
        fields = [
            "name",
            "target_amount",
            "target_date",
            "notes",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100",
                    "placeholder": "e.g. New Laptop",
                }
            ),
            "target_amount": forms.NumberInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100",
                    "step": "0.01",
                    "min": "0.01",
                    "placeholder": "0.00",
                }
            ),
            "target_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100",
                    "placeholder": "Optional notes",
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if not name:
            raise forms.ValidationError("Goal name is required.")

        return name

    def clean_target_amount(self):
        amount = self.cleaned_data["target_amount"]

        if amount <= 0:
            raise forms.ValidationError(
                "Target amount must be greater than zero."
            )

        return amount


class SavingsContributionForm(forms.Form):

    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(
            attrs={
                "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100",
                "step": "0.01",
                "min": "0.01",
                "placeholder": "0.00",
            }
        ),
    )

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100",
                "placeholder": "Optional note",
            }
        ),
    )













from django import forms

from .models import Bill


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = [
            "name",
            "amount",
            "due_date",
            "recurring",
            "frequency",
            "notes",
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-100",
                "placeholder": "e.g. Electricity bill",
            }),
            "amount": forms.NumberInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-100",
                "min": "0.01",
                "step": "0.01",
                "placeholder": "0.00",
            }),
            "due_date": forms.DateInput(attrs={
                "type": "date",
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-100",
            }),
            "recurring": forms.CheckboxInput(attrs={
                "class": "h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500",
            }),
            "frequency": forms.Select(attrs={
                "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-100",
            }),
            "notes": forms.Textarea(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-100",
                "rows": 4,
                "placeholder": "Optional details about this bill",
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        recurring = cleaned_data.get("recurring")
        frequency = cleaned_data.get("frequency")

        if recurring and not frequency:
            self.add_error("frequency", "Choose how often this bill repeats.")

        return cleaned_data