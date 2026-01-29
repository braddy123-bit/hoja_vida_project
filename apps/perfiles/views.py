from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import DatosPersonales
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO


class PerfilPublicoView(View):
    """Vista del perfil público"""
    
    def get(self, request, cedula=None):
        if cedula:
            perfil = get_object_or_404(
                DatosPersonales,
                numero_cedula=cedula,
                perfil_activo=True
            )
        else:
            # Obtener el primer perfil activo
            perfil = DatosPersonales.objects.filter(perfil_activo=True).first()
            if not perfil:
                return render(request, 'perfiles/no_perfil.html')
        
        # Obtener datos relacionados activos
        experiencias = perfil.experiencias.filter(
            activar_para_que_se_vea_en_front=True
        ).order_by('-fecha_inicio_gestion')
        
        cursos = perfil.cursos.filter(
            activar_para_que_se_vea_en_front=True
        ).order_by('-fecha_inicio')
        
        reconocimientos = perfil.reconocimientos.filter(
            activar_para_que_se_vea_en_front=True
        ).order_by('-fecha_reconocimiento')
        
        productos_academicos = perfil.productos_academicos.filter(
            activar_para_que_se_vea_en_front=True
        )
        
        productos_laborales = perfil.productos_laborales.filter(
            activar_para_que_se_vea_en_front=True
        ).order_by('-fecha_producto')
        
        context = {
            'perfil': perfil,
            'experiencias': experiencias,
            'cursos': cursos,
            'reconocimientos': reconocimientos,
            'productos_academicos': productos_academicos,
            'productos_laborales': productos_laborales,
        }
        
        return render(request, 'perfiles/perfil_publico.html', context)


class VentaGarageView(View):
    """Vista de venta garage"""
    
    def get(self, request, cedula=None):
        if cedula:
            perfil = get_object_or_404(
                DatosPersonales,
                numero_cedula=cedula,
                perfil_activo=True
            )
        else:
            perfil = DatosPersonales.objects.filter(perfil_activo=True).first()
            if not perfil:
                return render(request, 'perfiles/no_perfil.html')
        
        ventas = perfil.ventas_garage.filter(
            activar_para_que_se_vea_en_front=True
        ).order_by('-fecha_creacion')
        
        context = {
            'perfil': perfil,
            'ventas': ventas,
        }
        
        return render(request, 'perfiles/venta_garage.html', context)


class GenerarPDFView(View):
    """Vista para generar PDF de la hoja de vida"""
    
    def get(self, request, cedula):
        perfil = get_object_or_404(
            DatosPersonales,
            numero_cedula=cedula,
            perfil_activo=True
        )
        
        # Crear el PDF en memoria
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER,
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12,
            spaceBefore=12,
        )
        
        # Título
        story.append(Paragraph(f"{perfil.nombres} {perfil.apellidos}", title_style))
        story.append(Paragraph(perfil.descripcion_perfil, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Datos personales
        story.append(Paragraph("DATOS PERSONALES", heading_style))
        datos_personales = [
            ['Cédula:', perfil.numero_cedula],
            ['Fecha de Nacimiento:', perfil.fecha_nacimiento.strftime('%d/%m/%Y')],
            ['Edad:', f"{perfil.get_edad()} años"],
            ['Nacionalidad:', perfil.nacionalidad],
            ['Estado Civil:', perfil.estado_civil],
            ['Teléfono:', str(perfil.telefono_fijo or perfil.telefono_convencional or 'N/A')],
            ['Dirección:', perfil.direccion_domiciliaria],
        ]
        if perfil.sitio_web:
            datos_personales.append(['Sitio Web:', perfil.sitio_web])
        
        tabla = Table(datos_personales, colWidths=[2*inch, 4*inch])
        tabla.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(tabla)
        story.append(Spacer(1, 0.3*inch))
        
        # Experiencia laboral
        experiencias = perfil.experiencias.filter(
            activar_para_que_se_vea_en_front=True
        ).order_by('-fecha_inicio_gestion')
        
        if experiencias:
            story.append(Paragraph("EXPERIENCIA LABORAL", heading_style))
            for exp in experiencias:
                fecha_inicio = exp.fecha_inicio_gestion.strftime('%m/%Y')
                fecha_fin = exp.fecha_fin_gestion.strftime('%m/%Y') if exp.fecha_fin_gestion else 'Actualidad'
                
                story.append(Paragraph(
                    f"<b>{exp.cargo_desempenado}</b> - {exp.nombre_empresa}",
                    styles['Normal']
                ))
                story.append(Paragraph(
                    f"{fecha_inicio} - {fecha_fin} | {exp.lugar_empresa}",
                    styles['Normal']
                ))
                story.append(Paragraph(exp.descripcion_funciones, styles['Normal']))
                story.append(Spacer(1, 0.15*inch))
        
        # Cursos
        cursos = perfil.cursos.filter(
            activar_para_que_se_vea_en_front=True
        ).order_by('-fecha_inicio')
        
        if cursos:
            story.append(Paragraph("CURSOS Y CAPACITACIONES", heading_style))
            for curso in cursos:
                periodo = f"{curso.fecha_inicio.strftime('%m/%Y')} - {curso.fecha_fin.strftime('%m/%Y')}"
                story.append(Paragraph(
                    f"<b>{curso.nombre_curso}</b> - {curso.entidad_patrocinadora}",
                    styles['Normal']
                ))
                story.append(Paragraph(
                    f"{periodo} | {curso.total_horas} horas",
                    styles['Normal']
                ))
                story.append(Spacer(1, 0.1*inch))
        
        # Reconocimientos
        reconocimientos = perfil.reconocimientos.filter(
            activar_para_que_se_vea_en_front=True
        ).order_by('-fecha_reconocimiento')
        
        if reconocimientos:
            story.append(Paragraph("RECONOCIMIENTOS", heading_style))
            for rec in reconocimientos:
                story.append(Paragraph(
                    f"<b>{rec.tipo_reconocimiento}</b> - {rec.entidad_patrocinadora}",
                    styles['Normal']
                ))
                story.append(Paragraph(
                    f"{rec.fecha_reconocimiento.strftime('%m/%Y')} - {rec.descripcion_reconocimiento}",
                    styles['Normal']
                ))
                story.append(Spacer(1, 0.1*inch))
        
        # Productos académicos
        productos_academicos = perfil.productos_academicos.filter(
            activar_para_que_se_vea_en_front=True
        )
        
        if productos_academicos:
            story.append(Paragraph("PRODUCTOS ACADÉMICOS", heading_style))
            for prod in productos_academicos:
                story.append(Paragraph(
                    f"<b>{prod.nombre_recurso}</b> ({prod.clasificador})",
                    styles['Normal']
                ))
                story.append(Paragraph(prod.descripcion, styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
        
        # Construir PDF
        doc.build(story)
        
        # Preparar respuesta
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="CV_{perfil.nombres}_{perfil.apellidos}.pdf"'
        
        return response
