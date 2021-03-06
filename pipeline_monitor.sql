/*
Navicat MySQL Data Transfer

Source Server         : 10.0.7.68
Source Server Version : 50733
Source Host           : 10.0.7.68:3306
Source Database       : pipeline_monitor

Target Server Type    : MYSQL
Target Server Version : 50733
File Encoding         : 65001

Date: 2021-12-09 15:20:56
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `is_super` smallint(6) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `role_id` (`role_id`),
  KEY `ix_admin_add_time` (`add_time`),
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES ('1', 'admin', 'pbkdf2:sha256:150000$zDRyYrYG$6611d78b248957770aeb01e4188819644b1396d5b5ccf5cfc56e54306b457873', '0', '1', '2021-09-09 16:55:45');
INSERT INTO `admin` VALUES ('2', 'test', 'pbkdf2:sha256:50000$DjnMBDoo$6750e0fb05a5f81db381a1d1ca5f82c21f1474f90e9c5c45e0dfbd072ebd29a5', '1', '2', '2021-09-10 10:33:09');

-- ----------------------------
-- Table structure for adminlog
-- ----------------------------
DROP TABLE IF EXISTS `adminlog`;
CREATE TABLE `adminlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_adminlog_add_time` (`add_time`),
  CONSTRAINT `adminlog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of adminlog
-- ----------------------------

-- ----------------------------
-- Table structure for auth
-- ----------------------------
DROP TABLE IF EXISTS `auth`;
CREATE TABLE `auth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `url` (`url`),
  KEY `ix_auth_add_time` (`add_time`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth
-- ----------------------------
INSERT INTO `auth` VALUES ('1', '??????', '/admin/', '2021-09-10 10:36:45');
INSERT INTO `auth` VALUES ('2', '????????????????????????', '/admin/logs/user_log/', '2021-09-10 10:40:41');
INSERT INTO `auth` VALUES ('3', '????????????', '/admin/video/add/', '2021-09-10 11:15:09');
INSERT INTO `auth` VALUES ('4', '????????????', '/admin/video/list/<int:page>/', '2021-09-10 11:15:37');
INSERT INTO `auth` VALUES ('5', '??????????????????', '/admin/logs/operate_log/', '2021-09-10 11:16:17');
INSERT INTO `auth` VALUES ('6', '???????????????????????????', '/admin/logs/admin_log/', '2021-09-10 11:16:53');
INSERT INTO `auth` VALUES ('7', '????????????', '/admin/auth/add/', '2021-09-10 11:17:12');
INSERT INTO `auth` VALUES ('8', '????????????', '/admin/auth/list/<int:page>/', '2021-09-10 11:17:35');
INSERT INTO `auth` VALUES ('9', '????????????', '/admin/role/add/', '2021-09-10 11:18:26');
INSERT INTO `auth` VALUES ('10', '????????????', '/admin/role/list/<int:page>/', '2021-09-10 11:18:47');
INSERT INTO `auth` VALUES ('11', '????????????', '/admin/video/update/<int:update_id>/', '2021-09-10 13:42:23');
INSERT INTO `auth` VALUES ('12', '????????????', '/admin/role/update/<int:update_id>/', '2021-09-10 13:43:02');
INSERT INTO `auth` VALUES ('13', '????????????', '/admin/tag/add/', '2021-09-10 13:44:21');
INSERT INTO `auth` VALUES ('14', '????????????', '/admin/tag/list/<int:page>/', '2021-09-10 13:44:40');
INSERT INTO `auth` VALUES ('15', '????????????', '/admin/tag/update/<int:update_id>/', '2021-09-10 13:45:18');
INSERT INTO `auth` VALUES ('16', '???????????????', '/admin/admin/add/', '2021-09-10 14:43:08');
INSERT INTO `auth` VALUES ('17', '????????????', '/admin/auth/update/<int:update_id>/', '2021-09-10 15:53:20');
INSERT INTO `auth` VALUES ('18', '????????????', '/admin/video/delete/<int:delete_id>/', '2021-09-13 09:38:24');

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text,
  `video_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `movie_id` (`video_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_comment_add_time` (`add_time`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`video_id`) REFERENCES `video` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of comment
-- ----------------------------

-- ----------------------------
-- Table structure for operatelog
-- ----------------------------
DROP TABLE IF EXISTS `operatelog`;
CREATE TABLE `operatelog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `reason` varchar(600) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_operatelog_add_time` (`add_time`),
  CONSTRAINT `operatelog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of operatelog
-- ----------------------------

-- ----------------------------
-- Table structure for preview
-- ----------------------------
DROP TABLE IF EXISTS `preview`;
CREATE TABLE `preview` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `logo` (`logo`),
  KEY `ix_preview_add_time` (`add_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of preview
-- ----------------------------

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `auths` varchar(600) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_role_add_time` (`add_time`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES ('1', '???????????????', '', '2021-09-09 16:55:45');
INSERT INTO `role` VALUES ('2', '???????????????', '1,2,3,4,5,6,11,13,14,15', '2021-09-10 10:32:16');

-- ----------------------------
-- Table structure for tag
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_tag_add_time` (`add_time`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of tag
-- ----------------------------
INSERT INTO `tag` VALUES ('1', '??????', '2021-09-10 11:33:18');
INSERT INTO `tag` VALUES ('2', '??????', '2021-09-10 11:33:42');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `info` text,
  `face` varchar(255) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  `uuid` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `face` (`face`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_user_add_time` (`add_time`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'test', '123456', 'test@126.com', '13655667890', null, null, '2021-09-09 17:19:51', null);

-- ----------------------------
-- Table structure for userlog
-- ----------------------------
DROP TABLE IF EXISTS `userlog`;
CREATE TABLE `userlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_userlog_add_time` (`add_time`),
  CONSTRAINT `userlog_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of userlog
-- ----------------------------

-- ----------------------------
-- Table structure for video
-- ----------------------------
DROP TABLE IF EXISTS `video`;
CREATE TABLE `video` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL COMMENT '????????????',
  `url` varchar(255) DEFAULT NULL COMMENT '????????????????????????',
  `info` text COMMENT '????????????',
  `logo` varchar(255) DEFAULT NULL COMMENT 'logo',
  `star` smallint(6) DEFAULT NULL COMMENT '????????????',
  `play_num` bigint(20) DEFAULT NULL,
  `comment_num` bigint(20) DEFAULT NULL,
  `tag_id` int(11) DEFAULT NULL,
  `area` varchar(255) DEFAULT NULL,
  `release_time` date DEFAULT NULL,
  `length` varchar(100) DEFAULT NULL COMMENT '????????????',
  `add_time` datetime DEFAULT NULL COMMENT '??????????????????',
  `is_detect` char(1) NOT NULL DEFAULT '0' COMMENT '???????????????????????????0???????????????1????????????',
  `save_path` varchar(255) DEFAULT NULL COMMENT '????????????????????????',
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `url` (`url`),
  UNIQUE KEY `logo` (`logo`),
  UNIQUE KEY `save_path` (`save_path`),
  KEY `tag_id` (`tag_id`),
  KEY `ix_movie_add_time` (`add_time`),
  CONSTRAINT `video_ibfk_1` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of video
-- ----------------------------
INSERT INTO `video` VALUES ('1', '??????????????????????????????', '4f37d2361b09462986941bb2b510692c.mp4', 'test', '20210910170417c4cf4703a97142f48023814acd6f0294.jpg', '1', '0', '0', '2', '??????????????????????????????88???', '2021-09-24', '10', '2021-09-10 11:35:07', '0', null);
INSERT INTO `video` VALUES ('17', 'hello', '7a07728a56684438b06d327cdbb98e7b.mp4', 'd', 'cdf2959209a94ccfa9a97554ab39d04d.png', '1', '0', '0', '2', '??????', '2021-10-03', '2', '2021-09-13 17:13:53', '0', null);
INSERT INTO `video` VALUES ('18', '?????????12#??????', '2021-09-27/xxyyzz/81740a247729471186ea17d37cd17397.mp4', 'aaa', '086581cb74144c819eabcad599cc7028.jpg', '3', '0', '0', '1', '????????????', '2021-09-26', '3', '2021-09-27 11:12:11', '0', 'results\\81740a247729471186ea17d37cd17397');
