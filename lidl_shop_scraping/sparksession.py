from pyspark.pandas.typedef import infer_return_type
from pyspark.sql import SparkSession


spark = (
          SparkSession
                .builder
                .appName("Yello_test")
                .master("local[*]")
                .getOrCreate()

)

df_taxi = spark.read.format("csv").option("header",True).option("inferSchema", True).load("CsvFiles/silver_lild_data.csv")
print(df_taxi.schema)
df_taxi.createOrReplaceTempView("my_view")

def sql_spark():
    df1 = spark.sql("""
        SELECT old_price
        FROM my_view
        WHERE old_price RLIKE '[0-9],[0-9]'
    """)

    df1.show(10)