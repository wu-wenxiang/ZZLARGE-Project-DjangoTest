# -*- coding: UTF-8 -*-
import os
import sys
import django
import random
import datetime


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    django.setup()
    from django.contrib.auth.models import User, Group, Permission
    from account.models import Material, Order, Company
    
    operatorGroup = Group.objects.create(name='Operator')
    operatorGroup.permissions = [
        Permission.objects.get(name='Can add company'), 
        Permission.objects.get(name='Can add order'),
    ]
    operatorGroup.save()
    
    customerGroup = Group.objects.create(name='Customer')
    customerGroup.permissions = []
    customerGroup.save()
    
    user = User.objects.create_superuser('admin', 'admin@test.com',
                                         '56e1E@ab1234')
    user.save()
    
    OPEERATOR_NUM = 2
    COMPANY_NUM = 35
    MATERIAL_NUM = 5
    ORDER_NUM = COMPANY_NUM * 200
    
    for i in range(OPEERATOR_NUM):
        user = User.objects.create_user('op%s' % i, 'op%s@test.com' % i,
                                        '1E@ab1234')
        user.is_staff = True
        user.is_superuser = False
        user.groups.add(operatorGroup)
        user.save()      
    
    for i in range(MATERIAL_NUM):
        m = Material()
        m.name = '材料-%s' % i
        m.price = random.randint(100, 200)
        m.save()
    
    for i in range(COMPANY_NUM):
        user = User.objects.create_user('cx%s' % i, 'cx%s@test.com' % i,
                                        '@aB1234')
        user.is_staff = True
        user.is_superuser = False
        user.groups.add(customerGroup)
        user.save()   
    
    cxs = User.objects.filter(groups__name='Customer')
    ops = User.objects.filter(groups__name='Operator')

    for i in range(COMPANY_NUM):
        c = Company()
        c.name = "公司-%s" % i
        if i % 3:
            c.taxNumber = '1234567'
            c.bank = random.choice(['中国银行', '中国工商银行', '中国农业银行',
                                    '中国建设银行', '中国交通银行', '招商银行', '民生银行'])
            c.bankAccount = '1234567890'
        c.address = '丹凤路%s号' % random.randint(1, 2000)
        c.contact = '联系人-%s' % i
        c.username = list(cxs)[i]
        c.telephone = '138' + ''.join([str(random.randint(0,9)) for _i in range(8)])
        c.save()
    
    materials = Material.objects.all()
    companies = Company.objects.all()
    for i in range(ORDER_NUM):
        o = Order()
        o.company = random.choice(list(companies))
        o.date = datetime.datetime.now()-datetime.timedelta(days=random.randint(1, 500))
        o.content = '内容-%s' % i
        o.quantity = random.randint(1, 5)
        o.taxPercent = (random.choice(Order.ORDER_TAX))[0]
        if i % 4:
            o.type = Order.ORDER_TYPE[0][0]
            o.price = random.randint(10, 100)*50
        else:
            o.type = Order.ORDER_TYPE[1][0]
            o.material = random.choice(list(materials))
            o.sizeWidth = random.randint(1, 5)
            o.sizeHeight = random.randint(1, 5)
        o.author = random.choice(ops)
        o._autoFill()
        o.checkout = random.choice([True, False, False])
        o.save()
        
#     permissions = Permission.objects.all()
#     print [i.name for i in permissions]
#     print [i for i in permissions]