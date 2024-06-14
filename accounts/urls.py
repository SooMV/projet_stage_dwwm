
from django.urls import path
from accounts.views import login_user, signup, logout_user, profile

urlpatterns = [
   
    path("profile/", profile, name="profile"),
    path("signup/", signup, name="signup"),
    path('login/', login_user, name="login"),
    path("logout/", logout_user, name="logout"), 
]





