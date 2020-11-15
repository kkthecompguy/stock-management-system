from django import forms
from .models import Stock, StockHistory


class StockCreateForm(forms.ModelForm):
  date = forms.CharField(widget=forms.DateInput(attrs={'type': 'date'}))
  class Meta:
    model = Stock
    fields = ['category', 'item_name', 'quantity', 'date']

  def clean_category(self):
    category = self.cleaned_data.get('category')
    if not category:
      raise forms.ValidationError('This field is required')
    return category

  def clean_item_name(self):
    item_name = self.cleaned_data.get('item_name')
    if not item_name:
      raise forms.ValidationError('This field is required')

    for instance in Stock.objects.all():
      if instance.item_name == item_name:
        raise forms.ValidationError(f'{item_name} is already created')
    return item_name


class StockSearchForm(forms.ModelForm):
  export_to_csv = forms.BooleanField(required=False)
  class Meta:
    model = Stock
    fields = ['category', 'item_name']


class StockHistorySearchForm(forms.ModelForm):
  export_to_csv = forms.BooleanField(required=False)
  start_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'date'}))
  end_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'date'}))
  class Meta:
    model = StockHistory 
    fields = ['category', 'item_name', 'start_date', 'end_date', 'export_to_csv']


class StockUpdateForm(forms.ModelForm):
  class Meta:
    model = Stock
    fields = ['category', 'item_name', 'quantity']


class IssueForm(forms.ModelForm):
  class Meta:
    model = Stock
    fields = ['issue_quantity', 'issue_to']


class ReceiveForm(forms.ModelForm):
  class Meta:
    model = Stock
    fields = ['receive_quantity']


class ReorderLevelForm(forms.ModelForm):
  class Meta:
    model = Stock
    fields = ['reorder_level']