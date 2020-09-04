import itertools
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import tpch
import sqlalchemy as sa


SA_TYPES_BY_TPCH_TYPE = {
    tpch.ents.Column.Type.INTEGER: sa.Integer(),
    tpch.ents.Column.Type.IDENTIFIER: sa.Integer(),
    tpch.ents.Column.Type.DATE: sa.Date(),
    tpch.ents.Column.Type.DOUBLE: sa.Float(),
    tpch.ents.Column.Type.VARCHAR: sa.String(),
}


ENTS = [
    tpch.ents.Customer,
    tpch.ents.LineItem,
    tpch.ents.Nation,
    tpch.ents.Order,
    tpch.ents.Part,
    tpch.ents.PartSupplier,
    tpch.ents.Region,
    tpch.ents.Supplier,
]


def build_sa_tables(*, metadata: ta.Optional[sa.MetaData] = None) -> ta.Sequence[sa.Table]:
    if metadata is None:
        metadata = sa.MetaData()
    check.isinstance(metadata, sa.MetaData)

    sats = []
    for ent in ENTS:
        sacs = []
        for f in dc.fields(ent):
            if tpch.ents.Column not in f.metadata:
                continue
            tc = check.isinstance(f.metadata[tpch.ents.Column], tpch.ents.Column)
            sac = sa.Column(tc.name, SA_TYPES_BY_TPCH_TYPE[tc.type], primary_key=f.name in ent.__meta__.primary_key)
            sacs.append(sac)

        sat = sa.Table(ent.__name__.lower(), metadata, *sacs)
        sats.append(sat)

    return sats


def populate_sa_tables(conn: sa.engine.Connection, metadata: sa.MetaData) -> None:
    check.isinstance(conn, sa.engine.Connection)
    check.isinstance(metadata, sa.MetaData)

    cust_sat = check.single(t for t in metadata.tables.values() if t.name == 'customer')
    cg = tpch.gens.CustomerGenerator(10, 1, 20)
    for c in itertools.islice(cg, 100):
        dct = {}
        for f in dc.fields(c):
            try:
                col = check.isinstance(f.metadata[tpch.ents.Column], tpch.ents.Column)
            except KeyError:
                continue
            dct[col.name] = getattr(c, f.name)
        conn.execute(cust_sat.insert(), [dct])
