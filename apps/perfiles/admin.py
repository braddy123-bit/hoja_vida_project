from django.contrib import admin
from django.utils.html import format_html
from .models import (
    DatosPersonales, ExperienciaLaboral, Reconocimiento,
    CursoRealizado, ProductoAcademico, ProductoLaboral, VentaGarage
)


class ExperienciaLaboralInline(admin.TabularInline):
    model = ExperienciaLaboral
    extra = 0
    fields = ('cargo_desempenado', 'nombre_empresa', 'fecha_inicio_gestion', 
              'fecha_fin_gestion', 'activar_para_que_se_vea_en_front')


class ReconocimientoInline(admin.TabularInline):
    model = Reconocimiento
    extra = 0
    fields = ('tipo_reconocimiento', 'entidad_patrocinadora', 
              'fecha_reconocimiento', 'activar_para_que_se_vea_en_front')


class CursoRealizadoInline(admin.TabularInline):
    model = CursoRealizado
    extra = 0
    fields = ('nombre_curso', 'entidad_patrocinadora', 'fecha_inicio', 
              'fecha_fin', 'total_horas', 'activar_para_que_se_vea_en_front')


class ProductoAcademicoInline(admin.TabularInline):
    model = ProductoAcademico
    extra = 0
    fields = ('nombre_recurso', 'clasificador', 'activar_para_que_se_vea_en_front')


class ProductoLaboralInline(admin.TabularInline):
    model = ProductoLaboral
    extra = 0
    fields = ('nombre_producto', 'fecha_producto', 'activar_para_que_se_vea_en_front')


class VentaGarageInline(admin.TabularInline):
    model = VentaGarage
    extra = 0
    fields = ('nombre_producto', 'estado_producto', 'valor_del_bien', 
              'activar_para_que_se_vea_en_front')


@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'numero_cedula', 'edad_display', 
                    'perfil_activo', 'ver_foto')
    list_filter = ('perfil_activo', 'sexo', 'estado_civil', 'nacionalidad')
    search_fields = ('nombres', 'apellidos', 'numero_cedula')
    
    fieldsets = (
        ('Información del Perfil', {
            'fields': ('descripcion_perfil', 'perfil_activo', 'foto_perfil')
        }),
        ('Información Personal', {
            'fields': (('nombres', 'apellidos'), 
                      ('fecha_nacimiento', 'nacionalidad'),
                      ('numero_cedula', 'sexo', 'estado_civil'),
                      'licencia_conducir')
        }),
        ('Información de Contacto', {
            'fields': (('telefono_convencional', 'telefono_fijo'),
                      'direccion_domiciliaria',
                      'direccion_trabajo',
                      'sitio_web')
        }),
    )
    
    inlines = [
        ExperienciaLaboralInline,
        CursoRealizadoInline,
        ReconocimientoInline,
        ProductoAcademicoInline,
        ProductoLaboralInline,
        VentaGarageInline,
    ]
    
    def nombre_completo(self, obj):
        return f"{obj.nombres} {obj.apellidos}"
    nombre_completo.short_description = 'Nombre Completo'
    
    def edad_display(self, obj):
        return f"{obj.get_edad()} años"
    edad_display.short_description = 'Edad'
    
    def ver_foto(self, obj):
        if obj.foto_perfil:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%;" />',
                obj.foto_perfil.url
            )
        return "Sin foto"
    ver_foto.short_description = 'Foto'


@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ('cargo_desempenado', 'nombre_empresa', 'perfil',
                    'fecha_inicio_gestion', 'fecha_fin_gestion', 
                    'activar_para_que_se_vea_en_front')
    list_filter = ('activar_para_que_se_vea_en_front', 'perfil')
    search_fields = ('cargo_desempenado', 'nombre_empresa', 'perfil__nombres', 
                     'perfil__apellidos')
    date_hierarchy = 'fecha_inicio_gestion'
    
    fieldsets = (
        ('Información del Cargo', {
            'fields': ('perfil', 'cargo_desempenado', 'descripcion_funciones')
        }),
        ('Información de la Empresa', {
            'fields': (('nombre_empresa', 'lugar_empresa'),
                      ('email_empresa', 'sitio_web_empresa'))
        }),
        ('Período Laboral', {
            'fields': (('fecha_inicio_gestion', 'fecha_fin_gestion'),)
        }),
        ('Referencia Laboral', {
            'fields': (('nombre_contacto_empresarial', 'telefono_contacto_empresarial'),),
            'classes': ('collapse',)
        }),
        ('Opciones', {
            'fields': ('activar_para_que_se_vea_en_front', 'ruta_certificado')
        }),
    )


@admin.register(Reconocimiento)
class ReconocimientoAdmin(admin.ModelAdmin):
    list_display = ('tipo_reconocimiento', 'entidad_patrocinadora', 
                    'perfil', 'fecha_reconocimiento',
                    'activar_para_que_se_vea_en_front')
    list_filter = ('tipo_reconocimiento', 'activar_para_que_se_vea_en_front')
    search_fields = ('entidad_patrocinadora', 'descripcion_reconocimiento',
                     'perfil__nombres', 'perfil__apellidos')
    date_hierarchy = 'fecha_reconocimiento'
    
    fieldsets = (
        ('Información del Reconocimiento', {
            'fields': ('perfil', 'tipo_reconocimiento', 
                      'fecha_reconocimiento', 'descripcion_reconocimiento')
        }),
        ('Entidad Otorgante', {
            'fields': ('entidad_patrocinadora',
                      ('nombre_contacto_auspicia', 'telefono_contacto_auspicia'))
        }),
        ('Opciones', {
            'fields': ('activar_para_que_se_vea_en_front', 'ruta_certificado')
        }),
    )


@admin.register(CursoRealizado)
class CursoRealizadoAdmin(admin.ModelAdmin):
    list_display = ('nombre_curso', 'entidad_patrocinadora', 'perfil',
                    'fecha_inicio', 'fecha_fin', 'total_horas',
                    'activar_para_que_se_vea_en_front')
    list_filter = ('activar_para_que_se_vea_en_front', 'perfil')
    search_fields = ('nombre_curso', 'entidad_patrocinadora',
                     'perfil__nombres', 'perfil__apellidos')
    date_hierarchy = 'fecha_inicio'
    
    fieldsets = (
        ('Información del Curso', {
            'fields': ('perfil', 'nombre_curso', 'descripcion_curso')
        }),
        ('Período y Duración', {
            'fields': (('fecha_inicio', 'fecha_fin'), 'total_horas')
        }),
        ('Institución', {
            'fields': ('entidad_patrocinadora', 'email_empresa_patrocinadora',
                      ('nombre_contacto_auspicia', 'telefono_contacto_auspicia'))
        }),
        ('Opciones', {
            'fields': ('activar_para_que_se_vea_en_front', 'ruta_certificado')
        }),
    )


@admin.register(ProductoAcademico)
class ProductoAcademicoAdmin(admin.ModelAdmin):
    list_display = ('nombre_recurso', 'clasificador', 'perfil',
                    'ver_imagen', 'activar_para_que_se_vea_en_front')
    list_filter = ('clasificador', 'activar_para_que_se_vea_en_front')
    search_fields = ('nombre_recurso', 'descripcion', 
                     'perfil__nombres', 'perfil__apellidos')
    
    fieldsets = (
        ('Información del Proyecto', {
            'fields': ('perfil', 'nombre_recurso', 'clasificador', 
                      'descripcion', 'imagen_proyecto')
        }),
        ('Opciones', {
            'fields': ('activar_para_que_se_vea_en_front',)
        }),
    )
    
    def ver_imagen(self, obj):
        if obj.imagen_proyecto:
            return format_html(
                '<img src="{}" width="100" height="auto" />',
                obj.imagen_proyecto.url
            )
        return "Sin imagen"
    ver_imagen.short_description = 'Imagen'


@admin.register(ProductoLaboral)
class ProductoLaboralAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 'perfil', 'fecha_producto',
                    'activar_para_que_se_vea_en_front')
    list_filter = ('activar_para_que_se_vea_en_front', 'perfil')
    search_fields = ('nombre_producto', 'descripcion',
                     'perfil__nombres', 'perfil__apellidos')
    date_hierarchy = 'fecha_producto'
    
    fieldsets = (
        ('Información del Proyecto', {
            'fields': ('perfil', 'nombre_producto', 'fecha_producto',
                      'descripcion', 'link_proyecto')
        }),
        ('Opciones', {
            'fields': ('activar_para_que_se_vea_en_front',)
        }),
    )


@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 'perfil', 'estado_producto',
                    'valor_del_bien_display', 'fecha_publicacion',
                    'ver_imagen', 'activar_para_que_se_vea_en_front')
    list_filter = ('estado_producto', 'activar_para_que_se_vea_en_front')
    search_fields = ('nombre_producto', 'descripcion',
                     'perfil__nombres', 'perfil__apellidos')
    date_hierarchy = 'fecha_publicacion'
    
    fieldsets = (
        ('Información del Producto', {
            'fields': ('perfil', 'nombre_producto', 'estado_producto',
                      'valor_del_bien', 'descripcion', 'imagen_producto')
        }),
        ('Opciones', {
            'fields': ('activar_para_que_se_vea_en_front',)
        }),
    )
    
    def valor_del_bien_display(self, obj):
        return f"${obj.valor_del_bien:.2f}"
    valor_del_bien_display.short_description = 'Precio'
    
    def ver_imagen(self, obj):
        if obj.imagen_producto:
            return format_html(
                '<img src="{}" width="100" height="auto" />',
                obj.imagen_producto.url
            )
        return "Sin imagen"
    ver_imagen.short_description = 'Imagen'
