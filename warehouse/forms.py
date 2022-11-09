from django import forms
from django.forms import ClearableFileInput
from .models import *


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title', 'place', 'parent_id')


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('title', 'image')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'category', 'brand', 'model', 'summary', 'description', 'archive')


class StandartsForm(forms.ModelForm):
    class Meta:
        model = Standarts
        fields = ('title',)


class ProductSizeForm(forms.ModelForm):
    class Meta:
        model = ProductSize
        fields = ('title',)


class ProductColorForm(forms.ModelForm):
    class Meta:
        model = ProductColor
        fields = ('title', 'image')

    
class ProductItemForm(forms.ModelForm):
    class Meta:
        model = ProductItem
        fields = ('price', 'size', 'color', 'count_in_stock', 'active')


class ProductImageForm(forms.ModelForm):
    image_original = forms.ImageField(widget=ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = ProductImage
        fields = ('image_original',)


class ProductRatingForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = ('rating',)


class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ('body',)


class ProductDiscountForCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductDiscount
        fields = ('category', 'discount', 'start_time', 'end_time')


class ProductDiscountForm(forms.ModelForm):
    class Meta:
        model = ProductDiscount
        fields = ('discount', 'start_time', 'end_time')

