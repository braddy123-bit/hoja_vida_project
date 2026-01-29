from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, timedelta
from phonenumber_field.modelfields import PhoneNumberField


def validate_edad_minima(fecha_nacimiento):
    """Valida que la persona tenga al menos 15 años"""
    if fecha_nacimiento:
        hoy = date.today()
        edad = hoy.year - fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
        )
        if edad < 15:
            raise ValidationError('Debe tener al menos 15 años de edad.')
        if edad > 75:
            raise ValidationError('La edad no puede superar los 75 años.')


def validate_fecha_no_futura(fecha):
    """Valida que la fecha no sea futura"""
    if fecha and fecha > date.today():
        raise ValidationError('La fecha no puede ser futura.')


def validate_fecha_inicio_fin(fecha_inicio, fecha_fin):
    """Valida que la fecha de fin sea posterior a la de inicio"""
    if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
        raise ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio.')


class DatosPersonales(models.Model):
    """Modelo para datos personales del perfil"""
    
    SEXO_CHOICES = [
        ('M', 'Mujer'),
        ('H', 'Hombre'),
    ]
    
    ESTADO_CIVIL_CHOICES = [
        ('Soltero/a', 'Soltero/a'),
        ('Casado/a', 'Casado/a'),
        ('Divorciado/a', 'Divorciado/a'),
        ('Viudo/a', 'Viudo/a'),
        ('Unión libre', 'Unión libre'),
    ]
    
    # Información del perfil
    descripcion_perfil = models.CharField(
        max_length=100,
        verbose_name='Descripción del perfil',
        help_text='Ej: Desarrollador Web, Ingeniero, Estudiante'
    )
    perfil_activo = models.BooleanField(
        default=True,
        verbose_name='Perfil activo',
        help_text='Marcar si este perfil está activo'
    )
    
    # Datos personales
    nombres = models.CharField(max_length=60, verbose_name='Nombres')
    apellidos = models.CharField(max_length=60, verbose_name='Apellidos')
    
    nacionalidad = models.CharField(
        max_length=20,
        default='Ecuatoriana',
        verbose_name='Nacionalidad'
    )
    
    fecha_nacimiento = models.DateField(
        verbose_name='Fecha de nacimiento',
        validators=[validate_edad_minima, validate_fecha_no_futura]
    )
    
    numero_cedula = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Número de cédula'
    )
    
    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        verbose_name='Sexo'
    )
    
    estado_civil = models.CharField(
        max_length=50,
        choices=ESTADO_CIVIL_CHOICES,
        verbose_name='Estado civil'
    )
    
    licencia_conducir = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        verbose_name='Licencia de conducir',
        help_text='Tipo de licencia (Ej: B, C, D)'
    )
    
    # Datos de contacto
    telefono_convencional = PhoneNumberField(
        blank=True,
        null=True,
        region='EC',
        verbose_name='Teléfono convencional'
    )
    
    telefono_fijo = PhoneNumberField(
        blank=True,
        null=True,
        region='EC',
        verbose_name='Teléfono celular'
    )
    
    # Direcciones
    direccion_domiciliaria = models.CharField(
        max_length=100,
        verbose_name='Dirección domiciliaria'
    )
    
    direccion_trabajo = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Dirección de trabajo'
    )
    
    # Web
    sitio_web = models.URLField(
        blank=True,
        null=True,
        verbose_name='Sitio web personal'
    )
    
    # Foto de perfil
    foto_perfil = models.ImageField(
        upload_to='perfiles/',
        blank=True,
        null=True,
        verbose_name='Foto de perfil'
    )
    
    # Metadata
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Dato Personal'
        verbose_name_plural = 'Datos Personales'
        ordering = ['-fecha_actualizacion']
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
    def get_edad(self):
        """Calcula la edad actual"""
        hoy = date.today()
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )
    
    def clean(self):
        """Validaciones adicionales"""
        super().clean()
        validate_edad_minima(self.fecha_nacimiento)
        validate_fecha_no_futura(self.fecha_nacimiento)


class ExperienciaLaboral(models.Model):
    """Modelo para experiencia laboral"""
    
    perfil = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='experiencias',
        verbose_name='Perfil'
    )
    
    cargo_desempenado = models.CharField(
        max_length=100,
        verbose_name='Cargo desempeñado'
    )
    
    nombre_empresa = models.CharField(
        max_length=50,
        verbose_name='Nombre de la empresa'
    )
    
    lugar_empresa = models.CharField(
        max_length=50,
        verbose_name='Ubicación de la empresa'
    )
    
    email_empresa = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Email de la empresa'
    )
    
    sitio_web_empresa = models.URLField(
        blank=True,
        null=True,
        verbose_name='Sitio web de la empresa'
    )
    
    # Contacto de referencia
    nombre_contacto_empresarial = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Nombre del contacto'
    )
    
    telefono_contacto_empresarial = PhoneNumberField(
        blank=True,
        null=True,
        region='EC',
        verbose_name='Teléfono del contacto'
    )
    
    # Fechas
    fecha_inicio_gestion = models.DateField(
        verbose_name='Fecha de inicio',
        validators=[validate_fecha_no_futura]
    )
    
    fecha_fin_gestion = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha de fin',
        help_text='Dejar en blanco si actualmente trabaja aquí'
    )
    
    # Descripción
    descripcion_funciones = models.TextField(
        max_length=500,
        verbose_name='Descripción de funciones'
    )
    
    # Control de visibilidad
    activar_para_que_se_vea_en_front = models.BooleanField(
        default=True,
        verbose_name='Mostrar en CV público'
    )
    
    # Certificado
    ruta_certificado = models.FileField(
        upload_to='certificados/experiencia/',
        blank=True,
        null=True,
        verbose_name='Certificado laboral'
    )
    
    # Metadata
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Experiencia Laboral'
        verbose_name_plural = 'Experiencias Laborales'
        ordering = ['-fecha_inicio_gestion']
    
    def __str__(self):
        return f"{self.cargo_desempenado} en {self.nombre_empresa}"
    
    def clean(self):
        """Validaciones adicionales"""
        super().clean()
        validate_fecha_no_futura(self.fecha_inicio_gestion)
        
        if self.fecha_fin_gestion:
            validate_fecha_no_futura(self.fecha_fin_gestion)
            validate_fecha_inicio_fin(self.fecha_inicio_gestion, self.fecha_fin_gestion)
    
    def get_duracion(self):
        """Calcula la duración del trabajo"""
        fecha_fin = self.fecha_fin_gestion or date.today()
        delta = fecha_fin - self.fecha_inicio_gestion
        años = delta.days // 365
        meses = (delta.days % 365) // 30
        
        if años > 0:
            return f"{años} año{'s' if años > 1 else ''}" + (f" {meses} mes{'es' if meses > 1 else ''}" if meses > 0 else "")
        else:
            return f"{meses} mes{'es' if meses != 1 else ''}"


class Reconocimiento(models.Model):
    """Modelo para reconocimientos"""
    
    TIPO_CHOICES = [
        ('Académico', 'Académico'),
        ('Público', 'Público'),
        ('Privado', 'Privado'),
    ]
    
    perfil = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='reconocimientos',
        verbose_name='Perfil'
    )
    
    tipo_reconocimiento = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name='Tipo de reconocimiento'
    )
    
    fecha_reconocimiento = models.DateField(
        verbose_name='Fecha del reconocimiento',
        validators=[validate_fecha_no_futura]
    )
    
    descripcion_reconocimiento = models.TextField(
        max_length=300,
        verbose_name='Descripción'
    )
    
    entidad_patrocinadora = models.CharField(
        max_length=100,
        verbose_name='Entidad que otorga'
    )
    
    # Contacto
    nombre_contacto_auspicia = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Nombre del contacto'
    )
    
    telefono_contacto_auspicia = PhoneNumberField(
        blank=True,
        null=True,
        region='EC',
        verbose_name='Teléfono del contacto'
    )
    
    # Control
    activar_para_que_se_vea_en_front = models.BooleanField(
        default=True,
        verbose_name='Mostrar en CV público'
    )
    
    # Certificado
    ruta_certificado = models.FileField(
        upload_to='certificados/reconocimientos/',
        blank=True,
        null=True,
        verbose_name='Certificado'
    )
    
    # Metadata
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Reconocimiento'
        verbose_name_plural = 'Reconocimientos'
        ordering = ['-fecha_reconocimiento']
    
    def __str__(self):
        return f"{self.tipo_reconocimiento} - {self.entidad_patrocinadora}"
    
    def clean(self):
        super().clean()
        validate_fecha_no_futura(self.fecha_reconocimiento)


class CursoRealizado(models.Model):
    """Modelo para cursos realizados"""
    
    perfil = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='cursos',
        verbose_name='Perfil'
    )
    
    nombre_curso = models.CharField(
        max_length=100,
        verbose_name='Nombre del curso'
    )
    
    fecha_inicio = models.DateField(
        verbose_name='Fecha de inicio',
        validators=[validate_fecha_no_futura]
    )
    
    fecha_fin = models.DateField(
        verbose_name='Fecha de fin',
        validators=[validate_fecha_no_futura]
    )
    
    total_horas = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10000)],
        verbose_name='Total de horas'
    )
    
    descripcion_curso = models.TextField(
        max_length=300,
        verbose_name='Descripción del curso'
    )
    
    entidad_patrocinadora = models.CharField(
        max_length=100,
        verbose_name='Institución'
    )
    
    # Contacto
    nombre_contacto_auspicia = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Nombre del contacto'
    )
    
    telefono_contacto_auspicia = PhoneNumberField(
        blank=True,
        null=True,
        region='EC',
        verbose_name='Teléfono del contacto'
    )
    
    email_empresa_patrocinadora = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Email de la institución'
    )
    
    # Control
    activar_para_que_se_vea_en_front = models.BooleanField(
        default=True,
        verbose_name='Mostrar en CV público'
    )
    
    # Certificado
    ruta_certificado = models.FileField(
        upload_to='certificados/cursos/',
        blank=True,
        null=True,
        verbose_name='Certificado'
    )
    
    # Metadata
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Curso Realizado'
        verbose_name_plural = 'Cursos Realizados'
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.nombre_curso} - {self.entidad_patrocinadora}"
    
    def clean(self):
        super().clean()
        validate_fecha_no_futura(self.fecha_inicio)
        validate_fecha_no_futura(self.fecha_fin)
        validate_fecha_inicio_fin(self.fecha_inicio, self.fecha_fin)


class ProductoAcademico(models.Model):
    """Modelo para productos académicos"""
    
    CLASIFICADOR_CHOICES = [
        ('Proyecto Académico', 'Proyecto Académico'),
        ('Electrónica', 'Electrónica'),
        ('Desarrollo Web', 'Desarrollo Web'),
        ('Investigación', 'Investigación'),
        ('Otro', 'Otro'),
    ]
    
    perfil = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='productos_academicos',
        verbose_name='Perfil'
    )
    
    nombre_recurso = models.CharField(
        max_length=100,
        verbose_name='Nombre del proyecto'
    )
    
    clasificador = models.CharField(
        max_length=50,
        choices=CLASIFICADOR_CHOICES,
        verbose_name='Clasificación'
    )
    
    descripcion = models.TextField(
        max_length=500,
        verbose_name='Descripción'
    )
    
    imagen_proyecto = models.ImageField(
        upload_to='proyectos/academicos/',
        blank=True,
        null=True,
        verbose_name='Imagen del proyecto'
    )
    
    # Control
    activar_para_que_se_vea_en_front = models.BooleanField(
        default=True,
        verbose_name='Mostrar en CV público'
    )
    
    # Metadata
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Producto Académico'
        verbose_name_plural = 'Productos Académicos'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.nombre_recurso} ({self.clasificador})"


class ProductoLaboral(models.Model):
    """Modelo para productos laborales"""
    
    perfil = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='productos_laborales',
        verbose_name='Perfil'
    )
    
    nombre_producto = models.CharField(
        max_length=100,
        verbose_name='Nombre del proyecto'
    )
    
    fecha_producto = models.DateField(
        verbose_name='Fecha',
        validators=[validate_fecha_no_futura]
    )
    
    descripcion = models.TextField(
        max_length=500,
        verbose_name='Descripción'
    )
    
    link_proyecto = models.URLField(
        blank=True,
        null=True,
        verbose_name='Link del proyecto'
    )
    
    # Control
    activar_para_que_se_vea_en_front = models.BooleanField(
        default=True,
        verbose_name='Mostrar en CV público'
    )
    
    # Metadata
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Producto Laboral'
        verbose_name_plural = 'Productos Laborales'
        ordering = ['-fecha_producto']
    
    def __str__(self):
        return self.nombre_producto
    
    def clean(self):
        super().clean()
        validate_fecha_no_futura(self.fecha_producto)


class VentaGarage(models.Model):
    """Modelo para venta de garage"""
    
    ESTADO_CHOICES = [
        ('Bueno', 'Bueno'),
        ('Regular', 'Regular'),
    ]
    
    perfil = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='ventas_garage',
        verbose_name='Perfil'
    )
    
    nombre_producto = models.CharField(
        max_length=100,
        verbose_name='Nombre del producto'
    )
    
    estado_producto = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        verbose_name='Estado del producto'
    )
    
    descripcion = models.TextField(
        max_length=500,
        verbose_name='Descripción'
    )
    
    valor_del_bien = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Precio (USD)'
    )
    
    imagen_producto = models.ImageField(
        upload_to='ventas/',
        blank=True,
        null=True,
        verbose_name='Imagen del producto'
    )
    
    fecha_publicacion = models.DateField(
        auto_now_add=True,
        verbose_name='Fecha de publicación'
    )
    
    # Control
    activar_para_que_se_vea_en_front = models.BooleanField(
        default=True,
        verbose_name='Mostrar en venta garage'
    )
    
    # Metadata
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Venta Garage'
        verbose_name_plural = 'Ventas Garage'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.nombre_producto} - ${self.valor_del_bien}"
