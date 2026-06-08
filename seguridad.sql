-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 08-06-2026 a las 18:06:58
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
-- Base de datos: `seguridad`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_banco_preguntas`
--

CREATE TABLE `t_banco_preguntas` (
  `cod_preguntas` int(11) NOT NULL,
  `nombre_preguntas` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `t_banco_preguntas`
--

INSERT INTO `t_banco_preguntas` (`cod_preguntas`, `nombre_preguntas`) VALUES
(1, '¿Nombre de mi primera mascota?'),
(2, '¿Nombre de mi ciudad de nacimiento?'),
(3, '¿Nombre de mi escuela primaria?'),
(4, '¿Segundo nombre de mi padre?'),
(5, '¿Nombre de mi primer juguete favorito?'),
(6, '¿Nombre de mi comida favorita?'),
(7, '¿Nombre de mi color favorito?');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_bitacora`
--

CREATE TABLE `t_bitacora` (
  `cod_bitacora` int(11) NOT NULL,
  `usuario` varchar(100) NOT NULL,
  `cedula_usuario` varchar(20) NOT NULL,
  `accion` varchar(255) NOT NULL,
  `modulo` varchar(100) NOT NULL,
  `fecha` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_det_repuesta`
--

CREATE TABLE `t_det_repuesta` (
  `cod_repuesta` int(11) NOT NULL,
  `respuesta` varchar(50) NOT NULL,
  `cod_preguntas` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_modulo`
--

CREATE TABLE `t_modulo` (
  `cod_modulo` int(11) NOT NULL,
  `nombre_modulo` varchar(50) NOT NULL,
  `estatus` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `t_modulo`
--

INSERT INTO `t_modulo` (`cod_modulo`, `nombre_modulo`, `estatus`) VALUES
(1, 'Usuarios', 1),
(2, 'Vehículos', 1),
(3, 'Mantenimiento', 1),
(4, 'Bitacora', 1),
(5, 'Mantenimiento a la BD', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_permiso_rol_modulo`
--

CREATE TABLE `t_permiso_rol_modulo` (
  `cod_permiso` int(11) NOT NULL,
  `cod_rol` int(11) NOT NULL,
  `cod_modulo` int(11) NOT NULL,
  `p_crear` tinyint(1) NOT NULL DEFAULT 0,
  `p_leer` tinyint(1) NOT NULL DEFAULT 1,
  `p_actualizar` tinyint(1) NOT NULL DEFAULT 0,
  `p_eliminar` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `t_permiso_rol_modulo`
--

INSERT INTO `t_permiso_rol_modulo` (`cod_permiso`, `cod_rol`, `cod_modulo`, `p_crear`, `p_leer`, `p_actualizar`, `p_eliminar`) VALUES
(1, 2, 2, 0, 1, 0, 0),
(2, 1, 1, 1, 1, 1, 1),
(3, 1, 3, 1, 1, 1, 1),
(4, 1, 2, 1, 1, 1, 1),
(5, 3, 1, 1, 1, 1, 0),
(6, 3, 2, 1, 1, 1, 1),
(7, 1, 4, 1, 1, 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_personal`
--

CREATE TABLE `t_personal` (
  `cod_personal` int(11) NOT NULL,
  `cargo` varchar(45) NOT NULL,
  `departamento` varchar(45) NOT NULL,
  `estatus` varchar(20) NOT NULL,
  `id_usuario` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_rol`
--

CREATE TABLE `t_rol` (
  `cod_rol` int(11) NOT NULL,
  `nombre_rol` varchar(50) NOT NULL,
  `descripcion_rol` varchar(100) DEFAULT NULL,
  `estatus` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `t_rol`
--

INSERT INTO `t_rol` (`cod_rol`, `nombre_rol`, `descripcion_rol`, `estatus`) VALUES
(1, 'Super Usuario', 'Acceso total al sistema', 1),
(2, 'Administrador', 'Gestión operativa del negocio', 1),
(3, 'Vendedor', 'Atención al cliente y catálogos', 1),
(4, 'Cliente', 'Encargado de comprar y agendar cita', 1),
(5, 'Jefe de patio', 'Encargado de revsion de los vehiculos', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_usuario`
--

CREATE TABLE `t_usuario` (
  `cedula_usuario` varchar(20) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `direccion` text NOT NULL,
  `correo` varchar(50) NOT NULL,
  `password` varchar(160) NOT NULL,
  `estado` int(11) NOT NULL DEFAULT 1,
  `cod_rol` int(11) DEFAULT 5,
  `foto` varchar(255) DEFAULT 'default.png',
  `cod_preguntas` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `t_usuario`
--

INSERT INTO `t_usuario` (`cedula_usuario`, `nombre`, `apellido`, `telefono`, `direccion`, `correo`, `password`, `estado`, `cod_rol`, `foto`, `cod_preguntas`) VALUES
('../../../../../../..', 'ZAP', 'ZAP', '9999999999', 'ZAP', 'zaproxy@example.com', 'ZAP', 1, 3, 'default.png', NULL),
('..\\..\\..\\..\\..\\..\\..', 'ZAP', 'ZAP', '9999999999', 'ZAP', 'zaproxy@example.com', 'ZAP', 1, 3, 'default.png', NULL),
('/', 'ZAP', 'ZAP', '9999999999', 'ZAP', 'zaproxy@example.com', 'ZAP', 1, 3, 'default.png', NULL),
('/etc/passwd', 'ZAP', 'ZAP', '9999999999', 'ZAP', 'zaproxy@example.com', 'ZAP', 1, 3, 'default.png', NULL),
('/registro', 'ZAP', 'ZAP', '9999999999', 'ZAP', 'zaproxy@example.com', 'ZAP', 1, 3, 'default.png', NULL),
('/WEB-INF/web.xml', 'ZAP', 'ZAP', '9999999999', 'ZAP', 'zaproxy@example.com', 'ZAP', 1, 3, 'default.png', NULL),
('29880513', 'daryeli', 'gutierrez', '', 'villa productiva', 'darye@gmail.com', '12345678', 1, 1, 'default.png', NULL),
('c:/', 'ZAP', 'ZAP', '9999999999', 'ZAP', 'zaproxy@example.com', 'ZAP', 1, 3, 'default.png', NULL),
('c:/Windows/system.in', 'ZAP', 'ZAP', '9999999999', 'ZAP', 'zaproxy@example.com', 'ZAP', 1, 3, 'default.png', NULL),
('c:\\', 'ZAP', 'ZAP', '9999999999', 'ZAP', 'zaproxy@example.com', 'ZAP', 1, 3, 'default.png', NULL),
('c:\\Windows\\system.in', 'ZAP', 'ZAP', '9999999999', 'ZAP', 'zaproxy@example.com', 'ZAP', 1, 3, 'default.png', NULL),
('registro', 'ZAP', 'ZAP', '9999999999', 'ZAP', 'zaproxy@example.com', 'ZAP', 1, 3, 'default.png', NULL),
('thishouldnotexistand', 'ZAP', 'ZAP', '9999999999', 'ZAP', 'zaproxy@example.com', 'ZAP', 1, 3, 'default.png', NULL),
('WEB-INF/web.xml', 'ZAP', 'ZAP', '9999999999', 'ZAP', 'zaproxy@example.com', 'ZAP', 1, 3, 'default.png', NULL),
('WEB-INF\\web.xml', 'ZAP', 'ZAP', '9999999999', 'ZAP', 'zaproxy@example.com', 'ZAP', 1, 3, 'default.png', NULL),
('ZAP', 'ZAP', 'ZAP', '9999999999', 'ZAP', 'zaproxy@example.com', 'ZAP', 1, 3, 'default.png', NULL),
('\\registro', 'ZAP', 'ZAP', '9999999999', 'ZAP', 'zaproxy@example.com', 'ZAP', 1, 3, 'default.png', NULL),
('\\WEB-INF\\web.xml', 'ZAP', 'ZAP', '9999999999', 'ZAP', 'zaproxy@example.com', 'ZAP', 1, 3, 'default.png', NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `t_banco_preguntas`
--
ALTER TABLE `t_banco_preguntas`
  ADD PRIMARY KEY (`cod_preguntas`);

--
-- Indices de la tabla `t_bitacora`
--
ALTER TABLE `t_bitacora`
  ADD PRIMARY KEY (`cod_bitacora`),
  ADD KEY `t_bitacora_ibfk_usuario` (`cedula_usuario`);

--
-- Indices de la tabla `t_det_repuesta`
--
ALTER TABLE `t_det_repuesta`
  ADD PRIMARY KEY (`cod_repuesta`),
  ADD UNIQUE KEY `cod_preguntas` (`cod_preguntas`);

--
-- Indices de la tabla `t_modulo`
--
ALTER TABLE `t_modulo`
  ADD PRIMARY KEY (`cod_modulo`);

--
-- Indices de la tabla `t_permiso_rol_modulo`
--
ALTER TABLE `t_permiso_rol_modulo`
  ADD PRIMARY KEY (`cod_permiso`),
  ADD KEY `cod_rol` (`cod_rol`),
  ADD KEY `cod_modulo` (`cod_modulo`);

--
-- Indices de la tabla `t_personal`
--
ALTER TABLE `t_personal`
  ADD PRIMARY KEY (`cod_personal`) USING BTREE,
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `t_rol`
--
ALTER TABLE `t_rol`
  ADD PRIMARY KEY (`cod_rol`);

--
-- Indices de la tabla `t_usuario`
--
ALTER TABLE `t_usuario`
  ADD PRIMARY KEY (`cedula_usuario`),
  ADD UNIQUE KEY `cod_preguntas` (`cod_preguntas`),
  ADD KEY `cod_rol` (`cod_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `t_banco_preguntas`
--
ALTER TABLE `t_banco_preguntas`
  MODIFY `cod_preguntas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `t_bitacora`
--
ALTER TABLE `t_bitacora`
  MODIFY `cod_bitacora` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `t_det_repuesta`
--
ALTER TABLE `t_det_repuesta`
  MODIFY `cod_repuesta` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `t_modulo`
--
ALTER TABLE `t_modulo`
  MODIFY `cod_modulo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `t_permiso_rol_modulo`
--
ALTER TABLE `t_permiso_rol_modulo`
  MODIFY `cod_permiso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `t_personal`
--
ALTER TABLE `t_personal`
  MODIFY `cod_personal` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `t_rol`
--
ALTER TABLE `t_rol`
  MODIFY `cod_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `t_bitacora`
--
ALTER TABLE `t_bitacora`
  ADD CONSTRAINT `t_bitacora_ibfk_usuario` FOREIGN KEY (`cedula_usuario`) REFERENCES `t_usuario` (`cedula_usuario`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `t_det_repuesta`
--
ALTER TABLE `t_det_repuesta`
  ADD CONSTRAINT `t_det_repuesta_ibfk_1` FOREIGN KEY (`cod_preguntas`) REFERENCES `t_banco_preguntas` (`cod_preguntas`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `t_permiso_rol_modulo`
--
ALTER TABLE `t_permiso_rol_modulo`
  ADD CONSTRAINT `t_permiso_rol_modulo_ibfk_1` FOREIGN KEY (`cod_rol`) REFERENCES `t_rol` (`cod_rol`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `t_permiso_rol_modulo_ibfk_2` FOREIGN KEY (`cod_modulo`) REFERENCES `t_modulo` (`cod_modulo`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `t_personal`
--
ALTER TABLE `t_personal`
  ADD CONSTRAINT `t_personal_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `t_usuario` (`cedula_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `t_usuario`
--
ALTER TABLE `t_usuario`
  ADD CONSTRAINT `t_usuario_ibfk_1` FOREIGN KEY (`cod_rol`) REFERENCES `t_rol` (`cod_rol`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `t_usuario_ibfk_2` FOREIGN KEY (`cod_preguntas`) REFERENCES `t_banco_preguntas` (`cod_preguntas`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
