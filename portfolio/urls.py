
from django.urls import path
from . import views

urlpatterns = [
    path('crypto/', views.crypto_list, name='crypto_list'),
    path('crypto/add/', views.crypto_create, name='crypto_create'),
    path('crypto/update/<int:pk>/', views.crypto_update, name='crypto_update'),
    path('crypto/delete/<int:pk>/', views.crypto_delete, name='crypto_delete'),
    path('bank/', views.bank_list, name='bank_list'),
    path('bank/add/', views.bank_create, name='bank_create'),
    path('bank/update/<int:pk>/', views.bank_update, name='bank_update'),
    path('bank/delete/<int:pk>/', views.bank_delete, name='bank_delete'),
    path('history/', views.portfolio_history, name='portfolio_history'),
    path('history/add_manual/', views.add_portfolio_history_manual, name='add_portfolio_history_manual'),
    path('history/refresh_today/', views.refresh_portfolio_history_today, name='refresh_portfolio_history_today'),
]
