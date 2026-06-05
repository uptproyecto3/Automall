-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 05-06-2026 a las 15:47:28
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

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
  `copia_llaves` tinyint(1) DEFAULT NULL,
  `repuesto` tinyint(1) DEFAULT NULL,
  `triangulo` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `banco`
--

CREATE TABLE `banco` (
  `cod_banco` int(11) NOT NULL,
  `nombre_banco` varchar(100) NOT NULL,
  `estado` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `catalogo`
--

CREATE TABLE `catalogo` (
  `cod_catalogo` int(11) NOT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha_publicacion` date DEFAULT NULL,
  `placa` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `citas`
--

CREATE TABLE `citas` (
  `cod_citas` int(11) NOT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `hora` time DEFAULT NULL,
  `cod_catalogo` int(11) DEFAULT NULL,
  `cedula_usuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `compras_accesorios`
--

CREATE TABLE `compras_accesorios` (
  `cod_compras` int(11) NOT NULL,
  `fecha` date DEFAULT NULL,
  `monto_total` decimal(20,2) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cuentas_por_cobrar`
--

CREATE TABLE `cuentas_por_cobrar` (
  `cod_cuentas` int(11) NOT NULL,
  `deuda_total` decimal(10,2) DEFAULT NULL,
  `saldo_pendiente` decimal(10,2) DEFAULT NULL,
  `fecha_vencimiento` datetime DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `cod_venta` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `det_banco`
--

CREATE TABLE `det_banco` (
  `cod_det_banco` int(11) NOT NULL,
  `monto` int(30) NOT NULL,
  `refencia` int(50) NOT NULL,
  `cod_banco` int(11) NOT NULL,
  `cod_det_pago` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `det_compra`
--

CREATE TABLE `det_compra` (
  `cod_det_compra` int(11) NOT NULL,
  `producto` varchar(50) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `costo_unitario` decimal(10,2) DEFAULT NULL,
  `cod_insumo` int(11) NOT NULL,
  `placa` varchar(20) NOT NULL,
  `cod_compras` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `det_mantenimiento`
--

CREATE TABLE `det_mantenimiento` (
  `cod_detalle` int(11) NOT NULL,
  `tipo` varchar(20) DEFAULT NULL,
  `fecha_salida` date DEFAULT NULL,
  `fecha_entrega` date DEFAULT NULL,
  `cod_mantenimiento` int(11) DEFAULT NULL,
  `placa` varchar(20) DEFAULT NULL,
  `cod_taller` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `det_nom_digital`
--

CREATE TABLE `det_nom_digital` (
  `cod_det_digital` int(11) NOT NULL,
  `monto` int(100) NOT NULL,
  `referencia` int(20) NOT NULL,
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
-- Estructura de tabla para la tabla `det_servicios`
--

CREATE TABLE `det_servicios` (
  `cod_det_servicio` int(11) NOT NULL,
  `costo` decimal(10,2) DEFAULT NULL,
  `descripcion_especifica` varchar(250) DEFAULT NULL,
  `placa` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `det_venta`
--

CREATE TABLE `det_venta` (
  `cod_det_venta` int(11) NOT NULL,
  `poder` tinyint(1) DEFAULT NULL,
  `traspaso_papel` tinyint(1) DEFAULT NULL,
  `placa` varchar(20) DEFAULT NULL,
  `cod_venta` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `documentacion`
--

CREATE TABLE `documentacion` (
  `cod_documento` int(11) NOT NULL,
  `original_totalPropiedad` tinyint(1) DEFAULT NULL,
  `experticia_transito` tinyint(1) DEFAULT NULL,
  `certificado_origen` tinyint(1) DEFAULT NULL,
  `carnet_circulacion` tinyint(1) DEFAULT NULL,
  `reserva_dominio` tinyint(1) DEFAULT NULL,
  `garantia_vehiculo` tinyint(1) DEFAULT NULL,
  `certificado_garantia` tinyint(1) DEFAULT NULL,
  `manual_vehiculoGarantia` tinyint(1) DEFAULT NULL,
  `finiquito` tinyint(1) DEFAULT NULL,
  `resguardo` tinyint(1) DEFAULT NULL,
  `fecha_transferencia` tinyint(1) DEFAULT NULL,
  `seguro` tinyint(1) DEFAULT NULL,
  `factura_compra` tinyint(1) DEFAULT NULL,
  `fecha_ingreso` date DEFAULT NULL,
  `otro_documento` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `imagen`
--

CREATE TABLE `imagen` (
  `cod_imagen` int(11) NOT NULL,
  `URL` varchar(300) DEFAULT NULL,
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
  `stock` int(11) DEFAULT NULL,
  `cod_det_compra` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mantenimiento`
--

CREATE TABLE `mantenimiento` (
  `cod_mantenimiento` int(11) NOT NULL,
  `descripcion_general` text DEFAULT NULL,
  `quien_autoriza` varchar(30) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `marca`
--

CREATE TABLE `marca` (
  `cod_marca` int(11) NOT NULL,
  `nombre_marca` varchar(50) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `metodo_pago`
--

CREATE TABLE `metodo_pago` (
  `cod_metodo` int(11) NOT NULL,
  `nombre_metodo` varchar(50) NOT NULL,
  `estado` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `modelo`
--

CREATE TABLE `modelo` (
  `cod_modelo` int(11) NOT NULL,
  `nombre_modelo` varchar(50) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `cod_marca` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `moneda`
--

CREATE TABLE `moneda` (
  `cod_moneda` int(11) NOT NULL,
  `nombre_moneda` varchar(50) NOT NULL,
  `simbolo` varchar(10) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `moneda_digital`
--

CREATE TABLE `moneda_digital` (
  `cod_mon_digital` int(11) NOT NULL,
  `nombre_digital` varchar(50) NOT NULL,
  `simbolo_digital` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pago_cuentas`
--

CREATE TABLE `pago_cuentas` (
  `cod_pagos` int(11) NOT NULL,
  `monto_abonado` decimal(10,2) DEFAULT NULL,
  `fecha_pago` datetime DEFAULT NULL,
  `cod_cuentas` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedor`
--

CREATE TABLE `proveedor` (
  `cedula_proveedor` int(11) NOT NULL,
  `razon_social` varchar(100) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(250) DEFAULT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proveedor`
--

INSERT INTO `proveedor` (`cedula_proveedor`, `razon_social`, `telefono`, `direccion`, `tipo`, `estado`) VALUES
(29880513, 'daryeli gutierrez', '04122152649', 'villa productiva', 'Natural', 'Activo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios_realizados`
--

CREATE TABLE `servicios_realizados` (
  `cod_servicios` int(11) NOT NULL,
  `nombre_servicio` varchar(100) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `cod_det_servicio` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `taller`
--

CREATE TABLE `taller` (
  `cod_taller` int(11) NOT NULL,
  `nombre_taller` varchar(100) DEFAULT NULL,
  `direccion` varchar(250) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vehiculo`
--

CREATE TABLE `vehiculo` (
  `placa` varchar(20) NOT NULL,
  `color` varchar(50) DEFAULT NULL,
  `anio` int(11) DEFAULT NULL,
  `tipo` text DEFAULT NULL,
  `kilometraje` int(20) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `cod_modelo` int(11) DEFAULT NULL,
  `cod_documento` int(11) DEFAULT NULL,
  `cod_accesorio` int(11) DEFAULT NULL,
  `cedula_proveedor` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `cod_venta` int(11) NOT NULL,
  `estado` varchar(45) DEFAULT NULL,
  `fecha_venta` date DEFAULT NULL,
  `tipo_venta` varchar(45) DEFAULT NULL,
  `cedula_usuario` int(11) DEFAULT NULL
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
  ADD KEY `placa` (`placa`);

--
-- Indices de la tabla `citas`
--
ALTER TABLE `citas`
  ADD PRIMARY KEY (`cod_citas`),
  ADD UNIQUE KEY `cedula_usuario` (`cedula_usuario`),
  ADD KEY `cod_catalogo` (`cod_catalogo`);

--
-- Indices de la tabla `compras_accesorios`
--
ALTER TABLE `compras_accesorios`
  ADD PRIMARY KEY (`cod_compras`);

--
-- Indices de la tabla `cuentas_por_cobrar`
--
ALTER TABLE `cuentas_por_cobrar`
  ADD PRIMARY KEY (`cod_cuentas`),
  ADD KEY `cod_venta` (`cod_venta`);

--
-- Indices de la tabla `det_banco`
--
ALTER TABLE `det_banco`
  ADD PRIMARY KEY (`cod_det_banco`),
  ADD UNIQUE KEY `cod_banco` (`cod_banco`),
  ADD UNIQUE KEY `cod_det_pago` (`cod_det_pago`);

--
-- Indices de la tabla `det_compra`
--
ALTER TABLE `det_compra`
  ADD PRIMARY KEY (`cod_det_compra`),
  ADD UNIQUE KEY `cod_insumo` (`cod_insumo`),
  ADD UNIQUE KEY `placa` (`placa`),
  ADD UNIQUE KEY `cod_compras` (`cod_compras`);

--
-- Indices de la tabla `det_mantenimiento`
--
ALTER TABLE `det_mantenimiento`
  ADD PRIMARY KEY (`cod_detalle`),
  ADD KEY `cod_mantenimiento` (`cod_mantenimiento`),
  ADD KEY `placa` (`placa`),
  ADD KEY `cod_taller` (`cod_taller`);

--
-- Indices de la tabla `det_nom_digital`
--
ALTER TABLE `det_nom_digital`
  ADD PRIMARY KEY (`cod_det_digital`),
  ADD UNIQUE KEY `cod_mon_digital` (`cod_mon_digital`),
  ADD UNIQUE KEY `cod_det_pago` (`cod_det_pago`);

--
-- Indices de la tabla `det_pago`
--
ALTER TABLE `det_pago`
  ADD PRIMARY KEY (`cod_det_pago`),
  ADD UNIQUE KEY `cod_pago` (`cod_pagos`),
  ADD UNIQUE KEY `cod_metodo` (`cod_metodo`),
  ADD UNIQUE KEY `cod_moneda` (`cod_moneda`);

--
-- Indices de la tabla `det_servicios`
--
ALTER TABLE `det_servicios`
  ADD PRIMARY KEY (`cod_det_servicio`),
  ADD UNIQUE KEY `placa` (`placa`);

--
-- Indices de la tabla `det_venta`
--
ALTER TABLE `det_venta`
  ADD PRIMARY KEY (`cod_det_venta`),
  ADD UNIQUE KEY `cod_venta` (`cod_venta`),
  ADD KEY `placa` (`placa`);

--
-- Indices de la tabla `documentacion`
--
ALTER TABLE `documentacion`
  ADD PRIMARY KEY (`cod_documento`);

--
-- Indices de la tabla `imagen`
--
ALTER TABLE `imagen`
  ADD PRIMARY KEY (`cod_imagen`),
  ADD KEY `placa` (`placa`);

--
-- Indices de la tabla `insumos`
--
ALTER TABLE `insumos`
  ADD PRIMARY KEY (`cod_insumo`),
  ADD UNIQUE KEY `cod_det_compra` (`cod_det_compra`);

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
  ADD UNIQUE KEY `cod_marca` (`cod_marca`);

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
  ADD KEY `cod_cuentas` (`cod_cuentas`);

--
-- Indices de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  ADD PRIMARY KEY (`cedula_proveedor`);

--
-- Indices de la tabla `servicios_realizados`
--
ALTER TABLE `servicios_realizados`
  ADD PRIMARY KEY (`cod_servicios`),
  ADD UNIQUE KEY `cod_det_servicio` (`cod_det_servicio`);

--
-- Indices de la tabla `taller`
--
ALTER TABLE `taller`
  ADD PRIMARY KEY (`cod_taller`);

--
-- Indices de la tabla `vehiculo`
--
ALTER TABLE `vehiculo`
  ADD PRIMARY KEY (`placa`),
  ADD UNIQUE KEY `cod_accesorio` (`cod_accesorio`),
  ADD KEY `cod_modelo` (`cod_modelo`),
  ADD KEY `cod_documento` (`cod_documento`),
  ADD KEY `cedula_proveedor` (`cedula_proveedor`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`cod_venta`),
  ADD UNIQUE KEY `cedula_usuario` (`cedula_usuario`);

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
  MODIFY `cod_catalogo` int(11) NOT NULL AUTO_INCREMENT;

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
  MODIFY `cod_documento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `imagen`
--
ALTER TABLE `imagen`
  MODIFY `cod_imagen` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

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
-- AUTO_INCREMENT de la tabla `servicios_realizados`
--
ALTER TABLE `servicios_realizados`
  MODIFY `cod_servicios` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `taller`
--
ALTER TABLE `taller`
  MODIFY `cod_taller` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `catalogo`
--
ALTER TABLE `catalogo`
  ADD CONSTRAINT `catalogo_ibfk_1` FOREIGN KEY (`placa`) REFERENCES `vehiculo` (`placa`);

--
-- Filtros para la tabla `citas`
--
ALTER TABLE `citas`
  ADD CONSTRAINT `citas_ibfk_1` FOREIGN KEY (`cod_catalogo`) REFERENCES `catalogo` (`cod_catalogo`);

--
-- Filtros para la tabla `cuentas_por_cobrar`
--
ALTER TABLE `cuentas_por_cobrar`
  ADD CONSTRAINT `cuentas_por_cobrar_ibfk_1` FOREIGN KEY (`cod_venta`) REFERENCES `ventas` (`cod_venta`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `det_banco`
--
ALTER TABLE `det_banco`
  ADD CONSTRAINT `det_banco_ibfk_1` FOREIGN KEY (`cod_banco`) REFERENCES `banco` (`cod_banco`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `det_banco_ibfk_2` FOREIGN KEY (`cod_det_pago`) REFERENCES `det_pago` (`cod_det_pago`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `det_compra`
--
ALTER TABLE `det_compra`
  ADD CONSTRAINT `det_compra_ibfk_1` FOREIGN KEY (`placa`) REFERENCES `vehiculo` (`placa`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `det_compra_ibfk_2` FOREIGN KEY (`cod_compras`) REFERENCES `compras_accesorios` (`cod_compras`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `det_mantenimiento`
--
ALTER TABLE `det_mantenimiento`
  ADD CONSTRAINT `det_mantenimiento_ibfk_1` FOREIGN KEY (`cod_mantenimiento`) REFERENCES `mantenimiento` (`cod_mantenimiento`),
  ADD CONSTRAINT `det_mantenimiento_ibfk_3` FOREIGN KEY (`placa`) REFERENCES `vehiculo` (`placa`),
  ADD CONSTRAINT `det_mantenimiento_ibfk_4` FOREIGN KEY (`cod_taller`) REFERENCES `taller` (`cod_taller`);

--
-- Filtros para la tabla `det_nom_digital`
--
ALTER TABLE `det_nom_digital`
  ADD CONSTRAINT `det_nom_digital_ibfk_1` FOREIGN KEY (`cod_mon_digital`) REFERENCES `moneda_digital` (`cod_mon_digital`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `det_nom_digital_ibfk_2` FOREIGN KEY (`cod_det_pago`) REFERENCES `det_pago` (`cod_det_pago`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `det_pago`
--
ALTER TABLE `det_pago`
  ADD CONSTRAINT `det_pago_ibfk_1` FOREIGN KEY (`cod_pagos`) REFERENCES `pago_cuentas` (`cod_pagos`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `det_pago_ibfk_3` FOREIGN KEY (`cod_metodo`) REFERENCES `metodo_pago` (`cod_metodo`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `det_pago_ibfk_4` FOREIGN KEY (`cod_moneda`) REFERENCES `moneda` (`cod_moneda`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `det_servicios`
--
ALTER TABLE `det_servicios`
  ADD CONSTRAINT `det_servicios_ibfk_1` FOREIGN KEY (`placa`) REFERENCES `vehiculo` (`placa`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `det_venta`
--
ALTER TABLE `det_venta`
  ADD CONSTRAINT `det_venta_ibfk_2` FOREIGN KEY (`placa`) REFERENCES `vehiculo` (`placa`),
  ADD CONSTRAINT `det_venta_ibfk_3` FOREIGN KEY (`cod_venta`) REFERENCES `ventas` (`cod_venta`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `imagen`
--
ALTER TABLE `imagen`
  ADD CONSTRAINT `imagen_ibfk_1` FOREIGN KEY (`placa`) REFERENCES `vehiculo` (`placa`);

--
-- Filtros para la tabla `insumos`
--
ALTER TABLE `insumos`
  ADD CONSTRAINT `insumos_ibfk_1` FOREIGN KEY (`cod_det_compra`) REFERENCES `det_compra` (`cod_det_compra`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `modelo`
--
ALTER TABLE `modelo`
  ADD CONSTRAINT `modelo_ibfk_1` FOREIGN KEY (`cod_marca`) REFERENCES `marca` (`cod_marca`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `pago_cuentas`
--
ALTER TABLE `pago_cuentas`
  ADD CONSTRAINT `pago_cuentas_ibfk_1` FOREIGN KEY (`cod_cuentas`) REFERENCES `cuentas_por_cobrar` (`cod_cuentas`);

--
-- Filtros para la tabla `servicios_realizados`
--
ALTER TABLE `servicios_realizados`
  ADD CONSTRAINT `servicios_realizados_ibfk_1` FOREIGN KEY (`cod_det_servicio`) REFERENCES `det_servicios` (`cod_det_servicio`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `vehiculo`
--
ALTER TABLE `vehiculo`
  ADD CONSTRAINT `vehiculo_ibfk_2` FOREIGN KEY (`cod_modelo`) REFERENCES `modelo` (`cod_modelo`),
  ADD CONSTRAINT `vehiculo_ibfk_3` FOREIGN KEY (`cod_documento`) REFERENCES `documentacion` (`cod_documento`),
  ADD CONSTRAINT `vehiculo_ibfk_4` FOREIGN KEY (`cedula_proveedor`) REFERENCES `proveedor` (`cedula_proveedor`),
  ADD CONSTRAINT `vehiculo_ibfk_5` FOREIGN KEY (`cod_accesorio`) REFERENCES `accesorio` (`cod_accesorio`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
