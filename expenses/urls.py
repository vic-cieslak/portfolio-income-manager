from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.ExpenseListView.as_view(), name='list'),
    path('<int:pk>/', views.ExpenseDetailView.as_view(), name='detail'),
    path('new/', views.ExpenseCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.ExpenseUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ExpenseDeleteView.as_view(), name='delete'),
    path('calendar/', views.expense_calendar, name='calendar'),
    path('calendar/<int:year>/<int:month>/', views.expense_calendar, name='calendar'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/new/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('update-expense-ajax/', views.update_expense_ajax, name='update_expense_ajax'),
]
