--  creates a stored procedure AddBonus that adds a new correction for a student.
-- Procedure AddBonus is taking 3 inputs (in this order):
--		user_id, a users.id value (you can assume user_id is linked to an existing users)
--		project_name, a new or already exists projects - if no projects.name found in the table, you should create it
--		score, the score value for the correction

DROP PROCEDURE IF EXISTS AddBonus;
DELIMITER $$
CREATE PROCEDURE AddBonus(
	IN user_id INT,
	IN project_name VARCHAR(255),
	IN score INT)
BEGIN
	DECLARE project_id INT;

	-- Check if project exists
	SELECT id INTO project_id FROM projects WHERE name = project_name;
	IF project_id IS NULL THEN
		-- Create project if not exists
		INSERT INTO projects (name) VALUES (project_name);
		SET project_id = LAST_INSERT_ID();
	END IF;

	-- Insert correction
	SET project_id = (SELECT id FROM projects WHERE name = project_name LIMIT 1);
	INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);
END$$
DELIMITER ;
