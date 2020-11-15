from django.urls import path
from .views import index, list_items, add_items, update_items, delete_items, stock_detail, issue_items, receive_items, reorder_level, list_history

urlpatterns = [
  path('', index, name='index'),
  path('list_items', list_items, name='list-items'),
  path('add_items/', add_items, name='add-items'),
  path('update_items/<str:pk>/', update_items, name='update-items'),
  path('delete_items/<str:pk>/', delete_items, name='delete-items'),
  path('stock_detail/<str:pk>/', stock_detail, name='stock-detail'),
  path('issue_items/<str:pk>/', issue_items, name='issue-items'),
  path('receive_items/<str:pk>/', receive_items, name='receive-items'),
  path('reorder_level/<str:pk>/', reorder_level, name='reorder-level'),
  path('list_history', list_history, name='list-history'),
]