"""oase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path, include
from django.contrib.auth.views import LoginView
from main import views
from oase.forms import LoginForm


# from django.views.generic.base import TemplateView
# from main.views import IndexView

admin.site.site_header = "OASE Admin"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to OASE"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', LoginView.as_view(template_name='registration/login.html'), {'authentication_form':LoginForm}, name='login'),
    path('home/', views.home, name='home'),
    path('financial/', views.financial, name='financial'),
    path('financial/general/', views.fin_dashboard, name='fin_dashboard'),
    path('financial/detailed/', views.fin_dashboard2, name='fin_dashboard2'),
    path('financial/loan_app_list/', views.loan_app_list, name='loan_app_list'),
    path('financial/upload-csv/', views.add_loan_clients, name='add_loan_clients'),
    path('health/general/', views.health_dashboard, name='health_dashboard'),
    path('health/diet/', views.health_dashboard2, name='health_dashboard2'),
    path('health/workout/', views.health_dashboard3, name='health_dashboard3'),
    re_path(r'^financial/loan_form/(\w+)', views.form_detail, name='loan_form_detail'),
    path('health/', views.health, name='health'),
    path('health/nutrition_client_list/', views.nutr_cli_list, name='nutr_cli_list'),
    re_path(r'^health/nutr_detail/(\w+)', views.nutr_detail, name='nutr_detail'),
    path('contact/', views.contact, name='contact'),
]
