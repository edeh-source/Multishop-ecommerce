from django.contrib import admin
from .models import Order, OrderItem
import csv
import datetime
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    print("This is the request", request)
    print("This is the queryset", queryset)
    print("print this is opts",opts)
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    print("print this is content_disposition", content_disposition)
    response = HttpResponse(content_type='text/csv')
    print(response)
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields(include_parents=False) if not field.many_to_many and not field.one_to_many]
    print("This is the field", fields)
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            print("This is obj", obj)
            print("This is the value", value)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
        

    

def order_pdf(obj):
    url = reverse('admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
order_pdf.short_description = 'Invoice'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['country', 'region', 'user', 'paid', 'delivered', order_pdf]
    list_filter = ['country', 'user', 'paid', 'delivered']
    actions = [export_to_csv]
    
    
    
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['image']    
    
