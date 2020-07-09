-- https://docs.snowflake.com/en/sql-reference/constructs/with.html

with recursive cte_name (x, y) as (
  select related_to_x, related_to_y from table1
  union all
  select also_related_to_x, also_related_to_y from table1 join cte_name on 1
)
select * from t;

with albums_1976 as (
  select * from music_albums where album_year = 1976
)
select album_name from albums_1976 order by album_name;

with album_info_1976 as (
  select m.album_id, m.album_name, b.band_name
  from music_albums as m inner join music_bands as b
  where m.band_id = b.band_id and album_year = 1976
), journey_album_info_1976 as (
  select *
  from album_info_1976
  where band_name = 'Journey'
)
select album_name, band_name
from journey_album_info_1976;

select distinct musicians.musician_id, musician_name
 from musicians inner join musicians_and_albums inner join music_albums inner join music_bands
 where musicians.musician_id = musicians_and_albums.musician_id
   and musicians_and_albums.album_id = music_albums.album_id
   and music_albums.band_id = music_bands.band_id
   and music_bands.band_name = 'Santana'
intersect
select distinct musicians.musician_id, musician_name
 from musicians inner join musicians_and_albums inner join music_albums inner join music_bands
 where musicians.musician_id = musicians_and_albums.musician_id
   and musicians_and_albums.album_id = music_albums.album_id
   and music_albums.band_id = music_bands.band_id
   and music_bands.band_name = 'Journey'
order by musician_id;

with musicians_in_bands as (
  select distinct musicians.musician_id, musician_name, band_name
  from musicians inner join musicians_and_albums inner join music_albums inner join music_bands
  where musicians.musician_id = musicians_and_albums.musician_id
  and musicians_and_albums.album_id = music_albums.album_id
  and music_albums.band_id = music_bands.band_id)
select musician_id, musician_name from musicians_in_bands where band_name = 'Santana'
intersect
select musician_id, musician_name from musicians_in_bands where band_name = 'Journey'
order by musician_id;

with recursive current_f (current_val, previous_val) as (
  select 0, 1
  union all
  select current_val + previous_val, current_val from current_f
  where current_val + previous_val < 100
)
select current_val from current_f order by current_val;

with recursive current_layer (indent, layer_id, parent_component_id, component_id, description, sort_key) as (
  select '...', 1, parent_component_id, component_id, description, '0001'
  from components where component_id = 1
  union all
  select indent || '...', layer_id + 1, components.parent_component_id, components.component_id, components.description, sort_key || substring('000' || components.component_id, -4)
  from current_layer join components on (components.parent_component_id = current_layer.component_id)
)
select indent || description as description, component_id, parent_component_id
from current_layer
order by sort_key;


-- https://docs.snowflake.com/en/sql-reference/constructs/pivot.html

select *
from monthly_sales
pivot(sum(amount) for month in ('JAN', 'FEB', 'MAR', 'APR')) as p
order by empid;

select *
from monthly_sales
pivot(sum(amount) for month in ('JAN', 'FEB', 'MAR', 'APR')) as p (emp_id_renamed, jan, feb, mar, apr)
order by emp_id_renamed;

select empid as emp_id, "'JAN'" as january, "'FEB'" as february, "'MAR'" as march, "'APR'" as april
from monthly_sales
pivot(sum(amount) for month in ('JAN', 'FEB', 'MAR', 'APR')) as p
order by empid;


-- https://docs.snowflake.com/en/sql-reference/constructs/unpivot.html

select * from monthly_sales
unpivot(sales for month in (jan, feb, mar, april))
order by empid;

