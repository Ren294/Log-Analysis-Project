from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName("Final") \
    .master("local[*]") \
    .config("spark.sql.warehouse.dir", "/user/hive/warehouse")\
    .config("spark.sql.catalogImplementation", "hive")\
    .getOrCreate()

df = spark.read.csv("/output/nasa_log", inferSchema=True)
f_df = df.select(
    col("_c0").alias("host"),
    from_unixtime(col("_c1")).alias("time"),
    col("_c2").alias("method"),
    col("_c3").alias("url"),
    col("_c4").cast("int").alias("response"),
    col("_c5").alias("bytes"),
    from_unixtime(col("_c6")).alias("time_added"),
    col("_c7").alias("extension")
)
fa_df = f_df\
  .withColumn('ts_year', year(col("time")).cast(IntegerType()))\
  .withColumn('ts_month', month(col("time")).cast(IntegerType()))\
  .withColumn('ts_day', dayofmonth(col("time")).cast(IntegerType()))\
  .withColumn('ts_hour', hour(col("time")).cast(IntegerType()))\
  .withColumn("ts_minute", minute(col("time")).cast(IntegerType()))\
  .withColumn("ts_sec", second(col("time")).cast(IntegerType())) \
  .withColumn("ts_dayOfWeek", dayofweek(col("time")).cast(IntegerType()))
  
fa_df.write.mode("append").saveAsTable("nasa_log.log")