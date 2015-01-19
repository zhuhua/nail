/*
Navicat MariaDB Data Transfer

Source Server         : localhost
Source Server Version : 50540
Source Host           : localhost:3306
Source Database       : nail

Target Server Type    : MariaDB
Target Server Version : 50540
File Encoding         : 65001

Date: 2015-01-19 18:04:25
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for artisan
-- ----------------------------
DROP TABLE IF EXISTS `artisan`;
CREATE TABLE `artisan` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Id',
  `name` varchar(100) NOT NULL COMMENT '手艺人-名称',
  `password` varchar(255) NOT NULL,
  `gender` bit(1) NOT NULL COMMENT '性别',
  `mobile` varchar(16) NOT NULL COMMENT '手机',
  `avatar` varchar(255) NOT NULL COMMENT '头像',
  `level` tinyint(4) NOT NULL DEFAULT '0' COMMENT '等级（0-15）',
  `brief` varchar(1000) NOT NULL COMMENT '自我介绍',
  `avg_price` float NOT NULL,
  `cert_pop` bit(1) NOT NULL DEFAULT b'0' COMMENT '明星美甲师认证',
  `cert_pro` bit(1) NOT NULL DEFAULT b'0' COMMENT '高级职业美甲师认证',
  `create_time` datetime NOT NULL,
  `last_login` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28000011 DEFAULT CHARSET=utf8 COMMENT='手艺人';

-- ----------------------------
-- Records of artisan
-- ----------------------------
INSERT INTO `artisan` VALUES ('28000001', 'shouyiren', '7c4a8d09ca3762af61e59520943dc26494f8941b', '', 'ss', '/img/Grass.jpg', '1', '', '0', '\0', '\0', '2015-01-12 15:06:18', '0000-00-00 00:00:00');
INSERT INTO `artisan` VALUES ('28000002', 'shouyiren', '7c4a8d09ca3762af61e59520943dc26494f8941b', '', 'ss', '', '1', '', '0', '\0', '\0', '2015-01-12 15:06:38', '0000-00-00 00:00:00');
INSERT INTO `artisan` VALUES ('28000003', 'shouyiren', '7c4a8d09ca3762af61e59520943dc26494f8941b', '', 'ss', '', '1', '', '0', '\0', '\0', '2015-01-12 15:06:40', '0000-00-00 00:00:00');
INSERT INTO `artisan` VALUES ('28000004', 'shouyiren', '7c4a8d09ca3762af61e59520943dc26494f8941b', '', 'ss', '', '1', '', '0', '\0', '\0', '2015-01-12 15:06:42', '0000-00-00 00:00:00');
INSERT INTO `artisan` VALUES ('28000005', '是的发生', '7c4a8d09ca3762af61e59520943dc26494f8941b', '', 'ss', '/img/331838f47ff496ad525f38fc92785418.jpg', '1', 'PIL 中的 Image 模块 - oyzway - 博客园\r\n本文是节选自 PIL handbook online 并做了一些简单的翻译只能保证自己看懂,不...Image 类中的函数。0. new : 这个函数创建一幅给定模式(mode)和尺寸(size)...\r\nwww.cnblogs.com/way_te... 2011-04-20  - 百度快照 - 91%好评', '0', '\0', '\0', '2015-01-12 15:06:44', '2015-01-16 15:17:43');
INSERT INTO `artisan` VALUES ('28000006', 'shouyiren', '7c4a8d09ca3762af61e59520943dc26494f8941b', '', 'ss', '', '1', '', '0', '\0', '\0', '2015-01-12 15:06:46', '0000-00-00 00:00:00');
INSERT INTO `artisan` VALUES ('28000007', 'shouyiren', '7c4a8d09ca3762af61e59520943dc26494f8941b', '', 'ss', '', '1', '', '0', '\0', '\0', '2015-01-12 15:06:48', '0000-00-00 00:00:00');
INSERT INTO `artisan` VALUES ('28000008', 'shouyiren', '7c4a8d09ca3762af61e59520943dc26494f8941b', '', 'ss', '', '1', '', '0', '\0', '\0', '2015-01-12 15:06:50', '0000-00-00 00:00:00');
INSERT INTO `artisan` VALUES ('28000009', '哈哈哈哈', '7c4a8d09ca3762af61e59520943dc26494f8941b', '', '12345678', '', '1', '阿斯顿发生的发生打法', '0', '\0', '\0', '2015-01-12 17:06:22', '0000-00-00 00:00:00');
INSERT INTO `artisan` VALUES ('28000010', '阿斯顿发', '7c4a8d09ca3762af61e59520943dc26494f8941b', '', '111111111111', '', '1', '爱上发生地方', '0', '\0', '\0', '2015-01-13 15:51:36', '0000-00-00 00:00:00');

-- ----------------------------
-- Table structure for category
-- ----------------------------
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL COMMENT '类型（美甲，美足，美睫，护理）',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='作品分类';

-- ----------------------------
-- Records of category
-- ----------------------------
INSERT INTO `category` VALUES ('1', '美甲', '0000-00-00 00:00:00');
INSERT INTO `category` VALUES ('2', '美睫', '0000-00-00 00:00:00');
INSERT INTO `category` VALUES ('3', '手足护理', '0000-00-00 00:00:00');
INSERT INTO `category` VALUES ('4', '空气净化', '0000-00-00 00:00:00');

-- ----------------------------
-- Table structure for counts
-- ----------------------------
DROP TABLE IF EXISTS `counts`;
CREATE TABLE `counts` (
  `id` bigint(20) NOT NULL,
  `obj_id` varchar(32) NOT NULL,
  `key` varchar(255) NOT NULL COMMENT '类型（接单数，）',
  `value` int(11) NOT NULL DEFAULT '0',
  `version` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='通用计数';

-- ----------------------------
-- Records of counts
-- ----------------------------

-- ----------------------------
-- Table structure for faverite
-- ----------------------------
DROP TABLE IF EXISTS `faverite`;
CREATE TABLE `faverite` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `object_id` char(32) NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `is_valid` bit(1) NOT NULL DEFAULT b'1',
  `type` int(11) NOT NULL COMMENT '0, 收藏手艺人 1, 收藏样品',
  PRIMARY KEY (`id`),
  KEY `fk_user_id` (`user_id`),
  CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `account` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='收藏关系';

-- ----------------------------
-- Records of faverite
-- ----------------------------

-- ----------------------------
-- Table structure for gallery
-- ----------------------------
DROP TABLE IF EXISTS `gallery`;
CREATE TABLE `gallery` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `obj_id` varchar(255) NOT NULL,
  `url` varchar(500) NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='通用相册';

-- ----------------------------
-- Records of gallery
-- ----------------------------

-- ----------------------------
-- Table structure for login_token
-- ----------------------------
DROP TABLE IF EXISTS `login_token`;
CREATE TABLE `login_token` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(32) NOT NULL,
  `user_id` int(11) NOT NULL,
  `expire` bigint(20) NOT NULL,
  `last_login` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='登录令牌';

-- ----------------------------
-- Records of login_token
-- ----------------------------
INSERT INTO `login_token` VALUES ('1', 'c04ef209d3ed4e15b2554485f0650d0f', '1', '1422004202', '2014-12-24 17:10:01');

-- ----------------------------
-- Table structure for manager
-- ----------------------------
DROP TABLE IF EXISTS `manager`;
CREATE TABLE `manager` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Id',
  `name` varchar(16) NOT NULL,
  `password` varchar(48) NOT NULL,
  `role` varchar(255) NOT NULL COMMENT '角色',
  `last_login` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='管理员';

-- ----------------------------
-- Records of manager
-- ----------------------------
INSERT INTO `manager` VALUES ('1', 'admin', '7c4a8d09ca3762af61e59520943dc26494f8941b', 'ROLE_ADMIN', '2015-01-15 16:55:49');
INSERT INTO `manager` VALUES ('2', 'manager', '7c4a8d09ca3762af61e59520943dc26494f8941b', 'ROLE_MANAGER', '2015-01-15 16:55:52');

-- ----------------------------
-- Table structure for sample
-- ----------------------------
DROP TABLE IF EXISTS `sample`;
CREATE TABLE `sample` (
  `id` char(32) NOT NULL COMMENT 'uuid',
  `name` varchar(100) NOT NULL COMMENT '方案-名称',
  `price` float NOT NULL,
  `tag_price` float NOT NULL COMMENT '介绍',
  `sale` smallint(6) NOT NULL,
  `brief` varchar(1000) NOT NULL,
  `category_id` bigint(20) NOT NULL COMMENT '分类',
  `artisan_id` int(11) NOT NULL COMMENT '提供服务的手艺人',
  `status` bit(1) NOT NULL DEFAULT b'1',
  `tags` varchar(255) NOT NULL,
  `create_time` datetime NOT NULL,
  `version` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_category_id` (`category_id`),
  KEY `dj_atusab_id` (`artisan_id`),
  CONSTRAINT `dj_atusab_id` FOREIGN KEY (`artisan_id`) REFERENCES `artisan` (`id`),
  CONSTRAINT `fk_category_id` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='美甲师提供的作品方案';

-- ----------------------------
-- Records of sample
-- ----------------------------

-- ----------------------------
-- Table structure for tag
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '标签（圣诞节，日韩，纯色，新娘，法式，创意，彩绘，糖果）',
  `is_valid` bit(1) NOT NULL DEFAULT b'1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COMMENT='标签';

-- ----------------------------
-- Records of tag
-- ----------------------------
INSERT INTO `tag` VALUES ('1', '圣诞节', '');
INSERT INTO `tag` VALUES ('2', '特价款', '');
INSERT INTO `tag` VALUES ('3', '糖果 ', '');
INSERT INTO `tag` VALUES ('4', '创意 ', '');
INSERT INTO `tag` VALUES ('5', '彩绘 ', '');
INSERT INTO `tag` VALUES ('6', '日韩 ', '');
INSERT INTO `tag` VALUES ('7', '纯色 ', '');
INSERT INTO `tag` VALUES ('8', '新娘 ', '');
INSERT INTO `tag` VALUES ('9', '法式 ', '');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `mobile` varchar(16) NOT NULL,
  `password` varchar(48) NOT NULL,
  `nick` varchar(24) DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `reg_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='用户';

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('1', '13812345678', '7c4a8d09ca3762af61e59520943dc26494f8941b', '', '', '2014-12-24 17:02:44');
