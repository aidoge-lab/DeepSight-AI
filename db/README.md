# Database Setup

This directory contains scripts to set up and manage the SQLite database for the AI Insights Charts project.

## Setup Script

The `setup_database.py` script automatically reads all SQL files from the `data` directory and executes them in a local SQLite database.

### Features

- **Automatic file discovery**: Recursively finds all `*.sql` and `*_insert.sql` files in the data directory
- **Ordered execution**: Executes schema files first, then insert files
- **Error handling**: Continues execution even if some statements fail, with detailed logging
- **Statistics reporting**: Shows table counts after setup completion
- **Force recreation**: Option to delete and recreate existing databases

### Usage

#### Basic usage (from the db directory):
```bash
python setup_database.py
```

This will create `ai_insights.db` in the current directory using SQL files from `../data`.

#### Custom database path:
```bash
python setup_database.py --db-path /path/to/your/database.db
```

#### Custom data directory:
```bash
python setup_database.py --data-dir /path/to/your/data/directory
```

#### Force recreation of existing database:
```bash
python setup_database.py --force
```

#### Get help:
```bash
python setup_database.py --help
```

### File Naming Convention

The script looks for two types of SQL files:

1. **Schema files**: `*.sql` (but not ending with `_insert.sql`)
   - These contain table creation statements, indexes, etc.
   - Executed first

2. **Insert files**: `*_insert.sql`
   - These contain data insertion statements
   - Executed after schema files

### Example Output

```
2024-01-15 10:30:45,123 - INFO - Setting up database: /path/to/ai_insights.db
2024-01-15 10:30:45,124 - INFO - Data directory: /path/to/data
2024-01-15 10:30:45,125 - INFO - Found 1 schema files and 1 insert files
2024-01-15 10:30:45,126 - INFO - Executing schema files...
2024-01-15 10:30:45,127 - INFO - Executing SQL file: /path/to/data/models/notable_ai_models.sql
2024-01-15 10:30:45,128 - INFO - Successfully executed: /path/to/data/models/notable_ai_models.sql
2024-01-15 10:30:45,129 - INFO - Schema files executed successfully
2024-01-15 10:30:45,130 - INFO - Executing insert files...
2024-01-15 10:30:45,131 - INFO - Executing SQL file: /path/to/data/models/notable_ai_models_insert.sql
2024-01-15 10:30:47,456 - INFO - Successfully executed: /path/to/data/models/notable_ai_models_insert.sql
2024-01-15 10:30:47,457 - INFO - Insert files executed successfully
2024-01-15 10:30:47,458 - INFO - Database setup complete. Created 1 tables:
2024-01-15 10:30:47,459 - INFO -   - ai_models: 1250 rows
2024-01-15 10:30:47,460 - INFO - Database setup completed successfully: /path/to/ai_insights.db
```

### Requirements

- Python 3.6+
- No external dependencies (uses only standard library modules)

### Error Handling

The script includes robust error handling:

- Individual SQL statement failures are logged but don't stop the entire process
- File reading errors are reported and cause the script to exit
- Database connection errors are handled gracefully
- All changes are committed only after successful execution of each file group 