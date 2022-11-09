from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib import messages
from .models import *
from .forms import *

# category
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kategoriya muvaffaqiyatli yaratildi!")
            return HttpResponse("Categoriya muvaffaqiyatli yaratildi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'product/foradmin/category_create.html', context)


def category_update(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == "POST":
        form = CategoryForm(instance=category, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kategoriya muvaffaqiyatli yangilandi")
            return HttpResponse("Kategoriya muvaffaqiyatli yangilandi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
    }
    return render(request, 'product/foradmin/category_update.html', context)


def category_delete(request, slug):
    category = get_object_or_404(Category, slug=slug)
    category.delete()
    return redirect('category_list')
# end Category
# Brand
def brand_create(request):
    if request.method == "POST":
        form = BrandForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            brand = form.save(commit=False)
            brand.user = request.user
            brand.company = request.user.profile__company
            brand.save()
            messages.success(request, "Brand muvaffaqiyatli yaratildi!")
            return HttpResponse("Brand muvaffaqiyatli yaratildi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = BrandForm()
    context = {
        'form': form,
    }
    return render(request, 'product/forall/brand_create.html', context)


def brand_update(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    if request.user.is_staff or brand.company == request.user.profile__company:
        if request.method == "POST":
            form = BrandForm(instance=brand, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Brand muvaffaqiyatli yangilandi")
                return HttpResponse("Brand muvaffaqiyatli yangilandi!")
            else:
                messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
        else:
            form = BrandForm(instance=brand)
        context = {
            'form': form,
        }
        return render(request, 'product/forall/brand_update.html', context)
    else:
        messages.error(request, "Siz bu brand ni o'zgartira olmaysiz!")
        return redirect("account:dashboard")

def brand_delete(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    brand.delete()
    return redirect('brand_list')
# end brand
# product
def product_create(request):
    if request.method == "POST":
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.company = request.user.profile__company
            product.save()
            messages.success(request, "Product muvaffaqiyatli yaratildi!")
            return HttpResponse("Product muvaffaqiyatli yaratildi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = ProductForm()
    context = {
        'form': form,
    }
    return render(request, 'product/forall/product_create.html', context)


def product_update(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_staff or product.company == request.user.profile__company:
        if request.method == "POST":
            # if product.company == user.company or request.user.is_staff:
            form = ProductForm(instance=product, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Product muvaffaqiyatli yangilandi")
                return HttpResponse("Product muvaffaqiyatli yangilandi!")
            else:
                messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
        else:
            form = ProductForm(instance=product)
        context = {
            'form': form,
        }
        return render(request, 'product/forall/product_update.html', context)
    else:
        messages.error(request, "Siz bu product ni o'zgartira olmaysiz!")
        return redirect("account:dashboard")


def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product.delete()
    return redirect('product_list')
# end product
# Standarts
def standart_create(request):
    if request.method == "POST":
        form = StandartsForm(request.POST)
        if form.is_valid():
            standart = form.save(commit=False)
            standart.author = request.user
            standart.save()
            messages.success(request, "Standarts muvaffaqiyatli yaratildi!")
            return HttpResponse("Standarts muvaffaqiyatli yaratildi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = StandartsForm()
    context = {
        'form': form,
    }
    return render(request, 'product/foradmin/standart_create.html', context)


def standart_update(request, slug):
    standart = get_object_or_404(Standarts, slug=slug)
    if request.method == "POST":
        form = StandartsForm(instance=standart, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Standarts muvaffaqiyatli yangilandi")
            return HttpResponse("Standarts muvaffaqiyatli yangilandi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = StandartsForm(instance=standart)
    context = {
        'form': form,
    }
    return render(request, 'product/foradmin/category_update.html', context)


def standart_delete(request, slug):
    standart = get_object_or_404(Standarts, slug=slug)
    standart.delete()
    return redirect('standart_list')
# end Standarts
# ProductSize
def procuctSize_create(request):
    if request.method == "POST":
        form = ProductSizeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product o'lchami muvaffaqiyatli yaratildi!")
            return HttpResponse("Product o'lchami muvaffaqiyatli yaratildi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = ProductSizeForm()
    context = {
        'form': form,
    }
    return render(request, 'product/foradmin/size_create.html', context)


def procuctSize_update(request, slug):
    size = get_object_or_404(ProductSize, slug=slug)
    if request.method == "POST":
        form = ProductSizeForm(instance=size, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product o'lchami muvaffaqiyatli yangilandi")
            return HttpResponse("Product o'lchami muvaffaqiyatli yangilandi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = ProductSizeForm(instance=size)
    context = {
        'form': form,
    }
    return render(request, 'product/foradmin/size_update.html', context)


def procuctSize_delete(request, slug):
    size = get_object_or_404(ProductSize, slug=slug)
    size.delete()
    return redirect('size_list')
# end ProductSize
# ProductColor
def procuctColor_create(request):
    if request.method == "POST":
        form = ProductColorForm(request.POST)
        if form.is_valid():
            color = form.save(commit=False)
            color.author = request.user
            color.save()
            messages.success(request, "Product rangi muvaffaqiyatli yaratildi!")
            return HttpResponse("Product rangi muvaffaqiyatli yaratildi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = ProductColorForm()
    context = {
        'form': form,
    }
    return render(request, 'product/foradmin/color_create.html', context)


def procuctColor_update(request, slug):
    color = get_object_or_404(ProductColor, slug=slug)
    if request.method == "POST":
        form = ProductColorForm(instance=color, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product rangi muvaffaqiyatli yangilandi")
            return HttpResponse("Product rangi muvaffaqiyatli yangilandi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = ProductColorForm(instance=color)
    context = {
        'form': form,
    }
    return render(request, 'product/foradmin/color_update.html', context)


def procuctColor_delete(request, slug):
    color = get_object_or_404(ProductColor, slug=slug)
    color.delete()
    return redirect('color_list')
# end Standarts

# ProductItem and ProductImage
def product_item_create(request, slug):
    if request.method == "POST":
        item_form = ProductItemForm(request.POST)
        image_form = ProductImageForm(data=request.POST, files=request.FILES)
        if item_form.is_valid() and image_form.is_valid():
            product = get_object_or_404(Product, slug=slug)
            item = item_form.save(commit=False)
            item.user = request.user
            item.product = product
            item.save()
            images = request.POST.getlist('image_original')
            for img in images:
                ProductImage.objects.create(
                    product_item=item, image_original=img, image_detail=img, 
                    image_big=img, image_middle=img, image_presmall=img, 
                    image_small=img, image_for_cart=img
                )
            messages.success(request, "Produktni itemlari muvaffaqiyatli yaratildi!")
            return HttpResponse("Produktni itemlari muvaffaqiyatli yaratildi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        item_form = ProductItemForm()
        image_form = ProductImageForm()
    context = {
        'item_form': item_form,
        'image_form': image_form,
    }
    return render(request, 'product/foraall/item_create.html', context)


def product_item_update(request, id):
    item = get_object_or_404(ProductItem, id=id)
    if request.method == "POST":
        item_form = ProductItemForm(instance=item, data=request.POST)
        image_form = ProductImageForm(data=request.POST, files=request.FILES)
        if item_form.is_valid() and image_form.is_valid():
            item_form.save()
            images = request.POST.getlist('image_original')
            if images:
                ProductImage.objects.filter(product_item=item).delete()
                for img in images:
                    ProductImage.objects.create(
                    product_item=item, image_original=img, image_detail=img, 
                    image_big=img, image_middle=img, image_presmall=img, 
                    image_small=img, image_for_cart=img
                )
            messages.success(request, "Produktni itemlari muvaffaqiyatli yangilandi")
            return HttpResponse("Produktni itemlari muvaffaqiyatli yangilandi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        item_form = ProductItemForm(instance=item)
        image_form =ProductImageForm()
        product_images = ProductImage.objects.filter(product_item=item)
    context = {
        'item_form': item_form,
        'image_form': image_form,
        'product_images': product_images,
    }
    return render(request, 'product/foradmin/color_update.html', context)


def product_item_pre_delete(request, id):
    item = get_object_or_404(ProductItem, id=id)
    item.delete = True
    item.save()
    return redirect('product_list')


def procuct_item_delete(request, id):
    item = get_object_or_404(ProductItem, id=id)
    ProductImage.objects.filter(product_item=item).delete()
    item.delete()
    return redirect('product_list')
# end ProductItem and ProductImage
# ProductRating
def product_rating(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        form = ProductRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.product = product
            rating.user = request.user
            rating.save()
            messages.success(request, "Product rating muvaffaqiyatli yaratildi!")
            return HttpResponse("Product rating muvaffaqiyatli yaratildi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = ProductRatingForm()
    context = {
        'form': form,
    }
    return render(request, 'product/foradmin/color_create.html', context)
# end ProductRating
# ProductComment
def productColor_create(request, slug, id=None):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        form = ProductCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            if id:
                prod_comment = get_object_or_404(ProductComment, pk=id)
                comment.parent = prod_comment
            comment.save()
            messages.success(request, "Product kommentariyasi muvaffaqiyatli yaratildi!")
            return HttpResponse("Product kommentariyasi muvaffaqiyatli yaratildi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = ProductCommentForm()
    context = {
        'form': form,
    }
    return render(request, 'product/foradmin/color_create.html', context)


def product_comment_update(request, id):
    comment = get_object_or_404(ProductComment, pk=id)
    if request.method == "POST":
        form = ProductCommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product kommentariyasi muvaffaqiyatli yangilandi")
            return HttpResponse("Product kommentariyasi muvaffaqiyatli yangilandi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = ProductCommentForm(instance=comment)
    context = {
        'form': form,
    }
    return render(request, 'product/foradmin/color_update.html', context)


def procuct_comment_delete(request, slug):
    comment = get_object_or_404(ProductComment, id=id)
    comment.delete()
    return redirect('color_list')
# end ProductComment

# We should remake it
# ProductDiscount
def prod_discount_create(request, slug, id=None):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        form = ProductCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            if id:
                prod_comment = get_object_or_404(ProductComment, pk=id)
                comment.parent = prod_comment
            comment.save()
            messages.success(request, "Product kommentariyasi muvaffaqiyatli yaratildi!")
            return HttpResponse("Product kommentariyasi muvaffaqiyatli yaratildi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = ProductCommentForm()
    context = {
        'form': form,
    }
    return render(request, 'product/foradmin/color_create.html', context)


def procuct_comment_update(request, id):
    comment = get_object_or_404(ProductComment, pk=id)
    if request.method == "POST":
        form = ProductCommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product kommentariyasi muvaffaqiyatli yangilandi")
            return HttpResponse("Product kommentariyasi muvaffaqiyatli yangilandi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = ProductCommentForm(instance=comment)
    context = {
        'form': form,
    }
    return render(request, 'product/foradmin/color_update.html', context)


def product_comment_delete(request, slug):
    comment = get_object_or_404(ProductComment, id=id)
    comment.delete()
    return redirect('color_list')
# end ProductComment
