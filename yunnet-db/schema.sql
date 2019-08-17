-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema YunNet
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema YunNet
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `YunNet` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
USE `YunNet` ;

-- -----------------------------------------------------
-- Table `YunNet`.`permission`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `YunNet`.`permission` ;

CREATE TABLE IF NOT EXISTS `YunNet`.`permission` (
  `pid` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `str` TEXT NOT NULL,
  PRIMARY KEY (`pid`))
ENGINE = InnoDB
AUTO_INCREMENT = 12
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;

CREATE UNIQUE INDEX `permission_key` USING HASH ON `YunNet`.`permission` (`str`);


-- -----------------------------------------------------
-- Table `YunNet`.`group`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `YunNet`.`group` ;

CREATE TABLE IF NOT EXISTS `YunNet`.`group` (
  `gid` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` TEXT NULL DEFAULT NULL,
  `description` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`gid`))
ENGINE = InnoDB
AUTO_INCREMENT = 10
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `YunNet`.`group_permission`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `YunNet`.`group_permission` ;

CREATE TABLE IF NOT EXISTS `YunNet`.`group_permission` (
  `gid` INT(10) UNSIGNED NOT NULL,
  `pid` INT(10) UNSIGNED NOT NULL,
  PRIMARY KEY USING BTREE (`gid`, `pid`),
  CONSTRAINT `group_permission_fk_permission`
    FOREIGN KEY (`pid`)
    REFERENCES `YunNet`.`permission` (`pid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `group_permission_fk_group`
    FOREIGN KEY (`gid`)
    REFERENCES `YunNet`.`group` (`gid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;

CREATE INDEX `group_permission_fk_permission_idx` ON `YunNet`.`group_permission` (`pid` ASC);


-- -----------------------------------------------------
-- Table `YunNet`.`group_inherit`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `YunNet`.`group_inherit` ;

CREATE TABLE IF NOT EXISTS `YunNet`.`group_inherit` (
  `gid` INT(10) UNSIGNED NOT NULL,
  `parent_gid` INT(10) UNSIGNED NOT NULL,
  PRIMARY KEY USING BTREE (`gid`, `parent_gid`),
  CONSTRAINT `group_inherit_fk_group`
    FOREIGN KEY (`gid`)
    REFERENCES `YunNet`.`group` (`gid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `group_inherit_fk_group_p`
    FOREIGN KEY (`parent_gid`)
    REFERENCES `YunNet`.`group` (`gid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;

CREATE INDEX `fk_gid_groups_gid` USING BTREE ON `YunNet`.`group_inherit` (`gid`);

CREATE INDEX `group_inherit_fk_group_p_idx` ON `YunNet`.`group_inherit` (`parent_gid` ASC);


-- -----------------------------------------------------
-- Table `YunNet`.`switch`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `YunNet`.`switch` ;

CREATE TABLE IF NOT EXISTS `YunNet`.`switch` (
  `switch_id` INT(11) NOT NULL,
  `upper_id` INT(11) NULL DEFAULT NULL,
  `upper_port` INT(11) NULL DEFAULT NULL,
  `upper_port_type` INT(11) NOT NULL,
  `location` VARCHAR(10) NULL DEFAULT NULL,
  `remote_password` VARCHAR(30) NOT NULL,
  `account` VARCHAR(30) NOT NULL,
  `vlan` INT(11) NOT NULL,
  `machine_type` INT(11) NOT NULL,
  `port_description` LONGTEXT NULL DEFAULT NULL,
  `port_type` LONGTEXT CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_bin' NULL DEFAULT NULL,
  `MB_Serial_Number` VARCHAR(15) NULL DEFAULT NULL,
  PRIMARY KEY (`switch_id`),
  CONSTRAINT `switch_fk_self_upper_id`
    FOREIGN KEY (`upper_id`)
    REFERENCES `YunNet`.`switch` (`switch_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;

CREATE INDEX `switch_fk_self_upper_id_idx` ON `YunNet`.`switch` (`upper_id` ASC);


-- -----------------------------------------------------
-- Table `YunNet`.`ip_status`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `YunNet`.`ip_status` ;

CREATE TABLE IF NOT EXISTS `YunNet`.`ip_status` (
  `status_id` INT(11) UNSIGNED NOT NULL,
  `name` TEXT NULL,
  PRIMARY KEY (`status_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `YunNet`.`ip_type`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `YunNet`.`ip_type` ;

CREATE TABLE IF NOT EXISTS `YunNet`.`ip_type` (
  `ip_type_id` INT(11) UNSIGNED NOT NULL,
  `type` TEXT NULL,
  PRIMARY KEY (`ip_type_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `YunNet`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `YunNet`.`user` ;

CREATE TABLE IF NOT EXISTS `YunNet`.`user` (
  `uid` INT(10) UNSIGNED NOT NULL,
  `username` VARCHAR(20) NOT NULL,
  `password_hash` TEXT NULL DEFAULT NULL,
  `nick` TEXT NULL DEFAULT NULL,
  `department` TEXT NULL,
  `back_mail` TEXT NULL,
  `note` TEXT NULL,
  PRIMARY KEY (`uid`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;

CREATE UNIQUE INDEX `uid_UNIQUE` ON `YunNet`.`user` (`uid` ASC);

CREATE UNIQUE INDEX `back_mail_UNIQUE` ON `YunNet`.`user` (`back_mail` ASC);

CREATE UNIQUE INDEX `username_UNIQUE` ON `YunNet`.`user` (`username` ASC);


-- -----------------------------------------------------
-- Table `YunNet`.`ip`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `YunNet`.`ip` ;

CREATE TABLE IF NOT EXISTS `YunNet`.`ip` (
  `ip` VARCHAR(32) NOT NULL,
  `switch_id` INT(11) NULL DEFAULT NULL,
  `status_id` INT(11) UNSIGNED NOT NULL DEFAULT 0,
  `ip_type_id` INT(11) UNSIGNED NOT NULL DEFAULT 0,
  `mac` VARCHAR(18) NULL DEFAULT NULL,
  `port` INT(11) NOT NULL DEFAULT 0,
  `port_type` INT(11) NOT NULL DEFAULT 0,
  `is_updated` TINYINT(1) NOT NULL DEFAULT 0,
  `uid` INT(10) UNSIGNED NULL,
  `gid` INT(10) UNSIGNED NULL,
  `description` LONGTEXT NULL,
  PRIMARY KEY (`ip`),
  CONSTRAINT `ip_fk_switch`
    FOREIGN KEY (`switch_id`)
    REFERENCES `YunNet`.`switch` (`switch_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ip_fk_ip_status`
    FOREIGN KEY (`status_id`)
    REFERENCES `YunNet`.`ip_status` (`status_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ip_fk_ip_type`
    FOREIGN KEY (`ip_type_id`)
    REFERENCES `YunNet`.`ip_type` (`ip_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ip_fk_user`
    FOREIGN KEY (`uid`)
    REFERENCES `YunNet`.`user` (`uid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ip_fk_group`
    FOREIGN KEY (`gid`)
    REFERENCES `YunNet`.`group` (`gid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;

CREATE INDEX `ip_fk_ip_status_idx` ON `YunNet`.`ip` (`status_id` ASC);

CREATE INDEX `ip_fk_ip_type_idx` ON `YunNet`.`ip` (`ip_type_id` ASC);

CREATE INDEX `ip_fk_switch_idx` ON `YunNet`.`ip` (`switch_id` ASC);

CREATE INDEX `ip_fk_user_idx` ON `YunNet`.`ip` (`uid` ASC);

CREATE INDEX `ip_fk_group_idx` ON `YunNet`.`ip` (`gid` ASC);


-- -----------------------------------------------------
-- Table `YunNet`.`user_permission`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `YunNet`.`user_permission` ;

CREATE TABLE IF NOT EXISTS `YunNet`.`user_permission` (
  `uid` INT(10) UNSIGNED NOT NULL,
  `pid` INT(10) UNSIGNED NOT NULL,
  `is_excluded` TINYINT(1) NULL,
  PRIMARY KEY USING BTREE (`uid`, `pid`),
  CONSTRAINT `user_permission_fk_permission`
    FOREIGN KEY (`pid`)
    REFERENCES `YunNet`.`permission` (`pid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `user_permission_fk_user`
    FOREIGN KEY (`uid`)
    REFERENCES `YunNet`.`user` (`uid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;

CREATE INDEX `user_permission_fk_permission_idx` ON `YunNet`.`user_permission` (`pid` ASC);


-- -----------------------------------------------------
-- Table `YunNet`.`group_user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `YunNet`.`group_user` ;

CREATE TABLE IF NOT EXISTS `YunNet`.`group_user` (
  `gid` INT(10) UNSIGNED NOT NULL,
  `uid` INT(10) UNSIGNED NOT NULL,
  PRIMARY KEY (`gid`, `uid`),
  CONSTRAINT `group_user_fk_group`
    FOREIGN KEY (`gid`)
    REFERENCES `YunNet`.`group` (`gid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `group_user_fk_user`
    FOREIGN KEY (`uid`)
    REFERENCES `YunNet`.`user` (`uid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `group_user_fk_user_idx` ON `YunNet`.`group_user` (`uid` ASC);


-- -----------------------------------------------------
-- Table `YunNet`.`lock_type`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `YunNet`.`lock_type` ;

CREATE TABLE IF NOT EXISTS `YunNet`.`lock_type` (
  `lock_type_id` INT(10) UNSIGNED NOT NULL,
  `str` TEXT NULL,
  PRIMARY KEY (`lock_type_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `YunNet`.`lock`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `YunNet`.`lock` ;

CREATE TABLE IF NOT EXISTS `YunNet`.`lock` (
  `lock_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `lock_type_id` INT(10) UNSIGNED NOT NULL DEFAULT 0,
  `ip` VARCHAR(32) NULL,
  `lock_date` DATETIME NULL,
  `unlock_date` DATETIME NULL,
  `description` LONGTEXT NULL,
  `lock_by_user_id` INT(10) UNSIGNED NULL,
  PRIMARY KEY (`lock_id`),
  CONSTRAINT `lock_fk_ip`
    FOREIGN KEY (`ip`)
    REFERENCES `YunNet`.`ip` (`ip`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `lock_fk_lock_type`
    FOREIGN KEY (`lock_type_id`)
    REFERENCES `YunNet`.`lock_type` (`lock_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `lock_fk_user`
    FOREIGN KEY (`lock_by_user_id`)
    REFERENCES `YunNet`.`user` (`uid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `lock_fk_ip_idx` ON `YunNet`.`lock` (`ip` ASC) VISIBLE;

CREATE INDEX `lock_fk_lock_type_idx` ON `YunNet`.`lock` (`lock_type_id` ASC) VISIBLE;

CREATE INDEX `lock_fk_user_idx` ON `YunNet`.`lock` (`lock_by_user_id` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `YunNet`.`announcement`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `YunNet`.`announcement` ;

CREATE TABLE IF NOT EXISTS `YunNet`.`announcement` (
  `announcement_id` INT(10) UNSIGNED NOT NULL,
  `title` LONGTEXT NULL,
  `content` LONGTEXT NULL,
  `uid` INT(10) UNSIGNED NOT NULL,
  PRIMARY KEY (`announcement_id`),
  CONSTRAINT `announcement_fk_user`
    FOREIGN KEY (`uid`)
    REFERENCES `YunNet`.`user` (`uid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `announcement_fk_user_idx` ON `YunNet`.`announcement` (`uid` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `YunNet`.`token`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `YunNet`.`token` ;

CREATE TABLE IF NOT EXISTS `YunNet`.`token` (
  `uid` INT(10) UNSIGNED NOT NULL,
  `token` TEXT NULL,
  PRIMARY KEY (`uid`),
  CONSTRAINT `token_fk_user`
    FOREIGN KEY (`uid`)
    REFERENCES `YunNet`.`user` (`uid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `YunNet`.`backup_mac`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `YunNet`.`backup_mac` ;

CREATE TABLE IF NOT EXISTS `YunNet`.`backup_mac` (
  `ip` VARCHAR(32) NOT NULL,
  `mac` VARCHAR(18) NULL DEFAULT NULL,
  PRIMARY KEY (`ip`),
  CONSTRAINT `backup_mac_fk_ip`
    FOREIGN KEY (`ip`)
    REFERENCES `YunNet`.`ip` (`ip`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
