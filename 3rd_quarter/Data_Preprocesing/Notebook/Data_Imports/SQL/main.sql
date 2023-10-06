/*
CREATE TABLE `data_preprocessing`.`data_import_uat` (
  `ID` INT NOT NULL,
  `MSSubClass` VARCHAR(255) NULL,
  `MSZoning` VARCHAR(255) NULL,
  `LotFrontage` VARCHAR(45) NULL,
  `LotArea` VARCHAR(45) NULL,
  `Street` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`));
*/

CALL data_import();