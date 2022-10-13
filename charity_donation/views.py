from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth import (authenticate,
                                 login,
                                 logout)
from .models import User
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .forms import (SignUpForm,
                    LoginForm)

# Create your views here.
from django.views import View

from .models import (Institution,
                     Donation)

PAGINATION_OBJECTS_PER_PAGE = 5


class LandingPageView(View):

    def first_page(self, institution_type):
        paginator = Paginator(Institution.objects.filter(type=institution_type), PAGINATION_OBJECTS_PER_PAGE)
        return paginator.page(1)

    def get(self, request):
        donated_institutions = Institution.objects.all().filter(donation__quantity__gt=0).distinct().count()
        total_donated = Donation.objects.all().count()
        # total_donated = Donation.objects.all().aggregate(Sum('quantity'))

        get_type_num_by_type_name = {value: key for key, value in Institution.TYPECHOICE}
        foundations = self.first_page(institution_type=get_type_num_by_type_name.get('Fundacja'))
        ngos = self.first_page(institution_type=get_type_num_by_type_name.get('Organizacja pozarządowa'))
        local_collections = self.first_page(institution_type=get_type_num_by_type_name.get('Zbiórka lokalna'))

        context = {
            "donated_institutions": donated_institutions,
            'total_donated': total_donated,
            'foundations': foundations,
            'ngos': ngos,
            'local_collections': local_collections
        }

        return render(request, 'index.html', context)


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html', {})


class LoginView(View):
    def get(self, request):
        form = LoginForm
        return render(request, "login.html", {'form': form})

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email,
                            password=password)
        if user and user.is_active:
            login(request, user)
            return redirect('landing-page')
        else:
            form = LoginForm
            message = f'Użytkownik o podanym adresie: {email} nie istnieje.'
            return render(request, 'register.html', context={'form': form,
                                                          "message": message})


class RegisterView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, "register.html", {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            u = form.save()
            login(request, u)

            # messages.success(
            #     request, 'Konto zostało pomyślnie utworzone'
            # )
            return redirect('login')

        return render(request, 'register.html', context={'form': form})

# def register_user(request):
#     """Register a new user."""
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             u = form.save()
#             login(request, u)
#             messages.success(request, ('You Have Registered...'))
#             return redirect('login')
#         # what if form is not valid?
#         # we should display a message in register.html
#     else:
#         form = SignUpForm()
#     return render(request, 'register.html', context={'form': form})


class UserProfile(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'user_profile.html', context={form: form})


class LogoutUser(View):
    def get(self, request):
        logout(request)
        # messages.success(request, ('You Have Been Logged Out...'))
        return redirect('landing-page')
