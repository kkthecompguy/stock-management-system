import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Stock, StockHistory
from .forms import * 

# Create your views here.
def index(request):
  title = "Stock Management System | Welcome"
  content = "Home Page"
  context = {
    'title': title,
    'content': content
  }
  # return render(request, 'stockmgt/index.html', context)
  return redirect('list-items')


@login_required
def list_items(request):
  queryset = Stock.objects.all()
  title = "Stock Management System | List of Items"
  form = StockSearchForm(request.POST or None)
  context = {
    'objects': queryset,
    'title': title,
    'form': form
  }
  
  if request.method == 'POST':
    category = form['category'].value()
    queryset = Stock.objects.filter( item_name__icontains=form['item_name'].value())

    if category != '':
      queryset = queryset.filter(category_id=category)
      
    if form['export_to_csv'].value() == True:
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
      writer = csv.writer(response)
      writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
      instance = queryset
      for stock in instance:
        writer.writerow([stock.category, stock.item_name, stock.quantity])
      return response

    context = {
      'objects': queryset,
      'title': title,
      'form': form
    }

  return render(request, 'stockmgt/list_items.html', context)


@login_required
def add_items(request):
  title = 'Stock Management System | Add Items'
  form = StockCreateForm(request.POST or None)
  if form.is_valid():
    form.save()
    messages.success(request, 'Successfully added!')
    return redirect('list-items')
  context = {
    'form': form,
    'title': title,
    'action': 'Add'
  }
  return render(request, 'stockmgt/add_items.html', context)


@login_required
def update_items(request, pk):
  item = get_object_or_404(Stock, pk=pk)
  form = StockUpdateForm(request.POST or None, instance=item)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      messages.success(request, 'Successfully updated!')
      return redirect('list-items')
  context = {
    'form': form,
    'action': 'Update',
    'title': item.item_name
  }
  return render(request, 'stockmgt/add_items.html', context)


@login_required
def delete_items(request, pk):
  item = get_object_or_404(Stock, pk=pk)
  if request.method == 'POST':
    item.delete()
    messages.error(request, 'Successfully deleted!')
    return redirect('list-items')
  return render(request, 'stockmgt/delete.html', context={'item': item.item_name})


@login_required
def stock_detail(request, pk):
  queryset = get_object_or_404(Stock, pk=pk)
  context = {
    'title': queryset.item_name,
    'queryset': queryset
  }
  return render(request, 'stockmgt/stock_detail.html', context)


@login_required
def issue_items(request, pk):
  item = get_object_or_404(Stock, pk=pk)
  form = IssueForm(request.POST or None, instance=item)
  if form.is_valid():
    instance = form.save(commit=False)
    instance.receive_quantity = 0
    instance.quantity -= instance.issue_quantity
    instance.issue_by = str(request.user)
    instance.save()
    messages.success(request, f'Issued successfully, {instance.quantity} {instance.item_name} now in store')
    return redirect('stock-detail', instance.pk)
  context = {
    'title': 'Issue'+' '+ item.item_name,
    'instance': item,
    'form': form
  }
  return render(request, 'stockmgt/add_items.html', context)


@login_required
def receive_items(request, pk):
  item = get_object_or_404(Stock, pk=pk)
  form = ReceiveForm(request.POST or None, instance=item)
  if form.is_valid():
    instance = form.save(commit=False)
    instance.issue_quantity = 0
    instance.quantity += instance.receive_quantity
    instance.receive_by = str(request.user)
    instance.save()
    messages.success(request, f'Received successfully, {instance.quantity} {instance.item_name} now in store')
    return redirect('stock-detail', instance.pk)

  context = {
    'title': 'Receive'+' '+ item.item_name,
    'action': 'Receive'+' '+ item.item_name,
    'instance': item,
    'form': form
  }
  return render(request, 'stockmgt/add_items.html', context)


@login_required
def reorder_level(request, pk):
  item = get_object_or_404(Stock, pk=pk)
  form = ReorderLevelForm(request.POST or None, instance=item)
  if form.is_valid():
    instance = form.save(commit=False)
    instance.save()
    messages.success(request, f'Reorder level for {instance.item_name} is updated to {instance.reorder_level}')
    return redirect('list-items')
  context = {
    'form': form,
    'instance': item
  }
  return render(request, 'stockmgt/add_items.html', context)


@login_required
def list_history(request):
  queryset = StockHistory.objects.all()
  form = StockHistorySearchForm(request.POST or None)
  context = {
    'title': 'Stock Management System | History Data',
    'queryset': queryset,
    'form': form
  }
  
  if request.method == 'POST':
    category = form['category'].value()
    start_date = form['start_date'].value()
    end_date = form['end_date'].value()

    try:
      queryset = StockHistory.objects.filter(item_name__icontains=form['item_name'].value(), last_updated__range=[start_date, end_date])
    except:
      pass

    if category != '':
      queryset = queryset.filter(category_id=category)
      if form['export_to_csv'].value() == True:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
        writer = csv.writer(response)
        writer.writerow([
          'CATEGORY',
          'ITEM NAME',
          'QUANTITY',
          'ISSUE QUANTITY',
          'RECEIVE QUANTITY',
          'RECEIVE BY',
          'ISSUE BY',
          'ISSUE TO',
          'LAST UPDATED'
        ])
        instance = queryset
        for stock in instance:
          writer.writerow([
            stock.category,
            stock.item_name,
            stock.quantity,
            stock.issue_quantity,
            stock.receive_quantity,
            stock.receive_by,
            stock.issue_by,
            stock.issue_to,
            stock.last_updated,
          ])
        return response
    context = {
      'form': form,
      'queryset': queryset,
      'title': 'Stock Management System | History Data',
    }
  return render(request, 'stockmgt/list_history.html', context)