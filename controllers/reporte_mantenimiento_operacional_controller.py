from flask import Blueprint, request, redirect, url_for, flash, make_response
from models.mantenimiento_operacional import MantenimientoOperacional
from utils.permisos import requiere_permiso
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from io import BytesIO

reporte_mantenimiento_operacional_bp = Blueprint('reporte_mantenimiento_operacional', __name__)


@reporte_mantenimiento_operacional_bp.route('/mantenimiento-operacional/reporte/generar', methods=['GET'])
@requiere_permiso('mantenimiento_operacional', 'p_leer')
def generar_reporte_mantenimiento():
    cod_mantenimiento = request.args.get('cod_mantenimiento', '').strip()
    placa = request.args.get('placa', '').strip()
    estado = request.args.get('estado', '').strip()
    cod_taller = request.args.get('cod_taller', '').strip()
    fecha_inicio = request.args.get('fecha_inicio', '').strip()
    fecha_fin = request.args.get('fecha_fin', '').strip()
    accion = request.args.get('accion', 'ver').strip()

    datos = MantenimientoOperacional.filtrar_reporte(
        cod_mantenimiento, placa, estado, cod_taller, fecha_inicio, fecha_fin
    )

    if not datos:
        flash('No se encontraron registros para los filtros seleccionados.', 'warning')
        return redirect(url_for('mantenimiento_operacional.listar_mantenimiento'))

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
    story.append(Paragraph('Reporte de Mantenimiento Operacional', styles['CenterTitle']))
    story.append(Spacer(1, 12))

    encabezados = ['Código', 'Descripción', 'Autoriza', 'Estado', 'Tipo', 'Salida', 'Entrega', 'Placa', 'Taller']
    filas = [encabezados]

    for m in datos:
        filas.append([
            str(m.get('cod_mantenimiento', '')),
            str(m.get('descripcion_general', '')),
            str(m.get('quien_autoriza', '')),
            str(m.get('estado', '')),
            str(m.get('tipo', '')),
            str(m.get('fecha_salida', '')),
            str(m.get('fecha_entrega', '')),
            str(m.get('placa', '')),
            str(m.get('nombre_taller', ''))
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
        response.headers['Content-Disposition'] = 'attachment; filename=reporte_mantenimiento_operacional.pdf'
    else:
        response.headers['Content-Disposition'] = 'inline; filename=reporte_mantenimiento_operacional.pdf'

    return response