"""
TODO:
 - multi_exec for test parity
  - json type?
"""
from omnibus import lang
import sqlalchemy as sa

from .adapter import Adapter
from .elements import column_list_alias


"""
create or replace function multi_exec(stmts text[]) returns text[] as
$$
declare
    stmt  text;
    c     refcursor;
    r     record;
    o     text[];
begin
    foreach stmt in array stmts
        loop
            open c for execute stmt;
            fetch next from c into r;
            while found
                loop
                    o := array_append(o, cast(row_to_json(r) as text));
                    fetch next from c into r;
                end loop;
            close c;
        end loop;
    return o;
end
$$ language plpgsql;

select multi_exec(array['select 1 x', 'select 2 y union select 3']);
"""


class PostgresAdapter(Adapter):

    class Config(Adapter.Config):
        pass

    def __init__(self, config: Config = Config()) -> None:
        super().__init__(config)

    @lang.override
    def build_range(self, num):
        # select i from generate_series(1, 10) s(i)
        return sa.select([
            sa.column('i'),
        ]).select_from(
            column_list_alias(sa.func.generate_series(1, num), 's', ['i'])
        )
