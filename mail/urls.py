from django.urls import path
from mail.views import contact_us, user_confirmation_email


urlpatterns = [
    path("user_confirmation_email/", user_confirmation_email, name="user_confirmation_email"),
    path("contact/", contact_us, name="contact_us"),    
]


