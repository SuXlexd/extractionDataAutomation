
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Estructura de tabla para la tabla `registers`
--

CREATE TABLE `registers` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `location_id` bigint(20) UNSIGNED NOT NULL,
  `sku` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `brand` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `size` varchar(25) COLLATE utf8mb4_unicode_ci NOT NULL,
  `size_width` float DEFAULT NULL,
  `size_ratio` float DEFAULT NULL,
  `size_rim` float DEFAULT NULL,
  `price_og_fr` double(8,2) NOT NULL,
  `price_og_tx` double(8,2) NOT NULL,
  `price_mn_fr` double(8,2) NOT NULL,
  `price_mn_tx` double(8,2) NOT NULL,
  `price_us_fr` double(8,2) NOT NULL,
  `price_us_tx` double(8,2) NOT NULL,
  `number_tires` int(11) DEFAULT '1',
  `rate_exchange` double(8,2) NOT NULL,
  `rate_tax` double(8,2) NOT NULL,
  `load_index` int(11) DEFAULT NULL,
  `speed_rating` varchar(1) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `utqg` varchar(25) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ply_rating` varchar(3) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `location_origin` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `location_manufactured` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `perf` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `constr` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `offer` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `stock` int(11) DEFAULT NULL,
  `comment` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `scrap_link` varchar(1024) COLLATE utf8mb4_unicode_ci NOT NULL,
  `scrap_index` int(11) DEFAULT NULL,
  `status` tinyint(4) NOT NULL DEFAULT '0',
  `ss` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `store` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


--
-- Indices de la tabla `registers`
--
ALTER TABLE `registers`
  ADD PRIMARY KEY (`id`);


--
-- AUTO_INCREMENT de la tabla `registers`
--
ALTER TABLE `registers`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
