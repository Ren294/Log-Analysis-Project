from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName("Final") \
    .master("local[*]") \
    .config("spark.sql.warehouse.dir", "/user/hive/warehouse")\
    .config("spark.sql.catalogImplementation", "hive")\
    .getOrCreate()

schema = StructType([
    StructField("host", StringType(), True),
    StructField("time", StringType(), True),
    StructField("method", StringType(), True),
    StructField("url", StringType(), True),
    StructField("protocol", StringType(), True),
    StructField("response", IntegerType(), True),
    StructField("bytes", IntegerType(), True),
    StructField("time_added", StringType(), True),
    StructField("extension", StringType(), True)
])

df = spark.read.csv("hdfs://localhost:9000/output/nasa_log", schema=schema, header=False)

f_df = df.select(
    col("host"),
    to_timestamp(col("time"), "dd/MMM/yyyy:HH:mm:ss Z").alias("time"),
    col("method"),
    col("url"),
    col("protocol"),
    col("response"),
    col("bytes"),
    to_timestamp(col("time_added"), "yyyy-MM-dd'T'HH:mm:ss.SSSXXX").alias("time_added"),
    col("extension")
)

fa_df = f_df \
    .withColumn('ts_year', year(col("time")).cast(IntegerType()))\
    .withColumn('ts_month', month(col("time")).cast(IntegerType()))\
    .withColumn('ts_day', dayofmonth(col("time")).cast(IntegerType()))\
    .withColumn('ts_hour', hour(col("time")).cast(IntegerType()))\
    .withColumn("ts_minute", minute(col("time")).cast(IntegerType()))\
    .withColumn("ts_sec", second(col("time")).cast(IntegerType())) \
    .withColumn("ts_dayOfWeek", dayofweek(col("time")).cast(IntegerType()))

fa_df.write.mode("append").saveAsTable("nasa_log.log")
