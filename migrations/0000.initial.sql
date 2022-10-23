--
-- file: migrations/0000.initial.sql
--
CREATE TABLE containers (id SERIAL PRIMARY KEY, symbol VARCHAR(1), description TEXT);

CREATE TABLE locations (id SERIAL PRIMARY KEY, symbol VARCHAR(1), name TEXT);

CREATE TABLE products (id SERIAL PRIMARY KEY, symbol VARCHAR(1), name TEXT, limit_container INT, limit_amount INT);
ALTER TABLE products ADD FOREIGN KEY(limit_container) REFERENCES containers(id);

CREATE TABLE entries (id SERIAL PRIMARY KEY, product_id INT, location_id INT, amount INT, container_id INT, date TIMESTAMP, editor INT);
ALTER TABLE entries ADD FOREIGN KEY(container_id) REFERENCES containers(id);
ALTER TABLE entries ADD FOREIGN KEY(product_id) REFERENCES products(id);
ALTER TABLE entries ADD FOREIGN KEY(location_id) REFERENCES locations(id);
