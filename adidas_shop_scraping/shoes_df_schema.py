
from pyspark.sql.types import StructType, StructField, DecimalType, StringType, TimestampType

shoes_df_schema = (
        StructType
                ([

                StructField("price", StringType(), False),
                StructField("title", StringType(), True),
                StructField("subtitle", StringType(), True),
                StructField("number_of_color", StringType(), True),
                StructField("badge", StringType(), True),
                StructField("date", StringType(), False)


        ])
)
