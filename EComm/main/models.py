from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        from django.core.exceptions import ValidationError

        if not self.slug:
            self.slug = slugify(self.name)
            
        if not self.slug:
            raise ValidationError("Slug cannot be empty.")
            
        original_slug = self.slug
        queryset = Category.objects.all()
        if self.pk:
            queryset = queryset.exclude(pk=self.pk)
            
        counter = 1
        while queryset.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
            
        super().save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.5)
    rating_count = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    stock = models.IntegerField(default=10)
    specifications = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        from django.core.exceptions import ValidationError

        if not self.slug:
            self.slug = slugify(self.name)
            
        if not self.slug:
            raise ValidationError("Slug cannot be empty.")
            
        original_slug = self.slug
        queryset = Product.objects.all()
        if self.pk:
            queryset = queryset.exclude(pk=self.pk)
            
        counter = 1
        while queryset.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
            
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, default="India")
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance)

class Order(models.Model):
    STATUS_CHOICES = (
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    delivery_method = models.CharField(max_length=50, default='Standard')
    payment_method = models.CharField(max_length=50, default='Card')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Processing')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'Deleted Product'}"
