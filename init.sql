DELETE FROM spot_change;
DELETE FROM entrance_to_garage;
DELETE FROM entrance;
DELETE FROM building_to_garage;
DELETE FROM building;
DELETE FROM spot;
DELETE FROM zone;
DELETE FROM floor;
DELETE FROM garage;

-- Dummy data for garage
INSERT INTO garage (garage_id, garage_name, capacity) VALUES
  ('g1', 'Garage A', 200),
  ('g2', 'Garage B', 150);

-- Dummy data for floor
INSERT INTO floor (floor_id, garage_id, floor_name, capacity) VALUES
  ('f1', 'g1', 'Floor 1', 100),
  ('f2', 'g1', 'Floor 2', 100),
  ('f3', 'g2', 'Floor 1', 75);

-- Dummy data for zone
INSERT INTO zone (zone_id, floor_id, garage_id, zone_name, capacity) VALUES
  ('z1', 'f1', 'g1', 'Zone A', 50),
  ('z2', 'f1', 'g1', 'Zone B', 50),
  ('z3', 'f2', 'g1', 'Zone C', 100),
  ('z4', 'f3', 'g2', 'Zone D', 75);

-- Dummy data for spot
INSERT INTO spot (spot_id, zone_id, floor_id, garage_id, is_occupied, restriction_type) VALUES
  ('s1', 'z1', 'f1', 'g1', 0, 0),
  ('s2', 'z1', 'f1', 'g1', 1, 1),
  ('s3', 'z2', 'f1', 'g1', 0, 0),
  ('s4', 'z3', 'f2', 'g1', 1, 2),
  ('s5', 'z4', 'f3', 'g2', 0, 0);

-- Dummy data for building
INSERT INTO building (building_id, building_name) VALUES
  ('b1', 'Building Alpha'),
  ('b2', 'Building Beta');

-- Dummy data for building_to_garage
INSERT INTO building_to_garage (building_to_garage_id, garage_id, building_id, distance) VALUES
  ('bg1', 'g1', 'b1', '100'),
  ('bg2', 'g2', 'b2', '200');

-- Dummy data for entrance
INSERT INTO entrance (entrance_id, entrance_name) VALUES
  ('e1', 'North Entrance'),
  ('e2', 'South Entrance');

-- Dummy data for entrance_to_garage
INSERT INTO entrance_to_garage (entrance_to_garage_id, garage_id, entrance_id, distance) VALUES
  ('eg1', 'g1', 'e1', '50'),
  ('eg2', 'g2', 'e2', '75');

-- Dummy data for spot_change
INSERT INTO spot_change (spot_change_id, spot_id, is_parking, ts) VALUES
  ('sc1', 's1', 1, '2024-06-01 08:00:00'),
  ('sc2', 's2', 0, '2024-06-01 09:00:00');