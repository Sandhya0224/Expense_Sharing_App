"""
URL configuration for Expenses_Sharing_App project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from Expenses_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/',include('account.urls')),
    path("split_to_pay/<int:id>/", splitpay_to_id, name="splitpay_to_id"),
    path("split_to_be_paid/<int:id>/", splitpay_from_id, name="splitpay_from_id"),
    path("user_details/", user_details, name="user_details"),
    path("list_user_details/", list_user_details, name="list_user_details"),
    path('add_expense/', add_expense, name='add_expense'),
    path('users_expenses/', get_all_user_expenses, name='get_all_user_expenses'),
    path('download_balance_sheet/', download_balance_sheet, name='download_balance_sheet'),
]
