-- creates table users with these requirements:
-- id: integer, not null, primary key, autoincrement
-- email: string(255), not null, unique
-- name: string(255)
-- country: enum ('US', 'CO', 'TN') not null, default 'US'
-- if table already exists, do nothing

CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255),
	country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US'
);
