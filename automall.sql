CREATE DATABASE IF NOT EXISTS automall;
USE automall;

CREATE TABLE proveedor (
    cedula_proveedor INT(11) PRIMARY KEY,
    razon_social VARCHAR(100), 
    telefono VARCHAR(20),
    direccion VARCHAR(250),
    tipo VARCHAR(50),
    estado VARCHAR(20)
);

CREATE TABLE marca (
    cod_marca INT(11) PRIMARY KEY,
    nombre_marca VARCHAR(50),
    estado VARCHAR(20)
);

CREATE TABLE modelo (
    cod_modelo INT(11) PRIMARY KEY,
    nombre_modelo VARCHAR(50),
    estado VARCHAR(20)
);

CREATE TABLE documentacion (
    cod_documento INT(11) PRIMARY KEY,
    original_totalPropiedad TINYINT(1),
    experticia_transito TINYINT(1),
    certificado_origen TINYINT(1),
    carnet_circulacion TINYINT(1),
    reserva_dominio TINYINT(1),
    garantia_vehiculo TINYINT(1),
    certificado_garantia TINYINT(1),
    manual_vehiculoGarantia TINYINT(1),
    finiquito TINYINT(1),
    resguardo TINYINT(1),
    fecha_transferencia TINYINT(1),
    seguro TINYINT(1),
    factura_compra TINYINT(1),
    fecha_ingreso DATE,
    otro_documento VARCHAR(255)
);

CREATE TABLE taller (
    cod_taller INT(11) PRIMARY KEY,
    nombre_taller VARCHAR(100),
    direccion VARCHAR(250),
    estado VARCHAR(20)
);

CREATE TABLE metodo_pago (
    cod_metodo INT(11) PRIMARY KEY,
    nombre_metodo VARCHAR(50) NOT NULL,
    estado VARCHAR(20)
);

CREATE TABLE banco (
    cod_banco INT(11) PRIMARY KEY,
    nombre_banco VARCHAR(100) NOT NULL,
    estado VARCHAR(20)
);

CREATE TABLE moneda (
    cod_moneda INT(11) PRIMARY KEY,
    nombre_moneda VARCHAR(50) NOT NULL,
    simbolo VARCHAR(10),
    estado VARCHAR(20)
);

CREATE TABLE vehiculo (
    placa VARCHAR(20) PRIMARY KEY,
    color VARCHAR(50),
    anio INT(11),
    tipo TEXT,
    kilometraje INT(20),
    estado VARCHAR(20),
    cod_marca INT(11),
    cod_modelo INT(11),
    cod_documento INT(11),
    cedula_proveedor INT(11),
    FOREIGN KEY (cod_marca) REFERENCES marca(cod_marca),
    FOREIGN KEY (cod_modelo) REFERENCES modelo(cod_modelo),
    FOREIGN KEY (cod_documento) REFERENCES documentacion(cod_documento),
    FOREIGN KEY (cedula_proveedor) REFERENCES proveedor(cedula_proveedor)
);

CREATE TABLE accesorio (
    cod_accesorio INT(11) PRIMARY KEY,
    copia_llaves TINYINT(1),
    repuesto TINYINT(1),
    triangulo TINYINT(1),
    placa VARCHAR(20),
    FOREIGN KEY (placa) REFERENCES vehiculo(placa)
);

CREATE TABLE catalogo (
    cod_catalogo INT(11) PRIMARY KEY,
    estado VARCHAR(20),
    precio DECIMAL(10,2),
    descripcion TEXT,
    fecha_publicacion DATE,
    placa VARCHAR(20),
    FOREIGN KEY (placa) REFERENCES vehiculo(placa)
);

CREATE TABLE citas (
    cod_citas INT(11) PRIMARY KEY,
    estado VARCHAR(20),
    fecha DATE,
    hora TIME,
    cod_catalogo INT(11),
    FOREIGN KEY (cod_catalogo) REFERENCES catalogo(cod_catalogo)
);

CREATE TABLE imagen (
    cod_imagen INT(11) PRIMARY KEY,
    URL VARCHAR(300),
    placa VARCHAR(20),
    FOREIGN KEY (placa) REFERENCES vehiculo(placa)
);

CREATE TABLE mantenimiento_operacional (
    cod_mantenimiento INT(11) PRIMARY KEY,
    descripcion_general TEXT,
    quien_autoriza VARCHAR(30),
    estado VARCHAR(20)
);

CREATE TABLE detalle (
    cod_detalle INT(11) PRIMARY KEY,
    tipo VARCHAR(20),
    fecha_salida DATE,
    fecha_entrega DATE,
    cod_mantenimiento INT(11),
    cedula_proveedor INT(11),
    placa VARCHAR(20), 
    cod_taller INT(11), 
    FOREIGN KEY (cod_mantenimiento) REFERENCES mantenimiento_operacional(cod_mantenimiento),
    FOREIGN KEY (cedula_proveedor) REFERENCES proveedor(cedula_proveedor),
    FOREIGN KEY (placa) REFERENCES vehiculo(placa),
    FOREIGN KEY (cod_taller) REFERENCES taller(cod_taller)
);

CREATE TABLE servicios_realizados (
    cod_servicios INT(11) PRIMARY KEY,
    nombre_servicio VARCHAR(100),
    estado VARCHAR(20)
);

CREATE TABLE detalle_servicio (
    cod_detalle_servicio INT(11) PRIMARY KEY,
    cod_detalle INT(11),
    cod_servicios INT(11),
    costo DECIMAL(10,2),
    descripcion_especifica VARCHAR(250),
    FOREIGN KEY (cod_detalle) REFERENCES detalle(cod_detalle),
    FOREIGN KEY (cod_servicios) REFERENCES servicios_realizados(cod_servicios)
);

CREATE TABLE compras_accesorios (
    cod_compras INT(11) PRIMARY KEY,
    fecha DATE,
    monto_total DECIMAL(20,2),
    estado VARCHAR(20)
);

CREATE TABLE det_compra (
    cod_det_compra INT(11) PRIMARY KEY,
    producto VARCHAR(50),
    cantidad INT(11),
    costo_unitario DECIMAL(10,2),
    cod_compras INT(11),
    FOREIGN KEY (cod_compras) REFERENCES compras_accesorios(cod_compras)
);

CREATE TABLE insumos (
    cod_insumo INT(11) PRIMARY KEY,
    nombre_insumo VARCHAR(100) NOT NULL,
    descripcion TEXT,
    stock INT(11),
    cod_compras INT(11),
    FOREIGN KEY (cod_compras) REFERENCES compras_accesorios(cod_compras)
);

CREATE TABLE ventas (
    cod_venta INT(11) PRIMARY KEY,
    estado VARCHAR(45),
    fecha_venta DATE, 
    tipo_venta VARCHAR(45),
    id_usuario INT(11) -- Relación lógica (en código/API) al ID de t_usuario
);

CREATE TABLE det_venta (
    cod_det_venta INT(11) PRIMARY KEY,
    poder TINYINT(1),
    traspaso_papel TINYINT(1), 
    cod_venta INT(11),
    placa VARCHAR(20),
    FOREIGN KEY (cod_venta) REFERENCES ventas(cod_venta),
    FOREIGN KEY (placa) REFERENCES vehiculo(placa)
);

CREATE TABLE cuentas_por_cobrar (
    cod_cuentas INT(11) PRIMARY KEY,
    deuda_total DECIMAL(10,2),
    saldo_pendiente DECIMAL(10,2),
    fecha_vencimiento DATETIME,
    estado VARCHAR(20),
    cod_venta INT(11),
    FOREIGN KEY (cod_venta) REFERENCES ventas(cod_venta)
);

CREATE TABLE pago_cuentas (
    cod_pagos INT(11) PRIMARY KEY,
    monto_abonado DECIMAL(10,2),
    fecha_pago DATETIME,
    cod_cuentas INT(11),
    cod_metodo INT(11),  
    cod_banco INT(11),   
    cod_moneda INT(11),  
    FOREIGN KEY (cod_cuentas) REFERENCES cuentas_por_cobrar(cod_cuentas),
    FOREIGN KEY (cod_metodo) REFERENCES metodo_pago(cod_metodo),
    FOREIGN KEY (cod_banco) REFERENCES banco(cod_banco),
    FOREIGN KEY (cod_moneda) REFERENCES moneda(cod_moneda)
);