"""
TODO:
 - multi_exec for test parity
"""
from omnibus import lang
import sqlalchemy as sa

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

    @lang.override
    def build_range(self, num):
        # sa.alias
        # select i from generate_series(1, 5) s(i)
        # return sa.select([])
        raise NotImplementedError
