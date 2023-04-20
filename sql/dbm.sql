/*
 Navicat Premium Data Transfer

 Source Server         : python_crawl
 Source Server Type    : MySQL
 Source Server Version : 80027
 Source Host           : localhost:3306
 Source Schema         : dbm

 Target Server Type    : MySQL
 Target Server Version : 80027
 File Encoding         : 65001

 Date: 21/04/2023 00:18:47
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for china_tourism_data
-- ----------------------------
DROP TABLE IF EXISTS `china_tourism_data`;
CREATE TABLE `china_tourism_data`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `2022` float NULL DEFAULT NULL,
  `2021` float NULL DEFAULT NULL,
  `2020` float NULL DEFAULT NULL,
  `2019` float NULL DEFAULT NULL,
  `2018` float NULL DEFAULT NULL,
  `2017` float NULL DEFAULT NULL,
  `2016` float NULL DEFAULT NULL,
  `2015` float NULL DEFAULT NULL,
  `2014` float NULL DEFAULT NULL,
  `2013` float NULL DEFAULT NULL,
  `2012` float NULL DEFAULT NULL,
  `2011` float NULL DEFAULT NULL,
  `2010` float NULL DEFAULT NULL,
  `2009` float NULL DEFAULT NULL,
  `2008` float NULL DEFAULT NULL,
  `2007` float NULL DEFAULT NULL,
  `2006` float NULL DEFAULT NULL,
  `2005` float NULL DEFAULT NULL,
  `2004` float NULL DEFAULT NULL,
  `2003` float NULL DEFAULT NULL,
  `2002` float NULL DEFAULT NULL,
  `2001` float NULL DEFAULT NULL,
  `2000` float NULL DEFAULT NULL,
  `1999` float NULL DEFAULT NULL,
  `1998` float NULL DEFAULT NULL,
  `1997` float NULL DEFAULT NULL,
  `1996` float NULL DEFAULT NULL,
  `1995` float NULL DEFAULT NULL,
  `1994` float NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for comments
-- ----------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments`  (
  `id` int(0) UNSIGNED NOT NULL AUTO_INCREMENT,
  `sid` int(0) NULL DEFAULT NULL,
  `dpId` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `page` int(0) NULL DEFAULT NULL,
  `comment_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `comment_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `comment_stat` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `comment_cotent` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `reply_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `sid`(`sid`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 2068911 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for traffic_congestion_index
-- ----------------------------
DROP TABLE IF EXISTS `traffic_congestion_index`;
CREATE TABLE `traffic_congestion_index`  (
  `id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `time` datetime(0) NULL DEFAULT NULL,
  `code` int(0) NULL DEFAULT NULL,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `typyid` int(0) NULL DEFAULT NULL,
  `data` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `code`(`code`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for traffic_district_rank
-- ----------------------------
DROP TABLE IF EXISTS `traffic_district_rank`;
CREATE TABLE `traffic_district_rank`  (
  `id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `time` datetime(0) NULL DEFAULT NULL,
  `code` int(0) NULL DEFAULT NULL,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `typyid` int(0) NULL DEFAULT NULL,
  `data` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `code`(`code`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for traffic_roadrank_rank
-- ----------------------------
DROP TABLE IF EXISTS `traffic_roadrank_rank`;
CREATE TABLE `traffic_roadrank_rank`  (
  `id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `time` datetime(0) NULL DEFAULT NULL,
  `code` int(0) NULL DEFAULT NULL,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `typyid` int(0) NULL DEFAULT NULL,
  `data` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `code`(`code`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for travel
-- ----------------------------
DROP TABLE IF EXISTS `travel`;
CREATE TABLE `travel`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `sid` int(0) NULL DEFAULT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `detail_link` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `main_img` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `level` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `feature` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `price` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `full_address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `open_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `video` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `images` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `degreeLevel` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `totalNum` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `goodNum` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `midNum` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `badNum` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `hasImgNum` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `starNum` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `serviceScoreAvgList` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `contents` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `sid`(`sid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11896 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
