-- creates a stored procedure ComputeAverageWeightedScoreForUsers that computes
-- and store the average weighted score for all students.
-- Procedure ComputeAverageWeightedScoreForUsers is not taking any input.

DDROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	UPDATE users AS U,
	(SELECT U.id, SUM(score * weight) / SUM(weight) AS weighted_score
		FROM users AS U
		JOIN corrections as C ON U.id=C.user_id
		JOIN projects AS P ON C.project_id=P.id
		GROUP BY U.id)
	AS AW
	SET U.average_score = AW.weighted_score
	WHERE U.id=AW.id;
END
$$
DELIMITER ;
