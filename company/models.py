from django.db import models
from account.models import User

# Create your models here.
class Company(models.Model):
    user = models.OneToOneField(User, related_name='company', blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    image = models.ImageField(upload_to='company/', blank=True, null=True)
    inn = models.CharField(max_length=25, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


class CompanyAddress(models.Model):
    company = models.ForeignKey(Company, related_name='address', on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    email = models.EmailField(blank=True, null=True)
    tel1 = models.CharField(max_length=13)
    tel2 = models.CharField(max_length=13)
    map_url = models.URLField()
    main_add = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company.title}"



