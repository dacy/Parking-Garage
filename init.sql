-- Insert sample garages
INSERT INTO garages (id, name, location, total_capacity) VALUES 
(1, 'Garage A', 'North Campus', 200),
(2, 'Garage B', 'South Campus', 150),
(3, 'Garage C', 'East Campus', 300);

-- Insert sample floors for each garage
-- Garage A floors
INSERT INTO floors (id, level, garage_id) VALUES 
(1, 1, 1),
(2, 2, 1),
(3, 3, 1);

-- Garage B floors
INSERT INTO floors (id, level, garage_id) VALUES 
(4, 1, 2),
(5, 2, 2);

-- Garage C floors
INSERT INTO floors (id, level, garage_id) VALUES 
(6, 1, 3),
(7, 2, 3),
(8, 3, 3),
(9, 4, 3);

-- Insert sample spots for each floor
-- Garage A, Floor 1
INSERT INTO spots (spot_number, floor_id, is_available, type) VALUES 
('A1-01', 1, 1, 'Regular'),
('A1-02', 1, 0, 'Regular'),
('A1-03', 1, 1, 'Compact'),
('A1-04', 1, 1, 'Handicapped'),
('A1-05', 1, 0, 'Regular');

-- Garage A, Floor 2
INSERT INTO spots (spot_number, floor_id, is_available, type) VALUES 
('A2-01', 2, 1, 'Regular'),
('A2-02', 2, 1, 'Regular'),
('A2-03', 2, 0, 'Compact'),
('A2-04', 2, 1, 'Handicapped'),
('A2-05', 2, 1, 'Regular');

-- Garage A, Floor 3
INSERT INTO spots (spot_number, floor_id, is_available, type) VALUES 
('A3-01', 3, 0, 'Regular'),
('A3-02', 3, 0, 'Regular'),
('A3-03', 3, 1, 'Compact'),
('A3-04', 3, 0, 'Handicapped'),
('A3-05', 3, 1, 'Regular');

-- Garage B, Floor 1
INSERT INTO spots (spot_number, floor_id, is_available, type) VALUES 
('B1-01', 4, 1, 'Regular'),
('B1-02', 4, 0, 'Regular'),
('B1-03', 4, 1, 'Compact'),
('B1-04', 4, 1, 'Handicapped'),
('B1-05', 4, 0, 'Regular');

-- Garage B, Floor 2
INSERT INTO spots (spot_number, floor_id, is_available, type) VALUES 
('B2-01', 5, 1, 'Regular'),
('B2-02', 5, 1, 'Regular'),
('B2-03', 5, 0, 'Compact'),
('B2-04', 5, 1, 'Handicapped'),
('B2-05', 5, 0, 'Regular');

-- Garage C, Floor 1
INSERT INTO spots (spot_number, floor_id, is_available, type) VALUES 
('C1-01', 6, 1, 'Regular'),
('C1-02', 6, 0, 'Regular'),
('C1-03', 6, 1, 'Compact'),
('C1-04', 6, 1, 'Handicapped'),
('C1-05', 6, 0, 'Regular');

-- Garage C, Floor 2
INSERT INTO spots (spot_number, floor_id, is_available, type) VALUES 
('C2-01', 7, 1, 'Regular'),
('C2-02', 7, 1, 'Regular'),
('C2-03', 7, 0, 'Compact'),
('C2-04', 7, 1, 'Handicapped'),
('C2-05', 7, 0, 'Regular');

-- Garage C, Floor 3
INSERT INTO spots (spot_number, floor_id, is_available, type) VALUES 
('C3-01', 8, 1, 'Regular'),
('C3-02', 8, 0, 'Regular'),
('C3-03', 8, 1, 'Compact'),
('C3-04', 8, 1, 'Handicapped'),
('C3-05', 8, 0, 'Regular');

-- Garage C, Floor 4
INSERT INTO spots (spot_number, floor_id, is_available, type) VALUES 
('C4-01', 9, 1, 'Regular'),
('C4-02', 9, 1, 'Regular'),
('C4-03', 9, 0, 'Compact'),
('C4-04', 9, 1, 'Handicapped'),
('C4-05', 9, 0, 'Regular'); 