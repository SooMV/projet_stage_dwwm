from django import forms

from store.models import Product


class CartItemForm(forms.ModelForm):
    # Case a cocher pour supprimer un ou plusiuer produits 
    delete = forms.BooleanField(initial=False, required=False, label="Supprimer")
    class Meta:
        fields =["quantity", "delete"]
        
    def save(self, *arg,**kwargs):
        if self.cleaned_data["delete"]:
            self.instance.delete()
                   
            # Si  les articles sont 0 après suppression
            if self.instance.user.cart.orders.count() == 0:
                self.instance.user.cart.delete()
            else:
                 self.instance.quantity = self.cleaned_data.get('quantity')
                 self.instance.save()
                 self.instance.user.cart.calc_totaux()
            return True
        
        #  class -> super() appelle automatiquement lélément parent 
        return super().save(*arg, **kwargs)

    
class RechercheProduitForm(forms.Form):
    query = forms.CharField(label='Recherche de produit', max_length=100)
    class Meta:
        model = Product