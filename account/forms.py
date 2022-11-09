from django import forms
from django.forms import ValidationError
from .models import User, Profile


class UserLogForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError("Parollar mos emas")
        return cd['password2']
    

class UserUpdateForm(forms.ModelForm):
     class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class PassUpdateForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise ValidationError("Parollar mos emas")
        return cd['password2']


class PassResetForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError("Parollar mos emas")
        return cd['password2']


class ProfileRegisterForm(forms.ModelForm):
    model = Profile
    fields = ('terms',)


class ProfileUpdateForm(forms.ModelForm):
    model = Profile
    fields = ('image', 'date_of_birth', 'tel', 'city', 'district', 'address', 'postal_code')



