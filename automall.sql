-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 03-07-2026 a las 04:04:51
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `automall`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `accesorio`
--

CREATE TABLE `accesorio` (
  `cod_accesorio` int(11) NOT NULL,
  `copia_llaves` tinyint(1) DEFAULT 0,
  `repuesto` tinyint(1) DEFAULT 0,
  `triangulo` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `accesorio`
--

INSERT INTO `accesorio` (`cod_accesorio`, `copia_llaves`, `repuesto`, `triangulo`) VALUES
(1, 1, 1, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `banco`
--

CREATE TABLE `banco` (
  `cod_banco` int(11) NOT NULL,
  `cod_oficial` int(11) NOT NULL,
  `nombre_banco` varchar(100) NOT NULL,
  `estado` varchar(20) DEFAULT 'Activo',
  `fecha_registro` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `catalogo`
--

CREATE TABLE `catalogo` (
  `cod_catalogo` int(11) NOT NULL,
  `estado` varchar(50) DEFAULT 'Disponible',
  `precio` decimal(10,2) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha_publicacion` datetime NOT NULL,
  `placa` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `catalogo`
--

INSERT INTO `catalogo` (`cod_catalogo`, `estado`, `precio`, `descripcion`, `fecha_publicacion`, `placa`) VALUES
(1, 'Disponible', 58000.00, 'Gran vehiculo bueno', '0000-00-00 00:00:00', 'AH8L71D');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `citas`
--

CREATE TABLE `citas` (
  `cod_citas` int(11) NOT NULL,
  `estado` varchar(20) DEFAULT 'Pendiente',
  `fecha` date NOT NULL,
  `hora` time DEFAULT NULL,
  `cod_catalogo` int(11) DEFAULT NULL,
  `cedula_usuario` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `compras_accesorios`
--

CREATE TABLE `compras_accesorios` (
  `cod_compras` int(11) NOT NULL,
  `fecha_compra` date NOT NULL,
  `precio` decimal(20,2) DEFAULT NULL,
  `tipo_compra` varchar(50) NOT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `observaciones` varchar(100) NOT NULL,
  `rif_cedula_proveedor` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cuentas_por_cobrar`
--

CREATE TABLE `cuentas_por_cobrar` (
  `cod_cuentas` int(11) NOT NULL,
  `deuda_total` int(30) DEFAULT NULL,
  `fecha_vencimiento` datetime DEFAULT NULL,
  `fecha_emision` date NOT NULL,
  `estado` varchar(20) DEFAULT 'Pendiente',
  `cod_venta` int(11) DEFAULT NULL,
  `deuda` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `det_banco`
--

CREATE TABLE `det_banco` (
  `cod_det_banco` int(11) NOT NULL,
  `monto` decimal(12,2) NOT NULL,
  `referencia` varchar(50) NOT NULL,
  `cod_banco` int(11) NOT NULL,
  `cod_det_pago` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `det_compra`
--

CREATE TABLE `det_compra` (
  `cod_det_compra` int(11) NOT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `cod_insumo` int(11) NOT NULL,
  `cod_compras` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `det_mantenimiento`
--

CREATE TABLE `det_mantenimiento` (
  `cod_detalle` int(11) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `fecha_solicitud` date NOT NULL,
  `fecha_completada` date DEFAULT NULL,
  `cod_mantenimiento` int(11) DEFAULT NULL,
  `placa` varchar(20) NOT NULL,
  `cod_taller` int(11) NOT NULL,
  `cedula_usuario` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `det_nom_digital`
--

CREATE TABLE `det_nom_digital` (
  `cod_det_digital` int(11) NOT NULL,
  `monto` decimal(12,2) NOT NULL,
  `referencia` varchar(50) NOT NULL,
  `cod_mon_digital` int(11) NOT NULL,
  `cod_det_pago` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `det_pago`
--

CREATE TABLE `det_pago` (
  `cod_det_pago` int(11) NOT NULL,
  `tipo_pago` varchar(20) NOT NULL,
  `fecha_det_pago` datetime NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `cod_pagos` int(11) NOT NULL,
  `cod_metodo` int(11) NOT NULL,
  `cod_moneda` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `det_salida`
--

CREATE TABLE `det_salida` (
  `cod_salida` int(11) NOT NULL,
  `fecha_salida` date NOT NULL,
  `cantidad_usada` int(50) NOT NULL,
  `descrpcion` varchar(250) NOT NULL,
  `placa` varchar(20) NOT NULL,
  `cod_insumo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `det_servicios`
--

CREATE TABLE `det_servicios` (
  `cod_det_servicio` int(11) NOT NULL,
  `costo_final` decimal(10,2) DEFAULT NULL,
  `descripcion_especifica` varchar(250) DEFAULT NULL,
  `fecha_realizacion` date NOT NULL,
  `placa` varchar(20) NOT NULL,
  `cod_servicios` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `det_venta`
--

CREATE TABLE `det_venta` (
  `cod_det_venta` int(11) NOT NULL,
  `poder` tinyint(1) DEFAULT 0,
  `traspaso_papel` tinyint(1) DEFAULT 0,
  `precio` decimal(12,2) NOT NULL,
  `placa` varchar(20) DEFAULT NULL,
  `cod_venta` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `documentacion`
--

CREATE TABLE `documentacion` (
  `cod_documento` int(11) NOT NULL,
  `original_totalPropiedad` tinyint(1) DEFAULT 0,
  `experticia_transito` tinyint(1) DEFAULT 0,
  `certificado_origen` tinyint(1) DEFAULT 0,
  `carnet_circulacion` tinyint(1) DEFAULT 0,
  `reserva_dominio` tinyint(1) DEFAULT 0,
  `garantia_vehiculo` tinyint(1) DEFAULT 0,
  `certificado_garantia` tinyint(1) DEFAULT 0,
  `manual_vehiculoGarantia` tinyint(1) DEFAULT 0,
  `finiquito` tinyint(1) DEFAULT 0,
  `resguardo` tinyint(1) DEFAULT 0,
  `fecha_transferencia` tinyint(1) DEFAULT 0,
  `seguro` tinyint(1) DEFAULT 0,
  `factura_compra` tinyint(1) DEFAULT 0,
  `fecha_ingreso` date NOT NULL,
  `otro_documento` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `documentacion`
--

INSERT INTO `documentacion` (`cod_documento`, `original_totalPropiedad`, `experticia_transito`, `certificado_origen`, `carnet_circulacion`, `reserva_dominio`, `garantia_vehiculo`, `certificado_garantia`, `manual_vehiculoGarantia`, `finiquito`, `resguardo`, `fecha_transferencia`, `seguro`, `factura_compra`, `fecha_ingreso`, `otro_documento`) VALUES
(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, '0000-00-00', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historia_estado_vehiculo`
--

CREATE TABLE `historia_estado_vehiculo` (
  `cod_historia` int(11) NOT NULL,
  `placa` varchar(20) NOT NULL,
  `estado` varchar(50) DEFAULT NULL,
  `fecha_cambio` datetime DEFAULT current_timestamp(),
  `observaciones` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `imagen`
--

CREATE TABLE `imagen` (
  `cod_imagen` int(11) NOT NULL,
  `URL` varchar(300) NOT NULL,
  `fecha_subida` date NOT NULL,
  `placa` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `insumos`
--

CREATE TABLE `insumos` (
  `cod_insumo` int(11) NOT NULL,
  `nombre_insumo` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `stock` int(11) DEFAULT 0,
  `unidad_medida` varchar(20) NOT NULL,
  `estado` tinyint(1) NOT NULL DEFAULT 1,
  `fecha_registro` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mantenimiento`
--

CREATE TABLE `mantenimiento` (
  `cod_mantenimiento` int(11) NOT NULL,
  `descripcion_general` text DEFAULT NULL,
  `quien_autoriza` varchar(30) NOT NULL,
  `estado` varchar(20) DEFAULT 'Pendiente'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `marca`
--

CREATE TABLE `marca` (
  `cod_marca` int(11) NOT NULL,
  `nombre_marca` varchar(50) NOT NULL,
  `estado` varchar(20) DEFAULT 'Activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `marca`
--

INSERT INTO `marca` (`cod_marca`, `nombre_marca`, `estado`) VALUES
(1, 'Volswaguen', 'Activo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `metodo_pago`
--

CREATE TABLE `metodo_pago` (
  `cod_metodo` int(11) NOT NULL,
  `nombre_metodo` varchar(50) NOT NULL,
  `requiere_referencia` tinyint(1) NOT NULL,
  `estado` varchar(20) DEFAULT 'Activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `modelo`
--

CREATE TABLE `modelo` (
  `cod_modelo` int(11) NOT NULL,
  `nombre_modelo` varchar(50) NOT NULL,
  `estado` varchar(20) DEFAULT 'Activo',
  `cod_marca` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `modelo`
--

INSERT INTO `modelo` (`cod_modelo`, `nombre_modelo`, `estado`, `cod_marca`) VALUES
(1, 'Hilux', 'Activo', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `moneda`
--

CREATE TABLE `moneda` (
  `cod_moneda` int(11) NOT NULL,
  `nombre_moneda` varchar(50) NOT NULL,
  `simbolo` varchar(10) DEFAULT NULL,
  `estado` varchar(20) DEFAULT 'Activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `moneda_digital`
--

CREATE TABLE `moneda_digital` (
  `cod_mon_digital` int(11) NOT NULL,
  `nombre_digital` varchar(50) NOT NULL,
  `simbolo_digital` varchar(30) DEFAULT NULL,
  `estado` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pago_cuentas`
--

CREATE TABLE `pago_cuentas` (
  `cod_pagos` int(11) NOT NULL,
  `monto_abonado` decimal(10,2) DEFAULT NULL,
  `fecha_pago` datetime NOT NULL,
  `referencia` varchar(50) NOT NULL,
  `cod_cuentas` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `propietario`
--

CREATE TABLE `propietario` (
  `cedula_propietario` int(11) NOT NULL,
  `razon_social` varchar(100) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `correo` varchar(50) DEFAULT NULL,
  `direccion` varchar(250) DEFAULT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  `estado` varchar(20) DEFAULT 'Activo',
  `fecha_registro` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `propietario`
--

INSERT INTO `propietario` (`cedula_propietario`, `razon_social`, `telefono`, `correo`, `direccion`, `tipo`, `estado`, `fecha_registro`) VALUES
(28123456, 'Alberto Perez', '04125558744', 'alberto@mail.com', 'Cbudare agua viva', 'Dueño', 'Activo', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedor_compra`
--

CREATE TABLE `proveedor_compra` (
  `rif_cedula_proveedor` int(11) NOT NULL,
  `razon social` varchar(250) NOT NULL,
  `direccion` text NOT NULL,
  `telefono` int(20) NOT NULL,
  `correo` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios`
--

CREATE TABLE `servicios` (
  `cod_servicios` int(11) NOT NULL,
  `nombre_servicio` varchar(100) DEFAULT NULL,
  `costo_base` decimal(10,2) DEFAULT NULL,
  `estado` varchar(20) DEFAULT 'Activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `taller`
--

CREATE TABLE `taller` (
  `cod_taller` int(11) NOT NULL,
  `nombre_taller` varchar(100) NOT NULL,
  `direccion` varchar(250) DEFAULT NULL,
  `estado` varchar(20) DEFAULT 'Activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tasa_cambio`
--

CREATE TABLE `tasa_cambio` (
  `id` int(11) NOT NULL,
  `valor` decimal(10,4) NOT NULL,
  `fecha` date NOT NULL,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tasa_cambio`
--

INSERT INTO `tasa_cambio` (`id`, `valor`, `fecha`, `creado_en`) VALUES
(1, 596.7824, '2026-06-17', '2026-06-17 05:14:45'),
(2, 607.3919, '2026-06-20', '2026-06-21 03:23:14'),
(3, 617.6388, '2026-06-23', '2026-06-24 02:56:24'),
(4, 617.6388, '2026-06-24', '2026-06-24 04:05:01'),
(5, 639.7029, '2026-07-02', '2026-07-02 05:31:42');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_vehiculo`
--

CREATE TABLE `tipo_vehiculo` (
  `cod_tipo` int(11) NOT NULL,
  `nombre_tipo` varchar(50) NOT NULL,
  `descripcion` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipo_vehiculo`
--

INSERT INTO `tipo_vehiculo` (`cod_tipo`, `nombre_tipo`, `descripcion`) VALUES
(1, 'Sedan', NULL),
(2, 'Pick-up', NULL),
(3, 'Coupe', NULL),
(4, 'Suv', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vehiculo`
--

CREATE TABLE `vehiculo` (
  `placa` varchar(20) NOT NULL,
  `color` varchar(50) NOT NULL,
  `anio` int(11) NOT NULL,
  `kilometraje` int(20) NOT NULL,
  `estado` varchar(20) DEFAULT 'Disponible',
  `cod_tipo` int(11) NOT NULL,
  `cod_modelo` int(11) NOT NULL,
  `cod_documento` int(11) NOT NULL,
  `cod_accesorio` int(11) NOT NULL,
  `cedula_propietario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `vehiculo`
--

INSERT INTO `vehiculo` (`placa`, `color`, `anio`, `kilometraje`, `estado`, `cod_tipo`, `cod_modelo`, `cod_documento`, `cod_accesorio`, `cedula_propietario`) VALUES
('AH8L71D', 'negro', 2026, 30000, 'Disponible', 2, 1, 1, 1, 28123456);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `cod_venta` int(11) NOT NULL,
  `estado` varchar(20) DEFAULT 'Pendiente',
  `fecha_venta` date NOT NULL,
  `tipo_venta` varchar(45) DEFAULT NULL,
  `cedula_usuario` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `accesorio`
--
ALTER TABLE `accesorio`
  ADD PRIMARY KEY (`cod_accesorio`);

--
-- Indices de la tabla `banco`
--
ALTER TABLE `banco`
  ADD PRIMARY KEY (`cod_banco`);

--
-- Indices de la tabla `catalogo`
--
ALTER TABLE `catalogo`
  ADD PRIMARY KEY (`cod_catalogo`),
  ADD KEY `fk_cat_vehiculo` (`placa`);

--
-- Indices de la tabla `citas`
--
ALTER TABLE `citas`
  ADD PRIMARY KEY (`cod_citas`),
  ADD KEY `fk_citas_cat` (`cod_catalogo`),
  ADD KEY `cedula_usuario` (`cedula_usuario`);

--
-- Indices de la tabla `compras_accesorios`
--
ALTER TABLE `compras_accesorios`
  ADD PRIMARY KEY (`cod_compras`),
  ADD KEY `rif_cedula_proveedor` (`rif_cedula_proveedor`);

--
-- Indices de la tabla `cuentas_por_cobrar`
--
ALTER TABLE `cuentas_por_cobrar`
  ADD PRIMARY KEY (`cod_cuentas`),
  ADD KEY `fk_cpc_venta` (`cod_venta`);

--
-- Indices de la tabla `det_banco`
--
ALTER TABLE `det_banco`
  ADD PRIMARY KEY (`cod_det_banco`),
  ADD KEY `fk_detbanco_banco` (`cod_banco`),
  ADD KEY `fk_detbanco_pago` (`cod_det_pago`);

--
-- Indices de la tabla `det_compra`
--
ALTER TABLE `det_compra`
  ADD PRIMARY KEY (`cod_det_compra`),
  ADD KEY `fk_detcomp_insumo` (`cod_insumo`),
  ADD KEY `fk_detcomp_compra` (`cod_compras`);

--
-- Indices de la tabla `det_mantenimiento`
--
ALTER TABLE `det_mantenimiento`
  ADD PRIMARY KEY (`cod_detalle`),
  ADD KEY `fk_detmant_mant` (`cod_mantenimiento`),
  ADD KEY `fk_detmant_veh` (`placa`),
  ADD KEY `fk_detmant_taller` (`cod_taller`),
  ADD KEY `cedula_usuario` (`cedula_usuario`);

--
-- Indices de la tabla `det_nom_digital`
--
ALTER TABLE `det_nom_digital`
  ADD PRIMARY KEY (`cod_det_digital`),
  ADD KEY `fk_detdig_moneda` (`cod_mon_digital`),
  ADD KEY `fk_detdig_pago` (`cod_det_pago`);

--
-- Indices de la tabla `det_pago`
--
ALTER TABLE `det_pago`
  ADD PRIMARY KEY (`cod_det_pago`),
  ADD KEY `fk_detpago_pagocuenta` (`cod_pagos`),
  ADD KEY `fk_detpago_metodo` (`cod_metodo`),
  ADD KEY `fk_detpago_moneda` (`cod_moneda`);

--
-- Indices de la tabla `det_salida`
--
ALTER TABLE `det_salida`
  ADD PRIMARY KEY (`cod_salida`),
  ADD KEY `placa` (`placa`),
  ADD KEY `cod_insumo` (`cod_insumo`);

--
-- Indices de la tabla `det_servicios`
--
ALTER TABLE `det_servicios`
  ADD PRIMARY KEY (`cod_det_servicio`),
  ADD KEY `fk_detserv_veh` (`placa`),
  ADD KEY `fk_detserv_serv` (`cod_servicios`);

--
-- Indices de la tabla `det_venta`
--
ALTER TABLE `det_venta`
  ADD PRIMARY KEY (`cod_det_venta`),
  ADD KEY `fk_detventa_veh` (`placa`),
  ADD KEY `fk_detventa_venta` (`cod_venta`);

--
-- Indices de la tabla `documentacion`
--
ALTER TABLE `documentacion`
  ADD PRIMARY KEY (`cod_documento`);

--
-- Indices de la tabla `historia_estado_vehiculo`
--
ALTER TABLE `historia_estado_vehiculo`
  ADD PRIMARY KEY (`cod_historia`),
  ADD KEY `fk_hist_vehiculo` (`placa`);

--
-- Indices de la tabla `imagen`
--
ALTER TABLE `imagen`
  ADD PRIMARY KEY (`cod_imagen`),
  ADD KEY `fk_img_vehiculo` (`placa`);

--
-- Indices de la tabla `insumos`
--
ALTER TABLE `insumos`
  ADD PRIMARY KEY (`cod_insumo`);

--
-- Indices de la tabla `mantenimiento`
--
ALTER TABLE `mantenimiento`
  ADD PRIMARY KEY (`cod_mantenimiento`);

--
-- Indices de la tabla `marca`
--
ALTER TABLE `marca`
  ADD PRIMARY KEY (`cod_marca`);

--
-- Indices de la tabla `metodo_pago`
--
ALTER TABLE `metodo_pago`
  ADD PRIMARY KEY (`cod_metodo`);

--
-- Indices de la tabla `modelo`
--
ALTER TABLE `modelo`
  ADD PRIMARY KEY (`cod_modelo`),
  ADD KEY `fk_modelo_marca` (`cod_marca`);

--
-- Indices de la tabla `moneda`
--
ALTER TABLE `moneda`
  ADD PRIMARY KEY (`cod_moneda`);

--
-- Indices de la tabla `moneda_digital`
--
ALTER TABLE `moneda_digital`
  ADD PRIMARY KEY (`cod_mon_digital`);

--
-- Indices de la tabla `pago_cuentas`
--
ALTER TABLE `pago_cuentas`
  ADD PRIMARY KEY (`cod_pagos`),
  ADD KEY `fk_pagocuenta_cpc` (`cod_cuentas`);

--
-- Indices de la tabla `propietario`
--
ALTER TABLE `propietario`
  ADD PRIMARY KEY (`cedula_propietario`);

--
-- Indices de la tabla `proveedor_compra`
--
ALTER TABLE `proveedor_compra`
  ADD PRIMARY KEY (`rif_cedula_proveedor`);

--
-- Indices de la tabla `servicios`
--
ALTER TABLE `servicios`
  ADD PRIMARY KEY (`cod_servicios`);

--
-- Indices de la tabla `taller`
--
ALTER TABLE `taller`
  ADD PRIMARY KEY (`cod_taller`);

--
-- Indices de la tabla `tasa_cambio`
--
ALTER TABLE `tasa_cambio`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `tipo_vehiculo`
--
ALTER TABLE `tipo_vehiculo`
  ADD PRIMARY KEY (`cod_tipo`);

--
-- Indices de la tabla `vehiculo`
--
ALTER TABLE `vehiculo`
  ADD PRIMARY KEY (`placa`),
  ADD UNIQUE KEY `uk_cod_documento` (`cod_documento`),
  ADD UNIQUE KEY `uk_cod_accesorio` (`cod_accesorio`),
  ADD KEY `fk_vehiculo_modelo` (`cod_modelo`),
  ADD KEY `cod_tipo` (`cod_tipo`),
  ADD KEY `cedula_propietario` (`cedula_propietario`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`cod_venta`),
  ADD KEY `cedula_usuario` (`cedula_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `accesorio`
--
ALTER TABLE `accesorio`
  MODIFY `cod_accesorio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `banco`
--
ALTER TABLE `banco`
  MODIFY `cod_banco` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `catalogo`
--
ALTER TABLE `catalogo`
  MODIFY `cod_catalogo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `citas`
--
ALTER TABLE `citas`
  MODIFY `cod_citas` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `compras_accesorios`
--
ALTER TABLE `compras_accesorios`
  MODIFY `cod_compras` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cuentas_por_cobrar`
--
ALTER TABLE `cuentas_por_cobrar`
  MODIFY `cod_cuentas` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `det_banco`
--
ALTER TABLE `det_banco`
  MODIFY `cod_det_banco` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `det_compra`
--
ALTER TABLE `det_compra`
  MODIFY `cod_det_compra` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `det_mantenimiento`
--
ALTER TABLE `det_mantenimiento`
  MODIFY `cod_detalle` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `det_nom_digital`
--
ALTER TABLE `det_nom_digital`
  MODIFY `cod_det_digital` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `det_pago`
--
ALTER TABLE `det_pago`
  MODIFY `cod_det_pago` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `det_salida`
--
ALTER TABLE `det_salida`
  MODIFY `cod_salida` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `det_servicios`
--
ALTER TABLE `det_servicios`
  MODIFY `cod_det_servicio` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `det_venta`
--
ALTER TABLE `det_venta`
  MODIFY `cod_det_venta` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `documentacion`
--
ALTER TABLE `documentacion`
  MODIFY `cod_documento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `historia_estado_vehiculo`
--
ALTER TABLE `historia_estado_vehiculo`
  MODIFY `cod_historia` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `imagen`
--
ALTER TABLE `imagen`
  MODIFY `cod_imagen` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `insumos`
--
ALTER TABLE `insumos`
  MODIFY `cod_insumo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `mantenimiento`
--
ALTER TABLE `mantenimiento`
  MODIFY `cod_mantenimiento` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `marca`
--
ALTER TABLE `marca`
  MODIFY `cod_marca` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `metodo_pago`
--
ALTER TABLE `metodo_pago`
  MODIFY `cod_metodo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `modelo`
--
ALTER TABLE `modelo`
  MODIFY `cod_modelo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `moneda`
--
ALTER TABLE `moneda`
  MODIFY `cod_moneda` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `moneda_digital`
--
ALTER TABLE `moneda_digital`
  MODIFY `cod_mon_digital` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pago_cuentas`
--
ALTER TABLE `pago_cuentas`
  MODIFY `cod_pagos` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `servicios`
--
ALTER TABLE `servicios`
  MODIFY `cod_servicios` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `taller`
--
ALTER TABLE `taller`
  MODIFY `cod_taller` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tasa_cambio`
--
ALTER TABLE `tasa_cambio`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `tipo_vehiculo`
--
ALTER TABLE `tipo_vehiculo`
  MODIFY `cod_tipo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `cod_venta` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `catalogo`
--
ALTER TABLE `catalogo`
  ADD CONSTRAINT `fk_cat_vehiculo` FOREIGN KEY (`placa`) REFERENCES `vehiculo` (`placa`);

--
-- Filtros para la tabla `citas`
--
ALTER TABLE `citas`
  ADD CONSTRAINT `fk_citas_cat` FOREIGN KEY (`cod_catalogo`) REFERENCES `catalogo` (`cod_catalogo`);

--
-- Filtros para la tabla `compras_accesorios`
--
ALTER TABLE `compras_accesorios`
  ADD CONSTRAINT `compras_accesorios_ibfk_1` FOREIGN KEY (`rif_cedula_proveedor`) REFERENCES `proveedor_compra` (`rif_cedula_proveedor`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `cuentas_por_cobrar`
--
ALTER TABLE `cuentas_por_cobrar`
  ADD CONSTRAINT `fk_cpc_venta` FOREIGN KEY (`cod_venta`) REFERENCES `ventas` (`cod_venta`) ON DELETE CASCADE;

--
-- Filtros para la tabla `det_banco`
--
ALTER TABLE `det_banco`
  ADD CONSTRAINT `fk_detbanco_banco` FOREIGN KEY (`cod_banco`) REFERENCES `banco` (`cod_banco`),
  ADD CONSTRAINT `fk_detbanco_pago` FOREIGN KEY (`cod_det_pago`) REFERENCES `det_pago` (`cod_det_pago`);

--
-- Filtros para la tabla `det_compra`
--
ALTER TABLE `det_compra`
  ADD CONSTRAINT `fk_detcomp_compra` FOREIGN KEY (`cod_compras`) REFERENCES `compras_accesorios` (`cod_compras`),
  ADD CONSTRAINT `fk_detcomp_insumo` FOREIGN KEY (`cod_insumo`) REFERENCES `insumos` (`cod_insumo`);

--
-- Filtros para la tabla `det_mantenimiento`
--
ALTER TABLE `det_mantenimiento`
  ADD CONSTRAINT `fk_detmant_mant` FOREIGN KEY (`cod_mantenimiento`) REFERENCES `mantenimiento` (`cod_mantenimiento`),
  ADD CONSTRAINT `fk_detmant_taller` FOREIGN KEY (`cod_taller`) REFERENCES `taller` (`cod_taller`),
  ADD CONSTRAINT `fk_detmant_veh` FOREIGN KEY (`placa`) REFERENCES `vehiculo` (`placa`);

--
-- Filtros para la tabla `det_nom_digital`
--
ALTER TABLE `det_nom_digital`
  ADD CONSTRAINT `fk_detdig_moneda` FOREIGN KEY (`cod_mon_digital`) REFERENCES `moneda_digital` (`cod_mon_digital`),
  ADD CONSTRAINT `fk_detdig_pago` FOREIGN KEY (`cod_det_pago`) REFERENCES `det_pago` (`cod_det_pago`);

--
-- Filtros para la tabla `det_pago`
--
ALTER TABLE `det_pago`
  ADD CONSTRAINT `fk_detpago_metodo` FOREIGN KEY (`cod_metodo`) REFERENCES `metodo_pago` (`cod_metodo`),
  ADD CONSTRAINT `fk_detpago_moneda` FOREIGN KEY (`cod_moneda`) REFERENCES `moneda` (`cod_moneda`),
  ADD CONSTRAINT `fk_detpago_pagocuenta` FOREIGN KEY (`cod_pagos`) REFERENCES `pago_cuentas` (`cod_pagos`);

--
-- Filtros para la tabla `det_salida`
--
ALTER TABLE `det_salida`
  ADD CONSTRAINT `det_salida_ibfk_1` FOREIGN KEY (`placa`) REFERENCES `vehiculo` (`placa`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `det_salida_ibfk_2` FOREIGN KEY (`cod_insumo`) REFERENCES `insumos` (`cod_insumo`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `det_servicios`
--
ALTER TABLE `det_servicios`
  ADD CONSTRAINT `fk_detserv_serv` FOREIGN KEY (`cod_servicios`) REFERENCES `servicios` (`cod_servicios`),
  ADD CONSTRAINT `fk_detserv_veh` FOREIGN KEY (`placa`) REFERENCES `vehiculo` (`placa`);

--
-- Filtros para la tabla `det_venta`
--
ALTER TABLE `det_venta`
  ADD CONSTRAINT `fk_detventa_veh` FOREIGN KEY (`placa`) REFERENCES `vehiculo` (`placa`),
  ADD CONSTRAINT `fk_detventa_venta` FOREIGN KEY (`cod_venta`) REFERENCES `ventas` (`cod_venta`) ON DELETE CASCADE;

--
-- Filtros para la tabla `historia_estado_vehiculo`
--
ALTER TABLE `historia_estado_vehiculo`
  ADD CONSTRAINT `fk_hist_vehiculo` FOREIGN KEY (`placa`) REFERENCES `vehiculo` (`placa`) ON DELETE CASCADE;

--
-- Filtros para la tabla `imagen`
--
ALTER TABLE `imagen`
  ADD CONSTRAINT `fk_img_vehiculo` FOREIGN KEY (`placa`) REFERENCES `vehiculo` (`placa`);

--
-- Filtros para la tabla `modelo`
--
ALTER TABLE `modelo`
  ADD CONSTRAINT `fk_modelo_marca` FOREIGN KEY (`cod_marca`) REFERENCES `marca` (`cod_marca`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `pago_cuentas`
--
ALTER TABLE `pago_cuentas`
  ADD CONSTRAINT `fk_pagocuenta_cpc` FOREIGN KEY (`cod_cuentas`) REFERENCES `cuentas_por_cobrar` (`cod_cuentas`);

--
-- Filtros para la tabla `vehiculo`
--
ALTER TABLE `vehiculo`
  ADD CONSTRAINT `fk_vehiculo_acc` FOREIGN KEY (`cod_accesorio`) REFERENCES `accesorio` (`cod_accesorio`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_vehiculo_doc` FOREIGN KEY (`cod_documento`) REFERENCES `documentacion` (`cod_documento`),
  ADD CONSTRAINT `fk_vehiculo_modelo` FOREIGN KEY (`cod_modelo`) REFERENCES `modelo` (`cod_modelo`),
  ADD CONSTRAINT `fk_vehiculo_prov` FOREIGN KEY (`cedula_propietario`) REFERENCES `propietario` (`cedula_propietario`),
  ADD CONSTRAINT `vehiculo_ibfk_1` FOREIGN KEY (`cod_tipo`) REFERENCES `tipo_vehiculo` (`cod_tipo`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
