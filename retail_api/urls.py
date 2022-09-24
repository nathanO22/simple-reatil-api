from django.urls import path 
from . import views

urlpatterns = [
    path('inventories/', views.InventoryView.as_view(), name='category_list'),
    path('new/<int:inventory_id>', views.InventoryDetailView.as_view(), name='category_detail'),
]