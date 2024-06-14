from django.db import models

# Create your models here.

from decimal import Decimal
from django.db import models
from store.models import Product, Categorie, CartItem
from django.utils.translation import gettext_lazy as _

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales', verbose_name=_("Sales"))
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='sales', verbose_name=_("Categorie"))
    quantity = models.PositiveIntegerField(default=0, verbose_name=_("Quantity"))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name=_("Total_Amount"))
    sale_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Sales_date"))

    def __str__(self):
        return f"{self.product.name} - {self.category.name} - {self.quantity}"
    
    def calculate_total_amount(self):
        if self.product.promo:
            self.total_amount = self.quantity * self.product.price_promo
        else:
            self.total_amount = self.quantity * self.product.price

        self.total_amount = Decimal(self.total_amount).quantize(Decimal("0.00"))
        self.save()

    def save(self, *args, **kwargs):
        self.calculate_total_amount()
        super(Sale, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name=_("Sale")
        verbose_name_plural=_("Sales")
