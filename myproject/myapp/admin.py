from django.contrib import admin
from django.contrib.auth.models import User
from .models import datab , datab2

@admin.register(datab)

class databAdmin(admin.ModelAdmin):
    list_display = ['title','image','content','jn','vn','sn','my',]
    search_fields = ['title','content']

@admin.register(datab2)

class datab2Admin(admin.ModelAdmin):
    list_display = ['year','pdf']
    search_fields = ['year']
    

