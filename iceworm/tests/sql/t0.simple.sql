select 1;
select 'x';
select 1 from x;
select x from y;
select "x" from "y";
select x, y from z;
select f(x, 2) from y;
select x as y from z;
select x and y;
select not z;
select x from y join z;
select x from y join z on 1;
select x from y where 2;
select x from y group by 1;
select null;
select * from x;
select * from (x);
select (1) x;
select 1 - 2;
select -1;
select * from a inner join b;
select * from a left outer join b;
select * from l join r on 1 = 2;
select distinct 1;
select a.b from c.d;
select * from a b;
select * from a as b;
select * from t where a = b;
select f(g(x));
with a as (select 1) select * from a;
with a as (with b as (select 1) select * from b) select * from a;
select case when s = 'c' then v_u when s = 'd' then v_d else 0 end;
select '1'::int;
select * from x order by f desc;
select 1 union select 2;
select 1 union all select 2;
with a as (select 1) select 1 from a union all select 2 from a;
select * from (select 1);
select (select 1);
select a like 'b';
select f() over (order by x asc);
select true;
select 'true';
select "true";
select {{ hi }};
select * from {{ hi }};
select * where a in {{ a }};
<<<<<<< HEAD
select count(*);
select * having x = 1;
select top 1 *;
select 1.2;  -- [+-][digits][.digits][e[+-]digits]
select 0.1e4;
select +0.1e-4;
=======

-- FIXME:
select count(*);
select * having 1;
select * from (select * from t) unpivot(v for v in (a, b));
select * from (select * from c join n on n.i = c.i) pivot(min(v) for v in (a, b)) p(i, j);
>>>>>>> 0f60adb822846053482a23bcb9e13475524f5560
