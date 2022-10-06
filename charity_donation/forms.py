from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
# from .models import User

User = get_user_model()


class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                                                      'placeholder': 'Imię'}))
    # last_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                                                     'placeholder': 'Nazwisko'
    #                                                                                     }))
    # username = forms.EmailField(empty_value=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Adres Email'
        self.fields['email'].label = ''
        # self.fields['email'].help_text = (
        #     '<small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small>')

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Imię'
        self.fields['first_name'].label = ''

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Nazwisko'
        self.fields['last_name'].label = ''

        self.fields['password1'].widget.attrs['placeholder'] = 'Hasło'
        self.fields['password1'].label = ''
        self.fields[
            'password1'].help_text = '<li>Twoje hasło nie może być zbyt podobne do innych Twoich danych osobowych.</li><li>Twoje hasło musi zawierać co najmniej 8 znaków.</li><li>Twoje hasło nie może być powszechnie używanym hasłem.</li><li>Twoje hasło nie może być całkowicie numeryczne.</li>'

        self.fields['password2'].widget.attrs['placeholder'] = 'Powtórz Hasło'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<li>W celu weryfikacji wpisz hasło ponownie.</li>'


class LoginForm(forms.ModelForm):
    # email = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    # password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))

    # username = forms.EmailField(empty_value=False)

    class Meta:
        model = User
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Adres Email'
        self.fields['email'].label = ''

        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Hasło'
        self.fields['password'].label = ""


