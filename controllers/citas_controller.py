from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.citas import seleccionar
citas_bp = Blueprint('citas', __name__)



@citas_bp.route('/consultar')
def consultar():
    
    lista_citas = seleccionar.obtener_citas_transito()
       
    return render_template('citas/consultar.html', citas=lista_citas)

@citas_bp.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if request.method == 'POST':
        fecha = request.form.get('fecha_cita')
        hora = request.form.get('hora_cita')
        cod_catalogo = request.form.get('cod_catalogo')

        if not fecha or not hora or not cod_catalogo:
            flash("Por favor, complete todos los campos del formulario", "danger")
            lista_vehiculos = seleccionar.obtener_todos()
            return render_template('citas/agendar.html', seleccionar=lista_vehiculos)


        seleccionar.registrar_citas(fecha, hora, cod_catalogo)
        
        flash("¡Su cita ha sido agendada con éxito!", "success")
        # 🌟 OBLIGATORIO: Redireccionamos a la vista de consulta tras registrar
        return redirect(url_for('citas.consultar')) 

    # --- 🌟 BLOQUE GET (Cuando se entra a la página por primera vez) ---
    lista_vehiculos = seleccionar.obtener_todos()
    return render_template('citas/agendar.html', seleccionar=lista_vehiculos)

