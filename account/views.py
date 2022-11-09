from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import User, Profile
from .forms import *
# email
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
# token
from .tokens import activation_token


# Create your views here. Registration
def user_register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            cd = user_form.cleaned_data
            try: 
                user = User.objects.filter(Q(username=cd['username']) | Q(email=cd['email']))[:1].get()
            except:
                user = None
            if user is not None:
                if not user.is_active:
                    activateEmail(request, user, user.email)
                else:
                    if user.username == cd['username']:
                        messages.error(request, "Bunday username mavjud. Boshqa username tanlashingizni so'raymiz/")
                    elif user.email == cd['email']:
                        messages.error(request, "Bunday email mavjud. Boshqa emaildan foydalanishingiz yoki email orqali parolingizni tiklashingiz mumkin!")
                    return redirect('accoun:register')
            else:
                new_user = user_form.save(commit=False)
                new_user.set_password(cd['password'])
                new_user.is_active = False
                new_user.save()
                profile = profile_form.save(commit=False)
                profile.user = new_user
                profile.save()
                activateEmail(request, new_user, cd['email'])
                return redirect('shop:index')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileRegisterForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'account/registrations/registration.html', context)

# account activation and password reset confirmation email
def activateEmail(request, user, to_email, pass_reset=None):
    if not pass_reset:
        mail_subject = 'Akkountingizni aktivlashtiring!'
        template = 'account/registrations/template_activate_account.html'
    else:
        mail_subject = "Parolingizni qayta tiklang!"
        template = 'account/registrations/template_reset_password.html'
    message = render_to_string(template, {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"Akkatuntingiz muvaffaqiyatli yaratildi. {user} akkauntini aktivlashtirish uchun \
                            {to_email} pochtangizni yuborilgan link ustiga bosing va ro'yxatdan o'tishni yakunlang! <b>Muhim</b> Spam katalogini tekshiring!"
        )
    else:
        messages.error(request, f"{to_email} pochtaga xabar yuborishda xatolik. To'g'ri elektron manzil kiritilganini tekshiring!")


def user_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except:
        user = None
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Emailni tasdiqlash muvaffaqiyatli amalga oshirildi. Akkountingizga kirishingiz mumkin.")
        return redirect('account:login')
    else:
        messages.error(request, "Tasdiqlash linki muddati o'tgan, Boshqattan ro'yxatdan o'tishingizni so'raymiz!")
    return redirect("account:register")
# end account activation and password reset confirmation email

# password reset 
def password_reset_start(request):
    if request.method == 'POST':
        form = request.POST.get('email')
        user = User.objects.get(email=form)
        if user and form:
            activateEmail(request, user, form, pass_reset=True)
            messages.success(request, "Parolni tiklash uchun lik elektron pochtangizga yuborildi.")
            return redirect("shop:index")
        else:
            messages.error(request, "Kiritilgan emailga bog'liq akkount topilmadi. Tekshirib qaytadan urinib ko'ring!")
    return render(request, "account/registrations/password_reset_email.html")


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except:
        user = None
    if user and activation_token.check_token(user, token):
        form = PassResetForm()
        messages.success(request, "Emailni tasdiqlash muvaffaqiyatli amalga oshirildi parolingizni almashtirishingiz mumkin!")
        return render(request, "account/registrations/password_reset_confirmed.html", {'form': form, 'id': user.id})
    else:
        messages.error(request, "Tasdiqlash linki muddati o'tgan. Boshqattan so'rov yuborishingiz mumkin.")
    return redirect("account:login")

# is not validni so'ra!!!!!!!!!!!
def password_reset(request, uid64):
    if request.method == 'POST':
        form = PassResetForm(request.POST)
        if form.is_valid():
            uid = force_str(urlsafe_base64_decode(uid64))
            try:
                user = User.objects.get(id=uid)
            except:
                user = None
            if user:
                user.set_password(form.cleaned_data['password'])
                user.save()
                messages.success(request, "Parolingiz muvaffaqiyatli almashtirildi. Akkountingizga kirishingiz mumkin!")
                return redirect("account:login")
            else:
                messages.error(request, "Xatolik mavjud. Birozdan so'ng qaytadan urinib ko'ring!")
                return redirect("shop:index")
    else:
        messages.error(request, "Xatolik mavjud. Birozdan so'ng qaytadan urinib ko'ring!")
        return redirect("shop:index")
# end password reset 

# login
def user_login(request):
    if request.method == "POST":
        form = UserLogForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    if user.is_staff:
                        return redirect('shop:index')
                    elif user.status == 'client':
                        return redirect("account:dashboard")
                    elif user.status == 'in_company':
                        return redirect("account:seller_dashboard")
                    elif user.status == 'company':
                        return redirect("account:company_dashboard")
                    elif user.status == 'manager':
                        return redirect("account:manager_dashboard")
                    elif user.status == 'analytic':
                        return redirect("account:analytic_dashboard")
                    elif user.status == 'director':
                        return redirect("account:director_dashboard")
                        
                else:
                    if not user.last_login:
                        messages.error(request, "Akkauntiniz aktivlashtirilmagan. Aktivlashtirish linki elektron pochtangizga yuborilgan."\
                            "Agar aktivlashtirish linki muddati o'tgan bo'lsa registratsiya bo'limidagi aktivlashtirish ni ustiga bosing!"
                        )
                    else:
                        messages.error(request, "Akkountingiz adminstratsiya tomonidan bloklangan. Support bilan bog'laning!")
            else:
                messages.error(request, "Bunday akkount mavjud emas. Login va parolingizni tekshirib qaytadan urinib ko'ring!")
        else:
            messages.error(request, "Login yoki parol to'ldirilishida xatolik mavjud. Tekshirib qaytadan urinib ko'ring")
    else:
        form = UserLogForm()
    return render(request, 'account/registrations/login.html', {'form':form})
# end login

# logout
def user_logout(request):
    logout(request)
    return redirect('shop:index')
# endlogout

# update user details
def user_update(request):
    pass_form = PassUpdateForm()
    if request.method == "POST":
        user_form = UserUpdateForm(instance=request.user, data=request.POST)
        profile_form = ProfileUpdateForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Ma'lumotlar muvaffaqiyatli o'zgartirildi.")
            return redirect('account/details')
        else:
            messages.error(request, "Ma'lumotlar to'ldirilishida xatolik mavjud.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'pass_form': pass_form,
    }
    return render(request, 'account/update.html', context)
# update user details

# password update
def password_update(request):
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)
    if request.method == "POST":
        pass_form = PassUpdateForm(request.POST)
        if  pass_form.is_valid():
            user = User.objects.get(id=request.user.id)
            if user.check_password(pass_form.cleaned_data['password']):
                user.set_password(pass_form.cleaned_data['password1'])
                user.save()
                messages.success(request, "Parol muvaffaqiyatli almashtirildi.")
                return redirect('account:details')
            else:
                messages.error(request, "Joriy parol xato!")
        else:
            messages.error(request, "Formani to'ldirishda xatolik mavjud.")
    else:
        pass_form = PassUpdateForm()
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'pass_form': pass_form,
    }
    return render(request, 'account/update.html', context)
# end password update
