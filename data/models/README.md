# Data Source 
Epoch AI, ‘Data on Notable AI Models’. Published online at epoch.ai. Retrieved from ‘https://epoch.ai/data/notable-ai-models’ [online resource]. Accessed 7 Jun 2025.

# AI Models Database Conversion

This project converts the `notable_ai_models.csv` dataset into SQL format for database import.

## Generated Files

### 1. `ai_models.sql`
- Complete SQL table schema with detailed field comments
- Includes all 41 columns from the CSV with appropriate data types
- Contains indexes for optimized querying
- English documentation with examples for each field

### 2. `ai_models_insert.sql`
- SQL INSERT statements for all 956 records from the CSV
- Properly formatted values with SQL escaping
- Ready to import into any SQL database

### 3. `convert.py` 
- Python conversion script that processes the CSV data
- Handles data type conversions (numbers, dates, booleans)
- Escapes SQL strings properly
- Progress tracking during conversion

## Usage

### Prerequisites
```bash
pip install pandas
```

### Running the Conversion
```bash
python convert.py
```

### Database Setup
```sql
-- 1. Create the table structure
\i ai_models.sql

-- 2. Import the data
\i ai_models_insert.sql
```

## Features

### Data Type Handling
- **BIGINT**: Parameter counts, dataset sizes
- **DECIMAL**: Scientific notation numbers, costs, training time
- **DATE**: Publication dates in YYYY-MM-DD format
- **TEXT**: Long descriptions, abstracts, notes
- **VARCHAR**: Short text fields with size limits
- **BOOLEAN**: Frontier model flags

### Data Quality
- **NULL handling**: Empty/missing values converted to SQL NULL
- **String escaping**: Single quotes properly escaped
- **Scientific notation**: Large numbers properly converted
- **Encoding**: UTF-8 support for international characters

### Schema Highlights
- **41 columns** covering all aspects of AI models
- **Indexes** on frequently queried fields
- **Comments** explaining each field with examples
- **Foreign key ready** structure for relational databases

## Example Queries

```sql
-- Find all models by OpenAI
SELECT model, publication_date, parameters 
FROM ai_models 
WHERE organization LIKE '%OpenAI%';

-- Get frontier models with >100B parameters
SELECT model, parameters, training_compute_flop 
FROM ai_models 
WHERE frontier_model = TRUE AND parameters > 100000000000;

-- Models by country
SELECT country_of_organization, COUNT(*) as model_count
FROM ai_models 
GROUP BY country_of_organization 
ORDER BY model_count DESC;
```

## Data Statistics
- **Total Records**: 956 AI models
- **Date Range**: 1950-2025
- **Organizations**: Academia and Industry
- **Domains**: Language, Vision, Multimodal, Robotics, etc. 