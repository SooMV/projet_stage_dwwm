from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.conf import settings
from accounts.models import Customer, ShippingAddress
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.core.validators import RegexValidator
from django.contrib.auth.forms import PasswordChangeForm

from django_countries.fields import CountryField

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    captcha = ReCaptchaField()

    class Meta:
        model = Customer
        fields = ['email', 'password1', 'password2', 'captcha']

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(),
        error_messages={
            'required': settings.RECAPTCHA_ERROR_MSG['required'],
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("L'adresse e-mail ou le mot de passe est incorrect.")
        return cleaned_data


class DeliveryForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'Entrez votre numéro de téléphone (par exemple, +33123456789)',
            'pattern': '^\\+33[1-9]\\d{8}$',
            'title': 'Veuillez entrer un numéro de téléphone valide (format français uniquement, par exemple +33123456789)',
        })
    )
    address_1 = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    address_2 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    city = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    zip_code = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    country = CountryField().formfield(
        required=True,
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
        })
    )
    
    class Meta:
        model = ShippingAddress  
        fields = ['first_name', 'last_name', 'phone_number', 'address_1', 'address_2', 'city', 'zip_code', 'country']

class PasswordResetForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label="Nouveau mot de passe", 
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        }))
    new_password2 = forms.CharField(
        label="Confirmer nouveau mot de passe", 
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        }))
    
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = Customer
        fields = ['new_password1', 'new_password2']
