# Advanced Transfer Management & Automated Income Allocation Plan

## 1. Overview

This plan outlines a sophisticated "Transfers" feature. A `Transfer` model will represent money movements. A key enhancement is the ability for a single incoming transfer to automatically allocate its amount towards multiple unpaid/partially-paid `Income` items of a user-selected `IncomeCategory`. This provides robust tracking of payments and their application to expected revenues.

## 2. Core Changes: New `transfers` App & Models

### 2.1. Create New Django App: `transfers`

*   **Action:** Run `python manage.py startapp transfers`.
*   **Configuration:** Add `'transfers'` to `INSTALLED_APPS` in `django_project/settings.py`.
*   **Purpose:** Centralize transfer-related logic and data.

### 2.2. `Transfer` Model Definition (`transfers/models.py`)

```python
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

# Forward string references for models in other apps
# from portfolio.models import BankAccount
# from income.models import Income, IncomeCategory

class Transfer(models.Model):
    DIRECTION_CHOICES = [
        ('INCOMING', 'Incoming'),
        ('OUTGOING', 'Outgoing'),
        ('INTERNAL', 'Internal'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transfers')
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2) # Total amount of the transfer
    transfer_date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    
    destination_account = models.ForeignKey(
        'portfolio.BankAccount', 
        on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='incoming_transfers_destination' # Renamed for clarity
    )
    source_account = models.ForeignKey(
        'portfolio.BankAccount', 
        on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='outgoing_transfers_source' # Renamed for clarity
    )
    
    # For INCOMING transfers: if this transfer is intended to pay off incomes of a specific category
    apply_to_income_category = models.ForeignKey(
        'income.IncomeCategory',
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='applied_transfers',
        help_text="If selected, this transfer will attempt to pay off unpaid incomes of this category."
    )
    # Optional: Direct link to a single income, bypassing category allocation.
    # Mutually exclusive with apply_to_income_category in form logic.
    direct_linked_income = models.ForeignKey(
        'income.Income',
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='directly_linked_transfers',
        help_text="Directly link this transfer to a single income item."
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='COMPLETED')
    reference_number = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.direction} - {self.amount} on {self.transfer_date} ({self.status})"

    class Meta:
        ordering = ['-transfer_date', '-created_at']

    def clean(self):
        super().clean()
        # Basic validation (more can be added in form)
        if self.direction == 'INCOMING' and not self.destination_account:
            raise models.ValidationError({'destination_account': 'Incoming transfers must have a destination account.'})
        if self.direction == 'OUTGOING' and not self.source_account:
            raise models.ValidationError({'source_account': 'Outgoing transfers must have a source account.'})
        if self.direction == 'INTERNAL' and (not self.source_account or not self.destination_account):
            raise models.ValidationError("Internal transfers must have both source and destination accounts.")
        if self.apply_to_income_category and self.direct_linked_income:
            raise models.ValidationError("Cannot select both 'Apply to Income Category' and 'Direct Linked Income'. Choose one.")
        if (self.apply_to_income_category or self.direct_linked_income) and self.direction != 'INCOMING':
            raise models.ValidationError("Linking to income (category or direct) is only for INCOMING transfers.")

    @property
    def allocated_amount(self):
        """Returns the total amount of this transfer that has been allocated to income items."""
        return self.allocations.aggregate(total=Sum('amount_allocated'))['total'] or Decimal('0.00')

    @property
    def unallocated_amount(self):
        """Returns the amount of this transfer that is not yet allocated to any income."""
        if self.direction == 'INCOMING':
            return self.amount - self.allocated_amount
        return Decimal('0.00') # Only incoming transfers are allocated to income
```

### 2.3. New `TransferIncomeAllocation` Model (`transfers/models.py`)
This "through" model links `Transfer` to `Income` and stores the allocated amount.

```python
# In transfers/models.py

class TransferIncomeAllocation(models.Model):
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE, related_name='allocations')
    income = models.ForeignKey('income.Income', on_delete=models.CASCADE, related_name='transfer_allocations')
    amount_allocated = models.DecimalField(max_digits=12, decimal_places=2)
    allocation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('transfer', 'income') # A transfer can allocate to an income only once
        ordering = ['-allocation_date']

    def __str__(self):
        return f"{self.transfer.amount} from Transfer {self.transfer.id} allocated to Income {self.income.id} ({self.amount_allocated})"
```

### 2.4. `Income` Model Modification (`income/models.py`)

*   **Remove Mock/Old Fields:** Ensure no direct payment status fields (`is_paid`, `paid_date`, `target_bank_account`) exist on the `Income` model.
*   **Update Properties for Payment Status:**

```python
# In income/models.py, within the Income class:
from django.db.models import Sum, Q, F, ExpressionWrapper, fields # Add F, ExpressionWrapper, fields
from decimal import Decimal # Ensure Decimal is imported

# ... (existing Income model fields: user, amount, date, category, description) ...

@property
def paid_amount(self):
    """Calculates the total amount paid towards this income via linked COMPLETED transfers."""
    # Sum 'amount_allocated' from TransferIncomeAllocation where the related Transfer is COMPLETED
    total_paid = self.transfer_allocations.filter(
        transfer__status='COMPLETED'
    ).aggregate(total=Sum('amount_allocated'))['total'] or Decimal('0.00')
    return total_paid

@property
def is_fully_paid(self):
    """Checks if the income is fully paid."""
    return self.paid_amount >= self.amount

@property
def outstanding_amount(self):
    """Calculates the remaining amount to be paid for this income."""
    return max(Decimal('0.00'), self.amount - self.paid_amount)

@property
def payment_status_display(self):
    paid = self.paid_amount
    if paid >= self.amount:
        return "Paid"
    elif paid > Decimal('0.00'):
        return "Partially Paid"
    else:
        return "Unpaid"

@property
def payment_dates(self):
    """Returns a list of distinct dates of COMPLETED transfers allocated to this income."""
    return list(
        self.transfer_allocations.filter(transfer__status='COMPLETED')
        .values_list('transfer__transfer_date', flat=True)
        .distinct()
        .order_by('transfer__transfer_date')
    )

def __str__(self):
    return f"Income: {self.amount} due {self.date} ({self.payment_status_display})"
```

## 3. Database Migrations

*   Run `python manage.py makemigrations income` (to reflect model changes).
*   Run `python manage.py makemigrations transfers` (to create new models).
*   Run `python manage.py migrate`.

## 4. Business Logic: Bank Updates & Income Allocation

### 4.1. Signal Handler for Bank Balance (`transfers/signals.py`)
The bank balance update logic (from previous plan, section 4.1) remains largely the same, triggered by `Transfer` save/delete for 'COMPLETED' transfers. It adjusts `source_account` or `destination_account` balances.

### 4.2. Income Allocation Logic (New - in `transfers/signals.py` or a service)
This is triggered when an incoming `Transfer` is saved and `status` is 'COMPLETED'.

```python
# In transfers/signals.py, add to handle_transfer_save or create a new signal/service

# ... (existing signal code for bank balance updates) ...

# This function would be called from handle_transfer_save when an INCOMING transfer is COMPLETED
def allocate_income_from_transfer(transfer_instance):
    from income.models import Income # Local import to avoid circularity at module level
    
    if not (transfer_instance.direction == 'INCOMING' and transfer_instance.status == 'COMPLETED'):
        return

    # Clear existing allocations for this transfer first if re-allocation is desired on update.
    # Or, only allocate if it's newly completed or amount/category changed.
    # For simplicity, let's assume we re-evaluate allocations if key fields change.
    # This needs careful thought: if a transfer is updated, how do allocations change?
    # For now, let's focus on initial allocation.
    # A more robust solution might prevent changing category/amount once allocations exist,
    # or have a more complex reconciliation logic.

    # If direct_linked_income is set, create a single allocation
    if transfer_instance.direct_linked_income:
        income_to_pay = transfer_instance.direct_linked_income
        if income_to_pay.user == transfer_instance.user: # Ensure same user
            amount_to_allocate = min(transfer_instance.amount, income_to_pay.outstanding_amount)
            if amount_to_allocate > Decimal('0.00'):
                TransferIncomeAllocation.objects.update_or_create(
                    transfer=transfer_instance,
                    income=income_to_pay,
                    defaults={'amount_allocated': amount_to_allocate}
                )
        return # Allocation done via direct link

    # If apply_to_income_category is set, allocate across multiple incomes
    if transfer_instance.apply_to_income_category:
        # Delete previous allocations for this transfer if re-allocating
        transfer_instance.allocations.all().delete()

        remaining_transfer_amount = transfer_instance.amount
        
        # Find unpaid/partially paid incomes of the selected category for the user, oldest first
        # We need to use outstanding_amount which is a property.
        # This requires annotating the queryset or filtering in Python.
        # For simplicity, let's fetch and filter in Python. A more performant way might involve raw SQL or complex annotations.
        
        candidate_incomes = Income.objects.filter(
            user=transfer_instance.user,
            category=transfer_instance.apply_to_income_category
        ).order_by('date') # Oldest first

        for income_item in candidate_incomes:
            if remaining_transfer_amount <= Decimal('0.00'):
                break # Transfer amount fully allocated
            
            outstanding_on_income = income_item.outstanding_amount # Uses the property
            if outstanding_on_income > Decimal('0.00'):
                amount_to_allocate_to_this_income = min(remaining_transfer_amount, outstanding_on_income)
                
                TransferIncomeAllocation.objects.create(
                    transfer=transfer_instance,
                    income=income_item,
                    amount_allocated=amount_to_allocate_to_this_income
                )
                remaining_transfer_amount -= amount_to_allocate_to_this_income
    
# Modify handle_transfer_save in transfers/signals.py:
# @receiver(post_save, sender=Transfer)
# def handle_transfer_save(sender, instance, created, **kwargs):
    # ... (bank balance update logic as before) ...
    
    # After bank balance updates, if it's an INCOMING COMPLETED transfer:
    # if instance.direction == 'INCOMING' and instance.status == 'COMPLETED':
        # allocate_income_from_transfer(instance) # Call the new allocation logic

# Note: The interaction between updating a transfer and its existing allocations needs careful design.
# E.g., if a COMPLETED transfer's amount is reduced, how are allocations adjusted?
# Or if its category link is changed. This plan focuses on initial creation.
```
The `Decimal` import should be at the top of `transfers/signals.py`.
The `update_bank_balance` helper needs `from decimal import Decimal`.

## 5. User Interface (UI) - "Transfers" Section

### 5.1. Forms (`transfers/forms.py`)
Update `TransferForm`:
```python
from django import forms
from .models import Transfer # TransferIncomeAllocation not directly in form
from income.models import Income, IncomeCategory # For choices
from portfolio.models import BankAccount
from bootstrap_datepicker_plus.widgets import DatePickerInput

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = [
            'direction', 'amount', 'transfer_date', 'description', 
            'source_account', 'destination_account', 
            'apply_to_income_category', 'direct_linked_income',
            'status', 'reference_number'
        ]
        # ... widgets ...

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # self.fields['source_account'].queryset = BankAccount.objects.filter(user=user) # If BankAccount is user-specific
            # self.fields['destination_account'].queryset = BankAccount.objects.filter(user=user)
            self.fields['apply_to_income_category'].queryset = IncomeCategory.objects.all() # Or filter by user if categories are user-specific
            self.fields['direct_linked_income'].queryset = Income.objects.filter(user=user).order_by('-date')
        # ... make fields not required initially, JS will handle visibility/requirements ...
        self.fields['apply_to_income_category'].required = False
        self.fields['direct_linked_income'].required = False
        # ... (other fields like source/destination account also conditionally required)
```
JavaScript in `transfer_form.html` will be crucial to:
*   Show/hide `source_account`, `destination_account` based on `direction`.
*   If `direction` is 'INCOMING', show `apply_to_income_category` and `direct_linked_income`.
*   Ensure only one of `apply_to_income_category` or `direct_linked_income` can be selected.

### 5.2. Views & Templates (`transfers/`)
*   Standard CRUD views.
*   `TransferListView` to show transfers and their allocated/unallocated amounts.
*   `TransferDetailView` to show allocations made by a specific transfer.

## 6. UI Updates - Income Section

### 6.1. Income List (`income/templates/income/income_list.html`)
*   Display `{{ income.payment_status_display }}`, `{{ income.paid_amount }}`, `{{ income.outstanding_amount }}`.
*   "Record Payment" button links to `TransferCreateView` with `?direct_linked_income={{ income.id }}&direction=INCOMING`.

### 6.2. Income Detail (`income/templates/income/income_detail.html`)
*   Show payment status details.
*   List all `TransferIncomeAllocation` records for this income (`income.transfer_allocations.all`), displaying details of each allocated transfer and amount.

## 7. Testing
*   Extensive testing for the allocation logic:
    *   Transfer fully allocates to one income.
    *   Transfer partially allocates to one income.
    *   Transfer allocates to multiple incomes.
    *   Transfer amount less than total outstanding for category.
    *   Transfer amount more than total outstanding for category.
    *   Correct handling of `direct_linked_income` vs `apply_to_income_category`.
*   Signal handlers for bank balance and income allocation.
*   Form validation and conditional field logic.

This plan introduces a more complex but powerful system for handling payments and linking them to income.
