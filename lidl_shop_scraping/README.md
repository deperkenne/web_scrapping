# Batch Processing
Lidl Products Scraper & ETL Pipeline
===============================

This project performs web scraping of Lidl's online product catalog and processes the data through a simple ETL pipeline. The system:

- Scrapes product data from Lidl's website across multiple categories

- Cleans and formats the scraped data

- Processes it through Bronze (raw) and Silver (validated) layers in Databricks

## Key Features
### Web Scraper
- Scrapes 8 product categories from Lidl.de

- Handles cookie consent and dynamic content loading

- Extracts:

   - Product titles and descriptions

   - Pricing and discount information

   - Product images

   - Category classification

## Data Processing
- CSV cleaning utility
  - Preserves quoted fields
  - Replaces problematic commas in unquoted sections
## ETL Pipeline(Databricks)
### Bronze Layer:
  - Ingest raw scraped data
  - Adds unique procduct IDs
  -  Tracks last update timestamp
### Silver Layer:
  - Applies data quality checks
  - Standardizes column names
  - Removes duplicates
  - Formats numeric values

## Setup Instructions
1. Prerequisites:
  - Python 3.8+
  - Window
  - Chrome browser
  - ChromeDriver matching your browser version
  - Databricks workspace (for ETL portion)
2. Install dependencies:
   - pip install selenium 
   - pip install beautifulsoup4
     

3. Run the scraper:
   - python scraper/main.py
####
4. Process CSV files:
   - python scraper/csv_cleaner.py
####
5. Run ETL pipeline
   1. Create a New Notebook:
      - In your Databricks workspace, click "Create" → "Notebook"
      - Name it ETL_Lidl_Products and select "Python" as the language
   2. Copy the Pipeline Code:
      - copy pipeline Code Data_processing_with_DataBricks(DLT)/ETL_lidl_product/transformations/etl_lidl_product.py into your Notebook
   3. Configure Your Pipeline:
      - Go to "Workflows" → "Delta Live Tables" → "Create Pipeline"
      - Pipeline name: Lidl_Products_ETL
      - Notebook path: Select your ETL_Lidl_Products notebook
      - Storage location: /pipelines/lidl_products
      - Target schema: default (or your preferred database)
      - Click "Start" to execute the pipeline
  ####
## Output
- Raw CSV files per category (e.g., Multimedia.csv)
- Cleaned CSV versions (*_update.csv)
- Processed data in Databricks Delta tables:
- bronze_lidl_products (raw data)
- silver_ldl_products (validated data)
####
## Screenshots
### Lidl ETL
![Lidl_data_pipeline.png](image%2FLidl_data_pipeline.png)

####
### Silver Lidl Table part 1
![silver_lidl_table.png](image%2Fsilver_lidl_table.png)
### Silver Lidl Table part 2
![silver_lidl_table02.png](image%2Fsilver_lidl_table02.png)

