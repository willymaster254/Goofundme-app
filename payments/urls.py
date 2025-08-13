from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('stripe/', views.donate_stripe, name="donate_stripe"),
    path('paypal/', views.donate_paypal, name="donate_paypal"),
    path('success', views.success, name='success'),
    path('cancel', views.cancel, name='cancel'),
    path('payment_selection/', views.payment_selection, name='payment_selection'),
]
