-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Хост: localhost
-- Время создания: Мар 01 2026 г., 13:34
-- Версия сервера: 9.4.0
-- Версия PHP: 8.4.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `boots_store`
--

-- --------------------------------------------------------

--
-- Структура таблицы `orders`
--

CREATE TABLE `orders` (
  `id_order` int NOT NULL,
  `date_order` date DEFAULT NULL,
  `date_delivery` date DEFAULT NULL,
  `id_pick_up_point` int DEFAULT NULL,
  `id_client` int DEFAULT NULL,
  `code` int DEFAULT NULL,
  `id_status` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `orders`
--

INSERT INTO `orders` (`id_order`, `date_order`, `date_delivery`, `id_pick_up_point`, `id_client`, `code`, `id_status`) VALUES
(1, '2025-02-27', '2025-04-20', 1, 4, 901, 2),
(2, '2022-09-28', '2025-04-21', 11, 1, 902, 2),
(3, '2025-03-21', '2025-04-22', 2, 2, 903, 2),
(4, '2025-02-20', '2025-04-23', 11, 3, 904, 2),
(5, '2025-03-17', '2025-04-24', 2, 4, 905, 2),
(6, '2025-03-01', '2025-04-25', 15, 1, 906, 2),
(7, '2025-02-28', '2025-04-26', 3, 2, 907, 2),
(8, '2025-03-31', '2025-04-27', 19, 3, 908, 1),
(9, '2025-04-02', '2025-04-28', 5, 4, 909, 1),
(10, '2025-04-03', '2025-04-29', 19, 4, 910, 1);

-- --------------------------------------------------------

--
-- Структура таблицы `order_status`
--

CREATE TABLE `order_status` (
  `id_status` int NOT NULL,
  `name` varchar(8) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `order_status`
--

INSERT INTO `order_status` (`id_status`, `name`) VALUES
(1, 'Новый'),
(2, 'Завершен');

-- --------------------------------------------------------

--
-- Структура таблицы `pick_up_points`
--

CREATE TABLE `pick_up_points` (
  `id_point` int NOT NULL,
  `index_address` int DEFAULT NULL,
  `city` varchar(9) DEFAULT NULL,
  `street` varchar(20) DEFAULT NULL,
  `house` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `pick_up_points`
--

INSERT INTO `pick_up_points` (`id_point`, `index_address`, `city`, `street`, `house`) VALUES
(1, 420151, 'г. Лесной', 'ул. Вишневая', 32),
(2, 125061, 'г. Лесной', 'ул. Подгорная', 8),
(3, 630370, 'г. Лесной', 'ул. Шоссейная', 24),
(4, 400562, 'г. Лесной', 'ул. Зеленая', 32),
(5, 614510, 'г. Лесной', 'ул. Маяковского', 47),
(6, 410542, 'г. Лесной', 'ул. Светлая', 46),
(7, 620839, 'г. Лесной', 'ул. Цветочная', 8),
(8, 443890, 'г. Лесной', 'ул. Коммунистическая', 1),
(9, 603379, 'г. Лесной', 'ул. Спортивная', 46),
(10, 603721, 'г. Лесной', 'ул. Гоголя', 41),
(11, 410172, 'г. Лесной', 'ул. Северная', 13),
(12, 614611, 'г. Лесной', 'ул. Молодежная', 50),
(13, 454311, 'г.Лесной', 'ул. Новая', 19),
(14, 660007, 'г.Лесной', 'ул. Октябрьская', 19),
(15, 603036, 'г. Лесной', 'ул. Садовая', 4),
(16, 394060, 'г.Лесной', 'ул. Фрунзе', 43),
(17, 410661, 'г. Лесной', 'ул. Школьная', 50),
(18, 625590, 'г. Лесной', 'ул. Коммунистическая', 20),
(19, 625683, 'г. Лесной', 'ул. 8 Марта', NULL),
(20, 450983, 'г.Лесной', 'ул. Комсомольская', 26),
(21, 394782, 'г. Лесной', 'ул. Чехова', 3),
(22, 603002, 'г. Лесной', 'ул. Дзержинского', 28),
(23, 450558, 'г. Лесной', 'ул. Набережная', 30),
(24, 344288, 'г. Лесной', 'ул. Чехова', 1),
(25, 614164, 'г.Лесной', '  ул. Степная', 30),
(26, 394242, 'г. Лесной', 'ул. Коммунистическая', 43),
(27, 660540, 'г. Лесной', 'ул. Солнечная', 25),
(28, 125837, 'г. Лесной', 'ул. Шоссейная', 40),
(29, 125703, 'г. Лесной', 'ул. Партизанская', 49),
(30, 625283, 'г. Лесной', 'ул. Победы', 46),
(31, 614753, 'г. Лесной', 'ул. Полевая', 35),
(32, 426030, 'г. Лесной', 'ул. Маяковского', 44),
(33, 450375, 'г. Лесной', 'ул. Клубная', 44),
(34, 625560, 'г. Лесной', 'ул. Некрасова', 12),
(35, 630201, 'г. Лесной', 'ул. Комсомольская', 17),
(36, 190949, 'г. Лесной', 'ул. Мичурина', 26);

-- --------------------------------------------------------

--
-- Структура таблицы `producers`
--

CREATE TABLE `producers` (
  `id_producer` int NOT NULL,
  `name` varchar(13) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `producers`
--

INSERT INTO `producers` (`id_producer`, `name`) VALUES
(1, 'Kari'),
(2, 'Marco Tozzi'),
(3, 'Рос'),
(4, 'Rieker'),
(5, 'Alessio Nesca'),
(6, 'CROSBY');

-- --------------------------------------------------------

--
-- Структура таблицы `products`
--

CREATE TABLE `products` (
  `id_product` int NOT NULL,
  `article` varchar(6) DEFAULT NULL,
  `id_type` int DEFAULT NULL,
  `unit_of_measurement` varchar(3) DEFAULT NULL,
  `price` int DEFAULT NULL,
  `id_supplier` int DEFAULT NULL,
  `id_producer` int DEFAULT NULL,
  `id_category` int DEFAULT NULL,
  `current_discount` int DEFAULT NULL,
  `amount_in_warehouse` int DEFAULT NULL,
  `description` varchar(71) DEFAULT NULL,
  `photo` varchar(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `products`
--

INSERT INTO `products` (`id_product`, `article`, `id_type`, `unit_of_measurement`, `price`, `id_supplier`, `id_producer`, `id_category`, `current_discount`, `amount_in_warehouse`, `description`, `photo`) VALUES
(1, 'А112Т4', 1, 'шт.', 4990, 1, 1, 1, 3, 6, 'Женские Ботинки демисезонные kari', '1.jpg'),
(2, 'F635R4', 1, 'шт.', 3244, 2, 2, 1, 2, 13, 'Ботинки Marco Tozzi женские демисезонные, размер 39, цвет бежевый', '2.jpg'),
(3, 'H782T5', 2, 'шт.', 4499, 1, 1, 2, 4, 5, 'Туфли kari мужские классика MYZ21AW-450A, размер 43, цвет: черный', '3.jpg'),
(4, 'G783F5', 1, 'шт.', 5900, 1, 3, 2, 2, 8, 'Мужские ботинки Рос-Обувь кожаные с натуральным мехом', '4.jpg'),
(5, 'J384T6', 1, 'шт.', 3800, 2, 4, 2, 2, 16, 'B3430/14 Полуботинки мужские Rieker', '5.jpg'),
(6, 'D572U8', 3, 'шт.', 4100, 2, 3, 2, 3, 6, '129615-4 Кроссовки мужские', '6.jpg'),
(7, 'F572H7', 2, 'шт.', 2700, 1, 2, 1, 2, 14, 'Туфли Marco Tozzi женские летние, размер 39, цвет черный', '7.jpg'),
(8, 'D329H3', 4, 'шт.', 1890, 2, 5, 1, 4, 4, 'Полуботинки Alessio Nesca женские 3-30797-47, размер 37, цвет: бордовый', '8.jpg'),
(9, 'B320R5', 2, 'шт.', 4300, 1, 4, 1, 2, 6, 'Туфли Rieker женские демисезонные, размер 41, цвет коричневый', '9.jpg'),
(10, 'G432E4', 2, 'шт.', 2800, 1, 1, 1, 3, 15, 'Туфли kari женские TR-YR-413017, размер 37, цвет: черный', '10.jpg'),
(11, 'S213E3', 4, 'шт.', 2156, 2, 6, 2, 3, 6, '407700/01-01 Полуботинки мужские CROSBY', NULL),
(12, 'E482R4', 4, 'шт.', 1800, 1, 1, 1, 2, 14, 'Полуботинки kari женские MYZ20S-149, размер 41, цвет: черный', NULL),
(13, 'S634B5', 5, 'шт.', 5500, 2, 6, 2, 3, 0, 'Кеды Caprice мужские демисезонные, размер 42, цвет черный', NULL),
(14, 'K345R4', 4, 'шт.', 2100, 2, 6, 2, 2, 3, '407700/01-02 Полуботинки мужские CROSBY', NULL),
(15, 'O754F4', 2, 'шт.', 5400, 2, 4, 1, 4, 18, 'Туфли женские демисезонные Rieker артикул 55073-68/37', NULL),
(16, 'G531F4', 1, 'шт.', 6600, 1, 1, 1, 12, 9, 'Ботинки женские зимние ROMER арт. 893167-01 Черный', NULL),
(17, 'J542F5', 6, 'шт.', 500, 1, 1, 2, 13, 0, 'Тапочки мужские Арт.70701-55-67син р.41', NULL),
(18, 'B431R5', 1, 'шт.', 2700, 2, 4, 2, 2, 5, 'Мужские кожаные ботинки/мужские ботинки', NULL),
(19, 'P764G4', 2, 'шт.', 6800, 1, 6, 1, 15, 15, 'Туфли женские, ARGO, размер 38', NULL),
(20, 'C436G5', 1, 'шт.', 10200, 1, 5, 1, 15, 9, 'Ботинки женские, ARGO, размер 40', NULL),
(21, 'F427R5', 1, 'шт.', 11800, 2, 4, 1, 15, 11, 'Ботинки на молнии с декоративной пряжкой FRAU', NULL),
(22, 'N457T5', 4, 'шт.', 4600, 1, 6, 1, 3, 13, 'Полуботинки Ботинки черные зимние, мех', NULL),
(23, 'D364R4', 2, 'шт.', 12400, 1, 1, 1, 16, 5, 'Туфли Luiza Belly женские Kate-lazo черные из натуральной замши', NULL),
(24, 'S326R5', 6, 'шт.', 9900, 2, 6, 2, 17, 15, 'Мужские кожаные тапочки \"Профиль С.Дали\" ', NULL),
(25, 'L754R4', 4, 'шт.', 1700, 1, 1, 1, 2, 7, 'Полуботинки kari женские WB2020SS-26, размер 38, цвет: черный', NULL),
(26, 'M542T5', 3, 'шт.', 2800, 2, 4, 2, 18, 3, 'Кроссовки мужские TOFA', NULL),
(27, 'D268G5', 2, 'шт.', 4399, 2, 4, 1, 3, 12, 'Туфли Rieker женские демисезонные, размер 36, цвет коричневый', NULL),
(28, 'T324F5', 7, 'шт.', 4699, 1, 6, 1, 2, 5, 'Сапоги замша Цвет: синий', NULL),
(29, 'K358H6', 6, 'шт.', 599, 1, 4, 2, 20, 2, 'Тапочки мужские син р.41', NULL),
(30, 'H535R5', 1, 'шт.', 2300, 2, 4, 1, 2, 7, 'Женские Ботинки демисезонные', NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `products_in_orders`
--

CREATE TABLE `products_in_orders` (
  `id_product_in_order` int NOT NULL,
  `id_order` int DEFAULT NULL,
  `id_product` int DEFAULT NULL,
  `amount_product` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `products_in_orders`
--

INSERT INTO `products_in_orders` (`id_product_in_order`, `id_order`, `id_product`, `amount_product`) VALUES
(1, 1, 1, 2),
(2, 1, 2, 2),
(3, 2, 3, 1),
(4, 2, 4, 1),
(5, 3, 5, 10),
(6, 3, 6, 10),
(7, 4, 7, 5),
(8, 4, 8, 4),
(9, 5, 1, 2),
(10, 5, 2, 2),
(11, 6, 3, 1),
(12, 6, 4, 1),
(13, 7, 5, 10),
(14, 7, 6, 10),
(15, 8, 7, 5),
(16, 8, 8, 4),
(17, 9, 9, 5),
(18, 9, 10, 1),
(19, 10, 11, 5),
(20, 10, 12, 5);

-- --------------------------------------------------------

--
-- Структура таблицы `product_category`
--

CREATE TABLE `product_category` (
  `id_category` int NOT NULL,
  `name` varchar(13) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `product_category`
--

INSERT INTO `product_category` (`id_category`, `name`) VALUES
(1, 'Женская обувь'),
(2, 'Мужская обувь');

-- --------------------------------------------------------

--
-- Структура таблицы `product_type`
--

CREATE TABLE `product_type` (
  `id_type` int NOT NULL,
  `name` varchar(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `product_type`
--

INSERT INTO `product_type` (`id_type`, `name`) VALUES
(1, 'Ботинки'),
(2, 'Туфли'),
(3, 'Кроссовки'),
(4, 'Полуботинки'),
(5, 'Кеды'),
(6, 'Тапочки'),
(7, 'Сапоги');

-- --------------------------------------------------------

--
-- Структура таблицы `suppliers`
--

CREATE TABLE `suppliers` (
  `id_supplier` int NOT NULL,
  `name` varchar(13) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `suppliers`
--

INSERT INTO `suppliers` (`id_supplier`, `name`) VALUES
(1, 'Kari'),
(2, 'Обувь для вас');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id_user` int NOT NULL,
  `last_name` varchar(10) DEFAULT NULL,
  `first_name` varchar(7) DEFAULT NULL,
  `patronymic` varchar(12) DEFAULT NULL,
  `login` varchar(21) DEFAULT NULL,
  `password` varchar(6) DEFAULT NULL,
  `id_role` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id_user`, `last_name`, `first_name`, `patronymic`, `login`, `password`, `id_role`) VALUES
(1, 'Никифорова', 'Весения', 'Николаевна', '94d5ous@gmail.com', 'uzWC67', 1),
(2, 'Сазонов', 'Руслан', 'Германович', 'uth4iz@mail.com', '2L6KZG', 1),
(3, 'Одинцов', 'Серафим', 'Артёмович', 'yzls62@outlook.com', 'JlFRCZ', 1),
(4, 'Степанов', 'Михаил', 'Артёмович', '1diph5e@tutanota.com', '8ntwUp', 2),
(5, 'Ворсин', 'Петр', 'Евгеньевич', 'tjde7c@yahoo.com', 'YOyhfR', 2),
(6, 'Старикова', 'Елена', 'Павловна', 'wpmrc3do@tutanota.com', 'RSbvHv', 2),
(7, 'Михайлюк', 'Анна', 'Вячеславовна', '5d4zbu@tutanota.com', 'rwVDh9', 3),
(8, 'Ситдикова', 'Елена', 'Анатольевна', 'ptec8ym@yahoo.com', 'LdNyos', 3),
(9, 'Ворсин', 'Петр', 'Евгеньевич', '1qz4kw@mail.com', 'gynQMT', 3),
(10, 'Старикова', 'Елена', 'Павловна', '4np6se@mail.com', 'AtnDjr', 3);

-- --------------------------------------------------------

--
-- Структура таблицы `users_roles`
--

CREATE TABLE `users_roles` (
  `id_role` int NOT NULL,
  `name` varchar(23) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `users_roles`
--

INSERT INTO `users_roles` (`id_role`, `name`) VALUES
(1, 'Администратор'),
(2, 'Менеджер'),
(3, 'Авторизированный клиент');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id_order`),
  ADD KEY `id_pick_up_point` (`id_pick_up_point`,`id_client`,`id_status`),
  ADD KEY `id_status` (`id_status`),
  ADD KEY `id_client` (`id_client`);

--
-- Индексы таблицы `order_status`
--
ALTER TABLE `order_status`
  ADD PRIMARY KEY (`id_status`);

--
-- Индексы таблицы `pick_up_points`
--
ALTER TABLE `pick_up_points`
  ADD PRIMARY KEY (`id_point`);

--
-- Индексы таблицы `producers`
--
ALTER TABLE `producers`
  ADD PRIMARY KEY (`id_producer`);

--
-- Индексы таблицы `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id_product`),
  ADD KEY `id_type` (`id_type`,`id_supplier`,`id_producer`,`id_category`),
  ADD KEY `id_supplier` (`id_supplier`),
  ADD KEY `id_producer` (`id_producer`),
  ADD KEY `id_category` (`id_category`);

--
-- Индексы таблицы `products_in_orders`
--
ALTER TABLE `products_in_orders`
  ADD PRIMARY KEY (`id_product_in_order`),
  ADD KEY `id_order` (`id_order`,`id_product`),
  ADD KEY `id_product` (`id_product`);

--
-- Индексы таблицы `product_category`
--
ALTER TABLE `product_category`
  ADD PRIMARY KEY (`id_category`);

--
-- Индексы таблицы `product_type`
--
ALTER TABLE `product_type`
  ADD PRIMARY KEY (`id_type`);

--
-- Индексы таблицы `suppliers`
--
ALTER TABLE `suppliers`
  ADD PRIMARY KEY (`id_supplier`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id_user`),
  ADD KEY `id_role` (`id_role`);

--
-- Индексы таблицы `users_roles`
--
ALTER TABLE `users_roles`
  ADD PRIMARY KEY (`id_role`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `orders`
--
ALTER TABLE `orders`
  MODIFY `id_order` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `order_status`
--
ALTER TABLE `order_status`
  MODIFY `id_status` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `pick_up_points`
--
ALTER TABLE `pick_up_points`
  MODIFY `id_point` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT для таблицы `producers`
--
ALTER TABLE `producers`
  MODIFY `id_producer` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT для таблицы `products`
--
ALTER TABLE `products`
  MODIFY `id_product` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT для таблицы `products_in_orders`
--
ALTER TABLE `products_in_orders`
  MODIFY `id_product_in_order` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT для таблицы `product_category`
--
ALTER TABLE `product_category`
  MODIFY `id_category` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `product_type`
--
ALTER TABLE `product_type`
  MODIFY `id_type` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT для таблицы `suppliers`
--
ALTER TABLE `suppliers`
  MODIFY `id_supplier` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id_user` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `users_roles`
--
ALTER TABLE `users_roles`
  MODIFY `id_role` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`id_pick_up_point`) REFERENCES `pick_up_points` (`id_point`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`id_status`) REFERENCES `order_status` (`id_status`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`id_client`) REFERENCES `users` (`id_user`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`id_type`) REFERENCES `product_type` (`id_type`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `products_ibfk_2` FOREIGN KEY (`id_supplier`) REFERENCES `suppliers` (`id_supplier`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `products_ibfk_3` FOREIGN KEY (`id_producer`) REFERENCES `producers` (`id_producer`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `products_ibfk_4` FOREIGN KEY (`id_category`) REFERENCES `product_category` (`id_category`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `products_in_orders`
--
ALTER TABLE `products_in_orders`
  ADD CONSTRAINT `products_in_orders_ibfk_1` FOREIGN KEY (`id_order`) REFERENCES `orders` (`id_order`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `products_in_orders_ibfk_2` FOREIGN KEY (`id_product`) REFERENCES `products` (`id_product`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`id_role`) REFERENCES `users_roles` (`id_role`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
