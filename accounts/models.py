from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from iso3166 import countries
import stripe
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self,email, password, **Kwargs):
        if not email :
           raise ValueError("L'addresse email est obligatoire.")
        email = self.normalize_email(email)
        user = self.model(email = email, **Kwargs)
        user.set_password(password)
        user.save()
        
        return user
    
    def create_superuser(self, email, password, **Kwargs):
        Kwargs['is_staff'] = True
        Kwargs['is_superuser'] = True
        Kwargs['is_active'] = True
        
        return self.create_user(email = email, password = password, **Kwargs)

ADDRESSE_FORMAT = """ 

{name}
{phone_number}
{address_1}
{address_2}
{city} , {zip_code}
{country}

"""
    
class Customer(AbstractUser):
    username = None 
    email = models.EmailField(max_length=240, unique = True, verbose_name=_("User_Email"))
    stripe_id = models.CharField(max_length=90, blank = True,)
    
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [] 
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
    

class ShippingAddress(models.Model):
    # Typage des variables afin de spécifier quel sera la valeur du user
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name="addresses", verbose_name=_("User"))  
    name = models.CharField(max_length=120)
    address_1 = models.CharField(max_length=1024, help_text=_("Street address and number"), verbose_name=_("Address 1"))
    address_2 = models.CharField(max_length=1024, help_text=_("Building, floor, landmark, etc."), blank=True, verbose_name=_("Address 2"))
    city = models.CharField(max_length=1024, verbose_name=_("City"))
    zip_code = models.CharField(max_length=32,verbose_name=_("Zip Code"))
    phone_number = models.CharField(max_length=12, blank=True, null=True, verbose_name=_("Phone Number") )
    # défini le nombre de string à 2 dans la listes ISO 
    country = models.CharField(max_length=2, choices=[(c.alpha2.lower(), c.name) for c in countries], verbose_name=_("Country"))
    default = models.BooleanField(default=False, verbose_name=_("Default Address"))
    
    class Meta:
        verbose_name = _("Shipping Address")
        verbose_name_plural = _("Shipping Addresses")
        
    def __str__(self):
        data = self.__dict__.copy()
        data.update(country = self.get_country_display())
        return ADDRESSE_FORMAT.format(**data)

    def as_dict(self):
        return {
            "city" : self.city,
            "country" : self.country,
            "line1" : self.address_1,
            "line2" : self.address_2,
            "postal_code" : self.zip_code,
            "phone_number": self.phone_number
        }
        
    def set_default(self):
        if not self.user.stripe_id:
            raise ValueError(f"L'utilisateur {self.user.email} n'a pas de stripe ID")
        self.user.addresses.update(default = False)
        self.default = True
        self.save()
        
        stripe.Customer.modify(
            self.user.stripe_id,
            shipping ={
                "name" : self.name,
                "address": self.as_dict()
            },
            address=self.as_dict()
        )
       