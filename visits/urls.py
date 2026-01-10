from django.urls import path
from . import views

urlpatterns = [
    path('unresolved_cases/', views.unresolved_cases, name='unresolved_cases'),# ← 追加！
    path('customer_detail/<int:customer_id>/', views.customer_detail, name='customer_detail'),# ← 追加！
    path('visit_record/<int:customer_id>/', views.visit_record, name='visit_record'),# ← 追加！
]