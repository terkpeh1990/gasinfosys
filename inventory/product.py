from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages


def create_category(request):
    if request.method =="POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Added")
            return redirect("inventory:manage_category")
    else:
        form = CategoryForm()
    
    template = "inventory/create_category.html"
    context ={
        'form':form,
    }
    return render(request,template,context)

def edit_category(request,pk):
    category = Category.objects.get(id=pk)
    if request.method =="POST":
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Updated")
            return redirect("inventory:manage_category")
    else:
        form = CategoryForm(instance=category)
    
    template = "inventory/create_category.html"
    context ={
        'form':form,
    }
    return render(request,template,context)

def create_product(request):
    if request.method =="POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Added")
            return redirect("inventory:manage_product")
    else:
        form = ProductForm()
    
    template = "inventory/create_product.html"
    context ={
        'form':form,
    }
    return render(request,template,context)

def edit_product(request,pk):
    product = Product.objects.get(id=pk)
    if request.method =="POST":
        form = ProductForm(request.POST, instance= product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Updated")
            return redirect("inventory:manage_product")
    else:
        form = ProductForm(instance=product)
    
    template = "inventory/create_product.html"
    context ={
        'form':form,
    }
    return render(request,template,context)

def manage_category(request):
    category = Category.objects.all()
    template = "inventory/manage_category.html"
    context ={
        'category':category,
    }
    return render(request,template,context)

def manage_product(request):
    product = Product.objects.all()
    template = "inventory/manage_product.html"
    context ={
        'product':product,
    }
    return render(request,template,context)


def create_restock(request):
    if request.method == 'POST':
        form = RestockForm(request.POST)
        if form.is_valid():
            restockform = form.save(commit=False)
            restockform.status = "Incoming"
            product = Product.objects.get(id=restockform.product.id)
            restockform.unit_price = product.unit_price
            restockform.approval = "Pending"
            restockform.save()
            messages.success(request, 'Restock Created Waiting For Approval')
            return redirect('inventory:manage_restock')

    else:
        form = RestockForm()

    template = 'inventory/create_restock.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


def cancel_restock(request, pk):
    restock = Inventory_records.objects.get(pk=pk)
    restock.approval = "Cancelled"
    restock.save()
    messages.success(request, 'Restock Cancelled')
    return redirect('inventory:pending_restock')


def approve_restock(request, pk):
    restock = Inventory_records.objects.get(pk=pk)
    try:
        product = Product.objects.get(id=restock.product.id)
        get_product = Inventory.objects.get(product_id=product.id)
        get_product.instock += restock.quantity
        get_product.save()

    except Inventory.DoesNotExist:
        product = Product.objects.get(id=restock.product.id)
        Inventory.objects.create(
            product_id=product, instock=restock.quantity)
    restock.approval = "Approved"
    restock.save()
    messages.success(request, 'Restock Approved')
    return redirect('inventory:manage_restock')



def manage_restock(request):
    restock = Inventory_records.objects.all().order_by('-id')

    template = 'inventory/manage_restock.html'

    context = {
        'restock': restock,
    }

    return render(request, template, context)
