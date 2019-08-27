-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- 主機： db
-- 產生時間： 2019 年 08 月 27 日 08:32
-- 伺服器版本： 10.4.6-MariaDB-1:10.4.6+maria~bionic
-- PHP 版本： 7.2.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `YunNet`
--
CREATE DATABASE IF NOT EXISTS `YunNet` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
USE `YunNet`;

-- --------------------------------------------------------

--
-- 資料表結構 `announcement`
--
-- 建立時間： 2019 年 08 月 17 日 10:52
--

DROP TABLE IF EXISTS `announcement`;
CREATE TABLE `announcement` (
  `announcement_id` int(10) UNSIGNED NOT NULL,
  `content` longtext COLLATE utf8_unicode_ci DEFAULT NULL,
  `uid` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `backup_mac`
--
-- 建立時間： 2019 年 08 月 23 日 08:24
--

DROP TABLE IF EXISTS `backup_mac`;
CREATE TABLE `backup_mac` (
  `ip` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `mac` varchar(18) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `bed`
--
-- 建立時間： 2019 年 08 月 23 日 05:01
--

DROP TABLE IF EXISTS `bed`;
CREATE TABLE `bed` (
  `bed` varchar(9) COLLATE utf8_unicode_ci NOT NULL,
  `type` int(11) NOT NULL,
  `portal` varchar(9) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ip` varchar(32) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `group`
--
-- 建立時間： 2019 年 08 月 17 日 10:52
-- 最後更新： 2019 年 08 月 23 日 08:21
--

DROP TABLE IF EXISTS `group`;
CREATE TABLE `group` (
  `gid` int(10) UNSIGNED NOT NULL,
  `name` text COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `group_inherit`
--
-- 建立時間： 2019 年 08 月 17 日 10:52
--

DROP TABLE IF EXISTS `group_inherit`;
CREATE TABLE `group_inherit` (
  `gid` int(10) UNSIGNED NOT NULL,
  `parent_gid` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `group_permission`
--
-- 建立時間： 2019 年 08 月 17 日 10:52
--

DROP TABLE IF EXISTS `group_permission`;
CREATE TABLE `group_permission` (
  `gid` int(10) UNSIGNED NOT NULL,
  `pid` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `group_user`
--
-- 建立時間： 2019 年 08 月 17 日 10:52
--

DROP TABLE IF EXISTS `group_user`;
CREATE TABLE `group_user` (
  `gid` int(10) UNSIGNED NOT NULL,
  `uid` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `iptable`
--
-- 建立時間： 2019 年 08 月 23 日 08:23
-- 最後更新： 2019 年 08 月 25 日 18:03
--

DROP TABLE IF EXISTS `iptable`;
CREATE TABLE `iptable` (
  `ip` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `ip_type_id` int(11) UNSIGNED DEFAULT NULL,
  `is_unlimited` tinyint(1) NOT NULL DEFAULT 0,
  `switch_id` int(11) DEFAULT NULL,
  `port` int(11) NOT NULL,
  `port_type` int(11) NOT NULL,
  `mac` varchar(18) COLLATE utf8_unicode_ci DEFAULT NULL,
  `is_updated` tinyint(1) NOT NULL DEFAULT 0,
  `uid` int(11) UNSIGNED NOT NULL,
  `gid` int(11) UNSIGNED NOT NULL,
  `description` text COLLATE utf8_unicode_ci NOT NULL,
  `lock_id` int(10) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `ip_type`
--
-- 建立時間： 2019 年 08 月 17 日 10:52
-- 最後更新： 2019 年 08 月 23 日 05:27
--

DROP TABLE IF EXISTS `ip_type`;
CREATE TABLE `ip_type` (
  `ip_type_id` int(11) UNSIGNED NOT NULL,
  `type` text COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `lock`
--
-- 建立時間： 2019 年 08 月 25 日 05:01
-- 最後更新： 2019 年 08 月 25 日 06:04
--

DROP TABLE IF EXISTS `lock`;
CREATE TABLE `lock` (
  `lock_id` int(10) UNSIGNED NOT NULL,
  `lock_type_id` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `ip` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `lock_date` datetime DEFAULT NULL,
  `unlock_date` datetime DEFAULT NULL,
  `description` longtext COLLATE utf8_unicode_ci DEFAULT NULL,
  `lock_by_user_id` int(10) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `lock_type`
--
-- 建立時間： 2019 年 08 月 17 日 10:52
-- 最後更新： 2019 年 08 月 23 日 05:33
--

DROP TABLE IF EXISTS `lock_type`;
CREATE TABLE `lock_type` (
  `lock_type_id` int(10) UNSIGNED NOT NULL,
  `str` text COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `permission`
--
-- 建立時間： 2019 年 08 月 17 日 10:52
--

DROP TABLE IF EXISTS `permission`;
CREATE TABLE `permission` (
  `pid` int(10) UNSIGNED NOT NULL,
  `str` text COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `switch`
--
-- 建立時間： 2019 年 08 月 23 日 06:51
-- 最後更新： 2019 年 08 月 23 日 06:51
--

DROP TABLE IF EXISTS `switch`;
CREATE TABLE `switch` (
  `switch_id` int(11) NOT NULL,
  `upper_id` int(11) DEFAULT NULL,
  `upper_port` int(11) DEFAULT NULL,
  `upper_port_type` int(11) NOT NULL,
  `location` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `account` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `vlan` int(11) NOT NULL,
  `machine_type` int(11) NOT NULL,
  `port_description` longtext COLLATE utf8_unicode_ci DEFAULT NULL,
  `port_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `ip` varchar(32) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `token`
--
-- 建立時間： 2019 年 08 月 27 日 05:27
-- 最後更新： 2019 年 08 月 27 日 05:28
--

DROP TABLE IF EXISTS `token`;
CREATE TABLE `token` (
  `uid` int(10) UNSIGNED NOT NULL,
  `token` text COLLATE utf8_unicode_ci DEFAULT NULL,
  `timestamp` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `user`
--
-- 建立時間： 2019 年 08 月 17 日 10:52
-- 最後更新： 2019 年 08 月 23 日 07:51
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `uid` int(10) UNSIGNED NOT NULL,
  `username` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `password_hash` text COLLATE utf8_unicode_ci DEFAULT NULL,
  `nick` text COLLATE utf8_unicode_ci DEFAULT NULL,
  `department` text COLLATE utf8_unicode_ci DEFAULT NULL,
  `back_mail` text COLLATE utf8_unicode_ci DEFAULT NULL,
  `note` text COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `user_permission`
--
-- 建立時間： 2019 年 08 月 17 日 10:52
--

DROP TABLE IF EXISTS `user_permission`;
CREATE TABLE `user_permission` (
  `uid` int(10) UNSIGNED NOT NULL,
  `pid` int(10) UNSIGNED NOT NULL,
  `is_excluded` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `variable`
--
-- 建立時間： 2019 年 08 月 22 日 05:10
-- 最後更新： 2019 年 08 月 22 日 05:12
--

DROP TABLE IF EXISTS `variable`;
CREATE TABLE `variable` (
  `name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(16) COLLATE utf8_unicode_ci NOT NULL,
  `value` text COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `announcement`
--
ALTER TABLE `announcement`
  ADD PRIMARY KEY (`announcement_id`),
  ADD KEY `announcement_fk_user_idx` (`uid`);

--
-- 資料表索引 `backup_mac`
--
ALTER TABLE `backup_mac`
  ADD PRIMARY KEY (`ip`);

--
-- 資料表索引 `bed`
--
ALTER TABLE `bed`
  ADD PRIMARY KEY (`bed`);

--
-- 資料表索引 `group`
--
ALTER TABLE `group`
  ADD PRIMARY KEY (`gid`);

--
-- 資料表索引 `group_inherit`
--
ALTER TABLE `group_inherit`
  ADD PRIMARY KEY (`gid`,`parent_gid`) USING BTREE,
  ADD KEY `fk_gid_groups_gid` (`gid`) USING BTREE,
  ADD KEY `group_inherit_fk_group_p_idx` (`parent_gid`);

--
-- 資料表索引 `group_permission`
--
ALTER TABLE `group_permission`
  ADD PRIMARY KEY (`gid`,`pid`) USING BTREE,
  ADD KEY `group_permission_fk_permission_idx` (`pid`);

--
-- 資料表索引 `group_user`
--
ALTER TABLE `group_user`
  ADD PRIMARY KEY (`gid`,`uid`),
  ADD KEY `group_user_fk_user_idx` (`uid`);

--
-- 資料表索引 `iptable`
--
ALTER TABLE `iptable`
  ADD PRIMARY KEY (`ip`),
  ADD KEY `iptable_fk_switch` (`switch_id`),
  ADD KEY `iptable_fk_ip_type` (`ip_type_id`),
  ADD KEY `iptable_fk_user` (`uid`),
  ADD KEY `iptable_fk_group` (`gid`);

--
-- 資料表索引 `ip_type`
--
ALTER TABLE `ip_type`
  ADD PRIMARY KEY (`ip_type_id`);

--
-- 資料表索引 `lock`
--
ALTER TABLE `lock`
  ADD PRIMARY KEY (`lock_id`),
  ADD KEY `lock_fk_ip_idx` (`ip`),
  ADD KEY `lock_fk_lock_type_idx` (`lock_type_id`),
  ADD KEY `lock_fk_user_idx` (`lock_by_user_id`);

--
-- 資料表索引 `lock_type`
--
ALTER TABLE `lock_type`
  ADD PRIMARY KEY (`lock_type_id`);

--
-- 資料表索引 `permission`
--
ALTER TABLE `permission`
  ADD PRIMARY KEY (`pid`),
  ADD UNIQUE KEY `permission_key` (`str`) USING HASH;

--
-- 資料表索引 `switch`
--
ALTER TABLE `switch`
  ADD PRIMARY KEY (`switch_id`),
  ADD KEY `switch_fk_self_upper_id_idx` (`upper_id`);

--
-- 資料表索引 `token`
--
ALTER TABLE `token`
  ADD PRIMARY KEY (`uid`);

--
-- 資料表索引 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`uid`),
  ADD UNIQUE KEY `uid_UNIQUE` (`uid`),
  ADD UNIQUE KEY `username_UNIQUE` (`username`),
  ADD UNIQUE KEY `back_mail_UNIQUE` (`back_mail`) USING HASH;

--
-- 資料表索引 `user_permission`
--
ALTER TABLE `user_permission`
  ADD PRIMARY KEY (`uid`,`pid`) USING BTREE,
  ADD KEY `user_permission_fk_permission_idx` (`pid`);

--
-- 資料表索引 `variable`
--
ALTER TABLE `variable`
  ADD PRIMARY KEY (`name`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `group`
--
ALTER TABLE `group`
  MODIFY `gid` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `lock`
--
ALTER TABLE `lock`
  MODIFY `lock_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `permission`
--
ALTER TABLE `permission`
  MODIFY `pid` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `announcement`
--
ALTER TABLE `announcement`
  ADD CONSTRAINT `announcement_fk_user` FOREIGN KEY (`uid`) REFERENCES `user` (`uid`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- 資料表的限制式 `backup_mac`
--
ALTER TABLE `backup_mac`
  ADD CONSTRAINT `backup_mac_fk_iptable` FOREIGN KEY (`ip`) REFERENCES `iptable` (`ip`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- 資料表的限制式 `group_inherit`
--
ALTER TABLE `group_inherit`
  ADD CONSTRAINT `group_inherit_fk_group` FOREIGN KEY (`gid`) REFERENCES `group` (`gid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `group_inherit_fk_group_p` FOREIGN KEY (`parent_gid`) REFERENCES `group` (`gid`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- 資料表的限制式 `group_permission`
--
ALTER TABLE `group_permission`
  ADD CONSTRAINT `group_permission_fk_group` FOREIGN KEY (`gid`) REFERENCES `group` (`gid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `group_permission_fk_permission` FOREIGN KEY (`pid`) REFERENCES `permission` (`pid`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- 資料表的限制式 `group_user`
--
ALTER TABLE `group_user`
  ADD CONSTRAINT `group_user_fk_group` FOREIGN KEY (`gid`) REFERENCES `group` (`gid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `group_user_fk_user` FOREIGN KEY (`uid`) REFERENCES `user` (`uid`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- 資料表的限制式 `iptable`
--
ALTER TABLE `iptable`
  ADD CONSTRAINT `iptable_fk_group` FOREIGN KEY (`gid`) REFERENCES `group` (`gid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `iptable_fk_ip_type` FOREIGN KEY (`ip_type_id`) REFERENCES `ip_type` (`ip_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `iptable_fk_switch` FOREIGN KEY (`switch_id`) REFERENCES `switch` (`switch_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `iptable_fk_user` FOREIGN KEY (`uid`) REFERENCES `user` (`uid`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- 資料表的限制式 `lock`
--
ALTER TABLE `lock`
  ADD CONSTRAINT `lock_fk_lock_type` FOREIGN KEY (`lock_type_id`) REFERENCES `lock_type` (`lock_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `lock_fk_user` FOREIGN KEY (`lock_by_user_id`) REFERENCES `user` (`uid`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- 資料表的限制式 `switch`
--
ALTER TABLE `switch`
  ADD CONSTRAINT `switch_fk_self_upper_id` FOREIGN KEY (`upper_id`) REFERENCES `switch` (`switch_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- 資料表的限制式 `token`
--
ALTER TABLE `token`
  ADD CONSTRAINT `token_fk_user` FOREIGN KEY (`uid`) REFERENCES `user` (`uid`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- 資料表的限制式 `user_permission`
--
ALTER TABLE `user_permission`
  ADD CONSTRAINT `user_permission_fk_permission` FOREIGN KEY (`pid`) REFERENCES `permission` (`pid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `user_permission_fk_user` FOREIGN KEY (`uid`) REFERENCES `user` (`uid`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
