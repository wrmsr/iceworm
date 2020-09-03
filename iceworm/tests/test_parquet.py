"""
https://arrow.apache.org/docs/python/parquet.html
"""
import os.path
import tempfile

import pytest


@pytest.mark.xfail()
def test_pyarrow_parquet():
    import pyarrow as pa
    import pyarrow.parquet as pq

    # FIXME fuck pandas
    # with pytest.raises(ImportError):
    #     import pandas  # noqa

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


@pytest.mark.xfail()
def test_fastparquet_parquet():
    import pandas as pd
    import fastparquet

    d = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data=d)

    dp = tempfile.mkdtemp()
    fp = os.path.join(dp, 'example.parquet')
    fastparquet.write(fp, df)

    pf = fastparquet.ParquetFile(fp)
    df2 = pf.to_pandas()
    print(df2)
