from django.urls import path
from . import views

urlpatterns = [
    path('unresolved_cases/', views.unresolved_cases, name='unresolved_cases'),
    path('customer_detail/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('visit_record/<int:customer_id>/', views.visit_record, name='visit_record'),
    path("customer/<int:customer_id>/delete/", views.customer_delete, name="customer_delete"),
    path('map/', views.customer_map, name='customer_map'),
]