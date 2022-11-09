from django.db import models
from django.shortcuts import redirect
from django_resized import ResizedImageField
from django.utils.text import slugify
from django.urls import reverse
from account.models import User
from company.models import Company
import uuid

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=150, db_index=True)
    place = models.PositiveIntegerField()
    parent_id = models.ForeignKey('self', related_name='child', blank=True, null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('place',)

    def get_child(self):
        sub_cat = Category.objects.filter(parent_id=self.id)
        return sub_cat

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("shop:category_products", args=[self.slug])

class Brand(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True)
    image = models.ImageField(upload_to='brands/')
    user = models.ForeignKey(User, related_name='brands', blank=True, null=True, on_delete=models.SET_NULL)
    company = models.ForeignKey(Company, related_name='brands', blank=True, null=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=150, db_index=True, unique=True)
    category = models.ForeignKey(Category, related_name='products',  null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User,related_name='products', blank=True, null=True, on_delete=models.SET_NULL)
    company = models.ForeignKey(Company,related_name='products', blank=True, null=True, on_delete=models.SET_NULL)
    brand = models.ForeignKey(Brand,related_name='products', blank=True, null=True, on_delete=models.SET_NULL)
    model = models.CharField(max_length=150)
    summary = models.TextField()
    description = models.TextField()
    archive = models.BooleanField(default=False, db_index=True)
    active = models.BooleanField(default=True, db_index=True)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(uuid.uuid4())
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return self.title

    def get_items(self):
        items = ProductItem.objects.filter(product_id=self.id)
        return items
    

class Standarts(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(User, related_name='standarts', blank=True, null=True, on_delete=models.SET_NULL)
    
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('title',)
    
    def __str__(self):
        return self.title


class ProductSize(models.Model):
    title = models.CharField(max_length=10, unique=True)
    slug = models.SlugField(max_length=10, unique=True)
    standart = models.ForeignKey(Standarts, related_name='sizes', null=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('standart',)
    
    def __str__(self):
        return f"{self.standart_title} -> {self.title}"


class ProductColor(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=50, unique=True)
    image = models.ImageField(upload_to='colors/')
    author = models.ForeignKey(User, related_name='colors', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('title',)
    
    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(uuid.uuid4())
        super().save(*args, **kwargs)


class ProductItem(models.Model):
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='product_items', null=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.ForeignKey(ProductSize, related_name='product', blank=True, null=True, on_delete=models.SET_NULL)
    color = models.ForeignKey(ProductColor, related_name='product', blank=True, null=True, on_delete=models.SET_NULL)
    count_in_stock = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True, db_index=True)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('product', 'updated')
    
    def __str__(self):
        return f"{self.product.title} {self.price}"
    

class ProductImage(models.Model):
    product_item = models.ForeignKey(ProductItem, related_name='images', on_delete=models.CASCADE)
    image_original = models.ImageField(upload_to='products/')
    image_detail = ResizedImageField(size=[720, 660], crop=['middle', 'center'], quality=100, scale=1, upload_to='products/', blank=True, null=True)
    image_big = ResizedImageField(size=[564, 520], crop=['middle', 'center'], quality=100, scale=1, upload_to='products/', blank=True, null=True)
    image_middle= ResizedImageField(size=[212, 200], crop=['middle', 'center'], quality=100, scale=1, upload_to='products/', blank=True, null=True)
    image_presmall = ResizedImageField(size=[150, 140], crop=['middle', 'center'], quality=100, scale=1, upload_to='products/', blank=True, null=True)
    image_small = ResizedImageField(size=[75, 75], crop=['middle', 'center'], quality=100, scale=1, upload_to='products/', blank=True, null=True)
    image_for_cart = ResizedImageField(size=[300, 300], crop=['middle', 'center'], quality=100, scale=1, upload_to='products/', blank=True, null=True)
    
    class Meta:
        ordering = ('product_item',)
    
    def __str__(self):
        return f"{self.product_item.title}"
    

class ProductRating(models.Model):
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='ratings', blank=True, null=True, on_delete=models.SET_NULL)
    rating = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('-rating', '-updated')
    
    def __str__(self):
        return f"{self.product.title} -> {self.rating}"


class ProductComment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', blank=True, null=True, on_delete=models.SET_NULL)
    body = models.TextField()
    parent = models.ForeignKey('self', related_name='child', blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('-updated',)
    
    def __str__(self):
        return f"{self.product.title} -> {self.updated}"


class ProductDiscount(models.Model):
    product = models.ForeignKey(Product, related_name='discount', blank=True, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='discount_category', blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=150, db_index=True)
    user = models.ForeignKey(User, related_name='discount', blank=True, null=True, on_delete=models.SET_NULL)
    company = models.ForeignKey(Company, related_name='discount_category', blank=True, null=True, on_delete=models.SET_NULL)
    discount = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-end_time',)
    
    def __str__(self):
        return f"{self.product.title} -> {self.discount}"

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(uuid.uuid4())
        super().save(*args, **kwargs)


class ProductDeleted(models.Model):
    product = models.ForeignKey(Product, related_name='deletedprod', blank=True, null=True, on_delete=models.CASCADE)
    productItem = models.ForeignKey(ProductItem, related_name='deletedproditem', blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='deletedprod', blank=True, null=True, on_delete=models.SET_NULL)
    deleted_time = models.DateTimeField(auto_now_add=True)


# ads ni so'rash kerak!
