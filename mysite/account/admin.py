# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Company, Material, Order


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'taxNumber', 'address', 'bank', 'bankAccount',
                    'contact', 'username', 'telephone')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('company', 'date', 'type', 'content', 'material',
                    'sizeWidth', 'sizeHeight', 'priceMaterial', 'price',
                    'quantity', 'priceTotal', 'taxPercent', 'priceIncludeTax',
                    'checkout', 'author',)
    list_editable = ['checkout', ]

admin.site.register(Material, MaterialAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Order, OrderAdmin)