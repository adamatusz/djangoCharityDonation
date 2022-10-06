from django.contrib.auth import (authenticate,
                                 login,
                                 logout)
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .forms import (SignUpForm,
                    LoginForm)

# Create your views here.
from django.views import View

from charity_donation.models import Institution, Donation, User


class LandingPageView(View):
    def get(self, request):
        donated_institutions = Institution.objects.all().filter(donation__quantity__gt=0).distinct().count()
        total_donated = Donation.objects.all().count()
        # total_donated = Donation.objects.all().aggregate(Sum('quantity'))

        context = {
            "donated_institutions": donated_institutions,
            'total_donated': total_donated
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


class UserProfil(View):
    def get(self, request):
        user = User.objects.get(email=request.user.email)
        bags = Donation.objects.filter(user=user).aggregate(Sum('quantity'))
        institutions = Institution.objects.filter(donation__user=user)
        foundations = institutions.filter(type=0)
        non_government_organization = institutions.filter(type=1)
        community_collection = institutions.filter(type=2)
        donations = Donation.objects.filter(user=user)
        context = {
            "donations": donations,
            "user": user,
            "bags": bags,
            "foundations": foundations,
            "non_government_organization": non_government_organization,
            "community_collection": community_collection,
        }
        return render(request, "index.html", context)

    def post(self, request):
        donation_id = request.POST.get('id')
        donation = Donation.objects.get(id=donation_id)
        donation.is_taken = True
        donation.save()
        return redirect('profile')
