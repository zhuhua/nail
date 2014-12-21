/*
Navicat MySQL Data Transfer

Source Server         : mariadb
Source Server Version : 50540
Source Host           : localhost:3306
Source Database       : nail

Target Server Type    : MYSQL
Target Server Version : 50540
File Encoding         : 65001

Date: 2014-12-21 23:18:50
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `artisan`
-- ----------------------------
DROP TABLE IF EXISTS `artisan`;
CREATE TABLE `artisan` (
  `id` char(32) NOT NULL COMMENT 'uuid',
  `name` varchar(100) NOT NULL COMMENT '手艺人-名称',
  `level` tinyint(4) NOT NULL DEFAULT '0' COMMENT '等级（0-15）',
  `average_price` float NOT NULL,
  `certification_pop` bit(1) NOT NULL DEFAULT b'0' COMMENT '明星美甲师认证',
  `certification_pro` bit(1) NOT NULL DEFAULT b'0' COMMENT '高级职业美甲师认证',
  `brief` varchar(1000) NOT NULL COMMENT '自我介绍',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='手艺人';

-- ----------------------------
-- Records of artisan
-- ----------------------------

-- ----------------------------
-- Table structure for `category`
-- ----------------------------
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '类型（美甲，美足，美睫，护理）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of category
-- ----------------------------

-- ----------------------------
-- Table structure for `count`
-- ----------------------------
DROP TABLE IF EXISTS `count`;
CREATE TABLE `count` (
  `id` bigint(20) NOT NULL,
  `object_id` char(32) NOT NULL,
  `amount` int(11) NOT NULL DEFAULT '0',
  `type` tinyint(4) NOT NULL COMMENT '类型（接单数，）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of count
-- ----------------------------

-- ----------------------------
-- Table structure for `faverate`
-- ----------------------------
DROP TABLE IF EXISTS `faverate`;
CREATE TABLE `faverate` (
  `id` bigint(20) NOT NULL,
  `user_id` char(32) NOT NULL,
  `simple_id` char(32) NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `is_valid` bit(1) NOT NULL DEFAULT b'1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='收藏关系';

-- ----------------------------
-- Records of faverate
-- ----------------------------

-- ----------------------------
-- Table structure for `images`
-- ----------------------------
DROP TABLE IF EXISTS `images`;
CREATE TABLE `images` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `url` varchar(500) NOT NULL,
  `type` tinyint(4) NOT NULL COMMENT '图片类型，0.手艺人相册，1.样品图片，3.作品图片（订单完成实际效果图上）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of images
-- ----------------------------

-- ----------------------------
-- Table structure for `sample`
-- ----------------------------
DROP TABLE IF EXISTS `sample`;
CREATE TABLE `sample` (
  `name` varchar(100) NOT NULL COMMENT '方案-名称',
  `id` char(32) NOT NULL COMMENT 'uuid',
  `price` float NOT NULL,
  `tag_price` float NOT NULL COMMENT '介绍',
  `sale` smallint(6) NOT NULL,
  `brief` varchar(1000) NOT NULL,
  `category_id` bigint(20) NOT NULL COMMENT '分类',
  `artisan_id` char(32) NOT NULL COMMENT '提供服务的手艺人',
  `is_valid` bit(1) DEFAULT b'1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='美甲师提供的作品方案';

-- ----------------------------
-- Records of sample
-- ----------------------------

-- ----------------------------
-- Table structure for `tag`
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL COMMENT '标签（圣诞节，日韩，纯色，新娘，法式，创意，彩绘，糖果）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of tag
-- ----------------------------
