-- MySQL dump 10.13  Distrib 8.4.5, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: quikeryc_espot_scraping_tires_moto_mx
-- ------------------------------------------------------
-- Server version	8.4.5

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `links`
--

DROP TABLE IF EXISTS `links`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `links` (
  `id` int NOT NULL AUTO_INCREMENT,
  `link` varchar(2500) NOT NULL,
  `revisado` int NOT NULL,
  `marca` varchar(50) NOT NULL,
  `link_generador` varchar(1024) NOT NULL,
  `instance_id` varchar(64) DEFAULT NULL,
  `processed` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=402 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `registers`
--

DROP TABLE IF EXISTS `registers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registers` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `location_id` bigint unsigned NOT NULL,
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
  `number_tires` int DEFAULT '1',
  `rate_exchange` double(8,2) NOT NULL,
  `rate_tax` double(8,2) NOT NULL,
  `load_index` int DEFAULT NULL,
  `speed_rating` varchar(1) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `utqg` varchar(25) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ply_rating` varchar(3) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `location_origin` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `location_manufactured` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `perf` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `constr` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `offer` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `stock` int DEFAULT NULL,
  `comment` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `scrap_link` varchar(1024) COLLATE utf8mb4_unicode_ci NOT NULL,
  `scrap_index` int DEFAULT NULL,
  `status` tinyint NOT NULL DEFAULT '0',
  `ss` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `store` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=132 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping events for database 'quikeryc_espot_scraping_tires_moto_mx'
--

--
-- Dumping routines for database 'quikeryc_espot_scraping_tires_moto_mx'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-16 18:57:45
