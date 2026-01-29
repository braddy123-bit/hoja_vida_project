"""
URL configuration for hoja_vida_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('perfil/', include('apps.perfiles.urls')),
]

# Configuración del admin
admin.site.site_header = "Administración Hoja de Vida"
admin.site.site_title = "Panel Administrativo"
admin.site.index_title = "Gestión de Hojas de Vida"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
