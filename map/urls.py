from django.urls import path

from map.views import map_view, boutique_details

urlpatterns = [
    path("map/", map_view, name="map_view"),
    path('map/<int:id>/', boutique_details, name='boutique_details'),


]