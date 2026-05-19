-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-05-2026 a las 03:19:13
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
-- Base de datos: `seguridad`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_bitacora`
--

CREATE TABLE `t_bitacora` (
  `id` int(11) NOT NULL,
  `usuario` varchar(100) NOT NULL,
  `cedula_usuario` varchar(20) NOT NULL,
  `accion` varchar(255) NOT NULL,
  `modulo` varchar(100) NOT NULL,
  `fecha` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `t_bitacora`
--

INSERT INTO `t_bitacora` (`id`, `usuario`, `cedula_usuario`, `accion`, `modulo`, `fecha`) VALUES
(1, 'Pedro', '27123456', 'Inició Sesión', 'Autenticación', '2026-05-13 21:44:17'),
(2, 'Pedro', '27123456', 'Inició Sesión', 'Autenticación', '2026-05-13 21:45:41'),
(3, 'Generacion', '28123456', 'Inició Sesión', 'Autenticación', '2026-05-13 21:45:58'),
(4, 'Pedro', '27123456', 'Inició Sesión', 'Autenticación', '2026-05-13 21:46:47'),
(5, 'Pedro', '27123456', 'Inició Sesión', 'Autenticación', '2026-05-13 21:52:30'),
(6, 'Pedro', '27123456', 'Eliminó el Usuario ID: 4', 'Usuarios', '2026-05-13 21:52:42'),
(7, 'Pedro', '27123456', 'Inició Sesión', 'Autenticación', '2026-05-13 21:55:04'),
(8, 'Pedro', '27123456', 'Inició Sesión', 'Autenticación', '2026-05-13 21:57:57'),
(9, 'Pedro', '27123456', 'Inició Sesión', 'Autenticación', '2026-05-13 22:23:12'),
(10, 'Pedro', '27123456', 'Inició Sesión', 'Autenticación', '2026-05-13 22:31:48'),
(11, 'Pedro', '27123456', 'Inició Sesión', 'Autenticación', '2026-05-13 22:39:39'),
(12, 'Pedro', '27123456', 'Inició Sesión', 'Autenticación', '2026-05-13 22:45:23'),
(13, 'Pedro', '27123456', 'Inició Sesión', 'Autenticación', '2026-05-14 00:10:00'),
(14, 'Pedro', '27123456', 'Inició Sesión', 'Autenticación', '2026-05-14 00:10:36'),
(15, 'Pedro', '27123456', 'Inició Sesión', 'Autenticación', '2026-05-15 20:32:53'),
(16, 'Pedro', '27123456', 'Inició Sesión', 'Autenticación', '2026-05-15 20:33:13');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_mantenimiento`
--

CREATE TABLE `t_mantenimiento` (
  `cod_mantenimiento` int(11) NOT NULL,
  `fecha` datetime NOT NULL,
  `url` varchar(45) NOT NULL,
  `status` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_modulo`
--

CREATE TABLE `t_modulo` (
  `id_modulo` int(11) NOT NULL,
  `nombre_modulo` varchar(50) NOT NULL,
  `estatus` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `t_modulo`
--

INSERT INTO `t_modulo` (`id_modulo`, `nombre_modulo`, `estatus`) VALUES
(1, 'Usuarios', 1),
(2, 'Vehículos', 1),
(3, 'Mantenimiento', 1),
(4, 'Bitacora', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_permiso_rol_modulo`
--

CREATE TABLE `t_permiso_rol_modulo` (
  `id_permiso` int(11) NOT NULL,
  `id_rol` int(11) NOT NULL,
  `id_modulo` int(11) NOT NULL,
  `p_crear` tinyint(1) NOT NULL DEFAULT 0,
  `p_leer` tinyint(1) NOT NULL DEFAULT 1,
  `p_actualizar` tinyint(1) NOT NULL DEFAULT 0,
  `p_eliminar` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `t_permiso_rol_modulo`
--

INSERT INTO `t_permiso_rol_modulo` (`id_permiso`, `id_rol`, `id_modulo`, `p_crear`, `p_leer`, `p_actualizar`, `p_eliminar`) VALUES
(1, 2, 2, 0, 1, 0, 0),
(2, 1, 1, 1, 1, 1, 1),
(3, 1, 3, 1, 1, 1, 1),
(4, 1, 2, 1, 1, 1, 1),
(5, 3, 1, 1, 0, 0, 0),
(6, 3, 2, 1, 0, 0, 0),
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
  `id_usuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_rol`
--

CREATE TABLE `t_rol` (
  `id_rol` int(11) NOT NULL,
  `nombre_rol` varchar(50) NOT NULL,
  `descripcion_rol` varchar(100) DEFAULT NULL,
  `estatus` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `t_rol`
--

INSERT INTO `t_rol` (`id_rol`, `nombre_rol`, `descripcion_rol`, `estatus`) VALUES
(1, 'Super Usuario', 'Acceso total al sistema', 1),
(2, 'Administrador', 'Gestión operativa del negocio', 1),
(3, 'Vendedor', 'Atención al cliente y catálogos', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_usuario`
--

CREATE TABLE `t_usuario` (
  `id` int(11) NOT NULL,
  `cedula_usuario` varchar(20) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `direccion` text NOT NULL,
  `correo` varchar(50) NOT NULL,
  `password` varchar(160) NOT NULL,
  `estado` int(11) NOT NULL DEFAULT 1,
  `id_rol` int(11) DEFAULT 3,
  `pregunta_seguridad` varchar(255) DEFAULT NULL,
  `respuesta_seguridad` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `t_usuario`
--

INSERT INTO `t_usuario` (`id`, `cedula_usuario`, `nombre`, `apellido`, `telefono`, `direccion`, `correo`, `password`, `estado`, `id_rol`, `pregunta_seguridad`, `respuesta_seguridad`) VALUES
(1, '27123456', 'Pedro', 'Camacaro', '02512514852', 'Centro carrera 16', 'amazon@gmail.com', '123456', 1, 1, 'Nombre libro', 'Superman'),
(5, '28123456', 'Zoom', 'Pastor', '02512514852', 'Cabudare agua viva', 'generation@gmail.com', '123456', 1, 3, 'Lugar fav', 'Obelisco');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `t_bitacora`
--
ALTER TABLE `t_bitacora`
  ADD PRIMARY KEY (`id`),
  ADD KEY `t_bitacora_ibfk_usuario` (`cedula_usuario`);

--
-- Indices de la tabla `t_mantenimiento`
--
ALTER TABLE `t_mantenimiento`
  ADD PRIMARY KEY (`cod_mantenimiento`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `t_modulo`
--
ALTER TABLE `t_modulo`
  ADD PRIMARY KEY (`id_modulo`);

--
-- Indices de la tabla `t_permiso_rol_modulo`
--
ALTER TABLE `t_permiso_rol_modulo`
  ADD PRIMARY KEY (`id_permiso`),
  ADD KEY `id_rol` (`id_rol`),
  ADD KEY `id_modulo` (`id_modulo`);

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
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `t_usuario`
--
ALTER TABLE `t_usuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `cedula_usuario` (`cedula_usuario`),
  ADD KEY `id_rol` (`id_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `t_bitacora`
--
ALTER TABLE `t_bitacora`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `t_mantenimiento`
--
ALTER TABLE `t_mantenimiento`
  MODIFY `cod_mantenimiento` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `t_modulo`
--
ALTER TABLE `t_modulo`
  MODIFY `id_modulo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `t_permiso_rol_modulo`
--
ALTER TABLE `t_permiso_rol_modulo`
  MODIFY `id_permiso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `t_personal`
--
ALTER TABLE `t_personal`
  MODIFY `cod_personal` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `t_rol`
--
ALTER TABLE `t_rol`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `t_usuario`
--
ALTER TABLE `t_usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `t_bitacora`
--
ALTER TABLE `t_bitacora`
  ADD CONSTRAINT `t_bitacora_ibfk_usuario` FOREIGN KEY (`cedula_usuario`) REFERENCES `t_usuario` (`cedula_usuario`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `t_mantenimiento`
--
ALTER TABLE `t_mantenimiento`
  ADD CONSTRAINT `t_mantenimiento_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `t_usuario` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `t_permiso_rol_modulo`
--
ALTER TABLE `t_permiso_rol_modulo`
  ADD CONSTRAINT `t_permiso_rol_modulo_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `t_rol` (`id_rol`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `t_permiso_rol_modulo_ibfk_2` FOREIGN KEY (`id_modulo`) REFERENCES `t_modulo` (`id_modulo`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `t_personal`
--
ALTER TABLE `t_personal`
  ADD CONSTRAINT `t_personal_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `t_usuario` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `t_usuario`
--
ALTER TABLE `t_usuario`
  ADD CONSTRAINT `t_usuario_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `t_rol` (`id_rol`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
