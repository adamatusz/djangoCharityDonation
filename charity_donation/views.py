from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .forms import SignUpForm

# Create your views here.
from django.views import View

from charity_donation.models import Institution, Donation


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
        return render(request, "login.html", {})


class RegisterView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, "register.html", {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()


            messages.success(
                request, 'Konto zostało pomyślnie utworzone'
            )
            return redirect('login')

        return render(request, 'register.html', context={'form': form})
