from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Customer, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, Http404, HttpResponseNotFound
from .forms import CategoryForm, ProductForm, OrderForm
from django.urls import reverse




def del_product(request, pk):
    product_name = Product.objects.get(pk=pk)
    product_name.delete()
    return  HttpResponseRedirect(reverse('home'))

def edit_product(request, pk):
    try:
        product = Product.objects.all()
        product_name = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product_name)
        if form.is_valid():
            form.save()
            return redirect('product', pk=pk)
    else:
        form = ProductForm(instance=product_name)

    return render(request, 'edit_product.html', {'product': product, 'product_name': product_name, 'form': form})


def add_product(request):
    submitted = False

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('add_product?submitted=True')
    
    else: 
        form = ProductForm 
    
    if 'submitted' in request.GET: 
        submitted =True

    return render(request, 'add_product.html', {'form': form, 'submitted': submitted})


def del_category(request, pk):
    category_name = Category.objects.get(pk=pk)
    category_name.delete()
    return  HttpResponseRedirect(reverse('home'))
    

def edit_category(request, pk):
    category = Category.objects.all()
    category_name = Category.objects.filter(id=pk).first()
    form = CategoryForm(request.POST or None, instance=category_name)
    if form.is_valid():
        form.save()
        redirect('category', pk=pk)

    return render(request, 'edit_category.html', {'category':category, 'category_name':category_name, 'form': form})

def add_category(request):
    submitted = False 

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('add_category?submitted=True')
    else: 
        form = CategoryForm 
    
    if 'submitted' in request.GET: 
        submitted =True

    return render(request, 'add_category.html', {'form': form, 'submitted': submitted})

def category(request, pk):
    
    category = Category.objects.all()
    category_name = Category.objects.filter(id=pk).first()
    category_id = Category.objects.get(id=pk)
    products = Product.objects.filter(category=category_id)

    category_paginated = Paginator(Category.objects.all(), 3)
    page_number = request.GET.get('page')
    page = category_paginated.get_page(page_number)
    nums = "a" * page.paginator.num_pages

    return render(request, 'category.html', {'category':category, 'category_name':category_name, 'products':products, 'page': page , 'nums': nums})


def product(request, pk):
	category = Category.objects.all()
	product = Product.objects.get(id=pk)
	return render(request, 'product.html', {'category':category, 'product':product})

def home(request): 
    category = Category.objects.all()
    products = Product.objects.all()

    products_paginated = Paginator(Product.objects.all(), 3)
    page_number = request.GET.get('page')
    page = products_paginated.get_page(page_number)
    nums = "a" * page.paginator.num_pages

    return render(request, 'home.html', {'products': products, 'category':category, 'page': page, 'nums': nums})


def about(request):
    category = Category.objects.all()

    about_paginated = Paginator(Category.objects.all(), 5)
    page_number = request.GET.get('page')
    page = about_paginated.get_page(page_number)
    nums = "a" * page.paginator.num_pages

    return render(request, 'about.html', {'category':category, 'nums': nums})


def login_user(request): 
    if request.method == "POST": 
        username= request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None: 
            login(request, user)
            messages.success(request, ("You have been Logged in"))
            return redirect('home')

        else: 
            messages.success(request, ("There was an error, please try again"))
            return redirect('login')
    
    else:
     return render(request, 'login.html', {})
    

def logout_user(request): 
     logout(request)
     messages.success(request, ("You have been logged out"))
     return redirect('home')

def register_user(request): 
    form =SignUpForm()
    if request.method == "POST": 
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #log in user
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, ("You Have Registered Successfully..."))
            return redirect('home')
        
        else: 
            messages.success(request, ("There was a problem Registering, please try again..."))
            return  redirect('register')
        
    else:
        
     return render(request, 'register.html', {'form': form})


def create_order(request):
    submitted = False

    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return HttpResponseRedirect('create_order?submitted=True')
        
    
    else: 
        form = OrderForm()
    
    if 'submitted' in request.GET: 
        submitted =True

    return render(request, 'order_form.html', {'form': form, 'submitted': submitted}) 

