from itertools import product

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect , get_object_or_404
from pydantic import constr

from main.models import *
from order.models import *
from django.views import View

# class HomeView(View):
#     def get(self , request):
#         if request.user.is_authenticated:
#             if request.user.confirmed==True:
#                 return render(request , 'home.html')
#         return render(request , 'home-unauth.html')

class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.confirmed:
            categories = Category.objects.all()
            ads = ADbanner.objects.all()

            context = { "categories" : categories ,
                        "ads" : ads ,
                        }
            return render(request , 'home.html' , context)
        return render(request, 'home-unauth.html')

class SubcategoryView(View):
    def get(self , request , slug):
        if request.user.is_authenticated and request.user.confirmed:
            category = get_object_or_404(Category , slug=slug)
            # subcategories = SubCategory.objects.filter(category=category) """ bu ham togri """
            subcategories = category.subcategory_set.all()
            products = Product.objects.filter(sub_category__in=subcategories)

            context = {
                "subcategories" : subcategories ,
                "products" : products
            }
            return render(request , "subcategory.html" , context)
        return redirect('login')

"""class SubcategoryView(View):
    def get(self , request):
        if request.user.in_login():
            subcategories = SubCategory.objects.all()

            context = {
                "subcategories" : subcategories
            }

            return render(request , "subcategory")"""

class ProductView(View):
    def get(self , request , slug):
        if request.user.is_authenticated and request.user.confirmed:
            subcategory = get_object_or_404(SubCategory , slug=slug)
            products = Product.objects.filter(sub_category=subcategory)
            # products = subcategory.product_set.all()

            context = {
                "products" : products
            }

            return render(request , 'product.html' , context)

class ProductDetailView(View):
    def get(self , request , product_id):
        if request.user.is_authenticated and request.user.confirmed:
            product = get_object_or_404(Product , id=product_id)

            context = {
                'product' : product
            }

            return render(request , 'product_detail.html' , context)
        return redirect(request , 'home-unauth')









