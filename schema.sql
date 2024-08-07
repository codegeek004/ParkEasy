 CREATE TABLE `admin` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` varchar(40) DEFAULT 'admin',
  `SNo` int NOT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


 CREATE TABLE `allotment` (
  `AllotmentID` int NOT NULL AUTO_INCREMENT,
  `SNo` int NOT NULL,
  `OwnerID` int DEFAULT NULL,
  `BSlotID` int DEFAULT NULL,
  `VehicleID` int DEFAULT NULL,
  `PaymentID` int DEFAULT NULL,
  PRIMARY KEY (`AllotmentID`),
  KEY `fk_sno` (`SNo`),
  KEY `owner_fk` (`OwnerID`),
  KEY `fk_bookingslot` (`BSlotID`),
  KEY `fk_vehicle` (`VehicleID`),
  KEY `fk_payment` (`PaymentID`),
  CONSTRAINT `fk_bookingslot` FOREIGN KEY (`BSlotID`) REFERENCES `bookingslot` (`BSlotID`),
  CONSTRAINT `fk_payment` FOREIGN KEY (`PaymentID`) REFERENCES `payment` (`PaymentID`),
  CONSTRAINT `fk_sno` FOREIGN KEY (`SNo`) REFERENCES `user` (`SNo`),
  CONSTRAINT `fk_vehicle` FOREIGN KEY (`VehicleID`) REFERENCES `vehicle` (`VehicleID`),
  CONSTRAINT `owner_fk` FOREIGN KEY (`OwnerID`) REFERENCES `owner` (`OwnerID`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


CREATE TABLE `bookingslot` (
  `BSlotID` int NOT NULL AUTO_INCREMENT,
  `Date` date DEFAULT NULL,
  `TimeFrom` time DEFAULT NULL,
  `TimeTo` time DEFAULT NULL,
  `duration` varchar(30) DEFAULT NULL,
  `SNo` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`BSlotID`),
  CONSTRAINT `bookingslot_ibfk_1` FOREIGN KEY (`BSlotID`) REFERENCES `slots` (`SlotID`),
  CONSTRAINT `bookingslot_ibfk_2` FOREIGN KEY (`BSlotID`) REFERENCES `vehicle` (`VehicleID`),
  CONSTRAINT `bookingslot_ibfk_3` FOREIGN KEY (`BSlotID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=95 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


CREATE TABLE `owner` (
  `OwnerID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `contact` bigint DEFAULT NULL,
  `SNo` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`OwnerID`),
  CONSTRAINT `owner_ibfk_1` FOREIGN KEY (`OwnerID`) REFERENCES `user` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=150 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


 CREATE TABLE `payment` (
  `PaymentID` int NOT NULL AUTO_INCREMENT,
  `TotalPrice` int DEFAULT NULL,
  `mode` varchar(30) DEFAULT NULL,
  `SNo` int NOT NULL,
  PRIMARY KEY (`PaymentID`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`PaymentID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `payment_ibfk_2` FOREIGN KEY (`PaymentID`) REFERENCES `bookingslot` (`BSlotID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


CREATE TABLE `sensor` (
  `SensorID` int NOT NULL AUTO_INCREMENT,
  `isParked` tinyint DEFAULT NULL,
  PRIMARY KEY (`SensorID`),
  CONSTRAINT `sensor_ibfk_1` FOREIGN KEY (`SensorID`) REFERENCES `slots` (`SlotID`)
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


CREATE TABLE `slots` (
  `SlotID` int NOT NULL AUTO_INCREMENT,
  `space` varchar(30) DEFAULT NULL,
  `price` int DEFAULT NULL,
  PRIMARY KEY (`SlotID`)
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


CREATE TABLE `user` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` varchar(40) DEFAULT 'user',
  `SNo` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `SNo` (`SNo`)
) ENGINE=InnoDB AUTO_INCREMENT=206 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


CREATE TABLE `vehicle` (
  `VehicleID` int NOT NULL AUTO_INCREMENT,
  `VehicleType` varchar(40) DEFAULT NULL,
  `VehicleNumber` varchar(40) DEFAULT NULL,
  `SNo` int NOT NULL,
  PRIMARY KEY (`VehicleID`),
  CONSTRAINT `vehicle_ibfk_1` FOREIGN KEY (`VehicleID`) REFERENCES `slots` (`SlotID`),
  CONSTRAINT `vehicle_ibfk_2` FOREIGN KEY (`VehicleID`) REFERENCES `user` (`UserID`),
  CONSTRAINT `vehicle_ibfk_3` FOREIGN KEY (`VehicleID`) REFERENCES `owner` (`OwnerID`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
