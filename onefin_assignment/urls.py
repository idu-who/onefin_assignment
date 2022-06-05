"""onefin_assignment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from expenses import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add-employee/', views.create_employee_view, name='create_employee'),
    path('get-employee/', views.get_employee_view, name='get_employee'),
    path('add-vendor/', views.create_vendor_view, name='create_vendor'),
    path('get-vendor/', views.get_vendor_view, name='get_vendor'),
    path('add-expense/', views.create_expense_view, name='create_expense'),
    path('get-expense-for-employee/', views.get_employee_expense_view, name='get_employee_expense'),
    path('get-expense-for-vendor/', views.get_vendor_expense_view, name='get_vendor_expense'),
]
