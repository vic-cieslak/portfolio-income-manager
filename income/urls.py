
from django.urls import path
from . import views

app_name = 'income'

urlpatterns = [
    path('', views.IncomeListView.as_view(), name='list'),
    path('<int:pk>/', views.IncomeDetailView.as_view(), name='detail'),
    path('new/', views.IncomeCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.IncomeUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.IncomeDeleteView.as_view(), name='delete'),
    path('calendar/', views.income_calendar, name='calendar'),
    path('calendar/<int:year>/<int:month>/', views.income_calendar, name='calendar'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/new/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
]
