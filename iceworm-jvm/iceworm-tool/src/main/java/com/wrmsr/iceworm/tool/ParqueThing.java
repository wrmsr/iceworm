package com.wrmsr.iceworm.tool;

import com.wrmsr.iceworm.util.MoreFiles;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.parquet.bytes.BytesInput;
import org.apache.parquet.column.ColumnDescriptor;
import org.apache.parquet.column.Encoding;
import org.apache.parquet.column.page.DataPage;
import org.apache.parquet.column.page.DataPageV1;
import org.apache.parquet.column.page.PageReadStore;
import org.apache.parquet.column.page.PageReader;
import org.apache.parquet.hadoop.ParquetFileReader;
import org.apache.parquet.hadoop.ParquetFileWriter;
import org.apache.parquet.hadoop.metadata.CompressionCodecName;
import org.apache.parquet.hadoop.metadata.ParquetMetadata;
import org.apache.parquet.schema.MessageType;
import org.apache.parquet.schema.MessageTypeParser;
import org.apache.parquet.schema.PrimitiveType;
import org.apache.parquet.schema.Types;

import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;

import static org.apache.parquet.column.Encoding.BIT_PACKED;
import static org.apache.parquet.column.Encoding.PLAIN;
import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;

public class ParqueThing
{
    private static final MessageType SCHEMA = MessageTypeParser.parseMessageType("" +
            "message m {" +
            "  required group a {" +
            "    required binary b;" +
            "  }" +
            "  required group c {" +
            "    required int64 d;" +
            "  }" +
            "}");
    private static final String[] PATH1 = {"a", "b"};
    private static final ColumnDescriptor C1 = SCHEMA.getColumnDescription(PATH1);
    private static final String[] PATH2 = {"c", "d"};
    private static final ColumnDescriptor C2 = SCHEMA.getColumnDescription(PATH2);

    private static final byte[] BYTES1 = {0, 1, 2, 3};
    private static final byte[] BYTES2 = {1, 2, 3, 4};
    private static final byte[] BYTES3 = {2, 3, 4, 5};
    private static final byte[] BYTES4 = {3, 4, 5, 6};
    private static final CompressionCodecName CODEC = CompressionCodecName.UNCOMPRESSED;

    private static final org.apache.parquet.column.statistics.Statistics<?> EMPTY_STATS = org.apache.parquet.column.statistics.Statistics
            .getBuilderForReading(Types.required(PrimitiveType.PrimitiveTypeName.BINARY).named("test_binary")).build();

    public static void main(String[] args) throws Throwable
    {
        File testFile = new File(args[0]);

        Path path = new Path(testFile.toURI());
        Configuration configuration = new Configuration();

        ParquetFileWriter w = new ParquetFileWriter(configuration, SCHEMA, path);
        w.start();
        w.startBlock(3);
        w.startColumn(C1, 5, CODEC);
        long c1Starts = w.getPos();
        w.writeDataPage(2, 4, BytesInput.from(BYTES1), EMPTY_STATS, BIT_PACKED, BIT_PACKED, PLAIN);
        w.writeDataPage(3, 4, BytesInput.from(BYTES1), EMPTY_STATS, BIT_PACKED, BIT_PACKED, PLAIN);
        w.endColumn();
        long c1Ends = w.getPos();
        w.startColumn(C2, 6, CODEC);
        long c2Starts = w.getPos();
        w.writeDataPage(2, 4, BytesInput.from(BYTES2), EMPTY_STATS, BIT_PACKED, BIT_PACKED, PLAIN);
        w.writeDataPage(3, 4, BytesInput.from(BYTES2), EMPTY_STATS, BIT_PACKED, BIT_PACKED, PLAIN);
        w.writeDataPage(1, 4, BytesInput.from(BYTES2), EMPTY_STATS, BIT_PACKED, BIT_PACKED, PLAIN);
        w.endColumn();
        long c2Ends = w.getPos();
        w.endBlock();
        w.startBlock(4);
        w.startColumn(C1, 7, CODEC);
        w.writeDataPage(7, 4, BytesInput.from(BYTES3), EMPTY_STATS, BIT_PACKED, BIT_PACKED, PLAIN);
        w.endColumn();
        w.startColumn(C2, 8, CODEC);
        w.writeDataPage(8, 4, BytesInput.from(BYTES4), EMPTY_STATS, BIT_PACKED, BIT_PACKED, PLAIN);
        w.endColumn();
        w.endBlock();
        w.end(new HashMap<String, String>());

        ParquetMetadata readFooter = ParquetFileReader.readFooter(configuration, path);
        assertEquals("footer: " + readFooter, 2, readFooter.getBlocks().size());
        assertEquals(c1Ends - c1Starts, readFooter.getBlocks().get(0).getColumns().get(0).getTotalSize());
        assertEquals(c2Ends - c2Starts, readFooter.getBlocks().get(0).getColumns().get(1).getTotalSize());
        assertEquals(c2Ends - c1Starts, readFooter.getBlocks().get(0).getTotalByteSize());
        HashSet<Encoding> expectedEncoding = new HashSet<Encoding>();
        expectedEncoding.add(PLAIN);
        expectedEncoding.add(BIT_PACKED);
        assertEquals(expectedEncoding, readFooter.getBlocks().get(0).getColumns().get(0).getEncodings());

        { // read first block of col #1
            ParquetFileReader r = new ParquetFileReader(configuration, readFooter.getFileMetaData(), path,
                    Arrays.asList(readFooter.getBlocks().get(0)), Arrays.asList(SCHEMA.getColumnDescription(PATH1)));
            PageReadStore pages = r.readNextRowGroup();
            assertEquals(3, pages.getRowCount());
            validateContains(SCHEMA, pages, PATH1, 2, BytesInput.from(BYTES1));
            validateContains(SCHEMA, pages, PATH1, 3, BytesInput.from(BYTES1));
            assertNull(r.readNextRowGroup());
        }

        { // read all blocks of col #1 and #2

            ParquetFileReader r = new ParquetFileReader(configuration, readFooter.getFileMetaData(), path,
                    readFooter.getBlocks(), Arrays.asList(SCHEMA.getColumnDescription(PATH1), SCHEMA.getColumnDescription(PATH2)));

            PageReadStore pages = r.readNextRowGroup();
            assertEquals(3, pages.getRowCount());
            validateContains(SCHEMA, pages, PATH1, 2, BytesInput.from(BYTES1));
            validateContains(SCHEMA, pages, PATH1, 3, BytesInput.from(BYTES1));
            validateContains(SCHEMA, pages, PATH2, 2, BytesInput.from(BYTES2));
            validateContains(SCHEMA, pages, PATH2, 3, BytesInput.from(BYTES2));
            validateContains(SCHEMA, pages, PATH2, 1, BytesInput.from(BYTES2));

            pages = r.readNextRowGroup();
            assertEquals(4, pages.getRowCount());

            validateContains(SCHEMA, pages, PATH1, 7, BytesInput.from(BYTES3));
            validateContains(SCHEMA, pages, PATH2, 8, BytesInput.from(BYTES4));

            assertNull(r.readNextRowGroup());
        }
    }

    private static void validateContains(
            MessageType schema,
            PageReadStore pages,
            String[] path,
            int values,
            BytesInput bytes
    )
            throws IOException
    {
        PageReader pageReader = pages.getPageReader(schema.getColumnDescription(path));
        DataPage page = pageReader.readPage();
        assertEquals(values, page.getValueCount());
        assertArrayEquals(bytes.toByteArray(), ((DataPageV1) page).getBytes().toByteArray());
    }
}
