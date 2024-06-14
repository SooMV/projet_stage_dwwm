from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings
from dash_admin.views import averageCart
from store.views import index



urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("", index, name='index'),
    path('averageCart/', averageCart, name='averageCart'),
    
    path('store/', include('store.urls')),
    path('accounts/', include('accounts.urls')),
    path('map/', include('map.urls')),
    path('mail/', include('mail.urls')),
    

)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)