# AI Model Insights Analysis Requirement

## Data Source 
`data/models/notable_ai_models.sql` is the data format definition, and the database file is located in `db/ai_insights.db`.

## Insight Mining Requirements
I want to extract comprehensive model insights:
- Analyze all AI models with a scatter plot where:
  - X-axis: Model release year
  - Y-axis: Model parameter count (trainable parameters) 
  - Y-axis scale: Logarithmic (log10) to handle the wide range of parameter sizes
  - domain as series differentiation (The primary domain(s) the model is designed for)

folder_name=insights/model_size
Implementation approach divided into four stages:

## Stage 1.a: SQL Query Generation
Based on the database schema and insight mining requirements, 
write the corresponding SQL query to extract relevant data from the database.
Output to `$folder_name/extract.sql` file.

## Stage 1.b: Data Statistics SQL
Based on the database schema and insight mining requirements, generate SQL queries for statistical analysis of the database across various dimensions, which will guide the design of coordinate axis value ranges, number of series, etc. for subsequent charts.
Output to `$folder_name/stat.sql` 

## Stage 2: Data Extraction
Create an python script to execute the sql and save it as `$folder_name/extract.py`
This Python program takes a database path as input, two sql files as input.
The output file:
- the first file named `$folder_name/data.json` is a JSON format data containing the SQL execution result. This JSON format needs to be directly compatible with the echarts data format.
- the second file named `$folder_name/stat.json` is a JSON format data containing the SQL execution result.


## Stage 3: ECharts Design & HTML 
Based on the files output from the above steps, please generate ECharts format data script + simple HTML that can be directly opened and run locally through a simple HTTP server.
Reference this webpage design: https://echarts.apache.org/examples/zh/editor.html?c=scatter-painter-choice
Output `$folder_name/index.html`

