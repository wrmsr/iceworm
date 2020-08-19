package com.wrmsr.iceworm.spark;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.api.java.UDF1;
import org.apache.spark.sql.expressions.UserDefinedFunction;
import org.apache.spark.sql.types.DataTypes;
import scala.collection.Seq;
import scala.collection.TraversableLike;

import static org.apache.spark.sql.functions.*;

public class ExampleSql
{
    public static void main(String[] args)
            throws Throwable
    {
        SparkSession spark = SparkSession
                .builder()
                .appName("Java Spark SQL basic example")
                // .config("spark.some.config.option", "some-value")
                .getOrCreate();

        Dataset<Row> df = spark.read().format("com.databricks.spark.csv")
                .option("delimiter", "\t")
                .load("src/test/resources/com/wrmsr/iceworm/spark/users.tsv");

        UserDefinedFunction mode = udf(
                (UDF1<Seq<String>, Object>) TraversableLike::headOption, DataTypes.StringType);

        df.select(mode.apply(col("vs"))).show();

        System.out.println(df);
    }
}
