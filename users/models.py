from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager

# Create your models here.

class User(AbstractUser):
    Admin = 1
    Candidate = 2

    ROLE_CHOICES = (
        (Admin, 'Admin'),
        (Candidate, 'Candidate')
    )
    
    Male = 1
    Female = 2

    GENDER = (
        (Male, 'Male'),
        (Female, 'Female'),
    )

    email = models.EmailField(('email_address'), unique=True, max_length=200)
    password = models.CharField(max_length=100, blank=False)
    first_name = models.CharField(max_length=100, blank=False)
    last_name  = models.CharField(max_length=100)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=3)
    gender = models.PositiveSmallIntegerField(
        choices=GENDER, blank=True, null=True
    )
    dob = models.DateField(null=True, blank=True)
    mobile_no = PhoneNumberField(unique=True, null=True, blank=True)
    address = models.CharField(max_length=100)

    # Required fields for Django's AbstractUser
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    # Custom User manager
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)
