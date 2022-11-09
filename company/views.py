from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages
import uuid
from .models import Company, CompanyAddress
from account.models import User
from .forms import CompanyForm, CompanyAddressForm
# Create your views here.

@login_required
def company_create(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user_id)
            company = form.save(commit=False)
            company.user = user
            company.slug = slugify(uuid.uuid4())
            company.save()
            messages.success(request, "Kompaniya muvaffaqiyatli yaratildi, Kompaniya manzili"\
                "va qo'shimcha ma'lumotlarini kiritishingizni so'raymiz"            
            )
            return redirect(f"company:address_create {company.slug}")
        else:
            messages.error(request, "Ma'lumotlarni to'ldirishda xatolik mavjud!")
    else:
        company_count = Company.objects.filter(user=request.user).count()
        if company_count != 1 and request.user.status == 'company':
            messages.error(request, "1 ta akkountdan 1 ta kompaniya yaratish uchun foydalanish mumkin!")
            return redirect(f"company:update {request.user.company_slug}")
        elif request.user.status != 'company':
            return redirect('shop:bad_request')
        else:
            form = CompanyForm()
    return render(request, "company.create.html", {"form": form})


@login_required
def company_update(request, slug):
    company = Company.objects.filter(slug=slug)
    if request.method == "POST":
        form = CompanyForm(instance=company, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Ma'lumotlar muvaffaqiyatli yangilandi.")
            return redirect(f'company:details {company.id}')
        else:
            messages.error(request, "Ma'lumotlar kiritishda xatolik mavjud!")
    else:
        form = CompanyForm(instance=company)
    return render(request, "company/update.html", {'form': form})


# @login_required
# def company_update(request):
#     company = Company.objects.filter(user=request.user).get()
#     company.delete()


@login_required
def company_address_create(request, slug):
    company = Company.objects.get(slug=slug)
    if request.method == "POST":
        form = CompanyAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.company = company
            if company.address.count() == 0:
                address.main_add = True
            address.save()
            messages.success(request, "Kompaniya manzili muvaffaqiyatli kiritildi."            
            )
            return redirect(f"company:detail")
        else:
            messages.error(request, "Ma'lumotlarni to'ldirishda xatolik mavjud!")
    else:
        form = CompanyAddressForm(request.POST)
    return render(request, 'company/address_create.hml', {'form': form})


@login_required
def company_address_update(request, id):
    address = CompanyAddress.objects.get(id=id)
    if request.method == "POST":
        form = CompanyAddressForm(instance=address, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kompaniya manzili muvaffaqiyatli yangilandi."            
            )
            return redirect(f"company:address_create")
        else:
            messages.error(request, "Ma'lumotlarni to'ldirishda xatolik mavjud!")
    else:
        form = CompanyAddressForm(instance=address)
    return render(request, 'company/address_create.hml', {'form': form})


@login_required
def company_address_delete(request, id):
    address = CompanyAddress.objects.get(id=id)
    if address and address.company.user == request.user:
        address.delete()
    else:
        return redirect('shop:bad_request')
    return redirect("company:details")


