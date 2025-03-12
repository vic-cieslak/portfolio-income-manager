
from django.urls import path
from . import views

urlpatterns = [
    path('', views.income_list, name='income_list'),
    path('create/', views.income_create, name='income_create'),
    path('update/<int:pk>/', views.income_update, name='income_update'),
    path('delete/<int:pk>/', views.income_delete, name='income_delete'),
    path('calendar/', views.income_calendar, name='income_calendar'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
]
