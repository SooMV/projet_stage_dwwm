from django.db import models
from django.utils.translation import gettext_lazy as _


class Boutique(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Store Name"))
    ville = models.CharField(max_length=100, null=True, verbose_name=_("City"))
    zipcode = models.CharField(max_length=10, null=True, verbose_name=_("Zipcode"))
    address = models.CharField(max_length=255, verbose_name=_("Address"))
    latitude = models.FloatField(verbose_name=_("Latitude"))
    longitude = models.FloatField(verbose_name=_("Longitude"))
    opening_hours = models.CharField(max_length=255, verbose_name=_("Opening Hours"))
    description = models.TextField(verbose_name=_("Description"))
    thumbnails_ville = models.ImageField(upload_to="shop", blank=True, null=True, verbose_name=_("City Thumbnail"))
    shop_image = models.ImageField(upload_to="shop", blank=True, null=True, verbose_name=_("Shop Image"))
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Store")
        verbose_name_plural = _("Stores")