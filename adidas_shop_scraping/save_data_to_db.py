from os import truncate

from pyspark.sql import SparkSession

from pyspark.sql.functions import sum as spark_sum, col, trunc, regexp_replace
from shoes_df_schema import shoes_df_schema
from data_transform import  DataTransform


def main():
        # create a spark session
        spark = (
                  SparkSession
                        .builder
                        .appName("adidas_etl")
                        .master("local[*]")
                        .config("spark.driver.memory", "4g")
                        .config("spark.executor.memory", "4g")
                        .config("spark.executor.cores", "4")
                        .config("spark.sql.shuffle.partitions", "200")
                        .config("spark.jars", "postgresql-42.7.3.jar")  # PostgreSQL driver
                        .getOrCreate()

        )

        # read csv file
        adidas_shoes_DF = (
            spark
                .read
                .schema(shoes_df_schema)
                .csv("shoes_listings.csv", header=True, inferSchema=True)
        )
        df = adidas_shoes_DF.withColumn("price", regexp_replace("price", ",", "."))
        df.show(10, truncate=False)

        # JDBC params connexion
        url = "jdbc:postgresql://192.168.178.194:5432/db"
        properties = {
            "user": "root",
            "password": "root",
            "driver": "org.postgresql.Driver"
        }
        table_name_adidas_shoes = "adidas_shoes"

        df.createOrReplaceTempView("adidas_shoes")

        df_result = spark.sql("""
                  SELECT *,
                         COUNT(*) OVER (PARTITION BY title) AS total_title
                  FROM adidas_shoes
              """)
        df_result.show(10, truncate=False)




        # call data transform function
        transform_data_type_price_to_float_df = DataTransform.transform_data_type_price_to_float(df,"price")
        transform_data_type_date_to_timestamp_df = DataTransform.transform_data_type_date_to_timestamp(transform_data_type_price_to_float_df,"date")
        df = transform_data_type_date_to_timestamp_df

        df.createOrReplaceTempView("adidas_shoes")

        df_result = spark.sql("""
            SELECT *, 
                   
                   COUNT(*) OVER (PARTITION BY title) AS total_title
            FROM adidas_shoes
        """)
        df.show(10,truncate=False)

        # give number product categories


        #save df to table
        #df.write.jdbc(url=url, table=table_name_adidas_shoes,mode="append", properties=properties)

if __name__=="__main__":
    main()
