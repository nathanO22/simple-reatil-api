from . import views
from django.urls import path


urlpatterns = [
    # path('single-item/<int:item_id>/', views.ItemsEditView().as_view(), name='single-item-view'),
    path('cart/', views.CartView().as_view(), name='cart-view'),
    # path('cart-item-delete/<int:cart_id>/', views.CartEditView().as_view(), name='user-cart-edit'),
]
