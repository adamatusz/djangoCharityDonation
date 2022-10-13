from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (UserCreationForm,
                                       ReadOnlyPasswordHashField)

# from .models import User

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean(self):
        """
        Verify both passwords match.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'is_active', 'admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


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


