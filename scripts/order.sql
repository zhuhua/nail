/*
Navicat MySQL Data Transfer

Source Server         : db_maria
Source Server Version : 50540
Source Host           : localhost:3306
Source Database       : nail

Target Server Type    : MYSQL
Target Server Version : 50540
File Encoding         : 65001

Date: 2015-01-27 18:06:59
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for order
-- ----------------------------
DROP TABLE IF EXISTS `order`;
CREATE TABLE `order` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL COMMENT '购卖者ID',
  `buyer_name` varchar(255) NOT NULL,
  `address` varchar(1000) NOT NULL,
  `telephone` varchar(21) NOT NULL,
  `title` varchar(255) NOT NULL,
  `order_no` varchar(64) NOT NULL,
  `trade_no` varchar(64) NOT NULL,
  `status` int(11) NOT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `display_buyer` tinyint(4) NOT NULL,
  `display_seller` tinyint(4) NOT NULL,
  `is_reviewed` tinyint(4) NOT NULL,
  `artisan_id` int(11) NOT NULL,
  `artisan_name` varchar(255) NOT NULL,
  `sample_id` int(11) NOT NULL,
  `sample_name` varchar(255) NOT NULL,
  `cover` varchar(255) NOT NULL,
  `tag_price` float NOT NULL,
  `price` float NOT NULL,
  `date` date NOT NULL,
  `hour` int(11) NOT NULL COMMENT ' 预约时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `artisan_id` (`artisan_id`,`date`,`hour`),
  KEY `fk_order_artisan_id` (`artisan_id`),
  KEY `fk_order_user_id` (`user_id`),
  KEY `fk_order_sample_id` (`sample_id`),
  CONSTRAINT `fk_order_artisan_id` FOREIGN KEY (`artisan_id`) REFERENCES `artisan` (`id`),
  CONSTRAINT `fk_order_sample_id` FOREIGN KEY (`sample_id`) REFERENCES `sample` (`id`),
  CONSTRAINT `fk_order_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='订单';
