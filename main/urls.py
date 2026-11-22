from tkinter.font import names

from django.urls import path
from .views import *

urlpatterns = [
    path('' , HomeView.as_view() , name='home') ,
    path('category-<slug:slug>/' , SubcategoryView.as_view() , name='subcategory') ,
    path('product-detail-<int:product_id>' , ProductDetailView.as_view() , name='product_detail') ,
    path('product-<slug:slug>/', ProductView.as_view(), name='product') ,


]












