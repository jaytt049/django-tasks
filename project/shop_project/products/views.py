from django.http import HttpResponse
from django.db.models import (
    Q,
    F,
    Count,
    Avg,
    Sum
)
from django.db import transaction

from .models import *


# ------------------------------------------------
# FILTER
# ------------------------------------------------
def active_products(request):

    products = Product.objects.filter(
        is_active=True
    )

    return HttpResponse(products)


# ------------------------------------------------
# FILTER + RANGE + ORDER BY
# ------------------------------------------------
def price_range_products(request):

    products = Product.objects.filter(
        is_active=True,
        price__range=(100, 1000)
    ).order_by('price')

    return HttpResponse(products)


# ------------------------------------------------
# EXCLUDE
# ------------------------------------------------
def exclude_products(request):

    products = Product.objects.exclude(
        is_active=False
    )

    return HttpResponse(products)


# ------------------------------------------------
# Q OBJECTS
# ------------------------------------------------
def q_objects_demo(request):

    products = Product.objects.filter(
        Q(price__lt=500) |
        Q(stock__gt=200)
    )

    return HttpResponse(products)


# ------------------------------------------------
# F EXPRESSION
# ------------------------------------------------
def decrement_stock(request, pk):

    Product.objects.filter(
        pk=pk
    ).update(
        stock=F('stock') - 3
    )

    return HttpResponse("Stock Updated")


# ------------------------------------------------
# AGGREGATE
# ------------------------------------------------
def aggregate_demo(request):

    result = Product.objects.aggregate(
        total_products=Count('id'),
        avg_price=Avg('price'),
        total_stock=Sum('stock')
    )

    return HttpResponse(str(result))


# ------------------------------------------------
# ANNOTATE
# ------------------------------------------------
def annotate_demo(request):

    categories = Category.objects.annotate(
        product_count=Count('products')
    )

    output = []

    for category in categories:

        output.append(
            f"{category.name} : {category.product_count}"
        )

    return HttpResponse("<br>".join(output))


# ------------------------------------------------
# CUSTOM MANAGER
# ------------------------------------------------
def active_manager_demo(request):

    products = Product.active.in_stock()

    return HttpResponse(products)


# ------------------------------------------------
# TRANSACTION HANDLING
# ------------------------------------------------
def place_order(request, product_id):

    qty = 2

    with transaction.atomic():

        product = Product.objects.select_for_update().get(
            pk=product_id
        )

        if product.stock < qty:
            return HttpResponse(
                "Insufficient Stock"
            )

        Product.objects.filter(
            pk=product_id
        ).update(
            stock=F('stock') - qty
        )

        order = Order.objects.create(
            product=product,
            quantity=qty,
            total=product.price * qty
        )

        transaction.on_commit(
            lambda: print(
                f"Order {order.id} Created"
            )
        )

    return HttpResponse(
        "Order Placed Successfully"
    )


# ------------------------------------------------
# SELECT RELATED
# ------------------------------------------------
def select_related_demo(request):

    products = Product.objects.select_related(
        'category'
    )

    output = []

    for product in products:

        output.append(
            f"{product.name} - {product.category.name}"
        )

    return HttpResponse("<br>".join(output))


# ------------------------------------------------
# PREFETCH RELATED
# ------------------------------------------------
def prefetch_related_demo(request):

    products = Product.objects.prefetch_related(
        'tags'
    )

    output = []

    for product in products:

        tags = ", ".join(
            [
                tag.name
                for tag in product.tags.all()
            ]
        )

        output.append(
            f"{product.name} -> {tags}"
        )

    return HttpResponse("<br>".join(output))