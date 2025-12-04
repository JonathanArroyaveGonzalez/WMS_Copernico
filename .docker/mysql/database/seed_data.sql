-- ================================================================
-- SCRIPT DE DATOS ADICIONALES PARA INTELIGENCIA DE NEGOCIO
-- Sistema WMS - Warehouse Management System
-- Ejecutar después de init.sql
-- ================================================================

-- Usar la base de datos
USE wms_management_system;

-- ================================================================
-- 1. MÁS PROVEEDORES (para diversificar la cadena de suministro)
-- ================================================================

INSERT INTO `proveedores` (`id`, `nombre`, `ruc`, `telefono`, `email`, `direccion`, `activo`) VALUES
(6, 'Importadora del Oriente', '20678901234', '987654326', 'ventas@importadora-oriente.com', 'Av. Iquitos 890, Loreto', 1),
(7, 'Distribuidora Electrónica Sur', '20789012345', '987654327', 'pedidos@electrosur.com', 'Jr. Arequipa 456, Arequipa', 1),
(8, 'Manufacturas Textiles Perú', '20890123456', '987654328', 'contacto@textilesperu.com', 'Av. Los Industriales 789, Ate', 1),
(9, 'Alimentos Naturales SAC', '20901234567', '987654329', 'info@alimentosnaturales.com', 'Calle Organica 321, La Molina', 1),
(10, 'Deportes y Fitness Corp', '20012345678', '987654330', 'ventas@deportesfitness.com', 'Av. Olimpica 555, Surco', 1);

-- ================================================================
-- 2. MÁS CLIENTES (empresariales y particulares)
-- ================================================================

INSERT INTO `clientes` (`id`, `nombre`, `documento`, `telefono`, `email`, `direccion`, `activo`) VALUES
-- Clientes Empresariales
(26, 'Cadena de Farmacias Salud+', '20111333444', '989111222', 'compras@saludmas.com', 'Av. Salaverry 1500, Jesus Maria', 1),
(27, 'Hoteles del Pacifico S.A.', '20222444555', '989222333', 'suministros@hotelespacifico.com', 'Malecon Cisneros 200, Miraflores', 1),
(28, 'Constructora Los Andes', '20333555666', '989333444', 'logistica@constructoraandes.com', 'Av. Primavera 800, Surco', 1),
(29, 'Colegios Unidos del Peru', '20444666777', '989444555', 'adquisiciones@colegiosunidos.edu.pe', 'Jr. Educacion 450, San Isidro', 1),
(30, 'Restaurantes Gourmet Group', '20555777888', '989555666', 'proveedores@gourmetgroup.com', 'Calle Gastronomia 150, Barranco', 1),
(31, 'Clinica San Gabriel', '20666888999', '989666777', 'compras@clinicasangabriel.com', 'Av. Javier Prado 4500, La Molina', 1),
(32, 'Gimnasios PowerFit', '20777999000', '989777888', 'equipamiento@powerfit.pe', 'Av. Benavides 2500, Miraflores', 1),
(33, 'Universidad Tecnologica', '20888000111', '989888999', 'adquisiciones@utec.edu.pe', 'Jr. Medrano Silva 165, Barranco', 1),
-- Clientes Particulares adicionales
(34, 'Ricardo Vargas Mendez', '10111222', '990111222', 'rvargas@gmail.com', 'Calle Los Alamos 180, La Molina', 1),
(35, 'Elena Castro Paredes', '10222333', '990222333', 'ecastro@hotmail.com', 'Jr. Los Jazmines 290, San Borja', 1),
(36, 'Marco Antonio Ruiz', '10333444', '990333444', 'maruiz@yahoo.com', 'Av. Primavera 1200, Surco', 1),
(37, 'Lucia Fernandez Torres', '10444555', '990444555', 'lfernandez@gmail.com', 'Calle Las Orquideas 340, Surquillo', 1),
(38, 'Pedro Huaman Quispe', '10555666', '990555666', 'phuaman@outlook.com', 'Jr. Ayacucho 560, Breña', 1),
(39, 'Rosa Martinez Soto', '10666777', '990666777', 'rmartinez@gmail.com', 'Av. Venezuela 890, Lima', 1),
(40, 'Jorge Castañeda Vega', '10777888', '990777888', 'jcastaneda@hotmail.com', 'Calle Tacna 120, Magdalena', 1);

-- ================================================================
-- 3. MÁS VENTAS (distribuidas en varios meses para análisis temporal)
-- ================================================================

-- Ventas de Septiembre 2025
INSERT INTO `ventas` (`id`, `numero_factura`, `cliente_id`, `usuario_id`, `fecha`, `total`, `estado`, `tipo_pago`, `notas`) VALUES
(36, 'V-2025-036', 26, 4, '2025-11-02', 3450.00, 'completada', 'transferencia', 'Pedido inicial Farmacias Salud+'),
(37, 'V-2025-037', 27, 4, '2025-11-05', 8750.00, 'completada', 'transferencia', 'Equipamiento hoteles'),
(38, 'V-2025-038', 28, 4, '2025-11-08', 2890.00, 'completada', 'transferencia', 'Suministros construccion'),
(39, 'V-2025-039', 34, 4, '2025-11-10', 425.00, 'completada', 'tarjeta', 'Compra electronica'),
(40, 'V-2025-040', 29, 4, '2025-11-12', 5680.00, 'completada', 'transferencia', 'Material escolar inicial'),
(41, 'V-2025-041', 35, 4, '2025-11-15', 320.00, 'completada', 'efectivo', 'Productos hogar'),
(42, 'V-2025-042', 30, 4, '2025-11-18', 4250.00, 'completada', 'transferencia', 'Insumos restaurantes'),
(43, 'V-2025-043', 36, 4, '2025-11-20', 580.00, 'completada', 'tarjeta', 'Electronica personal'),
(44, 'V-2025-044', 31, 4, '2025-11-22', 6890.00, 'completada', 'transferencia', 'Equipos clinica'),
(45, 'V-2025-045', 37, 4, '2025-11-25', 290.00, 'completada', 'efectivo', 'Ropa deportiva'),
(46, 'V-2025-046', 32, 4, '2025-11-28', 12500.00, 'completada', 'transferencia', 'Equipamiento gimnasios'),
(47, 'V-2025-047', 38, 4, '2025-11-30', 185.00, 'completada', 'tarjeta', 'Articulos oficina');
-- Más ventas de Octubre 2025
INSERT INTO `ventas` (`id`, `numero_factura`, `cliente_id`, `usuario_id`, `fecha`, `total`, `estado`, `tipo_pago`, `notas`) VALUES
(48, 'V-2025-048', 33, 4, '2025-10-03', 9850.00, 'completada', 'transferencia', 'Equipos laboratorio universidad'),
(49, 'V-2025-049', 26, 4, '2025-10-07', 2750.00, 'completada', 'transferencia', 'Reposicion farmacias'),
(50, 'V-2025-050', 39, 4, '2025-10-10', 445.00, 'completada', 'efectivo', 'Productos varios'),
(51, 'V-2025-051', 27, 4, '2025-10-13', 5680.00, 'completada', 'transferencia', 'Suministros hoteles mensual'),
(52, 'V-2025-052', 40, 4, '2025-10-15', 680.00, 'completada', 'tarjeta', 'Electronica y hogar'),
(53, 'V-2025-053', 30, 4, '2025-10-18', 3890.00, 'completada', 'transferencia', 'Pedido quincenal restaurantes'),
(54, 'V-2025-054', 34, 4, '2025-10-21', 520.00, 'completada', 'tarjeta', 'Compra personal'),
(55, 'V-2025-055', 31, 4, '2025-10-24', 4560.00, 'completada', 'transferencia', 'Equipamiento medico adicional'),
(56, 'V-2025-056', 35, 4, '2025-10-27', 395.00, 'completada', 'efectivo', 'Productos mixtos'),
(57, 'V-2025-057', 28, 4, '2025-10-30', 3250.00, 'completada', 'transferencia', 'Materiales obra');

-- Ventas de Noviembre 2025 (más intensidad - temporada alta)
INSERT INTO `ventas` (`id`, `numero_factura`, `cliente_id`, `usuario_id`, `fecha`, `total`, `estado`, `tipo_pago`, `notas`) VALUES
(58, 'V-2025-058', 32, 4, '2025-11-02', 8950.00, 'completada', 'transferencia', 'Black Friday gimnasios'),
(59, 'V-2025-059', 26, 4, '2025-11-04', 4250.00, 'completada', 'transferencia', 'Stock farmacias noviembre'),
(60, 'V-2025-060', 36, 4, '2025-11-05', 890.00, 'completada', 'tarjeta', 'Ofertas electronica'),
(61, 'V-2025-061', 29, 4, '2025-11-06', 7850.00, 'completada', 'transferencia', 'Materiales fin de año escolar'),
(62, 'V-2025-062', 37, 4, '2025-11-07', 445.00, 'completada', 'efectivo', 'Ropa temporada'),
(63, 'V-2025-063', 30, 4, '2025-11-08', 5680.00, 'completada', 'transferencia', 'Preparacion fiestas restaurantes'),
(64, 'V-2025-064', 38, 4, '2025-11-09', 325.00, 'completada', 'tarjeta', 'Articulos varios'),
(65, 'V-2025-065', 33, 4, '2025-11-10', 6750.00, 'completada', 'transferencia', 'Equipos universidad'),
(66, 'V-2025-066', 39, 4, '2025-11-11', 580.00, 'completada', 'efectivo', 'Black Friday personal'),
(67, 'V-2025-067', 27, 4, '2025-11-12', 9850.00, 'completada', 'transferencia', 'Renovacion hoteles temporada'),
(68, 'V-2025-068', 40, 4, '2025-11-13', 750.00, 'completada', 'tarjeta', 'Promociones electronica'),
(69, 'V-2025-069', 31, 4, '2025-11-14', 5890.00, 'completada', 'transferencia', 'Equipos medicos especiales'),
(70, 'V-2025-070', 34, 4, '2025-11-15', 1250.00, 'completada', 'tarjeta', 'Compra grande personal'),
(71, 'V-2025-071', 28, 4, '2025-11-16', 4580.00, 'completada', 'transferencia', 'Materiales proyecto'),
(72, 'V-2025-072', 35, 4, '2025-11-17', 685.00, 'completada', 'efectivo', 'Productos hogar ofertas'),
(73, 'V-2025-073', 32, 4, '2025-11-18', 11250.00, 'completada', 'transferencia', 'Equipamiento nuevo local'),
(74, 'V-2025-074', 36, 4, '2025-11-19', 920.00, 'completada', 'tarjeta', 'Tech deals'),
(75, 'V-2025-075', 26, 4, '2025-11-20', 3890.00, 'completada', 'transferencia', 'Reposicion urgente'),
(76, 'V-2025-076', 37, 4, '2025-11-21', 545.00, 'completada', 'efectivo', 'Compras variadas'),
(77, 'V-2025-077', 30, 4, '2025-11-22', 6750.00, 'completada', 'transferencia', 'Pedido especial festividades'),
(78, 'V-2025-078', 38, 4, '2025-11-23', 420.00, 'completada', 'tarjeta', 'Cyber Monday'),
(79, 'V-2025-079', 29, 4, '2025-11-24', 8950.00, 'completada', 'transferencia', 'Clausura escolar'),
(80, 'V-2025-080', 39, 4, '2025-11-25', 780.00, 'completada', 'efectivo', 'Regalos navidad'),
(81, 'V-2025-081', 33, 4, '2025-11-26', 5450.00, 'completada', 'transferencia', 'Fin de semestre'),
(82, 'V-2025-082', 40, 4, '2025-11-27', 890.00, 'completada', 'tarjeta', 'Electronica regalos'),
(83, 'V-2025-083', 27, 4, '2025-11-28', 7850.00, 'completada', 'transferencia', 'Temporada alta hoteles'),
(84, 'V-2025-084', 34, 4, '2025-11-29', 1580.00, 'completada', 'tarjeta', 'Black Friday final'),
(85, 'V-2025-085', 31, 4, '2025-11-30', 4250.00, 'completada', 'transferencia', 'Cierre mes clinica');

-- Ventas de Diciembre 2025 (hasta fecha actual)
INSERT INTO `ventas` (`id`, `numero_factura`, `cliente_id`, `usuario_id`, `fecha`, `total`, `estado`, `tipo_pago`, `notas`) VALUES
(86, 'V-2025-086', 32, 4, '2025-12-01', 9580.00, 'completada', 'transferencia', 'Inicio temporada navideña gimnasios'),
(87, 'V-2025-087', 35, 4, '2025-12-01', 680.00, 'completada', 'efectivo', 'Decoracion navidad'),
(88, 'V-2025-088', 26, 4, '2025-12-02', 5250.00, 'completada', 'transferencia', 'Stock diciembre farmacias'),
(89, 'V-2025-089', 36, 4, '2025-12-02', 1450.00, 'completada', 'tarjeta', 'Regalos tecnologicos'),
(90, 'V-2025-090', 30, 4, '2025-12-03', 8950.00, 'pendiente', 'transferencia', 'Gran pedido navidad restaurantes');

-- ================================================================
-- 4. DETALLES DE VENTAS PARA LAS NUEVAS VENTAS
-- ================================================================

-- Detalles ventas Septiembre
INSERT INTO `detalle_ventas` (`venta_id`, `producto_id`, `cantidad`, `precio_unitario`, `subtotal`) VALUES
-- Venta 36 - Farmacias
(36, 55, 50, 20.00, 1000.00),
(36, 56, 30, 9.00, 270.00),
(36, 48, 20, 45.00, 900.00),
(36, 53, 40, 32.00, 1280.00),

-- Venta 37 - Hoteles
(37, 43, 25, 85.00, 2125.00),
(37, 44, 30, 55.00, 1650.00),
(37, 45, 40, 65.00, 2600.00),
(37, 47, 15, 155.00, 2325.00),

-- Venta 38 - Constructora
(38, 67, 15, 75.00, 1125.00),
(38, 72, 5, 155.00, 775.00),
(38, 66, 20, 42.00, 840.00),

-- Venta 39 - Personal
(39, 2, 3, 45.00, 135.00),
(39, 5, 2, 110.00, 220.00),
(39, 11, 2, 32.00, 64.00),

-- Venta 40 - Colegios
(40, 55, 80, 20.00, 1600.00),
(40, 56, 100, 9.00, 900.00),
(40, 57, 50, 11.50, 575.00),
(40, 61, 60, 32.00, 1920.00),
(40, 62, 40, 17.50, 700.00),

-- Venta 41 - Personal hogar
(41, 43, 2, 85.00, 170.00),
(41, 44, 2, 55.00, 110.00),
(41, 40, 2, 15.50, 31.00),

-- Venta 42 - Restaurantes
(42, 16, 80, 18.90, 1512.00),
(42, 17, 60, 12.50, 750.00),
(42, 20, 40, 24.00, 960.00),
(42, 22, 30, 35.00, 1050.00),

-- Venta 43 - Personal electronica
(43, 3, 2, 135.00, 270.00),
(43, 5, 2, 110.00, 220.00),
(43, 11, 3, 32.00, 96.00),

-- Venta 44 - Clinica
(44, 1, 2, 2200.00, 4400.00),
(44, 4, 3, 550.00, 1650.00),
(44, 9, 2, 450.00, 900.00),

-- Venta 45 - Personal deportes
(45, 66, 3, 42.00, 126.00),
(45, 68, 3, 22.00, 66.00),
(45, 70, 3, 35.00, 105.00),

-- Venta 46 - Gimnasios
(46, 67, 40, 75.00, 3000.00),
(46, 72, 30, 155.00, 4650.00),
(46, 66, 50, 42.00, 2100.00),
(46, 70, 60, 35.00, 2100.00),
(46, 71, 15, 45.00, 675.00),

-- Venta 47 - Oficina personal
(47, 55, 5, 20.00, 100.00),
(47, 56, 3, 9.00, 27.00),
(47, 58, 2, 45.00, 90.00);

-- Detalles ventas Octubre adicionales
INSERT INTO `detalle_ventas` (`venta_id`, `producto_id`, `cantidad`, `precio_unitario`, `subtotal`) VALUES
-- Venta 48 - Universidad
(48, 1, 3, 2200.00, 6600.00),
(48, 4, 4, 550.00, 2200.00),
(48, 58, 25, 45.00, 1125.00),

-- Venta 49 - Farmacias reposicion
(49, 55, 40, 20.00, 800.00),
(49, 48, 25, 45.00, 1125.00),
(49, 53, 25, 32.00, 800.00),

-- Venta 50 - Personal
(50, 33, 5, 35.00, 175.00),
(50, 40, 8, 15.50, 124.00),
(50, 41, 5, 28.00, 140.00),

-- Venta 51 - Hoteles mensual
(51, 43, 20, 85.00, 1700.00),
(51, 45, 35, 65.00, 2275.00),
(51, 54, 30, 52.00, 1560.00),

-- Venta 52 - Personal
(52, 3, 2, 135.00, 270.00),
(52, 8, 2, 185.00, 370.00),
(52, 40, 2, 15.50, 31.00),

-- Venta 53 - Restaurantes quincenal
(53, 16, 60, 18.90, 1134.00),
(53, 17, 50, 12.50, 625.00),
(53, 21, 35, 42.00, 1470.00),
(53, 20, 30, 24.00, 720.00),

-- Venta 54 - Personal
(54, 5, 2, 110.00, 220.00),
(54, 13, 3, 65.00, 195.00),
(54, 11, 4, 32.00, 128.00),

-- Venta 55 - Clinica equipos
(55, 9, 4, 450.00, 1800.00),
(55, 6, 3, 750.00, 2250.00),
(55, 10, 4, 155.00, 620.00),

-- Venta 56 - Personal
(56, 26, 15, 6.20, 93.00),
(56, 75, 5, 35.00, 175.00),
(56, 77, 2, 72.00, 144.00),

-- Venta 57 - Constructora
(57, 48, 30, 45.00, 1350.00),
(57, 67, 10, 75.00, 750.00),
(57, 72, 5, 155.00, 775.00),
(57, 71, 10, 45.00, 450.00);

-- Detalles ventas Noviembre (temporada alta)
INSERT INTO `detalle_ventas` (`venta_id`, `producto_id`, `cantidad`, `precio_unitario`, `subtotal`) VALUES
-- Venta 58 - Gimnasios Black Friday
(58, 67, 35, 75.00, 2625.00),
(58, 72, 25, 155.00, 3875.00),
(58, 66, 40, 42.00, 1680.00),
(58, 70, 25, 35.00, 875.00),

-- Venta 59 - Farmacias stock
(59, 55, 60, 20.00, 1200.00),
(59, 56, 80, 9.00, 720.00),
(59, 48, 30, 45.00, 1350.00),
(59, 53, 30, 32.00, 960.00),

-- Venta 60 - Personal electronica
(60, 1, 0, 2200.00, 0.00),  -- Solo para referencia
(60, 6, 1, 750.00, 750.00),
(60, 3, 1, 135.00, 135.00),

-- Venta 61 - Colegios fin año
(61, 55, 100, 20.00, 2000.00),
(61, 56, 150, 9.00, 1350.00),
(61, 64, 80, 22.00, 1760.00),
(61, 61, 80, 32.00, 2560.00),

-- Venta 62 - Personal ropa
(62, 31, 3, 65.00, 195.00),
(62, 33, 4, 35.00, 140.00),
(62, 37, 3, 42.00, 126.00),

-- Venta 63 - Restaurantes fiestas
(63, 16, 100, 18.90, 1890.00),
(63, 17, 80, 12.50, 1000.00),
(63, 20, 60, 24.00, 1440.00),
(63, 22, 40, 35.00, 1400.00),

-- Venta 64 - Personal
(64, 13, 3, 65.00, 195.00),
(64, 11, 4, 32.00, 128.00),

-- Venta 65 - Universidad equipos
(65, 1, 2, 2200.00, 4400.00),
(65, 9, 3, 450.00, 1350.00),
(65, 58, 25, 45.00, 1125.00),

-- Venta 66 - Personal Black Friday
(66, 8, 2, 185.00, 370.00),
(66, 5, 2, 110.00, 220.00),

-- Venta 67 - Hoteles renovacion
(67, 43, 35, 85.00, 2975.00),
(67, 44, 40, 55.00, 2200.00),
(67, 45, 50, 65.00, 3250.00),
(67, 47, 10, 155.00, 1550.00),

-- Venta 68 - Personal
(68, 6, 1, 750.00, 750.00),

-- Venta 69 - Clinica especial
(69, 9, 5, 450.00, 2250.00),
(69, 1, 1, 2200.00, 2200.00),
(69, 10, 10, 155.00, 1550.00),

-- Venta 70 - Personal grande
(70, 4, 1, 550.00, 550.00),
(70, 8, 2, 185.00, 370.00),
(70, 3, 2, 135.00, 270.00),

-- Venta 71 - Constructora proyecto
(71, 48, 40, 45.00, 1800.00),
(71, 67, 15, 75.00, 1125.00),
(71, 72, 8, 155.00, 1240.00),
(71, 66, 10, 42.00, 420.00),

-- Venta 72 - Personal hogar
(72, 43, 3, 85.00, 255.00),
(72, 44, 4, 55.00, 220.00),
(72, 45, 3, 65.00, 195.00),

-- Venta 73 - Gimnasios nuevo local
(73, 67, 50, 75.00, 3750.00),
(73, 72, 30, 155.00, 4650.00),
(73, 66, 40, 42.00, 1680.00),
(73, 70, 35, 35.00, 1225.00),

-- Venta 74 - Personal tech
(74, 3, 3, 135.00, 405.00),
(74, 7, 3, 95.00, 285.00),
(74, 5, 2, 110.00, 220.00),

-- Venta 75 - Farmacias urgente
(75, 55, 50, 20.00, 1000.00),
(75, 48, 35, 45.00, 1575.00),
(75, 57, 60, 11.50, 690.00),
(75, 59, 25, 28.00, 700.00),

-- Venta 76 - Personal
(76, 31, 3, 65.00, 195.00),
(76, 35, 3, 72.00, 216.00),
(76, 40, 8, 15.50, 124.00),

-- Venta 77 - Restaurantes especial
(77, 16, 120, 18.90, 2268.00),
(77, 17, 100, 12.50, 1250.00),
(77, 21, 50, 42.00, 2100.00),
(77, 22, 35, 35.00, 1225.00),

-- Venta 78 - Personal Cyber
(78, 2, 4, 45.00, 180.00),
(78, 11, 5, 32.00, 160.00),
(78, 14, 3, 28.00, 84.00),

-- Venta 79 - Colegios clausura
(79, 73, 30, 95.00, 2850.00),
(79, 74, 25, 85.00, 2125.00),
(79, 75, 40, 35.00, 1400.00),
(79, 78, 35, 78.00, 2730.00),

-- Venta 80 - Personal regalos
(80, 77, 5, 72.00, 360.00),
(80, 74, 3, 85.00, 255.00),
(80, 75, 5, 35.00, 175.00),

-- Venta 81 - Universidad semestre
(81, 1, 1, 2200.00, 2200.00),
(81, 4, 2, 550.00, 1100.00),
(81, 9, 2, 450.00, 900.00),
(81, 58, 30, 45.00, 1350.00),

-- Venta 82 - Personal electronica
(82, 6, 1, 750.00, 750.00),
(82, 3, 1, 135.00, 135.00),

-- Venta 83 - Hoteles alta
(83, 43, 30, 85.00, 2550.00),
(83, 44, 35, 55.00, 1925.00),
(83, 45, 40, 65.00, 2600.00),
(83, 54, 15, 52.00, 780.00),

-- Venta 84 - Personal BF final
(84, 1, 0, 2200.00, 0.00),
(84, 6, 2, 750.00, 1500.00),
(84, 5, 0, 110.00, 0.00),

-- Venta 85 - Clinica cierre
(85, 9, 4, 450.00, 1800.00),
(85, 55, 60, 20.00, 1200.00),
(85, 48, 30, 45.00, 1350.00);

-- Detalles ventas Diciembre
INSERT INTO `detalle_ventas` (`venta_id`, `producto_id`, `cantidad`, `precio_unitario`, `subtotal`) VALUES
-- Venta 86 - Gimnasios navidad
(86, 67, 40, 75.00, 3000.00),
(86, 72, 25, 155.00, 3875.00),
(86, 66, 35, 42.00, 1470.00),
(86, 70, 40, 35.00, 1400.00),

-- Venta 87 - Personal decoracion
(87, 54, 8, 52.00, 416.00),
(87, 53, 6, 32.00, 192.00),
(87, 50, 1, 72.00, 72.00),

-- Venta 88 - Farmacias diciembre
(88, 55, 80, 20.00, 1600.00),
(88, 56, 100, 9.00, 900.00),
(88, 48, 40, 45.00, 1800.00),
(88, 53, 30, 32.00, 960.00),

-- Venta 89 - Personal regalos tech
(89, 6, 1, 750.00, 750.00),
(89, 7, 3, 95.00, 285.00),
(89, 8, 2, 185.00, 370.00),

-- Venta 90 - Restaurantes navidad (pendiente)
(90, 16, 150, 18.90, 2835.00),
(90, 17, 120, 12.50, 1500.00),
(90, 20, 80, 24.00, 1920.00),
(90, 21, 60, 42.00, 2520.00);

-- ================================================================
-- 5. MÁS COMPRAS PARA EQUILIBRAR INVENTARIO
-- ================================================================

INSERT INTO `compras` (`id`, `numero_factura`, `proveedor_id`, `usuario_id`, `fecha`, `total`, `estado`, `notas`) VALUES
-- Compras Septiembre
(21, 'C-2025-021', 1, 2, '2025-09-01', 12500.00, 'completada', 'Stock inicial Q4 electronica'),
(22, 'C-2025-022', 2, 2, '2025-09-05', 4850.00, 'completada', 'Alimentos inicio trimestre'),
(23, 'C-2025-023', 3, 2, '2025-09-10', 3650.00, 'completada', 'Ropa temporada primavera'),
(24, 'C-2025-024', 4, 2, '2025-09-15', 5200.00, 'completada', 'Articulos hogar nuevos'),
(25, 'C-2025-025', 10, 2, '2025-09-20', 8500.00, 'completada', 'Equipamiento deportivo especial'),
(26, 'C-2025-026', 5, 2, '2025-09-25', 2800.00, 'completada', 'Material oficina escolar'),
-- Compras Octubre adicionales
(27, 'C-2025-027', 6, 2, '2025-10-02', 6500.00, 'completada', 'Productos importados oriente'),
(28, 'C-2025-028', 7, 2, '2025-10-08', 9800.00, 'completada', 'Electronica premium sur'),
(29, 'C-2025-029', 8, 2, '2025-10-15', 4200.00, 'completada', 'Textiles manufactura'),
(30, 'C-2025-030', 9, 2, '2025-10-22', 3500.00, 'completada', 'Alimentos organicos'),
-- Compras Noviembre (preparacion temporada alta)
(31, 'C-2025-031', 1, 2, '2025-11-01', 15800.00, 'completada', 'Stock electronica Black Friday'),
(32, 'C-2025-032', 10, 2, '2025-11-05', 12500.00, 'completada', 'Deportes temporada alta'),
(33, 'C-2025-033', 2, 2, '2025-11-08', 6800.00, 'completada', 'Alimentos festividades'),
(34, 'C-2025-034', 3, 2, '2025-11-12', 5500.00, 'completada', 'Ropa invierno y navidad'),
(35, 'C-2025-035', 4, 2, '2025-11-15', 7200.00, 'completada', 'Hogar decoracion navideña'),
(36, 'C-2025-036', 1, 2, '2025-11-20', 18500.00, 'completada', 'Juguetes campaña navidad'),
(37, 'C-2025-037', 5, 2, '2025-11-25', 4200.00, 'completada', 'Oficina fin de año'),
-- Compras Diciembre
(38, 'C-2025-038', 1, 2, '2025-12-01', 8500.00, 'completada', 'Reposicion urgente electronica'),
(39, 'C-2025-039', 2, 2, '2025-12-02', 5800.00, 'pendiente', 'Stock alimentos diciembre');

-- ================================================================
-- 6. DETALLES DE COMPRAS ADICIONALES
-- ================================================================

INSERT INTO `detalle_compras` (`compra_id`, `producto_id`, `cantidad`, `precio_unitario`, `subtotal`) VALUES
-- Compra 21 - Electronica Q4
(21, 1, 10, 1500.00, 15000.00),
(21, 4, 15, 350.00, 5250.00),
(21, 6, 12, 450.00, 5400.00),
(21, 9, 8, 280.00, 2240.00),

-- Compra 22 - Alimentos
(22, 16, 100, 12.50, 1250.00),
(22, 17, 80, 8.00, 640.00),
(22, 20, 60, 15.00, 900.00),
(22, 21, 50, 28.00, 1400.00),
(22, 22, 40, 22.00, 880.00),

-- Compra 23 - Ropa
(23, 31, 40, 35.00, 1400.00),
(23, 32, 35, 45.00, 1575.00),
(23, 35, 30, 38.00, 1140.00),

-- Compra 24 - Hogar
(24, 43, 30, 45.00, 1350.00),
(24, 44, 40, 30.00, 1200.00),
(24, 45, 50, 35.00, 1750.00),
(24, 47, 20, 85.00, 1700.00),

-- Compra 25 - Deportes
(25, 67, 50, 40.00, 2000.00),
(25, 72, 40, 85.00, 3400.00),
(25, 66, 60, 22.00, 1320.00),
(25, 70, 80, 18.00, 1440.00),

-- Compra 26 - Oficina
(26, 55, 100, 12.00, 1200.00),
(26, 56, 80, 4.50, 360.00),
(26, 61, 50, 18.00, 900.00),
(26, 64, 60, 12.00, 720.00),

-- Compra 31 - Black Friday electronica
(31, 1, 15, 1500.00, 22500.00),
(31, 6, 20, 450.00, 9000.00),
(31, 3, 30, 80.00, 2400.00),
(31, 8, 40, 120.00, 4800.00),

-- Compra 32 - Deportes alta
(32, 67, 80, 40.00, 3200.00),
(32, 72, 50, 85.00, 4250.00),
(32, 66, 100, 22.00, 2200.00),
(32, 70, 100, 18.00, 1800.00),

-- Compra 33 - Alimentos fiestas
(33, 16, 150, 12.50, 1875.00),
(33, 17, 120, 8.00, 960.00),
(33, 20, 100, 15.00, 1500.00),
(33, 21, 80, 28.00, 2240.00),

-- Compra 34 - Ropa navidad
(34, 31, 50, 35.00, 1750.00),
(34, 35, 40, 38.00, 1520.00),
(34, 42, 30, 42.00, 1260.00),

-- Compra 35 - Hogar decoracion
(35, 43, 40, 45.00, 1800.00),
(35, 54, 50, 28.00, 1400.00),
(35, 53, 60, 32.00, 1920.00),
(35, 50, 25, 38.00, 950.00),

-- Compra 36 - Juguetes navidad
(36, 73, 60, 55.00, 3300.00),
(36, 74, 50, 45.00, 2250.00),
(36, 76, 40, 65.00, 2600.00),
(36, 78, 50, 42.00, 2100.00),
(36, 75, 80, 18.00, 1440.00),
(36, 77, 60, 38.00, 2280.00),

-- Compra 37 - Oficina fin año
(37, 55, 120, 12.00, 1440.00),
(37, 56, 100, 4.50, 450.00),
(37, 64, 80, 12.00, 960.00),
(37, 57, 60, 6.00, 360.00),

-- Compra 38 - Electronica reposicion
(38, 6, 15, 450.00, 6750.00),
(38, 7, 25, 55.00, 1375.00),
(38, 5, 20, 60.00, 1200.00),

-- Compra 39 - Alimentos diciembre
(39, 16, 120, 12.50, 1500.00),
(39, 17, 100, 8.00, 800.00),
(39, 20, 80, 15.00, 1200.00),
(39, 22, 60, 22.00, 1320.00);

-- ================================================================
-- 7. MÁS MOVIMIENTOS DE INVENTARIO
-- ================================================================

INSERT INTO `movimientos_inventario` (`producto_id`, `almacen_id`, `tipo_movimiento`, `cantidad`, `usuario_id`, `referencia`, `motivo`, `fecha`) VALUES
-- Entradas de compras
(1, 1, 'entrada', 10, 2, 'C-2025-021', 'Reposicion laptops Q4', '2025-09-01 10:00:00'),
(6, 1, 'entrada', 12, 2, 'C-2025-021', 'Nuevas tablets', '2025-09-01 10:30:00'),
(67, 3, 'entrada', 50, 2, 'C-2025-025', 'Mancuernas deportes', '2025-09-20 09:00:00'),
(72, 3, 'entrada', 40, 2, 'C-2025-025', 'Kits pesas', '2025-09-20 09:30:00'),

-- Salidas por ventas
(1, 1, 'salida', 2, 4, 'V-2025-044', 'Venta clinica', '2025-09-22 14:00:00'),
(67, 3, 'salida', 40, 4, 'V-2025-046', 'Venta gimnasios', '2025-09-28 11:00:00'),
(43, 2, 'salida', 25, 4, 'V-2025-037', 'Venta hoteles', '2025-09-05 15:00:00'),

-- Ajustes
(16, 2, 'ajuste', -5, 5, 'AJ-004', 'Productos vencidos', '2025-10-15 08:00:00'),
(33, 1, 'ajuste', 3, 5, 'AJ-005', 'Encontrados en revision', '2025-10-20 09:00:00'),
(55, 1, 'ajuste', -10, 5, 'AJ-006', 'Daño por humedad', '2025-11-01 08:30:00'),

-- Transferencias entre almacenes
(6, 1, 'salida', 5, 5, 'TRF-003', 'Transferencia a zona sur', '2025-10-25 10:00:00'),
(6, 3, 'entrada', 5, 5, 'TRF-003', 'Recepcion zona sur', '2025-10-25 14:00:00'),
(67, 3, 'salida', 10, 5, 'TRF-004', 'Reubicacion almacen principal', '2025-11-10 09:00:00'),
(67, 1, 'entrada', 10, 5, 'TRF-004', 'Recepcion almacen principal', '2025-11-10 11:00:00'),

-- Entradas Black Friday
(1, 1, 'entrada', 15, 2, 'C-2025-031', 'Stock Black Friday', '2025-11-01 08:00:00'),
(73, 1, 'entrada', 60, 2, 'C-2025-036', 'Juguetes navidad', '2025-11-20 09:00:00'),
(74, 1, 'entrada', 50, 2, 'C-2025-036', 'Muñecas navidad', '2025-11-20 09:30:00'),

-- Salidas temporada alta
(73, 1, 'salida', 30, 4, 'V-2025-079', 'Venta colegios clausura', '2025-11-24 15:00:00'),
(67, 3, 'salida', 35, 4, 'V-2025-058', 'Venta gimnasios BF', '2025-11-02 11:00:00'),

-- Diciembre
(6, 1, 'entrada', 15, 2, 'C-2025-038', 'Reposicion tablets', '2025-12-01 08:00:00'),
(67, 3, 'salida', 40, 4, 'V-2025-086', 'Venta gimnasios navidad', '2025-12-01 14:00:00');

-- ================================================================
-- 8. ACTUALIZAR ESTADÍSTICAS DE PRODUCTOS (stock_actual)
-- ================================================================

-- Actualizar stock basado en movimientos recientes
UPDATE productos SET stock_actual = stock_actual + 25 WHERE id IN (1, 6);
UPDATE productos SET stock_actual = stock_actual + 50 WHERE id IN (67, 72);
UPDATE productos SET stock_actual = stock_actual + 80 WHERE id IN (73, 74, 75);
UPDATE productos SET stock_actual = stock_actual + 100 WHERE id IN (16, 17);
UPDATE productos SET stock_actual = stock_actual + 60 WHERE id IN (55, 56);

-- Algunos productos con stock bajo para alertas
UPDATE productos SET stock_actual = 3 WHERE id = 9;  -- Impresora
UPDATE productos SET stock_actual = 5 WHERE id = 47; -- Edredon
UPDATE productos SET stock_actual = 4 WHERE id = 49; -- Alfombra
UPDATE productos SET stock_actual = 2 WHERE id = 76; -- Auto RC

-- ================================================================
-- 9. RESUMEN DE DATOS INSERTADOS
-- ================================================================
-- Nuevos proveedores: 5 (total 10)
-- Nuevos clientes: 15 (total 40)
-- Nuevas ventas: 55 (total 90)
-- Nuevas compras: 19 (total 39)
-- Nuevos movimientos: 20+ adicionales
-- 
-- Esto proporciona:
-- - Datos de 4 meses (Sept, Oct, Nov, Dic 2025)
-- - Estacionalidad (temporada alta en Nov-Dic)
-- - Diferentes tipos de clientes (corporativos vs particulares)
-- - Variedad de métodos de pago
-- - Stock crítico en algunos productos
-- - Movimientos de inventario variados
-- ================================================================

SELECT '✅ Datos adicionales insertados correctamente!' AS mensaje;
SELECT CONCAT('Total Ventas: ', COUNT(*)) AS estadistica FROM ventas;
SELECT CONCAT('Total Compras: ', COUNT(*)) AS estadistica FROM compras;
SELECT CONCAT('Total Clientes: ', COUNT(*)) AS estadistica FROM clientes;
SELECT CONCAT('Total Productos: ', COUNT(*)) AS estadistica FROM productos;
