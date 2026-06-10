from django.db import models
from django.contrib.auth.models import User


# ---------------------
# CATEGORY
# ---------------------
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


# ---------------------
# TAG
# ---------------------
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# ---------------------
# CUSTOM MANAGER
# ---------------------
class ActiveProductManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def in_stock(self):
        return self.get_queryset().filter(stock__gt=0)

    def expensive(self, amount=1000):
        return self.get_queryset().filter(price__gte=amount)


# ---------------------
# PRODUCT
# ---------------------
class Product(models.Model):
    name = models.CharField(max_length=200)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.IntegerField(default=0)

    reorder_level = models.IntegerField(default=10)

    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    tags = models.ManyToManyField(
        Tag,
        related_name='products',
        blank=True
    )

    objects = models.Manager()
    active = ActiveProductManager()

    def __str__(self):
        return self.name


# ---------------------
# ORDER
# ---------------------
class Order(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    quantity = models.PositiveIntegerField()

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    placed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


# ---------------------
# USER PROFILE
# ---------------------
class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    bio = models.TextField(blank=True)

    location = models.CharField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return self.user.username


# ---------------------
# COLLECTION
# ---------------------
class Collection(models.Model):

    name = models.CharField(max_length=100)

    products = models.ManyToManyField(
        Product,
        through='CollectionItem',
        related_name='collections'
    )

    def __str__(self):
        return self.name


# ---------------------
# THROUGH MODEL
# ---------------------
class CollectionItem(models.Model):

    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    added_at = models.DateTimeField(
        auto_now_add=True
    )

    note = models.TextField(
        blank=True
    )

    class Meta:
        unique_together = ('collection', 'product')

    def __str__(self):
        return f"{self.collection.name} - {self.product.name}"