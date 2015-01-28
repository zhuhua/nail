/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 50622
Source Host           : localhost:3306
Source Database       : nail

Target Server Type    : MYSQL
Target Server Version : 50622
File Encoding         : 65001

Date: 2015-01-25 21:48:50
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
  `gender` int(1) NOT NULL COMMENT '性别',
  `mobile` varchar(16) NOT NULL COMMENT '手机',
  `avatar` varchar(255) NOT NULL COMMENT '头像',
  `level` tinyint(4) NOT NULL DEFAULT '0' COMMENT '等级（0-15）',
  `brief` varchar(1000) NOT NULL COMMENT '自我介绍',
  `avg_price` float NOT NULL,
  `cert_pop` int(1) NOT NULL DEFAULT '0' COMMENT '明星美甲师认证',
  `cert_pro` int(1) NOT NULL DEFAULT '0' COMMENT '高级职业美甲师认证',
  `create_time` datetime NOT NULL,
  `last_login` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28000011 DEFAULT CHARSET=utf8 COMMENT='手艺人';

-- ----------------------------
-- Records of artisan
-- ----------------------------
INSERT INTO `artisan` VALUES ('28000001', 'shouyiren', '7c4a8d09ca3762af61e59520943dc26494f8941b', '1', 'ss', '/img/Grass.jpg', '1', '', '0', '0', '0', '2015-01-12 15:06:18', '2015-01-25 21:11:16');
INSERT INTO `artisan` VALUES ('28000002', 'shouyiren', '7c4a8d09ca3762af61e59520943dc26494f8941b', '1', 'ss', '', '1', '', '0', '0', '0', '2015-01-12 15:06:38', '2015-01-25 21:11:17');
INSERT INTO `artisan` VALUES ('28000003', 'shouyiren', '7c4a8d09ca3762af61e59520943dc26494f8941b', '1', 'ss', '', '1', '', '0', '0', '0', '2015-01-12 15:06:40', '2015-01-25 21:11:18');
INSERT INTO `artisan` VALUES ('28000004', 'shouyiren', '7c4a8d09ca3762af61e59520943dc26494f8941b', '1', 'ss', '', '1', '', '0', '0', '0', '2015-01-12 15:06:42', '2015-01-25 21:11:18');
INSERT INTO `artisan` VALUES ('28000005', '是的发生1111', '7c4a8d09ca3762af61e59520943dc26494f8941b', '1', 'ss', '/img/f2bd1421e1d66ccd4ef0ab6a155cdba1.png', '1', 'PIL 中的 Image 模块 - oyzway - 博客园\r\n本文是节选自 PIL handbook online 并做了一些简单的翻译只能保证自己看懂,不...Image 类中的函数。0. new : 这个函数创建一幅给定模式(mode)和尺寸(size)...\r\nwww.cnblogs.com/way_te... 2011-04-20  - 百度快照 - 91%好评', '0', '0', '0', '2015-01-12 15:06:44', '2015-01-16 15:17:43');
INSERT INTO `artisan` VALUES ('28000006', '美甲师111', '7c4a8d09ca3762af61e59520943dc26494f8941b', '1', 'ss', '/img/076e3caed758a1c18c91a0e9cae3368f.jpg', '1', '如果你看过电视里演的清代历史剧就不难注意到剧中的后妃、贵妇们的纤纤玉指，以及指尖的华贵甲饰。指尖一转，手指无不散发出尊贵、华丽的贵族气息。也许从那时起，中国的女人们就注定与美甲结下了不解之缘，也许从那时起，女人们就已通过指甲来展示自己的美丽与气质。时代在变迁，社会在发展，技术在革新，不变的是美，不变的是悠久的文化，艺术家们说：“民族的，就是世界的。”中国的美甲技术发展到今天，我们是否还应记得历史的沉积呢？中国的美甲应具有中国的民族特色，通过这款美甲的设计，用艺术的形式，寓识着美甲的历史发展，让我们还记得中国曾经有过的美甲辉煌，而我们这些现代的美甲师更有理由把历史与民族特点融入艺术创作中。', '0', '0', '0', '2015-01-12 15:06:46', '2015-01-25 15:57:06');
INSERT INTO `artisan` VALUES ('28000007', 'shouyiren', '7c4a8d09ca3762af61e59520943dc26494f8941b', '1', 'ss', '', '1', '', '0', '0', '0', '2015-01-12 15:06:48', '2015-01-25 21:11:19');
INSERT INTO `artisan` VALUES ('28000008', 'shouyiren', '7c4a8d09ca3762af61e59520943dc26494f8941b', '1', 'ss', '', '1', '', '0', '0', '0', '2015-01-12 15:06:50', '2015-01-25 21:11:20');
INSERT INTO `artisan` VALUES ('28000009', '哈哈哈哈', '7c4a8d09ca3762af61e59520943dc26494f8941b', '1', '12345678', '', '1', '阿斯顿发生的发生打法', '0', '0', '0', '2015-01-12 17:06:22', '2015-01-25 21:11:20');
INSERT INTO `artisan` VALUES ('28000010', '阿斯顿发', '7c4a8d09ca3762af61e59520943dc26494f8941b', '1', '111111111111', '', '1', '爱上发生地方', '0', '0', '0', '2015-01-13 15:51:36', '2015-01-25 21:11:21');

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
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8 COMMENT='通用相册';

-- ----------------------------
-- Records of gallery
-- ----------------------------
INSERT INTO `gallery` VALUES ('23', 'dfe3a334fc99f298ac5a6673baa44184', '{\'url\': u\'/img/243f6827fe80944b6bb26e80e175c713.jpg\', \'create_time\': datetime.datetime(2015, 1, 21, 16, 8), \'id\': 1L, \'obj_id\': u\'dfe3a334fc99f298ac5a6673baa44184\'}', '2015-01-25 18:30:57');
INSERT INTO `gallery` VALUES ('24', '048a9df698dad13008d8ce3b2caa522f', '{\'url\': u\'/img/243f6827fe80944b6bb26e80e175c713.jpg\', \'create_time\': datetime.datetime(2015, 1, 22, 16, 47, 39), \'id\': 2L, \'obj_id\': u\'048a9df698dad13008d8ce3b2caa522f\'}', '2015-01-25 18:30:58');
INSERT INTO `gallery` VALUES ('25', '048a9df698dad13008d8ce3b2caa522f', '{\'url\': u\'/img/331838f47ff496ad525f38fc92785418.jpg\', \'create_time\': datetime.datetime(2015, 1, 22, 16, 47, 39), \'id\': 3L, \'obj_id\': u\'048a9df698dad13008d8ce3b2caa522f\'}', '2015-01-25 18:30:58');
INSERT INTO `gallery` VALUES ('26', '28efd832ac6f3fa5632f9776f5b3a637', '{\'url\': u\'/img/395fe57d7ee19290c7278b8c9c812cfe.jpg\', \'create_time\': datetime.datetime(2015, 1, 22, 16, 48, 50), \'id\': 4L, \'obj_id\': u\'28efd832ac6f3fa5632f9776f5b3a637\'}', '2015-01-25 18:30:58');
INSERT INTO `gallery` VALUES ('27', '28efd832ac6f3fa5632f9776f5b3a637', '{\'url\': u\'/img/ba87212acda512687138c941243e34e7.jpg\', \'create_time\': datetime.datetime(2015, 1, 22, 16, 48, 50), \'id\': 5L, \'obj_id\': u\'28efd832ac6f3fa5632f9776f5b3a637\'}', '2015-01-25 18:30:58');
INSERT INTO `gallery` VALUES ('28', '38887226972d8bef088a3ff945156403', '{\'url\': u\'/img/243f6827fe80944b6bb26e80e175c713.jpg\', \'create_time\': datetime.datetime(2015, 1, 23, 15, 27, 29), \'id\': 6L, \'obj_id\': u\'38887226972d8bef088a3ff945156403\'}', '2015-01-25 18:30:59');
INSERT INTO `gallery` VALUES ('29', '204f8ab57160c2deb4edb6e9371c01c4', '{\'url\': u\'/img/243f6827fe80944b6bb26e80e175c713.jpg\', \'create_time\': datetime.datetime(2015, 1, 23, 15, 28, 29), \'id\': 7L, \'obj_id\': u\'204f8ab57160c2deb4edb6e9371c01c4\'}', '2015-01-25 18:31:00');
INSERT INTO `gallery` VALUES ('30', '4a67697dc84f5e00efe1dcc046b6d13a', '{\'url\': u\'/img/331838f47ff496ad525f38fc92785418.jpg\', \'create_time\': datetime.datetime(2015, 1, 23, 15, 29, 19), \'id\': 8L, \'obj_id\': u\'4a67697dc84f5e00efe1dcc046b6d13a\'}', '2015-01-25 18:31:00');
INSERT INTO `gallery` VALUES ('31', 'cd49ded9694182bc2c8979fa1c7efd45', '{\'url\': u\'/img/174509341416b35b7cf23cf41b04906c.jpg\', \'create_time\': datetime.datetime(2015, 1, 23, 15, 32, 45), \'id\': 9L, \'obj_id\': u\'cd49ded9694182bc2c8979fa1c7efd45\'}', '2015-01-25 18:31:01');
INSERT INTO `gallery` VALUES ('32', '27adab09faa51aa50318851a1fc79766', '{\'url\': u\'/img/174509341416b35b7cf23cf41b04906c.jpg\', \'create_time\': datetime.datetime(2015, 1, 23, 15, 34, 39), \'id\': 10L, \'obj_id\': u\'27adab09faa51aa50318851a1fc79766\'}', '2015-01-25 18:31:01');
INSERT INTO `gallery` VALUES ('33', '5672e2c1d6b250baa86d8ce13919ff62', '{\'url\': u\'/img/331838f47ff496ad525f38fc92785418.jpg\', \'create_time\': datetime.datetime(2015, 1, 23, 15, 43, 53), \'id\': 11L, \'obj_id\': u\'5672e2c1d6b250baa86d8ce13919ff62\'}', '2015-01-25 18:31:01');
INSERT INTO `gallery` VALUES ('34', '42d551493a322a905f48eed726aade42', '{\'url\': u\'/img/331838f47ff496ad525f38fc92785418.jpg\', \'create_time\': datetime.datetime(2015, 1, 23, 15, 46, 37), \'id\': 12L, \'obj_id\': u\'42d551493a322a905f48eed726aade42\'}', '2015-01-25 18:31:02');
INSERT INTO `gallery` VALUES ('35', '283135d31b95ca326d5b5663485477a2', '{\'url\': u\'/img/395fe57d7ee19290c7278b8c9c812cfe.jpg\', \'create_time\': datetime.datetime(2015, 1, 23, 16, 5, 47), \'id\': 13L, \'obj_id\': u\'283135d31b95ca326d5b5663485477a2\'}', '2015-01-25 18:31:04');
INSERT INTO `gallery` VALUES ('36', '73a1661909d353a12b88b3c05ebb2296', '{\'url\': u\'/img/0842094a35a38fd2d1eeac7f7c19dbea.jpg\', \'create_time\': datetime.datetime(2015, 1, 23, 16, 7, 23), \'id\': 14L, \'obj_id\': u\'73a1661909d353a12b88b3c05ebb2296\'}', '2015-01-25 18:31:04');
INSERT INTO `gallery` VALUES ('37', 'cacef149c2916f2bcab42d727db25fbe', '{\'url\': u\'/img/0842094a35a38fd2d1eeac7f7c19dbea.jpg\', \'create_time\': datetime.datetime(2015, 1, 23, 16, 8, 20), \'id\': 15L, \'obj_id\': u\'cacef149c2916f2bcab42d727db25fbe\'}', '2015-01-25 18:31:05');
INSERT INTO `gallery` VALUES ('38', 'eed4111e465e4ea40f2d7919ce4f703d', '{\'url\': u\'/img/243f6827fe80944b6bb26e80e175c713.jpg\', \'create_time\': datetime.datetime(2015, 1, 23, 16, 9, 8), \'id\': 16L, \'obj_id\': u\'eed4111e465e4ea40f2d7919ce4f703d\'}', '2015-01-25 18:31:05');
INSERT INTO `gallery` VALUES ('39', '0428f180a256d6492558573464fed2fe', '{\'url\': u\'/img/243f6827fe80944b6bb26e80e175c713.jpg\', \'create_time\': datetime.datetime(2015, 1, 23, 16, 15, 2), \'id\': 17L, \'obj_id\': u\'0428f180a256d6492558573464fed2fe\'}', '2015-01-25 18:31:06');
INSERT INTO `gallery` VALUES ('40', 'ca0570344654cfbc36eae8d7361abe37', '{\'url\': u\'/img/243f6827fe80944b6bb26e80e175c713.jpg\', \'create_time\': datetime.datetime(2015, 1, 23, 16, 19, 32), \'id\': 18L, \'obj_id\': u\'ca0570344654cfbc36eae8d7361abe37\'}', '2015-01-25 18:31:06');
INSERT INTO `gallery` VALUES ('41', '786281595ff7175603b5dd78681c6f02', '{\'url\': u\'/img/331838f47ff496ad525f38fc92785418.jpg\', \'create_time\': datetime.datetime(2015, 1, 23, 16, 24, 17), \'id\': 19L, \'obj_id\': u\'786281595ff7175603b5dd78681c6f02\'}', '2015-01-25 18:31:07');
INSERT INTO `gallery` VALUES ('42', 'f1f57fc2a5c4804866c527dac5f802d2', '{\'url\': u\'/img/ba87212acda512687138c941243e34e7.jpg\', \'create_time\': datetime.datetime(2015, 1, 23, 16, 25, 31), \'id\': 20L, \'obj_id\': u\'f1f57fc2a5c4804866c527dac5f802d2\'}', '2015-01-25 18:31:07');
INSERT INTO `gallery` VALUES ('43', '9a69d808dbcb2a09850c3d88c2a36446', '{\'url\': u\'/img/243f6827fe80944b6bb26e80e175c713.jpg\', \'create_time\': datetime.datetime(2015, 1, 23, 16, 26, 20), \'id\': 21L, \'obj_id\': u\'9a69d808dbcb2a09850c3d88c2a36446\'}', '2015-01-25 18:31:08');
INSERT INTO `gallery` VALUES ('44', 'cba901536d2a07b4b5fe329aff2b9841', '{\'url\': u\'/img/243f6827fe80944b6bb26e80e175c713.jpg\', \'create_time\': datetime.datetime(2015, 1, 23, 18, 1, 23), \'id\': 22L, \'obj_id\': u\'cba901536d2a07b4b5fe329aff2b9841\'}', '2015-01-25 18:31:08');

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
INSERT INTO `login_token` VALUES ('1', '9dec494eeea44bf19a7b8e187b2b36ac', '1', '1424784039', '2015-01-25 21:20:39');

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
INSERT INTO `manager` VALUES ('1', 'admin', '7c4a8d09ca3762af61e59520943dc26494f8941b', 'ROLE_ADMIN', '2015-01-22 17:21:30');
INSERT INTO `manager` VALUES ('2', 'manager', '7c4a8d09ca3762af61e59520943dc26494f8941b', 'ROLE_MANAGER', '2015-01-15 16:55:52');

-- ----------------------------
-- Table structure for sample
-- ----------------------------
DROP TABLE IF EXISTS `sample`;
CREATE TABLE `sample` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'uuid',
  `name` varchar(100) NOT NULL COMMENT '方案-名称',
  `price` float NOT NULL,
  `tag_price` float NOT NULL COMMENT '介绍',
  `sale` smallint(6) NOT NULL,
  `brief` varchar(1000) NOT NULL,
  `category_id` bigint(20) NOT NULL COMMENT '分类',
  `artisan_id` int(11) NOT NULL COMMENT '提供服务的手艺人',
  `status` int(1) NOT NULL DEFAULT '1',
  `tags` varchar(255) NOT NULL,
  `create_time` datetime NOT NULL,
  `version` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_category_id` (`category_id`),
  KEY `dj_atusab_id` (`artisan_id`),
  CONSTRAINT `dj_atusab_id` FOREIGN KEY (`artisan_id`) REFERENCES `artisan` (`id`),
  CONSTRAINT `fk_category_id` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8 COMMENT='美甲师提供的作品方案';

-- ----------------------------
-- Records of sample
-- ----------------------------
INSERT INTO `sample` VALUES ('3', '但是发生', '111', '1111', '0', '阿斯顿发生地方', '1', '28000006', '0', '啊士大夫 啊士大夫', '2015-01-21 16:08:00', '2015-01-21 16:08:00');
INSERT INTO `sample` VALUES ('5', '阿斯顿发', '111', '1111', '0', '阿斯顿发生的发生打法', '1', '28000006', '0', '彩 绘', '2015-01-22 16:47:39', '2015-01-22 16:47:39');
INSERT INTO `sample` VALUES ('6', '啊发生的', '11', '111', '0', '阿斯顿发生的发生的', '1', '28000006', '0', '圣诞节 特价款 糖果 创意 彩绘', '2015-01-22 16:48:50', '2015-01-22 16:48:50');
INSERT INTO `sample` VALUES ('7', 'adfads', '1111', '11', '0', 'asdf', '1', '28000006', '0', '圣诞节 特价款 糖果 创意 彩绘 日韩 纯色 新娘 法式', '2015-01-23 15:27:29', '2015-01-23 15:27:29');
INSERT INTO `sample` VALUES ('8', 'adfads', '1111', '11', '0', 'asdf', '1', '28000006', '0', '圣诞节 特价款 糖果 创意 彩绘 日韩 纯色 新娘 法式', '2015-01-23 15:28:29', '2015-01-23 15:28:29');
INSERT INTO `sample` VALUES ('9', 'adfads', '1111', '11', '0', 'asdf', '1', '28000006', '0', '圣诞节 特价款 糖果 创意 彩绘 日韩 纯色 新娘 法式', '2015-01-23 15:29:19', '2015-01-23 15:29:19');
INSERT INTO `sample` VALUES ('10', 'adfads', '1111', '11', '0', 'asdf', '1', '28000006', '0', '圣诞节 特价款 糖果 创意 彩绘 日韩 纯色 新娘 法式', '2015-01-23 15:32:45', '2015-01-23 15:32:45');
INSERT INTO `sample` VALUES ('11', 'adfads', '1111', '11', '0', 'asdf', '1', '28000006', '0', '圣诞节 特价款 糖果 创意 彩绘 日韩 纯色 新娘 法式', '2015-01-23 15:34:39', '2015-01-23 15:34:39');
INSERT INTO `sample` VALUES ('12', 'adfads', '1111', '11', '0', 'asdf', '1', '28000006', '0', '圣诞节 特价款 糖果 创意 彩绘 日韩 纯色 新娘 法式', '2015-01-23 15:43:53', '2015-01-23 15:43:53');
INSERT INTO `sample` VALUES ('13', 'adfads', '1111', '11', '0', 'asdf', '1', '28000006', '0', '圣诞节 特价款 糖果 创意 彩绘 日韩 纯色 新娘 法式', '2015-01-23 15:46:37', '2015-01-23 15:46:37');
INSERT INTO `sample` VALUES ('14', 'adfads', '1111', '11', '0', 'asdf', '1', '28000006', '0', '圣诞节 特价款 糖果 创意 彩绘 日韩 纯色 新娘 法式', '2015-01-23 16:05:47', '2015-01-23 16:05:47');
INSERT INTO `sample` VALUES ('15', 'adfads', '1111', '11', '0', 'asdf', '1', '28000006', '0', '圣诞节 特价款 糖果 创意 彩绘 日韩 纯色 新娘 法式', '2015-01-23 16:07:23', '2015-01-23 16:07:23');
INSERT INTO `sample` VALUES ('16', 'adfads', '1111', '11', '0', 'asdf', '1', '28000006', '0', '圣诞节 特价款 糖果 创意 彩绘 日韩 纯色 新娘 法式', '2015-01-23 16:08:20', '2015-01-23 16:08:20');
INSERT INTO `sample` VALUES ('17', 'adfads', '1111', '11', '0', 'asdf', '1', '28000006', '0', '圣诞节 特价款 糖果 创意 彩绘 日韩 纯色 新娘 法式', '2015-01-23 16:09:08', '2015-01-23 16:09:08');
INSERT INTO `sample` VALUES ('18', 'adfads', '1111', '11', '0', 'asdf', '1', '28000006', '0', '圣诞节 特价款 糖果 创意 彩绘 日韩 纯色 新娘 法式', '2015-01-23 16:15:02', '2015-01-23 16:15:02');
INSERT INTO `sample` VALUES ('19', 'adfads', '1111', '11', '0', 'asdf', '1', '28000006', '0', '圣诞节 特价款 糖果 创意 彩绘 日韩 纯色 新娘 法式', '2015-01-23 16:19:32', '2015-01-23 16:19:32');
INSERT INTO `sample` VALUES ('20', '哈哈哈哈', '1111', '11', '0', 'asdf', '1', '28000006', '0', '圣诞节 特价款 糖果 创意 彩绘 日韩 纯色 新娘 法式', '2015-01-23 16:24:17', '2015-01-23 16:24:17');
INSERT INTO `sample` VALUES ('21', '在在重中之重', '1111', '11', '0', 'asdf', '1', '28000006', '0', '圣诞节 特价款 糖果 创意 彩绘 日韩 纯色 新娘 法式', '2015-01-23 16:25:31', '2015-01-23 16:25:31');
INSERT INTO `sample` VALUES ('22', '在在', '1111', '11', '0', 'asdf', '1', '28000006', '0', '圣诞节 特价款 糖果 创意 彩绘 日韩 纯色 新娘 法式', '2015-01-23 16:26:20', '2015-01-23 16:26:20');
INSERT INTO `sample` VALUES ('23', '阿斯顿发', '199', '299', '0', '阿斯顿发生的', '1', '28000006', '0', '圣诞节 特价款 糖果 创意 彩绘 日韩 纯色 新娘 法式', '2015-01-23 18:01:23', '2015-01-23 18:01:23');

-- ----------------------------
-- Table structure for tag
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '标签（圣诞节，日韩，纯色，新娘，法式，创意，彩绘，糖果）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COMMENT='标签';

-- ----------------------------
-- Records of tag
-- ----------------------------
INSERT INTO `tag` VALUES ('1', '圣诞节');
INSERT INTO `tag` VALUES ('2', '特价款');
INSERT INTO `tag` VALUES ('3', '糖果 ');
INSERT INTO `tag` VALUES ('4', '创意 ');
INSERT INTO `tag` VALUES ('5', '彩绘 ');
INSERT INTO `tag` VALUES ('6', '日韩 ');
INSERT INTO `tag` VALUES ('7', '纯色 ');
INSERT INTO `tag` VALUES ('8', '新娘 ');
INSERT INTO `tag` VALUES ('9', '法式 ');

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

-- ----------------------------
-- Table structure for order
-- ----------------------------
DROP TABLE IF EXISTS `order`;
CREATE TABLE `order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL COMMENT '购卖者ID',
  `buyer_name` varchar(255) NOT NULL COMMENT '买家姓名',
  `address` varchar(1000) NOT NULL COMMENT '买家地址',
  `telephone` varchar(21) NOT NULL COMMENT '买家电话',
  `title` varchar(255) NOT NULL COMMENT '订单名称',
  `order_no` varchar(64) NOT NULL COMMENT '订单号',
  `trade_no` varchar(64) NOT NULL COMMENT '交易号',
  `status` int(11) NOT NULL COMMENT '订单状态（）',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `display_buyer` tinyint(4) NOT NULL COMMENT '显示给买家（买家未删除）',
  `display_seller` tinyint(4) NOT NULL COMMENT '显示给卖家（卖家未删除）',
  `is_reviewed` tinyint(4) NOT NULL COMMENT '订单是否被评价',
  `artisan_id` int(11) NOT NULL COMMENT '手艺人ID',
  `artisan_name` varchar(255) NOT NULL COMMENT '手艺人名称',
  `sample_id` int(11) NOT NULL COMMENT '样品',
  `sample_name` varchar(255) NOT NULL COMMENT '样品名称',
  `cover` varchar(255) NOT NULL COMMENT '订单图片',
  `tag_price` float NOT NULL COMMENT '店面价',
  `price` float NOT NULL COMMENT '价格',
  PRIMARY KEY (`id`),
  KEY `fk_order_artisan_id` (`artisan_id`),
  KEY `fk_order_user_id` (`user_id`),
  KEY `fk_order_sample_id` (`sample_id`),
  CONSTRAINT `fk_order_artisan_id` FOREIGN KEY (`artisan_id`) REFERENCES `artisan` (`id`),
  CONSTRAINT `fk_order_sample_id` FOREIGN KEY (`sample_id`) REFERENCES `sample` (`id`),
  CONSTRAINT `fk_order_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='订单';

-- ----------------------------
-- Table structure for appointment
-- ----------------------------
DROP TABLE IF EXISTS `appointment`;
CREATE TABLE `appointment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `artisan_id` int(11) NOT NULL COMMENT '手艺人ID',
  `sample_id` int(11) DEFAULT NULL COMMENT '样品ID',
  `user_id` int(11) DEFAULT NULL COMMENT '预约发起人',
  `appt_date` date NOT NULL COMMENT '预约日期',
  `appt_hour` int(11) NOT NULL COMMENT '预约时间 ',
  `order_no` varchar(64) DEFAULT NULL COMMENT '预约订单号',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `artisan_id` (`artisan_id`,`appt_date`,`appt_hour`),
  KEY `fk_appointment_sample_id` (`sample_id`),
  KEY `fk_appointment_user_id` (`user_id`),
  CONSTRAINT `fk_appointment_artisan_id` FOREIGN KEY (`artisan_id`) REFERENCES `artisan` (`id`),
  CONSTRAINT `fk_appointment_sample_id` FOREIGN KEY (`sample_id`) REFERENCES `sample` (`id`),
  CONSTRAINT `fk_appointment_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='手艺人预约情况';

-- ----------------------------
-- Table structure for order_log
-- ----------------------------
DROP TABLE IF EXISTS `order_log`;
CREATE TABLE `order_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `trader_id` int(11) NOT NULL,
  `trader_type` varchar(255) NOT NULL,
  `action` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_order_log_order_id` (`order_id`),
  CONSTRAINT `fk_order_log_order_id` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='订单流转日志';