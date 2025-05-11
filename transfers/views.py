from django.shortcuts import render
from django.views.generic import ListView, View # Using View for simple form display
from django.utils import timezone
from datetime import timedelta, date
from decimal import Decimal
import random

# Mock data structures (can be expanded)
class MockAccount:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class MockIncomeCategory:
    def __init__(self, id, name):
        self.id = id
        self.name = name

mock_bank_accounts_data = [
    MockAccount(id=1, name="CyberBank Main"),
    MockAccount(id=2, name="Digital Wallet X"),
    MockAccount(id=3, name="Savings Vault 7"),
]

mock_income_categories_data = [
    MockIncomeCategory(id=1, name="Consulting Gigs"),
    MockIncomeCategory(id=2, name="Software Sales"),
    MockIncomeCategory(id=3, name="Ad Revenue"),
]

def generate_mock_transfers(count=15):
    transfers = []
    directions = ['INCOMING', 'OUTGOING', 'INTERNAL']
    statuses = ['COMPLETED', 'PENDING', 'CANCELLED']
    today = timezone.now().date()

    for i in range(count):
        direction = random.choice(directions)
        source_account = None
        destination_account = None
        applied_cat_name = None
        direct_income_id = None

        if direction == 'INCOMING':
            destination_account = random.choice(mock_bank_accounts_data).name
            if random.choice([True, False]):
                applied_cat_name = random.choice(mock_income_categories_data).name
            elif random.choice([True, False]):
                direct_income_id = random.randint(100, 200)
        elif direction == 'OUTGOING':
            source_account = random.choice(mock_bank_accounts_data).name
        elif direction == 'INTERNAL':
            source_account = random.choice(mock_bank_accounts_data).name
            destination_account = random.choice([acc.name for acc in mock_bank_accounts_data if acc.name != source_account] or [mock_bank_accounts_data[0].name])


        transfers.append({
            'id': i + 1,
            'date': today - timedelta(days=random.randint(0, 90)),
            'direction': direction,
            'amount': Decimal(random.uniform(50, 5000)).quantize(Decimal("0.01")),
            'source_account_name': source_account,
            'destination_account_name': destination_account,
            'status': random.choice(statuses),
            'applied_to_income_category_name': applied_cat_name,
            'direct_linked_income_id': direct_income_id,
            'description': f"Mock transfer operation #{i+1} for {direction.lower()} flow."
        })
    return sorted(transfers, key=lambda t: t['date'], reverse=True)


class MockTransferListView(ListView):
    template_name = 'transfers/transfer_list.html'
    context_object_name = 'mock_transfers'
    # paginate_by = 10 # Can add pagination later if needed for mock

    def get_queryset(self):
        return generate_mock_transfers()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Transfers Log (Mock)"
        # context['is_paginated'] = True # If you want to show mock pagination controls
        # context['page_obj'] = {'has_previous': False, 'has_next': True, 'previous_page_number': 0, 'next_page_number': 2, 'number': 1, 'paginator': {'page_range': range(1,3)}} # Mock page_obj
        return context


class MockTransferCreateView(View):
    template_name = 'transfers/transfer_form.html'

    def get(self, request, *args, **kwargs):
        context = {
            'title': "Add New Transfer (Mock)",
            'mock_bank_accounts': mock_bank_accounts_data,
            'mock_income_categories': mock_income_categories_data,
            # 'form': None # No actual Django form for this pure mock
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # For a mock, we don't actually process the form
        # In a real scenario, you'd handle form validation and saving here
        print("Mock Transfer Form POST data:", request.POST)
        # Redirect to list view or show a success message (mocked)
        # For now, just re-render the form page or redirect
        # messages.success(request, "Mock transfer submitted successfully!") # Requires messages framework
        return redirect('transfers:list_mock') # Assumes this URL name
