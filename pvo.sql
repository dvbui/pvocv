-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 08, 2021 at 05:08 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pvo`
--

-- --------------------------------------------------------

--
-- Table structure for table `edge`
--

CREATE TABLE `edge` (
  `id` int(11) NOT NULL,
  `node1` int(11) NOT NULL COMMENT 'parent node',
  `node2` int(11) NOT NULL COMMENT 'child node',
  `type` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `node`
--

CREATE TABLE `node` (
  `id` int(11) NOT NULL,
  `user` int(11) NOT NULL,
  `content` text COLLATE utf8_unicode_ci NOT NULL,
  `content_text` text COLLATE utf8_unicode_ci NOT NULL,
  `type` tinyint(1) NOT NULL COMMENT '0 - concept\r\n1 - example',
  `keyword` text COLLATE utf8_unicode_ci NOT NULL,
  `usage_note` text COLLATE utf8_unicode_ci NOT NULL,
  `usage_note_text` text COLLATE utf8_unicode_ci NOT NULL,
  `vn` text COLLATE utf8_unicode_ci NOT NULL,
  `source` text COLLATE utf8_unicode_ci NOT NULL,
  `media` text COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `rel_type`
--

CREATE TABLE `rel_type` (
  `id` int(11) NOT NULL,
  `rel` text COLLATE utf8_unicode_ci NOT NULL,
  `user` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `rel_type`
--

INSERT INTO `rel_type` (`id`, `rel`, `user`) VALUES
(1, 'Association', NULL),
(2, 'Type of', NULL),
(3, 'Same concept', NULL),
(4, 'Related concepts', NULL),
(5, 'Doer of action', NULL),
(6, 'Receiver of action', NULL),
(7, 'Action', NULL),
(8, 'Described by', NULL),
(9, 'Describing', NULL),
(10, 'Idiom', NULL),
(11, 'Related phrases', NULL),
(12, 'Temporary uncategorized', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `name` text COLLATE utf8_unicode_ci NOT NULL,
  `password` text COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `edge`
--
ALTER TABLE `edge`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `node1_2` (`node1`,`node2`),
  ADD KEY `node2` (`node2`),
  ADD KEY `type` (`type`),
  ADD KEY `node1` (`node1`);

--
-- Indexes for table `node`
--
ALTER TABLE `node`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user` (`user`);

--
-- Indexes for table `rel_type`
--
ALTER TABLE `rel_type`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`) USING HASH;

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `edge`
--
ALTER TABLE `edge`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=69;

--
-- AUTO_INCREMENT for table `node`
--
ALTER TABLE `node`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=54;

--
-- AUTO_INCREMENT for table `rel_type`
--
ALTER TABLE `rel_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `edge`
--
ALTER TABLE `edge`
  ADD CONSTRAINT `edge_ibfk_1` FOREIGN KEY (`node1`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `edge_ibfk_2` FOREIGN KEY (`node2`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `edge_ibfk_3` FOREIGN KEY (`type`) REFERENCES `rel_type` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `node`
--
ALTER TABLE `node`
  ADD CONSTRAINT `node_ibfk_1` FOREIGN KEY (`user`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
