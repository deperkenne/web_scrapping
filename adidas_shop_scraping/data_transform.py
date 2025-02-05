from pandas import DataFrame
from pyspark.sql.functions import col, to_timestamp


class DataTransform:

    @staticmethod
    def transform_data_type_price_to_float(df:DataFrame,columnName):
        return df.withColumn(columnName, col(columnName).cast("float"))

    @staticmethod
    def transform_data_type_date_to_timestamp(df,columnName):
         return df.withColumn("date", to_timestamp(col(columnName), "yyyy-MM-dd HH:mm:ss"))