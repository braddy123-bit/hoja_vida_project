from django.urls import path
from .views import PerfilPublicoView, VentaGarageView, GenerarPDFView

app_name = 'perfiles'

urlpatterns = [
    path('', PerfilPublicoView.as_view(), name='perfil_publico'),
    path('<str:cedula>/', PerfilPublicoView.as_view(), name='perfil_por_cedula'),
    path('<str:cedula>/pdf/', GenerarPDFView.as_view(), name='generar_pdf'),
    path('<str:cedula>/garage/', VentaGarageView.as_view(), name='venta_garage'),
]
