-- depends: 0000.initial

CREATE TABLE roles (id SERIAL PRIMARY KEY, name TEXT);

CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT, tg_id TEXT, viber_id TEXT, phone TEXT);

CREATE TABLE promotions (id SERIAL PRIMARY KEY, name TEXT, users_id INT, role_id INT, date TIMESTAMP, promoter INT);
ALTER TABLE promotions ADD FOREIGN KEY(users_id) REFERENCES users(id);
ALTER TABLE promotions ADD FOREIGN KEY(role_id) REFERENCES roles(id);
ALTER TABLE promotions ADD FOREIGN KEY(promoter) REFERENCES users(id);
