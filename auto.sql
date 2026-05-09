-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 30-04-2026 a las 05:59:03
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
-- Base de datos: `auto`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `modulo`
--

CREATE TABLE `modulo` (
  `id_modulo` int(11) NOT NULL,
  `nombre_modulo` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `modulo`
--

INSERT INTO `modulo` (`id_modulo`, `nombre_modulo`) VALUES
(1, 'Usuarios'),
(2, 'Vehículos'),
(3, 'Mantenimiento');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--

CREATE TABLE `rol` (
  `id_rol` int(11) NOT NULL,
  `nombre_rol` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `rol`
--

INSERT INTO `rol` (`id_rol`, `nombre_rol`) VALUES
(1, 'Super Usuario'),
(2, 'Administrador'),
(3, 'Vendedor');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol_permisos`
--

CREATE TABLE `rol_permisos` (
  `id_permiso` int(11) NOT NULL,
  `id_rol` int(11) DEFAULT NULL,
  `id_modulo` int(11) DEFAULT NULL,
  `p_crear` tinyint(1) DEFAULT 0,
  `p_leer` tinyint(1) DEFAULT 1,
  `p_actualizar` tinyint(1) DEFAULT 0,
  `p_eliminar` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `rol_permisos`
--

INSERT INTO `rol_permisos` (`id_permiso`, `id_rol`, `id_modulo`, `p_crear`, `p_leer`, `p_actualizar`, `p_eliminar`) VALUES
(1, 2, 2, 0, 1, 1, 1),
(2, 1, 1, 1, 0, 0, 1),
(3, 1, 3, 1, 1, 1, 1),
(4, 1, 2, 1, 1, 1, 1),
(5, 3, 1, 1, 1, 0, 0),
(6, 3, 2, 1, 0, 0, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `password` varchar(20) NOT NULL,
  `cedula` varchar(20) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `direccion` text NOT NULL,
  `id_rol` int(11) DEFAULT 3
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `correo`, `password`, `cedula`, `apellido`, `telefono`, `direccion`, `id_rol`) VALUES
(1, 'Pedro', 'amazon@gmail.com', '123456', '27123456', 'Camacaro', '02512514852', 'Centro carrera 16', 1),
(4, 'Generacion', 'diananb26@gmail.com', '123456', '27759045', 'Sivira', '041254487989', 'garagatal', 3),
(5, 'Zoom', 'generation@gmail.com', '123456', '28123456', 'Pastor', '02512514852', 'Cabudare agua viva', 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vehiculo`
--

CREATE TABLE `vehiculo` (
  `Id_Vehiculo` int(11) NOT NULL,
  `Placa` varchar(20) DEFAULT NULL,
  `Color` varchar(50) DEFAULT NULL,
  `Anio` int(11) DEFAULT NULL,
  `Tipo` varchar(50) DEFAULT NULL,
  `Estado` varchar(20) DEFAULT NULL,
  `Marca` varchar(50) DEFAULT NULL,
  `Modelo` varchar(50) DEFAULT NULL,
  `Cedula_Proveedor` int(11) DEFAULT NULL,
  `Imagen_URL` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `vehiculo`
--

INSERT INTO `vehiculo` (`Id_Vehiculo`, `Placa`, `Color`, `Anio`, `Tipo`, `Estado`, `Marca`, `Modelo`, `Cedula_Proveedor`, `Imagen_URL`) VALUES
(1, '21JA8777', 'Rojo', 2021, 'Camioneta', 'Disponible', 'toyota', 'xlr8', 20123456, 'Captura de pantalla (63).png'),
(2, '21jk8222', 'Verde', 2019, 'sedan', 'Disponible', 'Ford', 'Fiesta', 27759045, 'Captura_de_pantalla_55.png'),
(3, '456dad87', 'Azul', 2012, 'sdaada', 'Disponible', 'adadad', 'dadsad', 27759045, '1.jpg'),
(4, 'ABC-123', 'Blanco', 2022, 'Sedan', 'Disponible', 'Toyota', 'Corolla', 12345678, '1.jpg'),
(5, 'XYZ-789', 'Negro', 2023, 'SUV', 'Disponible', 'Ford', 'Explorer', 87654321, '2.jpg'),
(6, 'LMN-456', 'Gris', 2021, 'Sedan', 'Disponible', 'Chevrolet', 'Aveo', 11223344, '3.jpg'),
(7, 'DEF-321', 'Azul', 2024, 'Camioneta', 'Disponible', 'Hyundai', 'Santa Fe', 55667788, '4.jpg'),
(8, 'GHI-654', 'Rojo', 2020, 'Hatchback', 'Disponible', 'Kia', 'Rio', 99887766, '5.jpg'),
(9, 'JKL-987', 'Plata', 2025, 'SUV', 'Disponible', 'Honda', 'CR-V', 33445566, '6.jpg'),
(10, 'MNO-159', 'Blanco', 2023, 'Sedan', 'Disponible', 'Mazda', 'Mazda3', 22113344, '7.jpg'),
(11, 'PQR-753', 'Negro', 2022, 'Camioneta', 'Disponible', 'Toyota', 'Hilux', 77889900, '8.jpg'),
(12, 'STU-357', 'Azul', 2021, 'Sedan', 'Disponible', 'Volkswagen', 'Jetta', 44556677, '9.jpg'),
(13, 'VWX-951', 'Gris', 2024, 'SUV', 'Disponible', 'Nissan', 'X-Trail', 66554433, '10.jpg'),
(14, '21JA8777', 'Rojo', 1889, 'Camioneta', 'Disponible', 'toyota', 'xlr8', 20123456, '670513070_1621940843066734_827325321992557727_n.jpg');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `modulo`
--
ALTER TABLE `modulo`
  ADD PRIMARY KEY (`id_modulo`);

--
-- Indices de la tabla `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `rol_permisos`
--
ALTER TABLE `rol_permisos`
  ADD PRIMARY KEY (`id_permiso`),
  ADD KEY `id_rol` (`id_rol`),
  ADD KEY `id_modulo` (`id_modulo`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_rol` (`id_rol`);

--
-- Indices de la tabla `vehiculo`
--
ALTER TABLE `vehiculo`
  ADD PRIMARY KEY (`Id_Vehiculo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `modulo`
--
ALTER TABLE `modulo`
  MODIFY `id_modulo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `rol`
--
ALTER TABLE `rol`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `rol_permisos`
--
ALTER TABLE `rol_permisos`
  MODIFY `id_permiso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `vehiculo`
--
ALTER TABLE `vehiculo`
  MODIFY `Id_Vehiculo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `rol_permisos`
--
ALTER TABLE `rol_permisos`
  ADD CONSTRAINT `rol_permisos_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `rol` (`id_rol`),
  ADD CONSTRAINT `rol_permisos_ibfk_2` FOREIGN KEY (`id_modulo`) REFERENCES `modulo` (`id_modulo`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `rol` (`id_rol`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
