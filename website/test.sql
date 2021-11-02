-- select building_id, COUNT(*)
-- from favourites, building
-- group by building_id
-- having count(*) > 1

SELECT
    *
FROM
    favourites f,
    building b
WHERE
    f.building_id = b.id
GROUP BY
    f.building_id
HAVING
    count(*) > 1;
