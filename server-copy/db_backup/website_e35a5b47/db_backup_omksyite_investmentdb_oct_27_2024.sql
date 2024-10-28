-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Oct 27, 2024 at 10:53 PM
-- Server version: 8.0.39-30
-- PHP Version: 8.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `omksyite_investmentdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `Tickers`
--

CREATE TABLE `Tickers` (
  `TickerID` bigint NOT NULL,
  `UserName` varchar(255) DEFAULT NULL,
  `TickerName` varchar(255) NOT NULL,
  `EntryPrice` decimal(10,2) NOT NULL DEFAULT '0.00',
  `StopPercent` decimal(10,2) NOT NULL DEFAULT '0.00',
  `StopPrice` decimal(10,2) NOT NULL DEFAULT '0.00',
  `Target1` decimal(10,2) NOT NULL DEFAULT '0.00',
  `Target2` decimal(10,2) NOT NULL DEFAULT '0.00',
  `Target3` decimal(10,2) NOT NULL DEFAULT '0.00',
  `Target4` decimal(10,2) NOT NULL DEFAULT '0.00',
  `CreateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `TickerStatus` varchar(255) DEFAULT NULL,
  `TickerNotes` text,
  `TrailStop` decimal(10,2) NOT NULL DEFAULT '0.00',
  `UpdateDate` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Tickers`
--

INSERT INTO `Tickers` (`TickerID`, `UserName`, `TickerName`, `EntryPrice`, `StopPercent`, `StopPrice`, `Target1`, `Target2`, `Target3`, `Target4`, `CreateDate`, `TickerStatus`, `TickerNotes`, `TrailStop`, `UpdateDate`) VALUES
(92, 'Admin', 'AMSC', 23.00, 7.75, 21.22, 26.57, 30.13, 0.00, 0.00, '2024-10-25 12:06:17', 'Active', '', 0.00, '2024-10-25 13:32:16'),
(32, 'Admin', 'ARIS', 17.25, 4.10, 16.54, 18.29, 19.32, 0.00, 0.00, '2024-10-11 16:12:43', 'Inactive', '', 0.00, '2024-10-11 21:12:43'),
(70, 'Admin', 'ARQT', 9.80, 6.35, 9.18, 11.04, 12.29, 0.00, 0.00, '2024-10-18 12:52:49', 'Inactive', '', 0.00, '2024-10-18 17:52:49'),
(67, 'Admin', 'ATI', 63.45, 3.00, 61.55, 67.26, 71.06, 0.00, 0.00, '2024-10-17 12:22:32', 'Active', '', 0.00, '2024-10-17 17:22:32'),
(74, 'Admin', 'ATI', 63.67, 3.00, 61.76, 67.49, 71.31, 0.00, 0.00, '2024-10-21 12:22:35', 'Active', '', 0.00, '2024-10-22 04:00:11'),
(66, 'Admin', 'AVGO', 179.25, 4.10, 171.90, 193.95, 208.65, 0.00, 0.00, '2024-10-17 12:21:49', 'Inactive', '', 0.00, '2024-10-17 17:21:49'),
(21, 'Admin', 'BANR', 58.70, 3.06, 56.90, 62.29, 65.88, 0.00, 0.00, '2024-10-09 03:55:50', 'Inactive', 'Entered 10/03\n10/16 - Target 2 Achieved', 0.00, '2024-10-21 18:57:10'),
(26, 'Admin', 'BEKE', 22.00, 6.00, 20.00, 23.00, 25.00, 0.00, 0.00, '2024-10-11 03:32:28', 'Inactive', '', 0.00, '2024-10-11 08:32:28'),
(87, 'Admin', 'BHE', 42.96, 3.05, 41.65, 45.58, 48.20, 0.00, 0.00, '2024-10-23 12:52:34', 'Active', '', 0.00, '2024-10-23 13:33:57'),
(91, 'Admin', 'BHE', 42.96, 3.05, 41.65, 45.58, 48.20, 0.00, 0.00, '2024-10-23 13:49:56', 'Inactive', '', 0.00, '2024-10-23 13:49:56'),
(49, 'Admin', 'BLDR', 196.16, 3.70, 188.90, 210.68, 225.19, 0.00, 0.00, '2024-10-14 12:08:38', 'Inactive', '', 0.00, '2024-10-21 14:45:35'),
(75, 'Admin', 'BLDR', 196.47, 3.35, 189.89, 209.63, 222.80, 0.00, 0.00, '2024-10-21 12:23:30', 'Inactive', '', 0.00, '2024-10-21 12:23:30'),
(76, 'Admin', 'BLND', 370.00, 6.70, 2.80, 3.40, 3.80, 0.00, 0.00, '2024-10-21 12:24:18', 'Inactive', '', 0.00, '2024-10-21 12:24:18'),
(19, 'Admin', 'CCS', 98.00, 3.30, 94.77, 104.47, 110.94, 0.00, 0.00, '2024-10-09 03:52:10', 'Active', 'Entered 10/08', 0.00, '2024-10-09 08:52:10'),
(63, 'Admin', 'CHWY', 29.02, 5.00, 27.57, 31.92, 34.82, 0.00, 0.00, '2024-10-16 12:37:38', 'Active', '', 0.00, '2024-10-16 17:37:38'),
(42, 'Admin', 'COLL', 37.52, 4.10, 35.98, 39.77, 42.02, 0.00, 0.00, '2024-10-11 20:44:10', 'Inactive', '', 0.00, '2024-10-12 01:44:10'),
(93, 'Admin', 'DAve', 41.25, 7.00, 38.36, 47.02, 52.80, 0.00, 0.00, '2024-10-25 12:08:05', 'Inactive', '', 0.00, '2024-10-25 12:08:05'),
(65, 'Admin', 'DRS', 28.69, 3.20, 27.77, 30.53, 32.36, 0.00, 0.00, '2024-10-16 12:41:29', 'Active', '', 0.00, '2024-10-16 17:41:29'),
(79, 'Admin', 'DRS', 28.69, 3.20, 27.77, 30.53, 32.36, 0.00, 0.00, '2024-10-22 03:58:38', 'Inactive', '', 0.00, '2024-10-22 03:58:38'),
(59, 'Admin', 'GCI', 5.47, 5.55, 5.17, 6.08, 6.68, 0.00, 0.00, '2024-10-15 13:06:39', 'Active', 'Targets updated', 0.00, '2024-10-15 18:06:39'),
(77, 'Admin', 'GCI', 5.59, 5.30, 5.29, 6.18, 6.78, 0.00, 0.00, '2024-10-21 12:25:11', 'Inactive', '', 0.00, '2024-10-21 12:25:11'),
(95, 'Admin', 'HAIN', 8.55, 4.50, 8.16, 9.31, 10.08, 0.00, 0.00, '2024-10-25 12:10:21', 'Inactive', '', 0.00, '2024-10-25 12:10:21'),
(80, 'Admin', 'KYMR', 46.56, 5.10, 44.19, 51.31, 56.06, 0.00, 0.00, '2024-10-22 13:11:36', 'Active', '', 0.00, '2024-10-22 13:47:46'),
(46, 'Admin', 'LBPH', 35.35, 8.50, 32.35, 41.36, 47.37, 0.00, 0.00, '2024-10-11 20:49:45', 'Active', '10/11 - Target 1 Achieved. Trailstop updated to 35.35.\n10/14 - 51% Profit, Exited 80% positions at $58.90', 35.35, '2024-10-12 01:49:45'),
(51, 'Admin', 'LMAT', 90.90, 2.90, 88.26, 96.35, 101.81, 0.00, 0.00, '2024-10-14 12:10:26', 'Inactive', '', 0.00, '2024-10-14 17:10:26'),
(28, 'Admin', 'LTH', 25.00, 4.00, 24.00, 26.00, 28.00, 0.00, 0.00, '2024-10-11 03:33:21', 'Inactive', '', 0.00, '2024-10-11 08:33:21'),
(94, 'Admin', 'LUMN', 6.36, 8.70, 5.81, 7.47, 8.57, 0.00, 0.00, '2024-10-25 12:09:01', 'Active', '', 0.00, '2024-10-25 14:07:34'),
(44, 'Admin', 'MBC', 17.38, 3.50, 16.77, 18.42, 19.47, 0.00, 0.00, '2024-10-11 20:47:02', 'Inactive', '', 0.00, '2024-10-12 01:47:02'),
(27, 'Admin', 'MLI', 72.00, 3.00, 69.00, 76.00, 80.00, 0.00, 0.00, '2024-10-11 03:32:52', 'Inactive', '', 0.00, '2024-10-11 08:32:52'),
(68, 'Admin', 'MPWR', 916.00, 4.10, 878.44, 991.11, 1066.22, 0.00, 0.00, '2024-10-17 12:23:15', 'Inactive', '', 0.00, '2024-10-17 17:23:15'),
(29, 'Admin', 'MRVL', 73.00, 4.00, 70.00, 77.00, 82.00, 0.00, 0.00, '2024-10-11 03:33:47', 'Inactive', '', 0.00, '2024-10-11 08:33:47'),
(69, 'Admin', 'MTSI', 115.80, 3.60, 111.63, 124.14, 132.48, 0.00, 0.00, '2024-10-17 12:24:09', 'Active', '', 0.00, '2024-10-17 17:24:09'),
(78, 'Admin', 'MTSI', 114.51, 3.52, 110.48, 122.57, 130.63, 0.00, 0.00, '2024-10-21 12:26:11', 'Inactive', '', 0.00, '2024-10-21 12:26:11'),
(82, 'Admin', 'MTSi', 114.20, 3.50, 110.20, 122.19, 130.19, 0.00, 0.00, '2024-10-22 13:13:02', 'Active', '', 0.00, '2024-10-22 17:47:24'),
(25, 'Admin', 'NMM', 62.00, 4.00, 60.00, 66.00, 70.00, 0.00, 0.00, '2024-10-11 03:31:53', 'Inactive', '', 0.00, '2024-10-11 08:31:53'),
(89, 'Admin', 'NMM', 59.51, 3.22, 57.59, 63.34, 67.17, 0.00, 0.00, '2024-10-23 12:58:57', 'Inactive', '', 0.00, '2024-10-23 12:58:57'),
(54, 'Admin', 'NRG', 90.70, 1.20, 89.61, 96.14, 101.58, 0.00, 0.00, '2024-10-14 13:37:28', 'Inactive', '10/14 - Keeping Aggressive SL\nSL hit @ 89.61', 0.00, '2024-10-14 18:37:28'),
(53, 'Admin', 'ONON', 50.30, 3.85, 48.36, 53.32, 56.34, 0.00, 0.00, '2024-10-14 12:12:46', 'Inactive', '', 0.00, '2024-10-14 17:12:46'),
(18, 'Admin', 'OSIS', 146.46, 2.60, 142.65, 154.08, 161.69, 0.00, 0.00, '2024-10-08 17:22:07', 'Active', '', 0.00, '2024-10-08 17:22:07'),
(24, 'Admin', 'PAAS', 22.39, 3.90, 21.52, 24.14, 25.88, 0.00, 0.00, '2024-10-10 17:28:25', 'Active', 'Re-Entry Pass 10/18\nTarget 1 achieved for Entry given on 10/10 ', 0.00, '2024-10-18 16:46:20'),
(73, 'Admin', 'PAAS', 22.39, 3.90, 21.52, 24.14, 25.88, 0.00, 0.00, '2024-10-18 16:44:23', 'Inactive', 'Re-Entry Pass 10/18', 0.00, '2024-10-18 16:44:23'),
(88, 'Admin', 'PACS', 41.15, 3.60, 39.67, 44.11, 47.08, 0.00, 0.00, '2024-10-23 12:53:49', 'Inactive', '', 0.00, '2024-10-23 12:53:49'),
(90, 'Admin', 'PACS', 41.15, 3.60, 39.67, 44.11, 47.08, 0.00, 0.00, '2024-10-23 13:37:37', 'Active', '', 0.00, '2024-10-23 13:48:57'),
(83, 'Admin', 'POET', 4.17, 10.10, 3.75, 5.01, 5.85, 0.00, 0.00, '2024-10-22 13:13:44', 'Inactive', '', 0.00, '2024-10-22 13:13:44'),
(86, 'Admin', 'POET', 4.04, 10.00, 3.64, 4.85, 5.66, 0.00, 0.00, '2024-10-23 12:51:42', 'Inactive', '', 0.00, '2024-10-23 12:51:42'),
(56, 'Admin', 'PTCT', 39.24, 5.00, 37.28, 43.16, 47.09, 0.00, 0.00, '2024-10-14 13:46:49', 'Active', 'Entered 10/14 @ 39.25', 0.00, '2024-10-14 18:46:49'),
(31, 'Admin', 'RDNT', 65.91, 2.30, 64.39, 68.94, 71.97, 0.00, 0.00, '2024-10-11 16:12:15', 'Active', 'Re-entry 10/11, 10/14 - Target 1 Achieved and Trail Stop updated', 68.35, '2024-10-11 21:12:15'),
(60, 'Admin', 'SHAK', 108.31, 4.00, 103.98, 116.97, 125.64, 0.00, 0.00, '2024-10-15 13:07:34', 'Active', 'Targets updated', 0.00, '2024-10-15 18:07:34'),
(81, 'Admin', 'SMTC', 44.40, 5.30, 42.05, 49.11, 53.81, 0.00, 0.00, '2024-10-22 13:12:20', 'Active', '', 0.00, '2024-10-22 14:09:20'),
(40, 'Admin', 'TBBK', 53.05, 3.70, 51.09, 56.98, 60.90, 0.00, 0.00, '2024-10-11 20:41:05', 'Active', '10/14 - Target 1 achieved', 0.00, '2024-10-12 01:41:05'),
(20, 'Admin', 'USM', 56.18, 3.10, 54.44, 59.66, 63.15, 0.00, 0.00, '2024-10-09 03:54:57', 'Active', 'Entered 09/25\n10/16 - Target 1 Achieved', 0.00, '2024-10-09 08:54:57'),
(84, 'Admin', 'WHD', 60.38, 3.40, 58.33, 64.49, 68.59, 0.00, 0.00, '2024-10-22 13:14:27', 'Inactive', '', 0.00, '2024-10-22 13:14:27'),
(85, 'Admin', 'WHD', 60.14, 3.30, 58.16, 64.11, 68.08, 0.00, 0.00, '2024-10-23 12:50:59', 'Inactive', '', 0.00, '2024-10-23 12:50:59'),
(45, 'Admin', 'WING', 402.48, 3.30, 389.20, 426.63, 450.78, 0.00, 0.00, '2024-10-11 20:48:38', 'Inactive', '', 0.00, '2024-10-12 01:48:38'),
(33, 'Admin', 'WTTR', 11.00, 4.00, 10.56, 11.88, 12.76, 0.00, 0.00, '2024-10-11 16:13:18', 'Active', 'Entered at 11.38', 0.00, '2024-10-11 21:13:18'),
(71, 'Admin', 'ZIM', 21.20, 6.00, 19.93, 23.74, 26.29, 0.00, 0.00, '2024-10-18 12:53:26', 'Active', '10/20 - Target 1 achieve. SL moved to buying price', 0.00, '2024-10-21 18:54:09'),
(52, 'Admin', 'ZVRA', 8.20, 7.50, 7.58, 8.69, 9.18, 0.00, 0.00, '2024-10-14 12:11:37', 'Inactive', '', 0.00, '2024-10-14 17:11:37');

-- --------------------------------------------------------

--
-- Table structure for table `Users`
--

CREATE TABLE `Users` (
  `UserID` bigint NOT NULL,
  `UserName` varchar(255) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `UserPassword` varchar(255) DEFAULT NULL,
  `UserRole` varchar(255) DEFAULT NULL,
  `user_status` varchar(10) DEFAULT 'Active',
  `creation_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `expire_date` timestamp GENERATED ALWAYS AS ((`creation_date` + interval 6 month)) STORED NULL,
  `country_code` varchar(10) NOT NULL,
  `mobile_number` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Users`
--

INSERT INTO `Users` (`UserID`, `UserName`, `Email`, `UserPassword`, `UserRole`, `user_status`, `creation_date`, `country_code`, `mobile_number`) VALUES
(12, 'Vikram Malhotra', 'vikram@investinbulls.net', 'Test@123456', 'Admin', 'Active', '2024-10-06 18:42:52', '+1', '1234567890'),
(16, 'Harish', 'harish.ponnapureddy@gmail.com', 'pInvesting@2024', 'General', 'Active', '2024-10-09 18:43:39', '+1', '1234567890'),
(17, 'Paromita Chatterree', 'paromita2k4@gmail.com', 'Test#2024', 'Admin', 'Active', '2024-10-09 19:52:15', '+1', '1234567890'),
(18, 'siddharth.mullapudi@gmail.com', 'siddharth.mullapudi@gmail.com', 'Invest@1', 'General', 'Active', '2024-10-09 20:53:10', '+1', '1234567890'),
(19, 'Prasad SR', 'Prasadsr.4u@gmail.com', 'Inshaallah1$', 'General', 'Active', '2024-10-09 22:15:29', '+1', '1234567890'),
(20, 'Sheshacharya Tirumala ', 'tirumala.sheshu@gmail.com', 'Ishaan@07', 'General', 'Active', '2024-10-09 22:16:32', '+1', '1234567890'),
(21, 'Deepss', 'deepss1582@gmail.com', 'Shakthi@23', 'General', 'Active', '2024-10-10 03:29:10', '+1', '1234567890'),
(22, 'Kasim Mumtaz', 'kasim.mumtaz@gmail.com', 'Champa2040!', 'General', 'Active', '2024-10-10 04:05:01', '+1', '1234567890'),
(23, 'srinivas', 'Chennupati227@gmail.com', 'Harinya@1$', 'General', 'Active', '2024-10-10 04:08:57', '+1', '1234567890'),
(24, 'Krishna Muvva', 'krishna.muvva@gmail.com', 'Frisco2024$', 'General', 'Active', '2024-10-10 15:56:42', '+1', '1234567890'),
(25, 'Paromita Chat', 'chatterjee.paromita9@gmail.com', 'Test#2024', 'General', 'Active', '2024-10-10 16:56:56', '+1', '2144306791'),
(26, 'Vicky Malhotra', 'vmalhotra13@outlook.com', 'Abcd@123456', 'General', 'Active', '2024-10-10 17:38:17', '+1', '6098510433'),
(27, 'Srikanth K', 'srikanthkata1989@gmail.com', 'Ridhira@2023', 'General', 'Active', '2024-10-10 20:54:35', '+1', '7047337030'),
(28, 'Gopichand Gadde', 'ggopichand@gmail.com', 'Kirtana&468K', 'General', 'Active', '2024-10-11 00:16:55', '+1', '7204123545'),
(29, 'Vik', 'vmalhotr@icloud.com', 'Test@123456', 'General', 'Active', '2024-10-11 06:34:39', '+1', '6098510433'),
(30, 'Venkat Samala', 'svenkat.pega@gmail.com', 'Venky@575', 'General', 'Active', '2024-10-13 02:43:46', '+1', '9549038579'),
(31, 'Niranjan Aguru', 'ankishore@yahoo.com', 'Winter2024!', 'General', 'Active', '2024-10-14 12:30:15', '+1', '4044946572'),
(32, 'Raviteja Boyanapalli', 'raviteja.boyanapalli@yahoo.com', 'FreshPwd@9098', 'General', 'Active', '2024-10-14 17:01:28', '+1', '5174770345'),
(33, 'Sairam T', 'inform2sr@gmail.com', 'WCchec$5rufhy', 'General', 'Active', '2024-10-14 17:04:55', '+1', '9524289147'),
(34, 'Ram Siri', 'ram4nline@gmail.com', 'Pwd4Investing1@', 'General', 'Active', '2024-10-14 22:41:56', '+1', '7605834095'),
(35, 'Vikram Lakkireddy', 'lvreddy34@gmail.com', 'Invest@0614', 'General', 'Active', '2024-10-15 14:14:54', '+1', '3096215057'),
(36, 'Amita J', 'rohitaggie@gmail.com', 'PlayTennis@1980', 'General', 'Active', '2024-10-16 03:18:51', '+1', '8036409051'),
(37, 'Sridevi', 'sridevigattamneni@gmail.com', 'D!am0ndcreek', 'General', 'Active', '2024-10-17 12:37:47', '+1', '9083002020'),
(38, 'Ravi Rachappa', 'ravi.tradealgo@gmail.com', 'Ess@1069', 'General', 'Active', '2024-10-22 00:58:19', '+1', '4699255664');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Tickers`
--
ALTER TABLE `Tickers`
  ADD PRIMARY KEY (`TickerName`,`CreateDate`),
  ADD UNIQUE KEY `TickerID` (`TickerID`);

--
-- Indexes for table `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`UserID`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Tickers`
--
ALTER TABLE `Tickers`
  MODIFY `TickerID` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=96;

--
-- AUTO_INCREMENT for table `Users`
--
ALTER TABLE `Users`
  MODIFY `UserID` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
