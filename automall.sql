-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-05-2026 a las 03:19:01
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
  `copia_llaves` tinyint(1) DEFAULT NULL,
  `repuesto` tinyint(1) DEFAULT NULL,
  `triangulo` tinyint(1) DEFAULT NULL,
  `placa` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

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
  `placa` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `citas`
--

CREATE TABLE `citas` (
  `cod_citas` int(11) NOT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `hora` time DEFAULT NULL,
  `cod_catalogo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `det_mantenimiento`
--

CREATE TABLE `det_mantenimiento` (
  `cod_detalle` int(11) NOT NULL,
  `tipo` varchar(100) DEFAULT NULL,
  `fecha_entrega` date DEFAULT NULL,
  `fecha_salida` date NOT NULL,
  `cod_mantenimiento` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `det_venta`
--

CREATE TABLE `det_venta` (
  `cod_det_venta` int(11) NOT NULL,
  `poder` tinyint(1) DEFAULT NULL,
  `traspaso` tinyint(1) DEFAULT NULL,
  `cod_venta` int(11) DEFAULT NULL,
  `placa` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `imagen`
--

CREATE TABLE `imagen` (
  `cod_imagen` int(11) NOT NULL,
  `URL` varchar(300) DEFAULT NULL,
  `placa` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mantenimiento`
--

CREATE TABLE `mantenimiento` (
  `cod_mantenimiento` int(11) NOT NULL,
  `descripcion_general` text DEFAULT NULL,
  `quien_autoriza` varchar(30) NOT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `cod_catalogo` int(11) NOT NULL,
  `cod_taller` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `marca`
--

CREATE TABLE `marca` (
  `cod_marca` int(11) NOT NULL,
  `nombre_marca` varchar(50) NOT NULL,
  `estado` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `modelo`
--

CREATE TABLE `modelo` (
  `cod_modelo` int(11) NOT NULL,
  `nombre_modelo` varchar(50) NOT NULL,
  `estado` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedor`
--

CREATE TABLE `proveedor` (
  `cedula_proveedor` int(11) NOT NULL,
  `razon_social` int(11) NOT NULL,
  `telefono` int(20) NOT NULL,
  `direccion` varchar(250) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `estado` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios_realizados`
--

CREATE TABLE `servicios_realizados` (
  `cod_servicios` int(11) NOT NULL,
  `descripcion_detalle` varchar(100) DEFAULT NULL,
  `costo` decimal(10,2) DEFAULT NULL,
  `cantidad` int(50) DEFAULT NULL,
  `cod_detalle` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `taller`
--

CREATE TABLE `taller` (
  `cod_taller` int(11) NOT NULL,
  `razon_social` varchar(100) NOT NULL,
  `rif` int(50) NOT NULL,
  `direccion` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vehiculo`
--

CREATE TABLE `vehiculo` (
  `placa` varchar(20) NOT NULL,
  `color` varchar(50) DEFAULT NULL,
  `anio` int(11) NOT NULL,
  `tipo` text NOT NULL,
  `kilometraje` int(20) NOT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `cod_marca` int(11) NOT NULL,
  `cod_modelo` int(11) NOT NULL,
  `cod_documento` int(11) NOT NULL,
  `cedula_proveedor` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `cod_venta` int(11) NOT NULL,
  `estado` varchar(45) DEFAULT NULL,
  `fecha_venta` varchar(45) DEFAULT NULL,
  `copia_rif` int(11) DEFAULT NULL,
  `cedula_usuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `accesorio`
--
ALTER TABLE `accesorio`
  ADD PRIMARY KEY (`cod_accesorio`),
  ADD UNIQUE KEY `placa` (`placa`);

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
  ADD UNIQUE KEY `cod_catalogo` (`cod_catalogo`);

--
-- Indices de la tabla `det_mantenimiento`
--
ALTER TABLE `det_mantenimiento`
  ADD PRIMARY KEY (`cod_detalle`),
  ADD UNIQUE KEY `cod_mantenimiento` (`cod_mantenimiento`);

--
-- Indices de la tabla `det_venta`
--
ALTER TABLE `det_venta`
  ADD PRIMARY KEY (`cod_det_venta`),
  ADD UNIQUE KEY `placa` (`placa`),
  ADD UNIQUE KEY `cod_venta` (`cod_venta`);

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
  ADD UNIQUE KEY `placa` (`placa`);

--
-- Indices de la tabla `mantenimiento`
--
ALTER TABLE `mantenimiento`
  ADD PRIMARY KEY (`cod_mantenimiento`),
  ADD UNIQUE KEY `cod_catalogo` (`cod_catalogo`),
  ADD UNIQUE KEY `cod_taller` (`cod_taller`);

--
-- Indices de la tabla `marca`
--
ALTER TABLE `marca`
  ADD PRIMARY KEY (`cod_marca`);

--
-- Indices de la tabla `modelo`
--
ALTER TABLE `modelo`
  ADD PRIMARY KEY (`cod_modelo`);

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
  ADD KEY `cod_detalle` (`cod_detalle`);

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
  ADD KEY `vehiculo_ibfk_2` (`cedula_proveedor`),
  ADD KEY `cod_documento` (`cod_documento`),
  ADD KEY `cod_marca` (`cod_marca`),
  ADD KEY `cod_modelo` (`cod_modelo`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`cod_venta`),
  ADD UNIQUE KEY `cod_usuario` (`cedula_usuario`),
  ADD UNIQUE KEY `cedula_usuario` (`cedula_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `accesorio`
--
ALTER TABLE `accesorio`
  MODIFY `cod_accesorio` int(11) NOT NULL AUTO_INCREMENT;

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
-- AUTO_INCREMENT de la tabla `det_mantenimiento`
--
ALTER TABLE `det_mantenimiento`
  MODIFY `cod_detalle` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `det_venta`
--
ALTER TABLE `det_venta`
  MODIFY `cod_det_venta` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `documentacion`
--
ALTER TABLE `documentacion`
  MODIFY `cod_documento` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `imagen`
--
ALTER TABLE `imagen`
  MODIFY `cod_imagen` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `mantenimiento`
--
ALTER TABLE `mantenimiento`
  MODIFY `cod_mantenimiento` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `marca`
--
ALTER TABLE `marca`
  MODIFY `cod_marca` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `modelo`
--
ALTER TABLE `modelo`
  MODIFY `cod_modelo` int(11) NOT NULL AUTO_INCREMENT;

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
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `cod_venta` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `accesorio`
--
ALTER TABLE `accesorio`
  ADD CONSTRAINT `accesorio_ibfk_1` FOREIGN KEY (`placa`) REFERENCES `vehiculo` (`placa`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `catalogo`
--
ALTER TABLE `catalogo`
  ADD CONSTRAINT `catalogo_ibfk_1` FOREIGN KEY (`placa`) REFERENCES `vehiculo` (`placa`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `citas`
--
ALTER TABLE `citas`
  ADD CONSTRAINT `citas_ibfk_1` FOREIGN KEY (`cod_catalogo`) REFERENCES `catalogo` (`cod_catalogo`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `det_mantenimiento`
--
ALTER TABLE `det_mantenimiento`
  ADD CONSTRAINT `det_mantenimiento_ibfk_1` FOREIGN KEY (`cod_mantenimiento`) REFERENCES `mantenimiento` (`cod_mantenimiento`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `det_venta`
--
ALTER TABLE `det_venta`
  ADD CONSTRAINT `det_venta_ibfk_1` FOREIGN KEY (`cod_venta`) REFERENCES `ventas` (`cod_venta`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `det_venta_ibfk_2` FOREIGN KEY (`placa`) REFERENCES `vehiculo` (`placa`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `imagen`
--
ALTER TABLE `imagen`
  ADD CONSTRAINT `imagen_ibfk_1` FOREIGN KEY (`placa`) REFERENCES `vehiculo` (`placa`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `mantenimiento`
--
ALTER TABLE `mantenimiento`
  ADD CONSTRAINT `mantenimiento_ibfk_1` FOREIGN KEY (`cod_taller`) REFERENCES `taller` (`cod_taller`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `mantenimiento_ibfk_2` FOREIGN KEY (`cod_catalogo`) REFERENCES `catalogo` (`cod_catalogo`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `servicios_realizados`
--
ALTER TABLE `servicios_realizados`
  ADD CONSTRAINT `servicios_realizados_ibfk_1` FOREIGN KEY (`cod_detalle`) REFERENCES `det_mantenimiento` (`cod_detalle`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `vehiculo`
--
ALTER TABLE `vehiculo`
  ADD CONSTRAINT `vehiculo_ibfk_2` FOREIGN KEY (`cedula_proveedor`) REFERENCES `proveedor` (`cedula_proveedor`),
  ADD CONSTRAINT `vehiculo_ibfk_3` FOREIGN KEY (`cod_documento`) REFERENCES `documentacion` (`cod_documento`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `vehiculo_ibfk_4` FOREIGN KEY (`cod_marca`) REFERENCES `marca` (`cod_marca`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `vehiculo_ibfk_5` FOREIGN KEY (`cod_modelo`) REFERENCES `modelo` (`cod_modelo`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
