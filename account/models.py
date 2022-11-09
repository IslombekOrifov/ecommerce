from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_STATUS = (
        ('director', 'DIRECTOR'),
        ('manager', 'MANAGER'),
        ('analytic', 'ANALYTIC'),
        ('client', 'CLIENT'),
        ('company', 'COMPANY'),
        ('in_company', 'IN_COMPANY'),

    )
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=25, choices=USER_STATUS, default='client')
    is_deleted = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='accounts', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    tel = models.CharField(max_length=13,blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    postal_code = models.CharField(max_length=15, blank=True, null=True)
    terms = models.BooleanField(default=False)
    company = models.ForeignKey("company.Company", related_name='workers', blank=True, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"{self.user.username}"


        