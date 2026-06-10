from django.urls import path
from .views import *

urlpatterns = [

    path(
        'active-products/',
        active_products
    ),

    path(
        'price-range/',
        price_range_products
    ),

    path(
        'exclude-products/',
        exclude_products
    ),

    path(
        'q-objects/',
        q_objects_demo
    ),

    path(
        'decrement-stock/<int:pk>/',
        decrement_stock
    ),

    path(
        'aggregate/',
        aggregate_demo
    ),

    path(
        'annotate/',
        annotate_demo
    ),

    path(
        'custom-manager/',
        active_manager_demo
    ),

    path(
        'place-order/<int:product_id>/',
        place_order
    ),

    path(
        'select-related/',
        select_related_demo
    ),

    path(
        'prefetch-related/',
        prefetch_related_demo
    ),
]