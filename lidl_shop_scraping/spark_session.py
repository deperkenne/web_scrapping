
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr, regexp_replace
from scripts.regsetup import description
from sqlalchemy.future import select

spark = SparkSession.builder \
    .appName("Sparksession") \
    .getOrCreate()


df = spark.read.format("parquet").load("C:/Users/Win11 Pro/Downloads/delta-lake-azure-databricks-deep-dive/delta lake demo/Data Files/YellowTaxisParquet\YellowTaxis1.parquet")
df.show(2)


def line_formating():
    col_to_modify = ["description", "images"]
    df = spark.read.format("csv").option("header", "true").option("delimiter", ";").load("Baby&Kind_update.csv")
    for c in df.columns:
        if c in col_to_modify:
            if c == "images":
                df = df.withColumn(c, expr(f"replace({c}, ';', ',')"))
            df = df.withColumn(c, expr(f"replace({c}, '\"\"', '\"')"))
            df = df.withColumn(c, regexp_replace(c, '^"|"$', ''))
    return df



def show_data(df):
  df.createTempView("my_temp_view")
  df = spark.sql("""
      SELECT CabNumber,DriverLicenseNumber
      FROM my_temp_view
      WHERE DriverLicenseNumber = "5131685"
      LIMIT 20
  """)

  '''
  df = spark.sql("""
    SELECT get_json_object(images, '$.images') AS Farben
    FROM my_temp_view
  """)
  '''
  df.show()



#show_data(df)

