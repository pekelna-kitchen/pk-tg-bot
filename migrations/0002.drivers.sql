-- depends: 0001.users

CREATE TABLE districts (id SERIAL PRIMARY KEY, name TEXT);

CREATE TABLE coords (id SERIAL PRIMARY KEY, longitude VARCHAR(20), latitude varchar(20));

CREATE TABLE civils (id SERIAL PRIMARY KEY, district_id INT, address TEXT, phone_number TEXT, notes TEXT, coords_id INT);
ALTER TABLE civils ADD FOREIGN KEY(district_id) REFERENCES districts(id);
ALTER TABLE civils ADD FOREIGN KEY(coords_id) REFERENCES coords(id);
