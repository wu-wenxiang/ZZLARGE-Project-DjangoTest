# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^billing/(?P<page>\d*)?$', views.billing, name='billing'),
    url(r'^customer/(?P<page>\d*)?$', views.customer, name='customer'),
    url(r'^add/billing/$', views.addBilling, name='add_billing'),
    url(r'^add/customer/$', views.addCustomer, name='add_customer'),
    url(r'^makexlsx/$', views.makexlsx, name="makexlsx"),
]
