# hoja_vida_project
# 📊 RESUMEN DEL PROYECTO - HOJA DE VIDA DIGITAL

## 🎯 Descripción

Sistema web en Django para crear y gestionar hojas de vida profesionales.

**TODO se gestiona desde el panel administrativo**

## ✨ Características

- ✅ Validaciones: Edad 15-75 años, fechas coherentes
- ✅ Panel Admin completo y personalizado
- ✅ Diseño moderno y responsive (único, no copia ejemplos)
- ✅ Generación de PDF profesional
- ✅ Gestión de archivos (fotos, certificados)
- ✅ 7 módulos: Datos, Experiencia, Cursos, Reconocimientos, Proyectos, Venta
- ✅ Múltiples perfiles
- ✅ Control de visibilidad

## 🚀 Inicio Rápido

```bash
# Extraer y entrar
tar -xzf hoja_vida_project.tar.gz
cd hoja_vida_project

# Instalar
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurar
cp .env.example .env
# Editar .env con SECRET_KEY

# Preparar
python manage.py migrate
python manage.py createsuperuser

# Ejecutar
python manage.py runserver
```

## 🎯 Uso del Sistema

1. **Admin**: http://localhost:8000/admin/
2. **Crear Perfil**: "Datos Personales" → Añadir
3. **Agregar Info**: Experiencias, Cursos, etc. desde admin
4. **Ver CV**: http://localhost:8000/

**¡TODO desde el panel admin!**

## 🎨 Diseño

- Colores: Beige/Marrón (#C4A183, #8B7355)
- Layout: Sidebar fijo con degradado
- Tipografía: Inter
- Estilo: Moderno y minimalista
- **Completamente diferente al ejemplo original**

## 📦 Incluye

- Código fuente completo
- Configuración dev y prod
- Scripts para Render
- Documentación (README, INSTALL)
- Sin datos precargados

## ✅ Validaciones

- Edad: 15-75 años (automático)
- Fechas: No futuras, coherentes
- Cédula: Única
- Teléfonos, emails, URLs: Formato válido

## 🌐 Deploy en Render

```bash
Build: ./build.sh
Start: gunicorn config.wsgi:application
```

Variables de entorno en Render:
- SECRET_KEY
- DEBUG=False
- ALLOWED_HOSTS=.onrender.com

## 📱 URLs

- `/` - Inicio
- `/admin/` - Panel admin
- `/perfil/` - CV público
- `/perfil/<cedula>/pdf/` - Descargar PDF
- `/perfil/<cedula>/garage/` - Venta garage

## 💡 Notas Importantes

1. ❌ **NO** hay datos precargados
2. ❌ **NO** hay comandos de ejemplo
3. ✅ Todo se crea desde el admin
4. ✅ Diseño único (no copia)
5. ✅ Listo para producción

---

**¡Sistema limpio, profesional y listo para usar!** 🚀
