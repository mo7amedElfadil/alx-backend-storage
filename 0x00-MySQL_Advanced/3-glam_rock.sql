-- lists all bands with Glam Rock as their main style ranked by
-- logngevity (lifespan) in years until 2022
-- columns: band name, lifespan (years until 2022)
-- order by: lifespan descending

SELECT band_name, IFNULL(split, 2022) - formed AS lifespan
	FROM metal_bands
	Where style LIKE '%Glam Rock%'
	ORDER BY lifespan DESC;
