from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                         'placeholder': 'Imię'}))
    last_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                        'placeholder': 'Nazwisko'
                                                                                        }))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'Adres Email'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Hasło'
        self.fields['password1'].label = ''
        self.fields[
            'password1'].help_text = '<li>Twoje hasło nie może być zbyt podobne do innych Twoich danych osobowych.</li><li>Twoje hasło musi zawierać co najmniej 8 znaków.</li><li>Twoje hasło nie może być powszechnie używanym hasłem.</li><li>Twoje hasło nie może być całkowicie numeryczne.</li>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Powtórz Hasło'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<li>W celu weryfikacji wpisz hasło ponownie.</li>'
