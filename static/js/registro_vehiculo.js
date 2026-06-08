document.addEventListener('DOMContentLoaded', function() {
    console.log("JS de Automall cargado y listo.");

    // --- LÓGICA DE MARCA/MODELO (Para Registro y Editar) ---
    const selectMarca = document.getElementById('select-marca');
    const selectModelo = document.getElementById('select-modelo');

    if (selectMarca && selectModelo) {
        selectModelo.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            const marcaId = selectedOption.getAttribute('data-marca');
            if (marcaId) selectMarca.value = marcaId;
        });
    }

    // --- LÓGICA DE IMAGEN  ---
    const inputImg = document.getElementById('input-nueva-img');
    const imgActual = document.getElementById('img-actual');
    if (inputImg && imgActual) {
        inputImg.onchange = evt => {
            const [file] = inputImg.files;
            if (file) imgActual.src = URL.createObjectURL(file);
        }
    }

    // --- LÓGICA DEL MODAL DE DETALLES  ---
    const modalDetalles = document.getElementById('modalDetalles');
    if (modalDetalles) {
        modalDetalles.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const v = JSON.parse(button.getAttribute('data-vehiculo'));

            console.log("Cargando datos en modal para placa:", v.placa);
            document.getElementById('det-placa').textContent = v.placa;
            document.getElementById('det-vehiculo').textContent = `${v.nombre_marca} ${v.nombre_modelo}`;
            document.getElementById('det-anio').textContent = v.anio;
            document.getElementById('det-estado').textContent = v.estado;

            if (v.fecha_ingreso) {
                const fechaObj = new Date(v.fecha_ingreso);
                const opciones = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
                let fechaFormateada = fechaObj.toLocaleDateString('es-ES', opciones);
                
                fechaFormateada = fechaFormateada.charAt(0).toUpperCase() + fechaFormateada.slice(1);
                document.getElementById('det-fecha').textContent = fechaFormateada;
            } else {
                document.getElementById('det-fecha').textContent = "No registrada";
            }
            // ---------------------------------------

            document.getElementById('det-prov').textContent = v.nombre_proveedor;
            document.getElementById('det-obs').textContent = v.otro_documento || v.descripcion || "Sin observaciones.";

            const accContainer = document.getElementById('det-accesorios');
            accContainer.innerHTML = ''; // Limpiar previo
            const accesorios = [
                { key: 'copia_llaves', label: 'Copia de Llaves' },
                { key: 'repuesto', label: 'Caucho Repuesto' },
                { key: 'triangulo', label: 'Triángulo Seg.' }
            ];

            accesorios.forEach(acc => {
                const span = document.createElement('span');
                span.className = `badge ${v[acc.key] ? 'bg-success' : 'bg-light text-muted border'}`;
                span.style.padding = "8px 12px";
                span.innerHTML = `<i class="bi bi-${v[acc.key] ? 'check-circle' : 'x-circle'} me-1"></i> ${acc.label}`;
                accContainer.appendChild(span);
            });

            const docsList = document.getElementById('det-docs');
            docsList.innerHTML = '';
            const documentos = [
                { key: 'original_totalPropiedad', label: 'Título de Propiedad' },
                { key: 'experticia_transito', label: 'Experticia de Tránsito' },
                { key: 'certificado_origen', label: 'Certificado de Origen' },
                { key: 'carnet_circulacion', label: 'Carnet Circulación' },
                { key: 'reserva_dominio', label: 'Reserva de Dominio' },
                { key: 'garantia_vehiculo', label: 'Garantía Vehículo' },
                { key: 'certificado_garantia', label: 'Certificado de Garantía' },
                { key: 'manual_vehiculoGarantia', label: 'Manual del Vehículo' },
                { key: 'finiquito', label: 'Finiquito' },
                { key: 'resguardo', label: 'Resguardo' },
                { key: 'seguro', label: 'Seguro / Póliza' },
                { key: 'factura_compra', label: 'Factura Compra' }
            ];

            documentos.forEach(doc => {
                const li = document.createElement('li');
                li.className = "list-group-item d-flex justify-content-between align-items-center py-2 border-0 border-bottom";
                const icon = v[doc.key] ? 'check-lg text-success' : 'x-lg text-danger';
                li.innerHTML = `<span>${doc.label}</span> <i class="bi bi-${icon} fw-bold"></i>`;
                docsList.appendChild(li);
            });
        });
    }
    // --- LÓGICA DEL MODAL DE VER DETALLES EN INICIO   ---
    const modalDetalleVenta = document.getElementById('modalDetalleVenta');

    if (modalDetalleVenta) {
        modalDetalleVenta.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const v = JSON.parse(button.getAttribute('data-vehiculo'));

            const imgElement = document.getElementById('modal-v-img');
            imgElement.src = ""; 

            const imgPath = v.imagen_url ? `/static/${v.imagen_url}` : '/static/img/no-photo.jpg';
            
            setTimeout(() => {
                imgElement.src = imgPath;
            }, 50);

            document.getElementById('modal-v-marca').textContent = v.nombre_marca;
            document.getElementById('modal-v-modelo').textContent = v.nombre_modelo;
            document.getElementById('modal-v-anio').textContent = `Modelo ${v.anio}`;
            document.getElementById('modal-v-desc').textContent = v.descripcion || "Sin descripción disponible.";

            const precioFormateado = new Intl.NumberFormat('en-US', { 
                style: 'currency', 
                currency: 'USD',
                minimumFractionDigits: 2 
            }).format(v.precio);
            
            document.getElementById('modal-v-precio').textContent = precioFormateado;
        });
    }
});