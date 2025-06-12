-- Clear existing data
DELETE FROM spot_change;
DELETE FROM spot;
DELETE FROM zone;
DELETE FROM floor;
DELETE FROM entrance_to_garage;
DELETE FROM building_to_garage;
DELETE FROM entrance;
DELETE FROM buildings;
DELETE FROM garages;

-- Insert buildings
INSERT INTO buildings (id, name, location) VALUES
(1, 'Building A', 'North Campus'),
(2, 'Building B', 'South Campus'),
(3, 'Building C', 'East Campus'),
(4, 'Building F', 'West Campus');

-- Insert garages
INSERT INTO garages (id, name, total_spaces, available_spaces, location) VALUES
(1, 'Garage A', 1250, 875, 'North Campus'),
(2, 'Garage B', 1250, 1000, 'South Campus'),
(3, 'Garage C', 1250, 625, 'East Campus'),
(4, 'Garage F', 1250, 750, 'West Campus');

-- Insert entrances
INSERT INTO entrance (entrance_id, entrance_name) VALUES
('E1', 'Leadership Dr'),
('E2', 'Hwy 121'),
('E3', 'Headquarters Dr'),
('E4', 'Communication Pkwy');

-- Insert entrance to garage relationships
INSERT INTO entrance_to_garage (entrance_to_garage_id, garage_id, entrance_id, distance) VALUES
('ETG1', 1, 'E1', 0.2),
('ETG2', 1, 'E2', 0.5),
('ETG3', 1, 'E3', 0.8),
('ETG4', 1, 'E4', 1.0),
('ETG5', 2, 'E1', 0.8),
('ETG6', 2, 'E2', 0.3),
('ETG7', 2, 'E3', 0.6),
('ETG8', 2, 'E4', 0.9),
('ETG9', 3, 'E1', 0.9),
('ETG10', 3, 'E2', 0.7),
('ETG11', 3, 'E3', 0.4),
('ETG12', 3, 'E4', 0.2),
('ETG13', 4, 'E1', 0.7),
('ETG14', 4, 'E2', 0.9),
('ETG15', 4, 'E3', 0.3),
('ETG16', 4, 'E4', 0.5);

-- Insert building to garage relationships
INSERT INTO building_to_garage (id, building_id, garage_id, distance) VALUES
(1, 1, 1, 0.1),
(2, 1, 2, 0.8),
(3, 1, 3, 0.9),
(4, 1, 4, 0.7),
(5, 2, 1, 0.8),
(6, 2, 2, 0.2),
(7, 2, 3, 0.7),
(8, 2, 4, 0.9),
(9, 3, 1, 0.9),
(10, 3, 2, 0.7),
(11, 3, 3, 0.3),
(12, 3, 4, 0.8),
(13, 4, 1, 0.7),
(14, 4, 2, 0.9),
(15, 4, 3, 0.8),
(16, 4, 4, 0.2);

-- Insert floors for Garage A
INSERT INTO floor (floor_id, garage_id, floor_name, capacity) VALUES
('F1_1', 1, 'Floor 1', 250),
('F1_2', 1, 'Floor 2', 250),
('F1_3', 1, 'Floor 3', 250),
('F1_4', 1, 'Floor 4', 250),
('F1_5', 1, 'Floor 5', 250);

-- Insert floors for Garage B
INSERT INTO floor (floor_id, garage_id, floor_name, capacity) VALUES
('F2_1', 2, 'Floor 1', 250),
('F2_2', 2, 'Floor 2', 250),
('F2_3', 2, 'Floor 3', 250),
('F2_4', 2, 'Floor 4', 250),
('F2_5', 2, 'Floor 5', 250);

-- Insert floors for Garage C
INSERT INTO floor (floor_id, garage_id, floor_name, capacity) VALUES
('F3_1', 3, 'Floor 1', 250),
('F3_2', 3, 'Floor 2', 250),
('F3_3', 3, 'Floor 3', 250),
('F3_4', 3, 'Floor 4', 250),
('F3_5', 3, 'Floor 5', 250);

-- Insert floors for Garage F
INSERT INTO floor (floor_id, garage_id, floor_name, capacity) VALUES
('F4_1', 4, 'Floor 1', 250),
('F4_2', 4, 'Floor 2', 250),
('F4_3', 4, 'Floor 3', 250),
('F4_4', 4, 'Floor 4', 250),
('F4_5', 4, 'Floor 5', 250);

-- Insert zones for each floor
INSERT INTO zone (zone_id, floor_id, garage_id, zone_name, capacity) VALUES
-- Garage A Zones
('Z1_1_1', 'F1_1', 1, 'Zone 1', 50),
('Z1_1_2', 'F1_1', 1, 'Zone 2', 50),
('Z1_1_3', 'F1_1', 1, 'Zone 3', 50),
('Z1_1_4', 'F1_1', 1, 'Zone 4', 50),
('Z1_1_5', 'F1_1', 1, 'Zone 5', 50),
('Z1_2_1', 'F1_2', 1, 'Zone 1', 50),
('Z1_2_2', 'F1_2', 1, 'Zone 2', 50),
('Z1_2_3', 'F1_2', 1, 'Zone 3', 50),
('Z1_2_4', 'F1_2', 1, 'Zone 4', 50),
('Z1_2_5', 'F1_2', 1, 'Zone 5', 50),
('Z1_3_1', 'F1_3', 1, 'Zone 1', 50),
('Z1_3_2', 'F1_3', 1, 'Zone 2', 50),
('Z1_3_3', 'F1_3', 1, 'Zone 3', 50),
('Z1_3_4', 'F1_3', 1, 'Zone 4', 50),
('Z1_3_5', 'F1_3', 1, 'Zone 5', 50),
('Z1_4_1', 'F1_4', 1, 'Zone 1', 50),
('Z1_4_2', 'F1_4', 1, 'Zone 2', 50),
('Z1_4_3', 'F1_4', 1, 'Zone 3', 50),
('Z1_4_4', 'F1_4', 1, 'Zone 4', 50),
('Z1_4_5', 'F1_4', 1, 'Zone 5', 50),
('Z1_5_1', 'F1_5', 1, 'Zone 1', 50),
('Z1_5_2', 'F1_5', 1, 'Zone 2', 50),
('Z1_5_3', 'F1_5', 1, 'Zone 3', 50),
('Z1_5_4', 'F1_5', 1, 'Zone 4', 50),
('Z1_5_5', 'F1_5', 1, 'Zone 5', 50),

-- Garage B Zones
('Z2_1_1', 'F2_1', 2, 'Zone 1', 50),
('Z2_1_2', 'F2_1', 2, 'Zone 2', 50),
('Z2_1_3', 'F2_1', 2, 'Zone 3', 50),
('Z2_1_4', 'F2_1', 2, 'Zone 4', 50),
('Z2_1_5', 'F2_1', 2, 'Zone 5', 50),
('Z2_2_1', 'F2_2', 2, 'Zone 1', 50),
('Z2_2_2', 'F2_2', 2, 'Zone 2', 50),
('Z2_2_3', 'F2_2', 2, 'Zone 3', 50),
('Z2_2_4', 'F2_2', 2, 'Zone 4', 50),
('Z2_2_5', 'F2_2', 2, 'Zone 5', 50),
('Z2_3_1', 'F2_3', 2, 'Zone 1', 50),
('Z2_3_2', 'F2_3', 2, 'Zone 2', 50),
('Z2_3_3', 'F2_3', 2, 'Zone 3', 50),
('Z2_3_4', 'F2_3', 2, 'Zone 4', 50),
('Z2_3_5', 'F2_3', 2, 'Zone 5', 50),
('Z2_4_1', 'F2_4', 2, 'Zone 1', 50),
('Z2_4_2', 'F2_4', 2, 'Zone 2', 50),
('Z2_4_3', 'F2_4', 2, 'Zone 3', 50),
('Z2_4_4', 'F2_4', 2, 'Zone 4', 50),
('Z2_4_5', 'F2_4', 2, 'Zone 5', 50),
('Z2_5_1', 'F2_5', 2, 'Zone 1', 50),
('Z2_5_2', 'F2_5', 2, 'Zone 2', 50),
('Z2_5_3', 'F2_5', 2, 'Zone 3', 50),
('Z2_5_4', 'F2_5', 2, 'Zone 4', 50),
('Z2_5_5', 'F2_5', 2, 'Zone 5', 50),

-- Garage C Zones
('Z3_1_1', 'F3_1', 3, 'Zone 1', 50),
('Z3_1_2', 'F3_1', 3, 'Zone 2', 50),
('Z3_1_3', 'F3_1', 3, 'Zone 3', 50),
('Z3_1_4', 'F3_1', 3, 'Zone 4', 50),
('Z3_1_5', 'F3_1', 3, 'Zone 5', 50),
('Z3_2_1', 'F3_2', 3, 'Zone 1', 50),
('Z3_2_2', 'F3_2', 3, 'Zone 2', 50),
('Z3_2_3', 'F3_2', 3, 'Zone 3', 50),
('Z3_2_4', 'F3_2', 3, 'Zone 4', 50),
('Z3_2_5', 'F3_2', 3, 'Zone 5', 50),
('Z3_3_1', 'F3_3', 3, 'Zone 1', 50),
('Z3_3_2', 'F3_3', 3, 'Zone 2', 50),
('Z3_3_3', 'F3_3', 3, 'Zone 3', 50),
('Z3_3_4', 'F3_3', 3, 'Zone 4', 50),
('Z3_3_5', 'F3_3', 3, 'Zone 5', 50),
('Z3_4_1', 'F3_4', 3, 'Zone 1', 50),
('Z3_4_2', 'F3_4', 3, 'Zone 2', 50),
('Z3_4_3', 'F3_4', 3, 'Zone 3', 50),
('Z3_4_4', 'F3_4', 3, 'Zone 4', 50),
('Z3_4_5', 'F3_4', 3, 'Zone 5', 50),
('Z3_5_1', 'F3_5', 3, 'Zone 1', 50),
('Z3_5_2', 'F3_5', 3, 'Zone 2', 50),
('Z3_5_3', 'F3_5', 3, 'Zone 3', 50),
('Z3_5_4', 'F3_5', 3, 'Zone 4', 50),
('Z3_5_5', 'F3_5', 3, 'Zone 5', 50),

-- Garage F Zones
('Z4_1_1', 'F4_1', 4, 'Zone 1', 50),
('Z4_1_2', 'F4_1', 4, 'Zone 2', 50),
('Z4_1_3', 'F4_1', 4, 'Zone 3', 50),
('Z4_1_4', 'F4_1', 4, 'Zone 4', 50),
('Z4_1_5', 'F4_1', 4, 'Zone 5', 50),
('Z4_2_1', 'F4_2', 4, 'Zone 1', 50),
('Z4_2_2', 'F4_2', 4, 'Zone 2', 50),
('Z4_2_3', 'F4_2', 4, 'Zone 3', 50),
('Z4_2_4', 'F4_2', 4, 'Zone 4', 50),
('Z4_2_5', 'F4_2', 4, 'Zone 5', 50),
('Z4_3_1', 'F4_3', 4, 'Zone 1', 50),
('Z4_3_2', 'F4_3', 4, 'Zone 2', 50),
('Z4_3_3', 'F4_3', 4, 'Zone 3', 50),
('Z4_3_4', 'F4_3', 4, 'Zone 4', 50),
('Z4_3_5', 'F4_3', 4, 'Zone 5', 50),
('Z4_4_1', 'F4_4', 4, 'Zone 1', 50),
('Z4_4_2', 'F4_4', 4, 'Zone 2', 50),
('Z4_4_3', 'F4_4', 4, 'Zone 3', 50),
('Z4_4_4', 'F4_4', 4, 'Zone 4', 50),
('Z4_4_5', 'F4_4', 4, 'Zone 5', 50),
('Z4_5_1', 'F4_5', 4, 'Zone 1', 50),
('Z4_5_2', 'F4_5', 4, 'Zone 2', 50),
('Z4_5_3', 'F4_5', 4, 'Zone 3', 50),
('Z4_5_4', 'F4_5', 4, 'Zone 4', 50),
('Z4_5_5', 'F4_5', 4, 'Zone 5', 50);

-- Note: Spots are now created programmatically in main.py on startup.
-- The spot_change table will be populated with historical data for the programmatically created spots.

-- Insert some historical changes for a few spots to simulate data
INSERT INTO spot_change (spot_change_id, spot_id, is_parking, ts) VALUES
('SC1_1_1_1_1', 'S1_1_1_1', 1, datetime('now', '-4 hours')),
('SC1_1_1_1_2', 'S1_1_1_1', 0, datetime('now', '-3 hours')),
('SC1_1_1_1_3', 'S1_1_1_1', 1, datetime('now', '-2 hours')),
('SC1_1_1_1_4', 'S1_1_1_1', 0, datetime('now', '-1 hour')),
('SC1_1_1_2_1', 'S1_1_1_2', 1, datetime('now', '-5 hours')),
('SC1_1_1_2_2', 'S1_1_1_2', 0, datetime('now', '-4 hours')),
('SC1_1_1_2_3', 'S1_1_1_2', 1, datetime('now', '-3 hours')),
('SC1_1_1_2_4', 'S1_1_1_2', 0, datetime('now', '-2 hours')),
('SC1_1_1_2_5', 'S1_1_1_2', 1, datetime('now', '-1 hour'));