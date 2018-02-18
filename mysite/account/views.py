# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse,\
    StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from monthdelta import monthdelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Company, Material, Order
from django.contrib.auth.models import User, Group
import datetime
import os
import re
import tempfile
import uuid
import xlsxwriter

def _getOperators():
    operators = Group.objects.get(name='Operator').user_set.all()
    return [user for user in User.objects.all() if user.is_superuser or user in operators]

@login_required
def customer(request, page): 
    operators = _getOperators()
    
    if request.user not in operators:
        return HttpResponseRedirect('/')
    try:
        page = int(page)
    except Exception as _e:
        page = 1
     
    cleanData = {k.strip():v.strip() for k,v in request.GET.items()}
    queryString = '?'+'&'.join(['%s=%s' % (k,v) for k,v in cleanData.items()])
     
    companys = Company.objects
    if cleanData.get('name', ''):
        companys = companys.filter(name__icontains=cleanData['name'])
    if cleanData.get('contact', ''):
        companys = companys.filter(contact__icontains=cleanData['contact'])
    companys = companys.order_by('-id')
    paginator = Paginator(companys, 25)
    try:
        company_list = paginator.page(page)
    except PageNotAnInteger:
        company_list = paginator.page(1)
    except EmptyPage:
        company_list = paginator.page(paginator.num_pages)
         
    pageList = list(paginator.page_range)
    if page < (paginator.num_pages)-3:
        pageList[page+2:-1] = ['...']
    if page > 1+3:
        pageList[1:page-3] = ['...']
    offset = 25 * (page - 1)
     
    return render(request, 'account/customer.html', context=locals())

def _filterOrder(request, cleanData):
    orders = Order.objects
    operators = _getOperators()
    
    if request.user not in operators:
        orders = orders.filter(company__username=request.user)
    elif cleanData.get('company', ''):
        orders = orders.filter(company__name__icontains=cleanData['company'])
        
    if cleanData.get('content', ''):
        orders = orders.filter(content__icontains=cleanData['content'])
    
    if cleanData.get('author', ''):
        orders = orders.filter(author__username=cleanData['author'])
        
    if cleanData.get('checkout', '') == 'on' and cleanData.get('non_checkout', '') == 'on':
        orders = orders
    elif cleanData.get('checkout', '') == 'on':
        orders = orders.filter(checkout=True)
    elif cleanData.get('non_checkout', '') == 'on':
        orders = orders.filter(checkout=False)
    
    monthNum = cleanData.get('month', '1')
    try:
        monthNum = int(monthNum)
    except Exception as _e:
        monthNum = 1
    if monthNum > 0:
        endDate = datetime.date.today()
        startDate = endDate - monthdelta(monthNum)
        orders = orders.filter(date__range=[startDate, endDate])
    return orders, monthNum

@login_required
def billing(request, page):
    operators = _getOperators()
    
    try:
        page = int(page)
    except Exception as _e:
        page = 1

    cleanData = {k.strip():v.strip() for k,v in request.GET.items()}
    queryString = '?'+'&'.join(['%s=%s' % (k,v) for k,v in cleanData.items()])
    
    orders, monthNum = _filterOrder(request, cleanData)
    
    TotalTax = round(sum(orders.values_list('priceIncludeTax', flat=True)), 2)
    orders = orders.order_by('-date', '-id')
    
    paginator = Paginator(orders, 25)
    try:
        order_list = paginator.page(page)
    except PageNotAnInteger:
        order_list = paginator.page(1)
    except EmptyPage:
        order_list = paginator.page(paginator.num_pages)
        
    pageList = list(paginator.page_range)
    if page < (paginator.num_pages)-3:
        pageList[page+2:-1] = ['...']
    if page > 1+3:
        pageList[1:page-3] = ['...']
    offset = 25 * (page - 1)
    
    if request.user in operators:
        company_name_list = Company.objects.values_list('name', flat=True)
        type_list = [i[0] for i in Order.ORDER_TYPE]
        material_name_list = Material.objects.values_list('name', flat=True)
        taxPercent_list = [i[0] for i in Order.ORDER_TAX]
    
    return render(request, 'account/billing.html', context=locals())

@login_required
def addBilling(request):
    operators = _getOperators()

    if request.user not in operators or request.method != 'POST':
        return HttpResponseRedirect('/')
    
    cleanData = {k.strip():v.strip() for k,v in request.POST.items()}
    company = Company.objects.get(name=cleanData['company'])
    type = cleanData.get('type', '')
    if type not in [i[0] for i in Order.ORDER_TYPE]:
        type = 'Design'
    if type in ['Design', 'Other']:
        price = float(cleanData.get('price', ''))
    count = float(cleanData.get('count', '1'))
    taxPercent = cleanData.get('taxPercent', Order.ORDER_TAX[0][0])
    taxPercent = int(taxPercent)
    if taxPercent not in [int(i[0]) for i in Order.ORDER_TAX]:
        taxPercent = Order.ORDER_TAX[0][0]
    taxPercent = int(taxPercent)
     
    o = Order()
    o.company = company
    o.type = type
    o.content = cleanData.get('content', '')
     
    reCmp = re.compile('(\d+(\.\d+)?)')
    if type == 'Manufacture':
        material = Material.objects.get(name=cleanData['material'])
        o.material = material
         
        try:
            sizeHeight = reCmp.search(cleanData.get('sizeHeight', ''))
            sizeHeight = float(sizeHeight.groups()[0])
        except Exception as _e:
            sizeHeight = 1
        o.sizeHeight = sizeHeight
         
        try:
            sizeWidth = reCmp.search(cleanData.get('sizeWidth', ''))
            sizeWidth = float(sizeWidth.groups()[0])
        except Exception as _e:
            sizeWidth = 1
        o.sizeWidth = sizeWidth
         
        o.price = sizeHeight * sizeWidth * material.price
    else:
        o.price = price

    o.author = request.user
    o.quantity = count
    o.taxPercent = taxPercent
    o._autoFill()
    o.save()
      
    return HttpResponseRedirect('/account/billing/')

@login_required
def addCustomer(request):
    operators = _getOperators()
    
    if request.user not in operators or request.method != 'POST':
        return HttpResponseRedirect('/')
    cleanData = {k.strip():v.strip() for k,v in request.POST.items()}
    
    customerGroup = Group.objects.get(name='Customer')
    
    id = User.objects.all().last().id + 1
    username = 'cx%06d' % id
    user = User.objects.create_user(username=username, password='@aB1234')
    user.is_staff = True
    user.is_superuser = False
    user.groups.add(customerGroup)
    user.save()  
    user = User.objects.get(username=username)
    
    c = Company()
    c.name = cleanData['name']
    c.taxNumber = cleanData['tax_number']
    c.address = cleanData['address']
    c.bank = cleanData['bank']
    c.bankAccount = cleanData['account']
    c.contact = cleanData['contact']
    c.telephone = cleanData['telephone']
    c.username = user
    c.save()
    
    return HttpResponseRedirect('/account/customer/')

def convertxlsx(order_list, filePath):
    ret = True
    try:
        headings = ['ID',u'记录人',u'日期',u'公司',u'类型',u'内容',u'材料',\
                    u'单价',u'数量',u'税率',u'含税价',u'结算']

        ids = [i.id for i in order_list ]
        authors = [i.author.username for i in order_list ]
        dates = [str(i.date).decode('UTF-8') for i in order_list]
        names = [i.company.name for i in order_list]    
        types = [u'制作' if i.type == 'Manufacture' else i.type for i in order_list ]
        contents = [i.content for i in order_list ]
        materials = ['-' if i.type != 'Manufacture' else \
                     str(i.material).decode('UTF-8') + ' (' +str(i.priceMaterial) + \
                     ' * '+str(i.sizeHeight) + ' * '+str(i.sizeWidth) + ')'  for i in order_list ]            
        prices = [i.price for i in order_list ]
        quantitys = [i.quantity for i in order_list ]
        taxPercents = [i.taxPercent for i in order_list ]
        priceIncludeTaxs = [i.priceIncludeTax for i in order_list ]
        checkouts = [u'已完成' if i.checkout else u'未结算' for i in order_list ]
        data = [ids, authors, dates, names, types, contents, materials, \
            prices, quantitys, taxPercents, priceIncludeTaxs, checkouts, ]

        workbook = xlsxwriter.Workbook(filePath)
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})  #如何控制单元格宽度？  
        worksheet.write_row('A1', headings, bold)
        worksheet.write_column('A2', data[0])
        worksheet.write_column('B2', data[1])
        worksheet.write_column('C2', data[2])
        worksheet.write_column('D2', data[3])
        worksheet.write_column('E2', data[4])
        worksheet.write_column('F2', data[5])
        worksheet.write_column('G2', data[6])
        worksheet.write_column('H2', data[7])
        worksheet.write_column('I2', data[8])
        worksheet.write_column('J2', data[9])
        worksheet.write_column('K2', data[10])
        worksheet.write_column('L2', data[11])
        workbook.close()
    except Exception as _e:
        ret = False
    return ret

@login_required
def makexlsx(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/')
    
    cleanData = {k.strip():v.strip() for k,v in request.POST.items()}
    orders, _monthNum = _filterOrder(request, cleanData)
    order_list = orders.order_by('-date') 

    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    fileName = r'Orders-%s.xlsx' % (datetime.datetime.now().strftime('%Y%m%d'),)
    tempDir = tempfile.mkdtemp()
    tempFilePath = os.path.join(tempDir, 'account-online-%s' % uuid.uuid4().hex)
    if convertxlsx(order_list, tempFilePath):
        response = StreamingHttpResponse(file_iterator(tempFilePath))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(fileName)
        return response
    
    ignoreList = ['page', 'csrfmiddlewaretoken']
    queryString = '?'+'&'.join(['%s=%s' % (k,v) for k,v in cleanData.items() if k not in ignoreList])
    try:
        page = int(cleanData.get('page', 1))
    except:
        page = 1
    return HttpResponseRedirect(r'/account/billing/%s%s' % (page, queryString))

