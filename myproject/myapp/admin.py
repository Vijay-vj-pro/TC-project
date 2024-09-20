from django.contrib import admin
from .models import datab

@admin.register(datab)

class databAdmin(admin.ModelAdmin):
    list_display = ['title','image','content','jn','vn','sn','my',]
    search_fields = ['title','content']

