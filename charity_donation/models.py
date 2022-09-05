from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class TypeChoice(models.IntegerChoices):
    Foundation = 1
    NGO = 2
    Local = 3
    __empty__ = 'Fundation'


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)


class Institution(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField()
    type = models.IntegerField(choices=TypeChoice.choices, default='Foundation', null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category, blank=True)
    institution = models.ForeignKey(Institution,
                                    on_delete=models.CASCADE,
                                    null=True)
    address = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=16, verbose_name='numer telefonu')
    city = models.CharField(max_length=128, verbose_name='miasto')
    zip_code = models.CharField(max_length=6, verbose_name='kod pocztowy')
    pick_up_date = models.DateField(auto_now_add=True, verbose_name='data odbioru')
    pick_up_time = models.DateTimeField(auto_now_add=True, verbose_name='godzina odbioru')
    pick_up_comment = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
