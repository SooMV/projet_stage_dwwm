from django.db import models
from django.utils.translation import gettext_lazy as _

class Emails(models.Model):
    subject = models.CharField(max_length=500, verbose_name=_("Subject"))
    message = models.TextField(verbose_name=_("Message"))
    email = models.EmailField(verbose_name=_("Email"))
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_("Created At"))
    edited_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_("Edited At"))
   
    def __str__(self):
        return str(self.id)
   
    class Meta:
        verbose_name = _("Email")
        verbose_name_plural = _("Emails")
