#!/usr/bin/env python3
"""
CSV to SQL Converter for AI Models Dataset
Converts notable_ai_models.csv to SQL INSERT statements for the ai_models table
"""

import pandas as pd
import re
from datetime import datetime
import sys

def escape_sql_string(value):
    """Escape single quotes and handle None values for SQL strings"""
    if pd.isna(value) or value == '' or str(value).strip() == '':
        return 'NULL'
    
    # Convert to string and escape single quotes
    str_value = str(value).replace("'", "''")
    return f"'{str_value}'"

def convert_to_sql_number(value, is_decimal=False):
    """Convert numeric values to SQL format, handling scientific notation"""
    if pd.isna(value) or value == '' or str(value).strip() == '':
        return 'NULL'
    
    try:
        # Handle scientific notation
        if 'e+' in str(value).lower() or 'e-' in str(value).lower():
            num_value = float(value)
            if is_decimal:
                return str(num_value)
            else:
                return str(int(num_value)) if num_value.is_integer() else str(num_value)
        else:
            if is_decimal:
                return str(float(value))
            else:
                return str(int(float(value)))
    except (ValueError, TypeError):
        return 'NULL'

def convert_to_sql_date(value):
    """Convert date string to SQL DATE format"""
    if pd.isna(value) or value == '' or str(value).strip() == '':
        return 'NULL'
    
    try:
        # Assume the date is in YYYY-MM-DD format
        date_str = str(value).strip()
        # Validate date format
        datetime.strptime(date_str, '%Y-%m-%d')
        return f"'{date_str}'"
    except (ValueError, TypeError):
        return 'NULL'

def convert_to_sql_boolean(value):
    """Convert boolean values to SQL format"""
    if pd.isna(value) or value == '' or str(value).strip() == '':
        return 'NULL'
    
    # Check if it's explicitly True/False or contains True-like values
    str_value = str(value).strip().lower()
    if str_value in ['true', '1', 'yes', 't']:
        return 'TRUE'
    elif str_value in ['false', '0', 'no', 'f']:
        return 'FALSE'
    else:
        return 'NULL'

def generate_insert_statement(row):
    """Generate a single INSERT statement for a row"""
    
    # Map CSV columns to SQL values with appropriate conversions
    values = []
    
    # Model identification
    values.append(escape_sql_string(row.get('Model')))
    values.append(escape_sql_string(row.get('Organization')))
    values.append(convert_to_sql_date(row.get('Publication date')))
    
    # Model capabilities and domain
    values.append(escape_sql_string(row.get('Domain')))
    values.append(escape_sql_string(row.get('Task')))
    
    # Model architecture details
    values.append(convert_to_sql_number(row.get('Parameters')))
    values.append(escape_sql_string(row.get('Parameters notes')))
    
    # Training compute information
    values.append(convert_to_sql_number(row.get('Training compute (FLOP)'), is_decimal=True))
    values.append(escape_sql_string(row.get('Training compute notes')))
    
    # Training dataset information
    values.append(escape_sql_string(row.get('Training dataset')))
    values.append(convert_to_sql_number(row.get('Training dataset size (datapoints)')))
    values.append(escape_sql_string(row.get('Dataset size notes')))
    
    # Confidence and sources
    values.append(escape_sql_string(row.get('Confidence')))
    values.append(escape_sql_string(row.get('Link')))
    values.append(escape_sql_string(row.get('Reference')))
    values.append(convert_to_sql_number(row.get('Citations')))
    values.append(escape_sql_string(row.get('Authors')))
    values.append(escape_sql_string(row.get('Abstract')))
    
    # Organization details
    values.append(escape_sql_string(row.get('Organization categorization')))
    values.append(escape_sql_string(row.get('Country (of organization)')))
    
    # Performance and notability
    values.append(escape_sql_string(row.get('Notability criteria')))
    values.append(escape_sql_string(row.get('Notability criteria notes')))
    
    # Training details
    values.append(convert_to_sql_number(row.get('Epochs'), is_decimal=True))
    values.append(convert_to_sql_number(row.get('Training time (hours)'), is_decimal=True))
    values.append(escape_sql_string(row.get('Training time notes')))
    
    # Hardware information
    values.append(escape_sql_string(row.get('Training hardware')))
    values.append(convert_to_sql_number(row.get('Hardware quantity'), is_decimal=True))
    values.append(convert_to_sql_number(row.get('Hardware utilization'), is_decimal=True))
    
    # Cost information
    values.append(convert_to_sql_number(row.get('Training compute cost (2023 USD)'), is_decimal=True))
    values.append(escape_sql_string(row.get('Compute cost notes')))
    values.append(convert_to_sql_number(row.get('Training power draw (W)')))
    
    # Model relationships
    values.append(escape_sql_string(row.get('Base model')))
    values.append(convert_to_sql_number(row.get('Finetune compute (FLOP)'), is_decimal=True))
    values.append(escape_sql_string(row.get('Finetune compute notes')))
    
    # Training configuration
    values.append(convert_to_sql_number(row.get('Batch size')))
    values.append(escape_sql_string(row.get('Batch size notes')))
    
    # Accessibility information
    values.append(escape_sql_string(row.get('Model accessibility')))
    values.append(escape_sql_string(row.get('Training code accessibility')))
    values.append(escape_sql_string(row.get('Inference code accessibility')))
    values.append(escape_sql_string(row.get('Accessibility notes')))
    
    # Technical specifications
    values.append(escape_sql_string(row.get('Numerical format')))
    values.append(convert_to_sql_boolean(row.get('Frontier model')))
    
    # Generate the INSERT statement
    values_str = ', '.join(values)
    insert_sql = f"INSERT INTO ai_models VALUES ({values_str});"
    
    return insert_sql

def main():
    """Main function to convert CSV to SQL INSERT statements"""
    
    # Read the CSV file
    try:
        print("Reading CSV file...")
        df = pd.read_csv('data/models/notable_ai_models.csv')
        print(f"Successfully loaded {len(df)} records from CSV")
    except FileNotFoundError:
        print("Error: Could not find 'data/models/notable_ai_models.csv'")
        print("Please make sure the CSV file exists in the correct location.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)
    
    # Generate SQL INSERT statements
    print("Converting to SQL INSERT statements...")
    
    output_file = 'notable_ai_models_insert.sql'
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write header comments
            f.write("-- AI Models Data Import\n")
            f.write("-- Generated INSERT statements from notable_ai_models.csv\n")
            f.write(f"-- Total records: {len(df)}\n")
            f.write(f"-- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Write each INSERT statement
            for index, row in df.iterrows():
                try:
                    insert_statement = generate_insert_statement(row)
                    f.write(insert_statement + '\n')
                    
                    # Progress indicator
                    if (index + 1) % 100 == 0:
                        print(f"Processed {index + 1} records...")
                        
                except Exception as e:
                    print(f"Error processing row {index + 1}: {e}")
                    print(f"Row data: {row.get('Model', 'Unknown')}")
                    continue
            
            f.write('\n-- End of INSERT statements\n')
            
        print(f"\nConversion completed successfully!")
        print(f"SQL INSERT statements written to: {output_file}")
        print(f"Total records processed: {len(df)}")
        
    except Exception as e:
        print(f"Error writing to output file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 