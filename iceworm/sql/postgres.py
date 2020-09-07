"""
TODO:
 - multi_exec for test parity
"""
from .adapter import Adapter

"""
do
$$
    declare
        stmts text[] := array ['select 1 a, 2 b', 'select 3 c, 4 d, 5 e'];
        stmt  text;
        c     refcursor;
        r     record;
    begin
        foreach stmt in array stmts
            loop
                open c for execute stmt;
                fetch next from c into r;
                while found
                    loop
                        raise notice '%', r;
                        fetch next from c into r;
                    end loop;
                close c;
            end loop;
    end
$$;
"""


class PostgresAdapter(Adapter):
    pass
