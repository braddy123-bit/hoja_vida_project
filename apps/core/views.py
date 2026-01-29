from django.shortcuts import render
from django.views import View
from apps.perfiles.models import DatosPersonales


class HomeView(View):
    """Vista principal del sitio"""
    
    def get(self, request):
        # Obtener el primer perfil activo
        perfil = DatosPersonales.objects.filter(perfil_activo=True).first()
        
        context = {
            'perfil': perfil,
        }
        
        return render(request, 'core/home.html', context)
