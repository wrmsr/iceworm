select distinct m.i as u_i from e.p p left join e.a a on p.a_i = a.i left join e.i i on p.i_i = i.i left join e.i2 ir on i.i_i = ir.i inner join e.u u on c(a.u_i, ir.u_i) = u.i inner join et.u2 m on u.c_u_u = m.u where p.c_a is not null;
select distinct m.i as u_i, t_d(c_t('u', 'a/l_a', c_a)) as dt from e.p p left join e.a a on p.a_i = a.i left join e.i i on p.i_i = i.i left join e.i2 ir on i.i_i = ir.i inner join e.u u on c(a.u_i, ir.u_i) = u.i inner join et.u2 m on u.c_u_u = m.u where p.c_a is not null;
select distinct d, sum(e_b_u) as sum from t.f_u_d_c_c_b where dt = left(c_t('u/p', current_date-1),10) group by u_i, d;
select * from a where p.u_i is null and not (d.b_u = 'p' and p.u_i is null and c.u_i is null);
select x, row_number() over (partition by p.c, p.o_t order by datediff(SECOND, p.o_t, p.c_t) desc) as row_num;
select sum(c.d_h * c.a_s)::float / sum(c.a_s)::float as w_m_h_d;
select avg(b.s_b) over (partition by b.c, b.u_i order by b.d asc rows between 7 preceding and 1 preceding) as p_w_a_b;
select sum(case when a.c not in (x) then a.a * 1000000 else a.a end) over (partition by a.a_i order by a.h_b_a, a._i rows unbounded preceding) as a_b;
select e_r_id, listagg(d_n, ' | ') within group (order by d_n) as d_n;