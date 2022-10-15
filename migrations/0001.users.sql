-- depends: 0000.initial

CREATE TABLE roles (id SERIAL PRIMARY KEY, name TEXT);

CREATE TABLE user_entries (id SERIAL PRIMARY KEY, tg_id TEXT, viber_id TEXT);

CREATE TABLE civils (id SERIAL PRIMARY KEY, district_id INT, address TEXT, contact TEXT, coords_id INT);
ALTER TABLE civils ADD FOREIGN KEY(district_id) REFERENCES districts(id);
ALTER TABLE civils ADD FOREIGN KEY(coords_id) REFERENCES coords(id);

