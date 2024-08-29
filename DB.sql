CREATE DATABASE IF NOT EXISTS `auction` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
use auction;
CREATE TABLE IF NOT EXISTS `buyer` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(255) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    `phoneno` varchar(255) NOT NULL,   
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `seller` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(255) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL, 
    `phone` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `stock` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`stockname` varchar(255) NOT NULL,
  	`stockprice` int(255) NOT NULL,
    `stockid` varchar(255),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `book` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`stockname` varchar(255) NOT NULL,
  	`stockprice` int(255) NOT NULL,
    `stockid` varchar(255),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


select * from book;
