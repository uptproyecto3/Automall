-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 03-07-2026 a las 04:05:08
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
-- Estructura de tabla para la tabla `t_acciones`
--

CREATE TABLE `t_acciones` (
  `cod_accion` int(11) NOT NULL,
  `nom_accion` varchar(50) NOT NULL,
  `estatus` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `t_acciones`
--

INSERT INTO `t_acciones` (`cod_accion`, `nom_accion`, `estatus`) VALUES
(1, 'CREAR', 1),
(2, 'LEER', 1),
(3, 'ACTUALIZAR', 1),
(4, 'ELIMINAR', 1),
(5, 'IMPRIMIR', 1),
(6, 'APROBAR', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_banco_preguntas`
--

CREATE TABLE `t_banco_preguntas` (
  `cod_preguntas` int(11) NOT NULL,
  `nombre_preguntas` varchar(50) DEFAULT NULL,
  `estado` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `t_banco_preguntas`
--

INSERT INTO `t_banco_preguntas` (`cod_preguntas`, `nombre_preguntas`, `estado`) VALUES
(1, '¿Nombre de mi primera mascota?', 0),
(2, '¿Nombre de mi ciudad de nacimiento?', 0),
(3, '¿Nombre de mi escuela primaria?', 0),
(4, '¿Segundo nombre de mi padre?', 0),
(5, '¿Nombre de mi primer juguete favorito?', 0),
(6, '¿Nombre de mi comida favorita?', 0),
(7, '¿Nombre de mi color favorito?', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_bitacora`
--

CREATE TABLE `t_bitacora` (
  `cod_bitacora` int(11) NOT NULL,
  `cedula_usuario` varchar(20) NOT NULL,
  `cod_accion` int(11) NOT NULL,
  `cod_modulo` int(11) NOT NULL,
  `fecha` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_det_repuesta`
--

CREATE TABLE `t_det_repuesta` (
  `cod_repuesta` int(11) NOT NULL,
  `respuesta` varchar(50) NOT NULL,
  `fecha_registro` date NOT NULL,
  `cod_preguntas` int(11) NOT NULL,
  `cedula_usuario` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_modulo`
--

CREATE TABLE `t_modulo` (
  `cod_modulo` int(11) NOT NULL,
  `nombre_modulo` varchar(50) NOT NULL,
  `estatus` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `t_modulo`
--

INSERT INTO `t_modulo` (`cod_modulo`, `nombre_modulo`, `estatus`) VALUES
(1, 'Usuarios', 1),
(2, 'Vehiculos', 1),
(3, 'mantenimiento_operacional', 1),
(4, 'Bitacora', 1),
(5, 'Reportes', 1),
(6, 'Marca', 1),
(7, 'Modelo', 1),
(8, 'Catalogo', 1),
(9, 'servicios', 1),
(10, 'Taller', 1),
(11, 'Accesorios', 1),
(12, 'Insumos', 1),
(13, 'Citas', 1),
(14, 'Ventas', 1),
(15, 'Pagos', 1),
(16, 'Propietario', 1),
(17, 'Clientes', 1),
(18, 'Vendedor', 1),
(19, 'Mantenimiento a la BD', 1),
(20, 'Pagosadmin', 1),
(21, 'Compras', 1),
(22, 'Historial de Vehiculo', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_permiso`
--

CREATE TABLE `t_permiso` (
  `cod_permiso` int(11) NOT NULL,
  `cod_modulo` int(11) NOT NULL,
  `cod_accion` int(11) NOT NULL,
  `estatus` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `t_permiso`
--

INSERT INTO `t_permiso` (`cod_permiso`, `cod_modulo`, `cod_accion`, `estatus`) VALUES
(21, 2, 1, 1),
(22, 2, 2, 1),
(23, 2, 3, 1),
(24, 2, 4, 1),
(31, 3, 1, 1),
(32, 3, 2, 1),
(33, 3, 3, 1),
(35, 3, 5, 1),
(36, 3, 6, 1),
(52, 5, 2, 1),
(55, 5, 5, 1),
(61, 6, 1, 1),
(62, 6, 2, 1),
(63, 6, 3, 1),
(64, 6, 4, 1),
(71, 7, 1, 1),
(72, 7, 2, 1),
(73, 7, 3, 1),
(74, 7, 4, 1),
(81, 8, 1, 1),
(82, 8, 2, 1),
(83, 8, 3, 1),
(84, 8, 4, 1),
(91, 9, 1, 1),
(92, 9, 2, 1),
(93, 9, 3, 1),
(94, 9, 4, 1),
(101, 10, 1, 1),
(102, 10, 2, 1),
(103, 10, 3, 1),
(104, 10, 4, 1),
(111, 11, 1, 1),
(112, 11, 2, 1),
(113, 11, 3, 1),
(114, 11, 4, 1),
(121, 12, 1, 1),
(122, 12, 2, 1),
(123, 12, 3, 1),
(124, 12, 4, 1),
(131, 13, 1, 1),
(132, 13, 2, 1),
(133, 13, 3, 1),
(134, 13, 4, 1),
(136, 13, 6, 1),
(141, 14, 1, 1),
(142, 14, 2, 1),
(143, 14, 3, 1),
(145, 14, 5, 1),
(151, 15, 1, 1),
(152, 15, 2, 1),
(155, 15, 5, 1),
(161, 16, 1, 1),
(162, 16, 2, 1),
(163, 16, 3, 1),
(164, 16, 4, 1),
(171, 17, 1, 1),
(172, 17, 2, 1),
(173, 17, 3, 1),
(174, 17, 4, 1),
(181, 18, 1, 1),
(182, 18, 2, 1),
(183, 18, 3, 1),
(184, 18, 4, 1),
(201, 20, 1, 1),
(202, 20, 2, 1),
(203, 20, 3, 1),
(204, 20, 4, 1),
(205, 20, 5, 1),
(206, 20, 6, 1),
(211, 21, 1, 1),
(212, 21, 2, 1),
(213, 21, 3, 1),
(215, 21, 5, 1),
(216, 21, 6, 1),
(217, 4, 2, 1),
(218, 19, 2, 1),
(219, 19, 1, 1),
(220, 1, 1, 1),
(221, 1, 2, 1),
(222, 1, 3, 1),
(223, 1, 4, 1),
(224, 15, 3, 1),
(225, 15, 4, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_personal`
--

CREATE TABLE `t_personal` (
  `cod_personal` int(11) NOT NULL,
  `cargo` varchar(45) NOT NULL,
  `departamento` varchar(45) NOT NULL,
  `estatus` varchar(20) NOT NULL,
  `fecha_ingreso` date NOT NULL,
  `cedula_usuario` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_rol`
--

CREATE TABLE `t_rol` (
  `cod_rol` int(11) NOT NULL,
  `nombre_rol` varchar(50) NOT NULL,
  `descripcion_rol` varchar(100) DEFAULT NULL,
  `estatus` tinyint(1) NOT NULL DEFAULT 1
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
-- Estructura de tabla para la tabla `t_rol_permiso`
--

CREATE TABLE `t_rol_permiso` (
  `cod_rol_permiso` int(11) NOT NULL,
  `cod_rol` int(11) NOT NULL,
  `cod_permiso` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `t_rol_permiso`
--

INSERT INTO `t_rol_permiso` (`cod_rol_permiso`, `cod_rol`, `cod_permiso`) VALUES
(72, 3, 82),
(73, 3, 131),
(74, 3, 132),
(75, 3, 133),
(76, 3, 171),
(77, 3, 172),
(78, 3, 173),
(79, 3, 52),
(80, 3, 55),
(81, 3, 32),
(82, 3, 92),
(83, 3, 212),
(88, 5, 82),
(89, 5, 31),
(90, 5, 32),
(91, 5, 33),
(92, 5, 35),
(93, 5, 36),
(94, 5, 91),
(95, 5, 92),
(96, 5, 93),
(97, 5, 121),
(98, 5, 122),
(99, 5, 123),
(100, 5, 211),
(101, 5, 212),
(439, 4, 82),
(440, 4, 131),
(441, 4, 132),
(442, 4, 151),
(443, 4, 152),
(444, 4, 221),
(445, 4, 222),
(446, 2, 111),
(447, 2, 112),
(448, 2, 113),
(449, 2, 114),
(450, 2, 81),
(451, 2, 82),
(452, 2, 83),
(453, 2, 84),
(454, 2, 131),
(455, 2, 132),
(456, 2, 133),
(457, 2, 134),
(458, 2, 136),
(459, 2, 171),
(460, 2, 172),
(461, 2, 173),
(462, 2, 174),
(463, 2, 211),
(464, 2, 212),
(465, 2, 213),
(466, 2, 215),
(467, 2, 216),
(468, 2, 121),
(469, 2, 122),
(470, 2, 123),
(471, 2, 124),
(472, 2, 31),
(473, 2, 32),
(474, 2, 35),
(475, 2, 36),
(476, 2, 61),
(477, 2, 62),
(478, 2, 63),
(479, 2, 64),
(480, 2, 71),
(481, 2, 72),
(482, 2, 73),
(483, 2, 74),
(484, 2, 151),
(485, 2, 152),
(486, 2, 224),
(487, 2, 225),
(488, 2, 155),
(489, 2, 201),
(490, 2, 202),
(491, 2, 203),
(492, 2, 204),
(493, 2, 205),
(494, 2, 206),
(495, 2, 161),
(496, 2, 162),
(497, 2, 163),
(498, 2, 164),
(499, 2, 52),
(500, 2, 55),
(501, 2, 91),
(502, 2, 92),
(503, 2, 93),
(504, 2, 94),
(505, 2, 101),
(506, 2, 102),
(507, 2, 103),
(508, 2, 104),
(509, 2, 21),
(510, 2, 22),
(511, 2, 23),
(512, 2, 24),
(513, 2, 181),
(514, 2, 182),
(515, 2, 183),
(516, 2, 184),
(517, 2, 141),
(518, 2, 142),
(519, 2, 143),
(520, 2, 145),
(521, 1, 111),
(522, 1, 112),
(523, 1, 113),
(524, 1, 114),
(525, 1, 217),
(526, 1, 81),
(527, 1, 82),
(528, 1, 83),
(529, 1, 84),
(530, 1, 131),
(531, 1, 132),
(532, 1, 133),
(533, 1, 134),
(534, 1, 136),
(535, 1, 171),
(536, 1, 172),
(537, 1, 173),
(538, 1, 174),
(539, 1, 211),
(540, 1, 212),
(541, 1, 213),
(542, 1, 215),
(543, 1, 216),
(544, 1, 121),
(545, 1, 122),
(546, 1, 123),
(547, 1, 124),
(548, 1, 219),
(549, 1, 218),
(550, 1, 31),
(551, 1, 32),
(552, 1, 33),
(553, 1, 35),
(554, 1, 36),
(555, 1, 61),
(556, 1, 62),
(557, 1, 63),
(558, 1, 64),
(559, 1, 71),
(560, 1, 72),
(561, 1, 73),
(562, 1, 74),
(563, 1, 151),
(564, 1, 152),
(565, 1, 155),
(566, 1, 201),
(567, 1, 202),
(568, 1, 203),
(569, 1, 204),
(570, 1, 205),
(571, 1, 206),
(572, 1, 161),
(573, 1, 162),
(574, 1, 163),
(575, 1, 164),
(576, 1, 52),
(577, 1, 55),
(578, 1, 91),
(579, 1, 92),
(580, 1, 93),
(581, 1, 94),
(582, 1, 101),
(583, 1, 102),
(584, 1, 103),
(585, 1, 104),
(586, 1, 220),
(587, 1, 221),
(588, 1, 222),
(589, 1, 223),
(590, 1, 21),
(591, 1, 22),
(592, 1, 23),
(593, 1, 24),
(594, 1, 181),
(595, 1, 182),
(596, 1, 183),
(597, 1, 184),
(598, 1, 141),
(599, 1, 142),
(600, 1, 143),
(601, 1, 145);

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
  `password` varchar(255) NOT NULL,
  `estado` int(11) NOT NULL DEFAULT 1,
  `fecha_registro` date DEFAULT NULL,
  `intentos_fallidos` int(11) DEFAULT NULL,
  `ultimo_acceso` datetime DEFAULT NULL,
  `cod_rol` int(11) DEFAULT 5,
  `foto` varchar(255) DEFAULT 'default.png'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `t_usuario`
--

INSERT INTO `t_usuario` (`cedula_usuario`, `nombre`, `apellido`, `telefono`, `direccion`, `correo`, `password`, `estado`, `fecha_registro`, `intentos_fallidos`, `ultimo_acceso`, `cod_rol`, `foto`) VALUES
('18998754', 'Polinesia', 'suarez', '04122152649', 'av centro', 'prueba@gmail.com', '12345678', 1, NULL, NULL, NULL, 4, 'default.png'),
('29880513', 'daryeli', 'gutierrez', '0412555877', 'villa productiva', 'darye@gmail.com', '12345678', 1, NULL, NULL, NULL, 1, 'default.png');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `t_acciones`
--
ALTER TABLE `t_acciones`
  ADD PRIMARY KEY (`cod_accion`);

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
  ADD KEY `fk_bitacora_usuario` (`cedula_usuario`);

--
-- Indices de la tabla `t_det_repuesta`
--
ALTER TABLE `t_det_repuesta`
  ADD PRIMARY KEY (`cod_repuesta`),
  ADD UNIQUE KEY `cod_preguntas` (`cod_preguntas`),
  ADD UNIQUE KEY `cedula_usuario` (`cedula_usuario`);

--
-- Indices de la tabla `t_modulo`
--
ALTER TABLE `t_modulo`
  ADD PRIMARY KEY (`cod_modulo`);

--
-- Indices de la tabla `t_permiso`
--
ALTER TABLE `t_permiso`
  ADD PRIMARY KEY (`cod_permiso`),
  ADD KEY `fk_permiso_modulo` (`cod_modulo`),
  ADD KEY `fk_permiso_accion` (`cod_accion`);

--
-- Indices de la tabla `t_personal`
--
ALTER TABLE `t_personal`
  ADD PRIMARY KEY (`cod_personal`),
  ADD UNIQUE KEY `cedula_usuario` (`cedula_usuario`);

--
-- Indices de la tabla `t_rol`
--
ALTER TABLE `t_rol`
  ADD PRIMARY KEY (`cod_rol`);

--
-- Indices de la tabla `t_rol_permiso`
--
ALTER TABLE `t_rol_permiso`
  ADD PRIMARY KEY (`cod_rol_permiso`),
  ADD KEY `fk_rp_rol` (`cod_rol`),
  ADD KEY `fk_rp_permiso` (`cod_permiso`);

--
-- Indices de la tabla `t_usuario`
--
ALTER TABLE `t_usuario`
  ADD PRIMARY KEY (`cedula_usuario`),
  ADD UNIQUE KEY `correo_unique` (`correo`),
  ADD KEY `fk_usuario_rol` (`cod_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `t_acciones`
--
ALTER TABLE `t_acciones`
  MODIFY `cod_accion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `t_banco_preguntas`
--
ALTER TABLE `t_banco_preguntas`
  MODIFY `cod_preguntas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `t_bitacora`
--
ALTER TABLE `t_bitacora`
  MODIFY `cod_bitacora` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `t_det_repuesta`
--
ALTER TABLE `t_det_repuesta`
  MODIFY `cod_repuesta` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `t_modulo`
--
ALTER TABLE `t_modulo`
  MODIFY `cod_modulo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `t_permiso`
--
ALTER TABLE `t_permiso`
  MODIFY `cod_permiso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=226;

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
-- AUTO_INCREMENT de la tabla `t_rol_permiso`
--
ALTER TABLE `t_rol_permiso`
  MODIFY `cod_rol_permiso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=602;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `t_bitacora`
--
ALTER TABLE `t_bitacora`
  ADD CONSTRAINT `fk_bitacora_usuario` FOREIGN KEY (`cedula_usuario`) REFERENCES `t_usuario` (`cedula_usuario`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `t_det_repuesta`
--
ALTER TABLE `t_det_repuesta`
  ADD CONSTRAINT `fk_resp_preg` FOREIGN KEY (`cod_preguntas`) REFERENCES `t_banco_preguntas` (`cod_preguntas`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_resp_usu` FOREIGN KEY (`cedula_usuario`) REFERENCES `t_usuario` (`cedula_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `t_permiso`
--
ALTER TABLE `t_permiso`
  ADD CONSTRAINT `fk_permiso_accion` FOREIGN KEY (`cod_accion`) REFERENCES `t_acciones` (`cod_accion`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_permiso_modulo` FOREIGN KEY (`cod_modulo`) REFERENCES `t_modulo` (`cod_modulo`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `t_personal`
--
ALTER TABLE `t_personal`
  ADD CONSTRAINT `fk_personal_usuario` FOREIGN KEY (`cedula_usuario`) REFERENCES `t_usuario` (`cedula_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `t_rol_permiso`
--
ALTER TABLE `t_rol_permiso`
  ADD CONSTRAINT `fk_rp_permiso` FOREIGN KEY (`cod_permiso`) REFERENCES `t_permiso` (`cod_permiso`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_rp_rol` FOREIGN KEY (`cod_rol`) REFERENCES `t_rol` (`cod_rol`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `t_usuario`
--
ALTER TABLE `t_usuario`
  ADD CONSTRAINT `fk_usuario_rol` FOREIGN KEY (`cod_rol`) REFERENCES `t_rol` (`cod_rol`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
