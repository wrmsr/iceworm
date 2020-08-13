"""
c.yml:
 select a.id, a.a, a.b, b.c, b.d from a inner join b on a.id = b.id

d.yml
 select a.id, c.a aa, a.a ca, c.d cd from c inner join a on c.id = a.id where c.d = 60
"""
