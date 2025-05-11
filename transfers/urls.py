from django.urls import path
from .views import MockTransferListView, MockTransferCreateView

app_name = 'transfers'

urlpatterns = [
    path('', MockTransferListView.as_view(), name='list_mock'),
    path('create/', MockTransferCreateView.as_view(), name='create_mock'),
    # Add other URLs for edit, detail, delete mocks later if needed
]
