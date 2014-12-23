/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50540
Source Host           : localhost:3306
Source Database       : nail

Target Server Type    : MYSQL
Target Server Version : 50540
File Encoding         : 65001

Date: 2014-12-23 17:30:55
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `account`
-- ----------------------------
DROP TABLE IF EXISTS `account`;
CREATE TABLE `account` (
  `id` varchar(32) NOT NULL,
  `mobile` varchar(16) NOT NULL,
  `password` varchar(48) NOT NULL,
  `nick` varchar(24) DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `reg_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of account
-- ----------------------------
INSERT INTO `account` VALUES ('5524a72a504f40aa86f95ae43bedc14f', '13812345678', '7c4a8d09ca3762af61e59520943dc26494f8941b', '', '', '2014-12-23 17:22:51');
