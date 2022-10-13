from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager)
from django.db import models

# Create your models here.
# https://www.codingforentrepreneurs.com/blog/how-to-create-a-custom-django-user-model/

class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password=None):
        """
        made and saves a User with the given email and password.
        """
        if not first_name:
            raise ValueError('Proszę podać imię')
        if not last_name:
            raise ValueError('Proszę podać nazwisko')
        if not email:
            raise ValueError('Proszę podać email')
        if not password:
            raise ValueError('Proszę podać hasło')

        user = self.model(email=self.normalize_email(email),
                          first_name=first_name,
                          last_name=last_name)
#       change user password
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, first_name, last_name, email, password=None):
        """
        Creates and saves a staff user with the given email and password.
        """
        if not first_name:
            raise ValueError('Nie podałeś imienia')
        if not last_name:
            raise ValueError('Nie podałeś nazwiska')
        if not email:
            raise ValueError('Nie podałeś adresu email')
        if not password:
            raise ValueError('Nie podałeś hasła')

        user = self.create_user(email, first_name, last_name, password=password)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        if not first_name:
            raise ValueError('Nie podałeś imienia')
        if not last_name:
            raise ValueError('Nie podałeś nazwiska')
        if not email:
            raise ValueError('Nie podałeś adresu email')
        if not password:
            raise ValueError('Nie podałeś hasła')

        user = self.create_user(email, first_name, last_name, password=password)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
#   an admin user; non super-user
    staff = models.BooleanField(default=False)
#   a superuser
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
#   USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = ["first_name", "last_name"]  # ['first_name', 'last_name'] # python manage.py createsuperuser

    object = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.staff

    @property
    def is_admin(self):
        """Is the user an admin member?"""
        return self.admin


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)


class Institution(models.Model):
    TYPECHOICE = {
        (1, 'Fundacja'),
        (2, 'Organizacja pozarządowa'),
        (3, 'Zbiórka lokalna'),
    }

    name = models.CharField(max_length=250, unique=True)
    description = models.TextField()
    type = models.IntegerField(choices=TYPECHOICE, default=1, null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)


class Donation(models.Model):
    quantity = models.IntegerField(verbose_name='liczba worków')
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
