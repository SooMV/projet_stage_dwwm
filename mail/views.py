from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages

def contact_us(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        user_email = request.user.email
        
        # Email pour l'administrateur
        admin_email_content = f"Nom : {name}\nSujet : {subject}\n\n{message}"
        send_mail(
            'Formulaire de contact - Nouvelle soumission',
            admin_email_content,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],  # Email de l'administrateur
            fail_silently=False,
        )

        # Email de confirmation pour l'utilisateur
        context = {
            'name': name,
            'subject': subject,
        }
        html_content = render_to_string('mail/user_confirmation_email.html', context)
        text_content = strip_tags(html_content)  # Version texte pour les clients email ne supportant pas le HTML

        email = EmailMultiAlternatives(
            'Confirmation de votre demande de contact',
            text_content,
            settings.EMAIL_HOST_USER,
            [user_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

      
        return redirect('user_confirmation_email')  # Rediriger vers la page d'accueil ou tout autre alias de vue

    return render(request, 'mail/contact.html')


def send_welcome_email(user_email):
    # Récupération du mail du user pour le template
    context = {'user_email': user_email}

    # Création du contenu HTML à partir du template
    html_content = render_to_string('mail/welcome_email.html', context)
    # Création de la version texte en supprimant les balises HTML
    text_content = strip_tags(html_content)

    # Création de l'email 
    email = EmailMultiAlternatives(
        'Bienvenue sur notre plateforme !',  # sujet
        text_content,                        # contenu en texte
        settings.EMAIL_HOST_USER,            # adresse de l'expéditeur
        [user_email]                         # liste des destinataires
    )

    # Ajout de la version HTML comme alternative
    email.attach_alternative(html_content, "text/html")
    
    # Envoi de l'email
    email.send()


def user_confirmation_email(request):
    return render(request, 'mail/user_confirmation_email.html')