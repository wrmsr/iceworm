"""
https://arrow.apache.org/docs/python/parquet.html
"""
import os.path
import tempfile

import pyarrow as pa
import pyarrow.parquet as pq
import pytest


@pytest.mark.xfail()
def test_parquet():
    with pytest.raises(ImportError):
        import pandas  # noqa

    # pq.ParquetDataset

    # schema = pa.schema([
    #     ('id', pa.int32()),
    #     ('data', pa.string()),
    # ])

    data = [
        pa.array([1, 2, 3, 4]),
        pa.array(['foo', 'bar', 'baz', None]),
        pa.array([True, None, False, True]),
    ]
    batch = pa.RecordBatch.from_arrays(data, ['f0', 'f1', 'f2'])
    batches = [batch] * 5
    table = pa.Table.from_batches(batches)
    print(table)
    print(list(table))

    dp = tempfile.mkdtemp()
    fp = os.path.join(dp, 'example.parquet')
    pq.write_table(table, fp)
    print(fp)

    table2 = pq.read_table(fp, columns=['f0', 'f1', 'f2'])
    print(table2)
    print(list(table2))
