from django.shortcuts import get_object_or_404, render
from .models import Boutique

def map_view(request):
    boutiques = Boutique.objects.all()
    return render(request, 'map/maps.html', {'boutiques': boutiques, 'boutiques_count' : boutiques.count()})

def boutique_details(request, id):
    boutique = get_object_or_404(Boutique, id=id)
    return render(request, 'map/boutique_details.html', {'boutique': boutique})
