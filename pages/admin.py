from django.contrib import admin
from .models import Page, Rate

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'average_rate')

@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ('page', 'user', 'score')
