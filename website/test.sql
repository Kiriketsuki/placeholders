-- select building_id, COUNT(*) 
-- from favourites, building
-- group by building_id
-- having count(*) > 1

select *
from favourites f, building b
where f.building_id = b.id
group by f.building_id
having count(*) > 1;