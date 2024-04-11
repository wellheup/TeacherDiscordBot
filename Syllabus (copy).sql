-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: db-buf-05.sparkedhost.us:3306
-- Generation Time: Apr 06, 2024 at 01:21 AM
-- Server version: 11.1.3-MariaDB-1:11.1.3+maria~ubu2204
-- PHP Version: 8.1.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `s128490_Syllabus`
--

-- --------------------------------------------------------

--
-- Table structure for table `Syllabus`
--

CREATE TABLE `Syllabus` (
  `ID` int(2) UNSIGNED NOT NULL,
  `Book` varchar(100) DEFAULT NULL,
  `Author` varchar(19) DEFAULT NULL,
  `Series` varchar(33) DEFAULT NULL,
  `IsCompleted` tinyint(1) DEFAULT NULL,
  `AddedBy` varchar(15) DEFAULT NULL,
  `Season` int(13) DEFAULT NULL,
  `NumInSeries` int(13) DEFAULT NULL,
  `IsExtraCredit` tinyint(1) DEFAULT NULL,
  `DateCompleted` date DEFAULT NULL,
  `Votes` int(13) DEFAULT NULL,
  `DateAdded` date DEFAULT NULL,
  `Genre` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `Syllabus`
--

INSERT INTO `Syllabus` (`ID`, `Book`, `Author`, `Series`, `IsCompleted`, `AddedBy`, `Season`, `NumInSeries`, `IsExtraCredit`, `DateCompleted`, `Votes`, `DateAdded`, `Genre`) VALUES
(1, 'The Rage of Dragons', 'Evan Winter', 'The Burning', 1, '', NULL, 1, 0, NULL, NULL, '2022-12-12', NULL),
(2, 'The Fires of Vengeance', 'Evan Winter', 'The Burning', 1, '', NULL, 2, 0, NULL, NULL, '2022-12-12', NULL),
(3, 'The Lord of Demons', 'Evan Winter', 'The Burning', 0, '', NULL, 3, 0, NULL, NULL, '0000-00-00', NULL),
(4, 'Gideon the Ninth', 'Tamysyn Muir', 'The Locked Tomb', 1, '', NULL, 1, 0, NULL, NULL, '0000-00-00', NULL),
(5, 'Harrow the Ninth', 'Tamysyn Muir', 'The Locked Tomb', 1, '', NULL, 2, 0, NULL, NULL, '0000-00-00', NULL),
(6, 'Nona the Ninth', 'Tamysyn Muir', 'The Locked Tomb', 1, '', NULL, 3, 0, NULL, NULL, '0000-00-00', NULL),
(7, 'Alecto the Ninth', 'Tamysyn Muir', 'The Locked Tomb', 0, '', NULL, 4, 0, NULL, NULL, '0000-00-00', NULL),
(8, 'The Name of the Wind', 'Patrick Rothfuss', 'The Kingkiller Chronicle', 1, '', NULL, 1, 0, NULL, NULL, '0000-00-00', NULL),
(9, 'The Wise Man\'s Fear', 'Patrick Rothfuss', 'The Kingkiller Chronicle', 1, '', NULL, 2, 0, NULL, NULL, '0000-00-00', NULL),
(10, 'The Doors of Stone', 'Patrick Rothfuss', 'The Kingkiller Chronicle', 0, '', NULL, 3, 0, NULL, NULL, '0000-00-00', NULL),
(11, 'The Fifth Season', 'N. K. Jemisin', 'Broken Earth trilogy', 1, '', NULL, 1, 0, NULL, NULL, '0000-00-00', NULL),
(12, 'The Obelisk Gate', 'N. K. Jemisin', 'Broken Earth trilogy', 1, '', NULL, 2, 0, NULL, NULL, '0000-00-00', NULL),
(13, 'The Stone Sky', 'N. K. Jemisin', 'Broken Earth trilogy', 1, '', NULL, 3, 0, NULL, NULL, '0000-00-00', NULL),
(14, 'The Hundred Thousand Kingdoms', 'N. K. Jemisin', 'The Inheritance Trilogy', 0, 'mellymi', NULL, 1, 0, NULL, NULL, '2023-05-10', NULL),
(15, 'The Broken Kingdoms', 'N. K. Jemisin', 'The Inheritance Trilogy', 0, '', NULL, 2, 0, NULL, NULL, '0000-00-00', NULL),
(16, 'The Kingdom of Gods', 'N. K. Jemisin', 'The Inheritance Trilogy', 0, '', NULL, 3, 0, NULL, NULL, '0000-00-00', NULL),
(17, 'Parable of the Sower', 'Octavia Butler', 'Parable duology', 1, '', NULL, 1, 0, NULL, NULL, '0000-00-00', NULL),
(18, 'Parable of the Talents', 'Octavia Butler', 'Parable duology', 1, 'mudgoat', NULL, 2, 1, NULL, NULL, '2023-04-10', NULL),
(19, 'The Road', 'Cormac McCarthy', '', 1, '', NULL, 1, 1, NULL, NULL, '0000-00-00', NULL),
(20, 'The Priory of the Orange Tree', 'Samantha Shannon', 'The Priory of the Orange Tree', 1, 'mellymi', NULL, 1, 0, NULL, NULL, '2023-05-10', NULL),
(21, 'A Day of Fallen Night', 'Samantha Shannon', 'The Priory of the Orange Tree', 0, 'mellymi', NULL, 1, 1, NULL, NULL, '2023-05-10', NULL),
(22, 'Iron Widow', 'Xiran Jay Zhao', '', 0, 'mudgoat', NULL, 1, 0, NULL, NULL, '0000-00-00', NULL),
(23, 'A Psalm for the Wild-Built', 'Becky Chambers', 'Monk & Robot', 0, 'mudgoat', NULL, 1, 0, NULL, NULL, '0000-00-00', NULL),
(24, 'A Prayer for the Crown-Shy', 'Becky Chambers', 'Monk & Robot', 0, '', NULL, 2, 0, NULL, NULL, '0000-00-00', NULL),
(25, 'The Poppy War', 'R. F. Kuang', 'The Poppy War trilogy', 0, 'mudgoat', NULL, 1, 0, NULL, NULL, '2023-02-05', NULL),
(26, 'The Dragon Republic', 'R. F. Kuang', 'The Poppy War trilogy', 0, '', NULL, 2, 0, NULL, NULL, '0000-00-00', NULL),
(27, 'The Burning God', 'R. F. Kuang', 'The Poppy War trilogy', 0, '', NULL, 3, 0, NULL, NULL, '0000-00-00', NULL),
(28, 'Jade City', 'Fonda Lee', 'Green Bone Saga', 0, 'knamustarsunder', NULL, NULL, 0, NULL, NULL, '2023-03-06', NULL),
(29, 'Black Leopard Red Wolf', 'Marlon James', 'The Dark Star Trilogy', 0, 'shinibon', NULL, NULL, 0, NULL, NULL, '2023-04-20', NULL),
(30, 'The Adventures of Amina Al-Sirafi', 'Shannon Chakraborty', 'The Adventures of Amina al-Sirafi', 0, 'mudgoat', NULL, NULL, 0, NULL, NULL, '2023-04-24', NULL),
(31, 'One Dark Window', 'Rachel Gillig', 'The Shepherd King', 0, 'mudgoat', NULL, NULL, 0, NULL, NULL, '2023-04-24', NULL),
(32, 'Emily Wilde\'s Encyclopedia of Faeries', 'Heather Fawcett', 'Emily Wilde', 0, 'mudgoat', NULL, NULL, 0, NULL, NULL, '2023-04-24', NULL),
(33, 'A Song of Silver and Gold', 'Melissa Karibian', '', 0, 'shinibon', NULL, NULL, 0, NULL, NULL, '2023-06-05', NULL),
(34, 'In the Lives of Puppets', 'TJ Klune', '', 0, 'mellymi', NULL, NULL, 0, NULL, NULL, '2023-06-10', NULL),
(35, 'The Long Way to a Small,  Angry Planet', 'Becky Chambers', 'Wayfarers', 0, 'brigadier7527', NULL, 1, 0, NULL, NULL, '2023-06-30', NULL),
(36, 'Piranesi', 'Susanna Clarke', '', 0, 'mudgoat', NULL, NULL, 0, NULL, NULL, '2023-09-25', NULL),
(37, 'Fourth Wing', 'Rebecca Yarros', 'Empyrean', 0, 'mudgoat', NULL, NULL, 0, NULL, NULL, '2023-11-09', NULL),
(38, 'Ninefox Gambit', 'Yoon Ha Lee', 'Machineries of Empire', 0, 'mudgoat', NULL, NULL, 0, NULL, NULL, '2024-03-29', NULL),
(39, 'A Memory Called Empire', 'Arkady Martine', 'Teixcalaan ', 0, 'mudgoat', NULL, 1, 0, NULL, NULL, '2024-03-29', NULL),
(40, 'A Desolation Called Peace', 'Arkady Martine', 'Teixcalaan ', 0, 'mudgoat', NULL, 2, 0, NULL, NULL, '2024-03-29', NULL),
(41, 'A Deadly Education', 'Naomi Novik', '', 0, 'mudgoat', NULL, NULL, 0, NULL, NULL, '2024-03-30', NULL),
(42, 'A Broken Blade', 'Melissa Blair', 'The Halfling Sage', 0, 'mudgoat', NULL, 1, 0, NULL, NULL, '2024-03-30', NULL),
(43, 'A Shadow Crown', 'Melissa Blair', 'The Halfling Sage', 0, 'mudgoat', NULL, 2, 0, NULL, NULL, '2024-03-30', NULL),
(44, 'A Vicious Game', 'Melissa Blair', 'The Halfling Sage', 0, 'mudgoat', NULL, 3, 0, NULL, NULL, '2024-03-30', NULL),
(45, 'Neuromancer', 'William Gobson', '', 0, 'mudgoat', NULL, NULL, 0, NULL, NULL, '2024-03-30', NULL),
(46, 'Dark Matter', 'Blake Crouch', '', 0, 'mudgoat', NULL, NULL, 0, NULL, NULL, '2024-03-30', NULL),
(47, 'Klara and the Sun', 'Kazuo Ishiguro', '', 0, 'mudgoat', NULL, NULL, 0, NULL, NULL, '2024-03-30', NULL),
(48, 'Robot Dreams', 'Isaac Asimov', '', 0, 'mudgoat', NULL, NULL, 0, NULL, NULL, '2024-03-30', NULL),
(49, 'The Day of the Triffids', 'John Wyndham', '', 0, 'mudgoat', NULL, NULL, 0, NULL, NULL, '2024-03-30', NULL),
(50, 'The Last House on the Street', 'Catriona Ward', '', 0, 'shinibon', NULL, NULL, 0, NULL, NULL, '2024-04-01', NULL),
(51, 'Annihilation', 'Jeff VanderMeer', 'Southern Reach Trilogy', 0, 'mudgoat', NULL, 1, 0, NULL, NULL, '2024-04-04', NULL),
(52, 'Authority', 'Jeff VanderMeer', 'Southern Reach Trilogy', 0, 'mudgoat', NULL, 2, 0, NULL, NULL, '2024-04-04', NULL),
(53, 'Acceptance', 'Jeff VanderMeer', 'Southern Reach Trilogy', 0, 'mudgoat', NULL, 3, 0, NULL, NULL, '2024-04-04', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Syllabus`
--
ALTER TABLE `Syllabus`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `UniqueId` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
