
# from pyspark.sql.functions import *
# from pyspark.sql.types import *
# from pyspark.sql import SparkSession

# spark = SparkSession.builder \
#     .appName("pyspark-notebook") \
#     .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,com.datastax.spark:spark-cassandra-connector_2.12:3.0.0,com.datastax.spark:spark-cassandra-connector-driver_2.12:3.0.0") \
#     .config("spark.cassandra.connection.host",'localhost')\
#     .config("spark.cassandra.auth.username",'cassandra')\
#     .config("spark.cassandra.auth.password",'cassandra')\
#     .getOrCreate()

# df = spark.readStream.format("kafka") \
#     .option("kafka.bootstrap.servers", "localhost:9092") \
#     .option("subscribe", "nasa_log") \
#     .option("startingOffsets", "earliest")\
#     .option("maxOffsetsPerTrigger", 10000)\
#     .load()
# split_logic = split(col("url"),"\.").getItem(1)

# df =df.selectExpr("CAST(value AS STRING)")

# df_1 = df.select(
#     split(col("value"), ",").getItem(1).alias("host"),
#     split(col("value"), ",").getItem(2).alias("time"),
#     split(col("value"), ",").getItem(3).alias("method"),
#     split(col("value"), ",").getItem(4).alias("url"),
#     split(col("value"), ",").getItem(5).alias("response"),
#     split(col("value"), ",").getItem(6).alias("bytes"),
# ).withColumn('time_added',unix_timestamp())\
# .withColumn("extension",when(split_logic.isNull(),"None").otherwise(split_logic))


# def process_row(df, epoch_id):
#     df.write\
#     .format("org.apache.spark.sql.cassandra")\
#     .mode('append')\
#     .options(table="nasalog", keyspace="loganalysis")\
#     .save()
#     df.write.mode("append").csv("hdfs://localhost:9000/output/nasa_log")

# df_1 \
#     .writeStream \
#     .option("checkpointLocation", "file:///home/nhomb/Document/checkpoint") \
#     .foreachBatch(process_row) \
#     .start() \
#     .awaitTermination()
    
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

df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092").option("subscribe", "nasa_log").option("startingOffsets", "earliest").option("maxOffsetsPerTrigger", 10000).load()

split_logic = split(col("url"), "\\.").getItem(1)

df = df.selectExpr("CAST(value AS STRING)")

df_1 = df.select(
    split(col("value"), ",").getItem(1).alias("host"),
    from_unixtime(split(col("value"), ",").getItem(2)).cast("timestamp").alias("time"),
    split(col("value"), ",").getItem(3).alias("method"),
    split(col("value"), ",").getItem(4).alias("url"),
    split(col("value"), ",").getItem(5).alias("response").cast(IntegerType()),
    split(col("value"), ",").getItem(6).alias("bytes").cast(IntegerType()),
).withColumn('time_added', unix_timestamp().cast("timestamp"))\
.withColumn("extension", when(split_logic.isNull(), "None").otherwise(split_logic))
df_1 = df_1.na.drop(subset=["host", "time"])
def process_row(df, epoch_id):
    df.write\
    .format("org.apache.spark.sql.cassandra")\
    .mode('append')\
    .options(table="log", keyspace="loganalysis")\
    .save()
    #.options(table="nasalog", keyspace="loganalysis")
    # df.write.mode("append").csv("hdfs://localhost:9000/output/nasa_log")

df_1 \
    .writeStream \
    .option("checkpointLocation", "file:///home/nhomb/Document/checkpoint") \
    .foreachBatch(process_row) \
    .start() \
    .awaitTermination()
