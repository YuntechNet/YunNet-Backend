-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- 主機： db
-- 產生時間： 2020 年 10 月 07 日 16:52
-- 伺服器版本： 10.4.6-MariaDB-1:10.4.6+maria~bionic
-- PHP 版本： 7.4.9

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
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
-- 建立時間： 2020 年 09 月 01 日 20:35
--

DROP TABLE IF EXISTS `announcement`;
CREATE TABLE `announcement` (
  `announcement_id` int(10) UNSIGNED NOT NULL,
  `title` text COLLATE utf8_unicode_ci DEFAULT NULL,
  `content` longtext COLLATE utf8_unicode_ci DEFAULT NULL,
  `uid` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `backup_mac`
--
-- 建立時間： 2020 年 09 月 01 日 20:35
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
-- 建立時間： 2020 年 09 月 01 日 20:35
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
-- 建立時間： 2020 年 09 月 01 日 20:35
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
-- 建立時間： 2020 年 09 月 01 日 20:35
--

DROP TABLE IF EXISTS `group_inherit`;
CREATE TABLE `group_inherit` (
  `gid` int(10) UNSIGNED NOT NULL,
  `parent_gid` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `group_managed_by`
--
-- 建立時間： 2020 年 09 月 01 日 20:35
--

DROP TABLE IF EXISTS `group_managed_by`;
CREATE TABLE `group_managed_by` (
  `gid` int(10) UNSIGNED NOT NULL,
  `parent_gid` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `group_permission`
--
-- 建立時間： 2020 年 09 月 01 日 20:35
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
-- 建立時間： 2020 年 09 月 01 日 20:35
-- 最後更新： 2020 年 10 月 07 日 12:13
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
-- 建立時間： 2020 年 09 月 01 日 20:35
-- 最後更新： 2020 年 10 月 07 日 16:26
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

--
-- 觸發器 `iptable`
--
DROP TRIGGER IF EXISTS `status_update`;
DELIMITER $$
CREATE TRIGGER `status_update` BEFORE UPDATE ON `iptable` FOR EACH ROW BEGIN
IF (new.is_unlimited = 1 AND old.is_updated = 1) THEN
    SET new.is_updated = 0;
END IF;
IF (new.is_unlimited = 1) THEN
    SET new.lock_id = null;
END IF;
IF (new.mac != old.mac OR new.lock_id != old.lock_id OR new.switch_id != old.switch_id OR old.port != new.port OR old.port_type != new.port_type ) THEN
    SET new.is_updated = 0;
END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- 資料表結構 `iptable_test`
--
-- 建立時間： 2020 年 09 月 01 日 20:35
--

DROP TABLE IF EXISTS `iptable_test`;
CREATE TABLE `iptable_test` (
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
-- 建立時間： 2020 年 09 月 01 日 20:35
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
-- 建立時間： 2020 年 09 月 01 日 20:35
-- 最後更新： 2020 年 10 月 07 日 15:57
--

DROP TABLE IF EXISTS `lock`;
CREATE TABLE `lock` (
  `lock_id` int(10) UNSIGNED NOT NULL,
  `lock_type_id` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `ip` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `uid` int(10) UNSIGNED DEFAULT NULL,
  `gid` int(10) UNSIGNED DEFAULT NULL,
  `lock_date` datetime DEFAULT NULL,
  `unlock_date` datetime DEFAULT NULL,
  `title` text COLLATE utf8_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8_unicode_ci DEFAULT NULL,
  `lock_by_user_id` int(10) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `lock_type`
--
-- 建立時間： 2020 年 09 月 01 日 20:35
--

DROP TABLE IF EXISTS `lock_type`;
CREATE TABLE `lock_type` (
  `lock_type_id` int(10) UNSIGNED NOT NULL,
  `str` text COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `netflow`
--
-- 建立時間： 2020 年 09 月 01 日 20:35
--

DROP TABLE IF EXISTS `netflow`;
CREATE TABLE `netflow` (
  `ip` int(11) NOT NULL,
  `wan_upload` int(11) NOT NULL,
  `wan_download` int(11) NOT NULL,
  `lan_upload` int(11) NOT NULL,
  `lan_download` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `permission`
--
-- 建立時間： 2020 年 09 月 01 日 20:35
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
-- 建立時間： 2020 年 09 月 01 日 20:35
--

DROP TABLE IF EXISTS `switch`;
CREATE TABLE `switch` (
  `id` int(11) NOT NULL,
  `upper_switch` int(11) DEFAULT NULL,
  `upper_port` int(11) DEFAULT NULL,
  `upper_port_type` int(11) NOT NULL,
  `location` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `account` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `vlan` text COLLATE utf8_unicode_ci NOT NULL,
  `machine_type` int(11) NOT NULL,
  `port_description` longtext COLLATE utf8_unicode_ci DEFAULT NULL,
  `port_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `ip` varchar(32) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `temptable`
--
-- 建立時間： 2020 年 09 月 01 日 20:35
--

DROP TABLE IF EXISTS `temptable`;
CREATE TABLE `temptable` (
  `bed` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `username` varchar(200) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `token`
--
-- 建立時間： 2020 年 09 月 01 日 20:35
-- 最後更新： 2020 年 10 月 07 日 15:52
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
-- 建立時間： 2020 年 09 月 01 日 20:47
-- 最後更新： 2020 年 10 月 07 日 15:26
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `uid` int(10) UNSIGNED NOT NULL,
  `username` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` mediumtext COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nick` mediumtext COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `department` mediumtext COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `back_mail` mediumtext COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `note` mediumtext COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `user_permission`
--
-- 建立時間： 2020 年 09 月 01 日 20:35
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
-- 建立時間： 2020 年 09 月 01 日 20:35
-- 最後更新： 2020 年 10 月 07 日 16:10
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
-- 資料表索引 `group_managed_by`
--
ALTER TABLE `group_managed_by`
  ADD PRIMARY KEY (`gid`) USING BTREE,
  ADD KEY `fk_gid_managed_by_gid` (`gid`) USING BTREE,
  ADD KEY `fk_gid_managed_by_parent_gid` (`parent_gid`) USING BTREE;

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
  ADD UNIQUE KEY `mac` (`mac`),
  ADD KEY `iptable_fk_switch` (`switch_id`),
  ADD KEY `iptable_fk_ip_type` (`ip_type_id`),
  ADD KEY `iptable_fk_user` (`uid`),
  ADD KEY `iptable_fk_group` (`gid`);

--
-- 資料表索引 `iptable_test`
--
ALTER TABLE `iptable_test`
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
-- 資料表索引 `netflow`
--
ALTER TABLE `netflow`
  ADD PRIMARY KEY (`ip`);

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
  ADD PRIMARY KEY (`id`),
  ADD KEY `switch_fk_self_upper_switch_idx` (`upper_switch`) USING BTREE;

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
-- 使用資料表自動遞增(AUTO_INCREMENT) `announcement`
--
ALTER TABLE `announcement`
  MODIFY `announcement_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

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
-- 使用資料表自動遞增(AUTO_INCREMENT) `user`
--
ALTER TABLE `user`
  MODIFY `uid` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

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
-- 資料表的限制式 `group_managed_by`
--
ALTER TABLE `group_managed_by`
  ADD CONSTRAINT `fk_gid_managed_by_gid` FOREIGN KEY (`gid`) REFERENCES `group` (`gid`),
  ADD CONSTRAINT `fk_gid_managed_by_parent_gid` FOREIGN KEY (`parent_gid`) REFERENCES `group` (`gid`);

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
  ADD CONSTRAINT `iptable_fk_switch` FOREIGN KEY (`switch_id`) REFERENCES `switch` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
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
  ADD CONSTRAINT `switch_fk_self_upper_id` FOREIGN KEY (`upper_switch`) REFERENCES `switch` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

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
SET FOREIGN_KEY_CHECKS=1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
