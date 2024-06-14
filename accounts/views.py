from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model, login, logout , authenticate
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.contrib.auth import update_session_auth_hash
from accounts.forms import UserRegistrationForm, UserLoginForm, DeliveryForm, PasswordResetForm
from accounts.models import ShippingAddress
from mail.views import send_welcome_email
import logging

logger = logging.getLogger(__name__)
User = get_user_model()



# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            captcha_response = form.cleaned_data.get('captcha')

            if User.objects.filter(email=email).exists():
                messages.add_message(request, messages.ERROR, "Ce compte existe déjà.")
            elif captcha_response:  # Vérifiez si le captcha est valide
                user = User.objects.create_user(email=email, password=password)
                login(request, user)
                send_welcome_email(user.email)
                logger.info(f"New user {user.email} signed up and logged in.")
                return redirect('index')
            else:
                messages.add_message(request, messages.ERROR, "Le test reCAPTCHA a échoué. Veuillez réessayer.")
        else:
            messages.add_message(request, messages.ERROR, "Les informations fournies sont invalides.")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/signup.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Le compte n'existe pas ou les informations de connexion sont incorrectes")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})
     

def logout_user(request):
    logout(request)
    return redirect('index')

@login_required(login_url="../login/")
def profile(request):
    user = request.user

    if request.method == 'POST':
        delivery_form = DeliveryForm(request.POST, instance=user)
        password_form = PasswordResetForm(user, request.POST)

        if 'delivery_form' in request.POST and delivery_form.is_valid():
            delivery_form.save()
            messages.success(request, "Vos informations de livraison ont été mises à jour avec succès.")
        elif 'password_form' in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Votre mot de passe a été réinitialisé avec succès.")
        else:
            if not delivery_form.is_valid():
                messages.error(request, "Veuillez corriger les erreurs du formulaire de livraison.")
            if not password_form.is_valid():
                messages.error(request, "Veuillez corriger les erreurs du formulaire de réinitialisation du mot de passe.")
        return redirect('profile')

    else:
        delivery_form = DeliveryForm(instance=user)
        password_form = PasswordResetForm(user)

    addresses = user.addresses.all()  
    return render(request, "accounts/profile.html", context={
        "delivery_form": delivery_form,
        "password_form": password_form,
        "addresses": addresses
    })



@login_required
def set_default_shipping_addresse(request, pk):
    address: ShippingAddress = get_object_or_404(ShippingAddress, pk=pk)
    address.set_default()
    return redirect('profile')