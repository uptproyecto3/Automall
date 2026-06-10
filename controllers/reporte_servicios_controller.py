from flask import Blueprint, request, redirect, url_for, flash, make_response
from models.servicios import Servicios
from utils.permisos import requiere_permiso
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from io import BytesIO

reporte_servicios_bp = Blueprint('reporte_servicios', __name__)


@reporte_servicios_bp.route('/servicios/reporte/generar', methods=['GET'])
@requiere_permiso('servicios', 'p_leer')
def generar_reporte_servicios():
    cod_servicio = request.args.get('cod_servicio', '').strip()
    nombre_servicio = request.args.get('nombre_servicio', '').strip()
    estado = request.args.get('estado', '').strip()
    placa = request.args.get('placa', '').strip()
    accion = request.args.get('accion', 'ver').strip()

    datos = Servicios.filtrar_reporte(
        cod_servicio, nombre_servicio, estado, placa
    )

    if not datos:
        flash('No se encontraron registros para los filtros seleccionados.', 'warning')
        return redirect(url_for('servicios.listar_servicios'))

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=40,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='CenterTitle',
        parent=styles['Title'],
        alignment=TA_CENTER
    ))

    story = []
    story.append(Paragraph('Reporte de Servicios', styles['CenterTitle']))
    story.append(Spacer(1, 12))

    encabezados = ['Código', 'Servicio', 'Estado', 'Costo', 'Descripción', 'Placa']
    filas = [encabezados]

    for s in datos:
        filas.append([
            str(s.get('cod_servicios', '')),
            str(s.get('nombre_servicio', '')),
            str(s.get('estado', '')),
            str(s.get('costo', '')),
            str(s.get('descripcion_especifica', '')),
            str(s.get('placa', ''))
        ])

    tabla = Table(filas, repeatRows=1)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#343a40')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    story.append(tabla)
    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'

    if accion == 'descargar':
        response.headers['Content-Disposition'] = 'attachment; filename=reporte_servicios.pdf'
    else:
        response.headers['Content-Disposition'] = 'inline; filename=reporte_servicios.pdf'

    return response