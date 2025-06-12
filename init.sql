CREATE TABLE `garage` (
  `garage_id` UUID,
  `garage_name` VARCHAR(100),
  `capacity` INT,
  PRIMARY KEY (`garage_id`)
);
 
CREATE TABLE `zone` (
  `zone_id` UUID,
  `floor_id` Type,
  `garage_id` Type,
  `zone_name` VARCHAR(100),
  `capacity` INT,
  PRIMARY KEY (`zone_id`),
  FOREIGN KEY (`garage_id`) REFERENCES `garage`(`garage_id`)
);
 
CREATE TABLE `floor` (
  `floor_id` UUID,
  `garage_id` UUID,
  `floor_name` VARCHAR(100),
  `capacity` INT,
  PRIMARY KEY (`floor_id`),
  FOREIGN KEY (`garage_id`) REFERENCES `garage`(`garage_id`)
);
 
CREATE TABLE `spot` (
  `spot_id` UUID,
  `zone_id` UUID,
  `floor_id` UUID,
  `garage_id` UUID,
  `is_occupied` BOOLEAN,
  `restriction_type` INT,
  PRIMARY KEY (`spot_id`),
  FOREIGN KEY (`garage_id`) REFERENCES `garage`(`garage_id`),
  FOREIGN KEY (`zone_id`) REFERENCES `zone`(`zone_id`),
  FOREIGN KEY (`floor_id`) REFERENCES `floor`(`floor_id`)
);
 
CREATE TABLE `building` (
  `building_id` UUID,
  `building_name` Type,
  PRIMARY KEY (`building_id`)
);
 
CREATE TABLE `building_to_garage` (
  `building_to_garage_id` UUID,
  `garage_id` UUID,
  `building_id` UUID,
  `distance` Type,
  PRIMARY KEY (`building_to_garage_id`),
  FOREIGN KEY (`building_id`) REFERENCES `building`(`building_id`),
  FOREIGN KEY (`garage_id`) REFERENCES `garage`(`garage_id`)
);
 
CREATE TABLE `entrance` (
  `entrance_id` UUID,
  `entrance_name` Type,
  PRIMARY KEY (`entrance_id`)
);
 
CREATE TABLE `entrance_to_garage` (
  `entrance_to_garage_id` UUID,
  `garage_id` UUID,
  `entrance_id` UUID,
  `distance` Type,
  PRIMARY KEY (`entrance_to_garage_id`),
  FOREIGN KEY (`entrance_id`) REFERENCES `entrance`(`entrance_id`),
  FOREIGN KEY (`garage_id`) REFERENCES `garage`(`garage_id`)
);
 
CREATE TABLE `spot_change` (
  `spot_change_id` UUID,
  `spot_id` UUID,
  `is_parking` BOOLEAN,
  `ts` DATETIME,
  PRIMARY KEY (`spot_change_id`),
  FOREIGN KEY (`spot_id`) REFERENCES `spot`(`spot_id`)
);