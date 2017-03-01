/*
Navicat MySQL Data Transfer

Source Server         : 12
Source Server Version : 50711
Source Host           : 192.168.11.110:3306
Source Database       : inventer

Target Server Type    : MYSQL
Target Server Version : 50711
File Encoding         : 65001

Date: 2017-03-01 14:04:19
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for minutes
-- ----------------------------
DROP TABLE IF EXISTS `minutes`;
CREATE TABLE `minutes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `InvID` varchar(16) NOT NULL,
  `ETotal` decimal(7,1) NOT NULL DEFAULT '-1.0',
  `EToday` decimal(4,2) NOT NULL DEFAULT '-1.00',
  `Temp` decimal(4,1) NOT NULL DEFAULT '-1.0',
  `HTotal` int(8) NOT NULL DEFAULT '-1',
  `VPV1` decimal(4,1) NOT NULL DEFAULT '-1.0',
  `VPV2` decimal(4,1) NOT NULL DEFAULT '-1.0',
  `VPV3` decimal(4,1) NOT NULL DEFAULT '-1.0',
  `IPV1` decimal(3,1) NOT NULL DEFAULT '-1.0',
  `IPV2` decimal(3,1) NOT NULL DEFAULT '-1.0',
  `IPV3` decimal(3,1) NOT NULL DEFAULT '-1.0',
  `VAC1` decimal(4,1) NOT NULL DEFAULT '-1.0',
  `VAC2` decimal(4,1) NOT NULL DEFAULT '-1.0',
  `VAC3` decimal(4,1) NOT NULL DEFAULT '-1.0',
  `IAC1` decimal(3,1) NOT NULL DEFAULT '-1.0',
  `IAC2` decimal(3,1) NOT NULL DEFAULT '-1.0',
  `IAC3` decimal(3,1) NOT NULL DEFAULT '-1.0',
  `FAC` decimal(4,2) NOT NULL DEFAULT '-1.00',
  `PAC1` int(11) NOT NULL DEFAULT '-1',
  `PAC2` int(11) NOT NULL DEFAULT '-1',
  `PAC3` int(11) NOT NULL DEFAULT '-1',
  `ServerStamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of minutes
-- ----------------------------
INSERT INTO `minutes` VALUES ('1', 'CNCN252017060001', '0.0', '0.00', '0.0', '0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.00', '0', '0', '0', '2017-03-01 13:57:54');
INSERT INTO `minutes` VALUES ('2', 'CNCN252017060002', '0.0', '0.00', '0.0', '0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.00', '0', '0', '0', '2017-03-01 13:57:54');
INSERT INTO `minutes` VALUES ('3', 'CNCN252017060003', '0.0', '0.00', '0.0', '0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.00', '0', '0', '0', '2017-03-01 13:57:54');
INSERT INTO `minutes` VALUES ('4', 'CNCN252017060004', '0.0', '0.00', '0.0', '0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.00', '0', '0', '0', '2017-03-01 13:57:55');
INSERT INTO `minutes` VALUES ('5', 'CNCN252017060005', '0.0', '0.00', '0.0', '0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.00', '0', '0', '0', '2017-03-01 13:57:55');
INSERT INTO `minutes` VALUES ('6', 'CNCN252017060006', '0.0', '0.00', '0.0', '0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.00', '0', '0', '0', '2017-03-01 13:57:55');
INSERT INTO `minutes` VALUES ('7', 'CNCN252017060007', '0.0', '0.00', '0.0', '0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.00', '0', '0', '0', '2017-03-01 13:57:55');
INSERT INTO `minutes` VALUES ('8', 'CNCN252017060008', '0.0', '0.00', '0.0', '0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.00', '0', '0', '0', '2017-03-01 13:57:55');
INSERT INTO `minutes` VALUES ('9', 'CNCN252017060009', '0.0', '0.00', '0.0', '0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.00', '0', '0', '0', '2017-03-01 13:57:55');
INSERT INTO `minutes` VALUES ('10', 'CNCN252017060010', '0.0', '0.00', '0.0', '0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.00', '0', '0', '0', '2017-03-01 13:57:55');
INSERT INTO `minutes` VALUES ('11', 'CNCN252017060011', '0.0', '0.00', '0.0', '0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.00', '0', '0', '0', '2017-03-01 13:57:55');
INSERT INTO `minutes` VALUES ('12', 'CNCN252017060012', '0.0', '0.00', '0.0', '0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.00', '0', '0', '0', '2017-03-01 13:57:55');
INSERT INTO `minutes` VALUES ('13', 'CNCN203115966013', '0.0', '0.00', '0.0', '0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.00', '0', '0', '0', '2017-03-01 13:57:55');
INSERT INTO `minutes` VALUES ('14', 'CNCN203115966014', '0.0', '0.00', '0.0', '0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.00', '0', '0', '0', '2017-03-01 13:57:55');
INSERT INTO `minutes` VALUES ('15', 'CNCN203115966015', '0.0', '0.00', '0.0', '0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.00', '0', '0', '0', '2017-03-01 13:57:55');
