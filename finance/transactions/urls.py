from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.TransactionList.as_view(), name='transaction-list'),
    path('transactions/<int:category_id>/', views.TransactionListByCategory.as_view(),
         name='transaction-list-by-category'),
    path('transactions/<int:transaction_id>/', views.TransactionDetail.as_view(), name='transaction-detail'),
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('balance/', views.BalanceView.as_view(), name='balance'),
]
