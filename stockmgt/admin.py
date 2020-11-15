from django.contrib import admin
from .models import Stock, Category

# Register your models here.
class StockAdmin(admin.ModelAdmin):
  list_display = ['category', 'item_name', 'quantity']
  list_display_links = ['item_name']
  search_fields = ['category', 'item_name']
  list_filter = ['category', 'item_name']


admin.site.register(Stock, StockAdmin)
admin.site.register(Category)