from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("pyspark-notebook") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,com.datastax.spark:spark-cassandra-connector_2.12:3.2.0,com.datastax.spark:spark-cassandra-connector-driver_2.12:3.2.0") \
    .config("spark.cassandra.connection.host", 'localhost')\
    .config("spark.cassandra.auth.username", 'cassandra')\
    .config("spark.cassandra.auth.password", 'cassandra')\
    .getOrCreate()

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "nasa_log") \
    .option("startingOffsets", "earliest") \
    .option("maxOffsetsPerTrigger", 10000) \
    .load()


df = df.selectExpr("CAST(value AS STRING)")

df_1 = df.select(
    regexp_extract(col("value"), r'^(\S+)', 1).alias("remotehost"),
    regexp_extract(col("value"), r'^\S+\s+\S+\s+\S+\s+\[([^\]]+)\]', 1).alias("date"),
    regexp_extract(col("value"), r'\"(\S+)\s(\S+)\s*(\S*)\"', 1).alias("method"),
    regexp_extract(col("value"), r'\"(\S+)\s(\S+)\s*(\S*)\"', 2).alias("url"),
    regexp_extract(col("value"), r'\"(\S+)\s(\S+)\s*(\S*)\"', 3).alias("protocol"),
    regexp_extract(col("value"), r'\s(\d{3})\s', 1).alias("status").cast(IntegerType()),
    regexp_extract(col("value"), r'\s(\d+)$', 1).alias("bytes").cast(IntegerType())
).withColumn('time_added', unix_timestamp().cast("timestamp"))\
.withColumn("extension", when(split(col("url"), "\\.").getItem(1).isNull(), "None")
                                    .otherwise(split(col("url"), "\\.").getItem(1)))

df_1 = df_1.na.drop(subset=["remotehost", "date"])

def process_row(df, epoch_id):
    df.write\
        .format("org.apache.spark.sql.cassandra")\
        .mode('append')\
        .options(table="nasalog", keyspace="loganalysis")\
        .save()
    df.write.mode("append").csv("hdfs://localhost:9000/output/nasa_log")

df_1 \
    .writeStream \
    .option("checkpointLocation", "file:///home/nhomb/Document/checkpoint") \
    .foreachBatch(process_row) \
    .start() \
    .awaitTermination()
