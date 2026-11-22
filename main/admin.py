from django.contrib import admin
from pydantic_core.core_schema import model_field

from .models import *

admin.site.register(
    [Category , SubCategory , Seller , Media , Property ,
     Choice , Variant , Discount , Review , ADbanner]
)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name']

