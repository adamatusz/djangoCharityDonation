from django.db.models import Sum
from django.shortcuts import render

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
        return render(request, "register.html", {})
