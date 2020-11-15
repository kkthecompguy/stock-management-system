from django.db import models

# Create your models here.

CATEGORY_CHOICES = (
  ('IT Equipment', 'IT Equipment'),
  ('Networking', 'Networking'),
  ('Electronics', 'Electronnics'),
  ('Phone', 'Phone'),
  ('Furniture', 'Furniture'),
)

class Category(models.Model):
  name = models.CharField(max_length=50, blank=True, null=True)

  def __str__(self):
    return self.name


class Stock(models.Model):
  category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
  item_name = models.CharField(max_length=50, blank=True)
  quantity = models.IntegerField(default=0)
  receive_quantity = models.IntegerField(default=0)
  receive_by = models.CharField(max_length=50, null=True, blank=True)
  issue_quantity = models.IntegerField(default=0)
  issue_by = models.CharField(max_length=50, null=True, blank=True)
  issue_to = models.CharField(max_length=50, null=True, blank=True)
  phone_number = models.CharField(max_length=10, null=True, blank=True)
  created_by = models.CharField(max_length=50, null=True, blank=True)
  reorder_level = models.IntegerField(default=0)
  export_to_csv = models.BooleanField(default=False)
  date = models.DateTimeField()
  last_updated = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.item_name


class StockHistory(models.Model):
  category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
  item_name = models.CharField(max_length=50, blank=True, null=True)
  quantity = models.IntegerField(default=0, null=True)
  receive_quantity = models.IntegerField(default=0, null=True)
  receive_by = models.CharField(max_length=50, null=True, blank=True)
  issue_quantity = models.IntegerField(default=0, null=True)
  issue_by = models.CharField(max_length=50, null=True, blank=True)
  issue_to = models.CharField(max_length=50, null=True, blank=True)
  phone_number = models.CharField(max_length=10, null=True, blank=True)
  created_by = models.CharField(max_length=50, null=True, blank=True)
  reorder_level = models.IntegerField(default=0, null=True)
  export_to_csv = models.BooleanField(default=False, null=True)
  date = models.DateTimeField(null=True, blank=True)
  last_updated = models.DateTimeField(auto_now=False, null=True)
  created_at = models.DateTimeField(auto_now_add=False, null=True)

  def __str__(self):
    return self.item_name
