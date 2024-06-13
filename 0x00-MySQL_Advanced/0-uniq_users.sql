-- SQL scripte that creates a table users with the following requirements:
-- id: integer, never null, primary key, autoincrement
-- email: string(255 characters), never null, unique
-- name: string(255 characters)
-- script should not fail if table exists
-- script should be executable on any database

CREATE TABLE IF NOT EXISTS users (
	id INT AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255)
);
