from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'place', 'parent_id')
    list_filter = ('title', 'place', 'parent_id')
    ordering = ('place', 'parent_id')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'image')
    list_filter = ('title',)
    ordering = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user', 'company', 'brand', 'active', 'updated', 'deleted')
    list_filter = ('created', 'updated', 'active', 'deleted', 'archive')
    ordering = ('title', 'category', 'user', 'company', 'brand', 'active', 'updated', 'deleted')
    prepopulate_fields = {'slug': ('title',)}


@admin.register(Standarts)
class StandartsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author')
    ordering = ('title','author')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'standart')
    ordering = ('title', 'standart')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'image')
    ordering = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'price', 'size', 'color', 'count_in_stock', 'active', 'updated')
    list_filter = ('created', 'updated', 'active', 'deleted')
    ordering = ('product', 'user', 'count_in_stock', 'active', 'active', 'updated', 'deleted')



@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product_item', 'image_original', 'image_big', 'image_middle', 'image_small')
    ordering = ('product_item',)


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created', 'updated')
    list_filter = ('created', 'updated')
    ordering = ('product', 'user', 'rating')


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'active', 'created', 'updated')
    list_filter = ('created', 'updated', 'active')
    ordering = ('product', 'user', 'active')


@admin.register(ProductDiscount)
class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = ('product', 'category', 'user', 'discount', 'active', 'start_time', 'end_time')
    list_filter = ('start_time', 'end_time')
    ordering = ('product', 'user', 'active', 'start_time', 'end_time')


@admin.register(ProductDeleted)
class ProductDeletedAdmin(admin.ModelAdmin):
    list_display = ('product', 'productItem', 'user', 'deleted_time')
    ordering = ('product', 'productItem', 'user')