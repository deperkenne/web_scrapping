import dlt
from pyspark.sql.functions import *

# create a live table Bronze
@dlt.table(
  name="bronze_lidl_products",
  comment="Raw  lidl product data "
)
def bronze_lidl_products():
  df_bronze= spark.read.format("parquet").load("/Volumes/workspace/default/lidl_products/lidl_product.parquet")
  df_bronze = (
                df_bronze
                .dropDuplicates()
                .withColumn("productId", monotonically_increasing_id()) # add ProductId monotonically increasing
                .withColumn("last_updated", current_timestamp())
               )

  return df_bronze


# Create a live table Silver
@dlt.table(
   name="silver_ldl_products",
   comment="validated lidl product data"
)
@dlt.expect_all_or_drop({
    "old_price": "old_price IS NOT NULL OR old_price > 0",
    "title": "title IS NOT  NULL",
    "category": "category IS NOT NULL",
    "productId": "productId IS NOT NULL"
})
def silver_products():
    df = dlt.read("bronze_lidl_products")

    # Standard transformation
    transformed = (
        df
        .filter(col("title") != "title") 
        .dropDuplicates(["productId"])
        .withColumnRenamed("old_price", "temp_price")
        .withColumnRenamed("new_price", "old_price")
        .withColumnRenamed("temp_price", "new_price")
        .withColumn("discount", round(col("discount"), 2))
    )
    
    return transformed

  
