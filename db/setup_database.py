#!/usr/bin/env python3
"""
Database Setup Script

This script automatically reads all *.sql and *_insert.sql files from the data directory
and executes them in a local SQLite database.

Usage:
    python setup_database.py [--db-path database.db]
"""

import os
import sqlite3
import argparse
import glob
from pathlib import Path
from typing import List, Tuple
import logging
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def find_sql_files(data_dir: str) -> Tuple[List[str], List[str]]:
    """
    Find all SQL files in the data directory.
    
    Args:
        data_dir: Path to the data directory
        
    Returns:
        Tuple of (schema_files, insert_files)
    """
    schema_files = []
    insert_files = []
    
    # Recursively search for SQL files
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.sql'):
                file_path = os.path.join(root, file)
                if file.endswith('_insert.sql'):
                    insert_files.append(file_path)
                else:
                    schema_files.append(file_path)
    
    # Sort files for consistent execution order
    schema_files.sort()
    insert_files.sort()
    
    return schema_files, insert_files


def convert_postgres_to_sqlite(sql_content: str) -> str:
    """
    Convert PostgreSQL syntax to SQLite compatible syntax.
    
    Args:
        sql_content: SQL content with PostgreSQL syntax
        
    Returns:
        SQL content compatible with SQLite
    """
    # Remove COMMENT ON statements (SQLite doesn't support them)
    sql_content = re.sub(r'COMMENT ON .*?;', '', sql_content, flags=re.DOTALL)
    
    # Convert DECIMAL to REAL for SQLite
    sql_content = re.sub(r'DECIMAL\(\d+,\d+\)', 'REAL', sql_content)
    
    # Convert VARCHAR(n) to TEXT for SQLite
    sql_content = re.sub(r'VARCHAR\(\d+\)', 'TEXT', sql_content)
    
    # Convert BIGINT to INTEGER for SQLite
    sql_content = re.sub(r'BIGINT', 'INTEGER', sql_content)
    
    # Convert BOOLEAN to INTEGER for SQLite
    sql_content = re.sub(r'BOOLEAN', 'INTEGER', sql_content)
    
    # Remove empty lines and clean up
    lines = [line.strip() for line in sql_content.split('\n')]
    lines = [line for line in lines if line and not line.startswith('--')]
    
    return '\n'.join(lines)


def execute_sql_file(cursor: sqlite3.Cursor, file_path: str) -> None:
    """
    Execute a SQL file.
    
    Args:
        cursor: SQLite cursor
        file_path: Path to the SQL file
    """
    logger.info(f"Executing SQL file: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Convert PostgreSQL syntax to SQLite
        sql_content = convert_postgres_to_sqlite(sql_content)
        
        # For insert files, use executescript which handles multiple statements better
        if file_path.endswith('_insert.sql'):
            # Try to execute the entire file at once with error handling
            try:
                cursor.executescript(sql_content)
                logger.info(f"Successfully executed: {file_path}")
                return
            except sqlite3.Error as e:
                logger.warning(f"executescript failed for {file_path}: {e}")
                logger.info("Falling back to statement-by-statement execution...")
        
        # Split SQL content by semicolons and execute each statement
        statements = sql_content.split(';')
        
        successful_statements = 0
        failed_statements = 0
        
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    successful_statements += 1
                except sqlite3.Error as e:
                    failed_statements += 1
                    if failed_statements <= 10:  # Only log first 10 errors
                        logger.warning(f"Warning executing statement in {file_path}: {e}")
                        logger.warning(f"Statement preview: {statement[:100]}...")
                    elif failed_statements == 11:
                        logger.warning(f"Suppressing further error messages for {file_path}...")
                    # Continue with other statements
                    continue
        
        logger.info(f"Successfully executed: {file_path}")
        logger.info(f"  - Successful statements: {successful_statements}")
        if failed_statements > 0:
            logger.warning(f"  - Failed statements: {failed_statements}")
        
    except Exception as e:
        logger.error(f"Error executing {file_path}: {e}")
        raise


def setup_database(db_path: str, data_dir: str) -> None:
    """
    Set up the SQLite database by executing all SQL files.
    
    Args:
        db_path: Path to the SQLite database file
        data_dir: Path to the data directory containing SQL files
    """
    logger.info(f"Setting up database: {db_path}")
    logger.info(f"Data directory: {data_dir}")
    
    # Find all SQL files
    schema_files, insert_files = find_sql_files(data_dir)
    
    logger.info(f"Found {len(schema_files)} schema files and {len(insert_files)} insert files")
    
    if not schema_files and not insert_files:
        logger.warning("No SQL files found in the data directory")
        return
    
    # Create database connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Execute schema files first
        logger.info("Executing schema files...")
        for schema_file in schema_files:
            execute_sql_file(cursor, schema_file)
        
        # Commit schema changes
        conn.commit()
        logger.info("Schema files executed successfully")
        
        # Execute insert files
        if insert_files:
            logger.info("Executing insert files...")
            for insert_file in insert_files:
                execute_sql_file(cursor, insert_file)
            
            # Commit insert changes
            conn.commit()
            logger.info("Insert files executed successfully")
        
        # Get database statistics
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        logger.info(f"Database setup complete. Created {len(tables)} tables:")
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            logger.info(f"  - {table[0]}: {count} rows")
    
    except Exception as e:
        logger.error(f"Error setting up database: {e}")
        conn.rollback()
        raise
    
    finally:
        conn.close()


def main():
    """Main function to handle command line arguments and execute the script."""
    parser = argparse.ArgumentParser(
        description="Set up SQLite database from SQL files in data directory"
    )
    parser.add_argument(
        '--db-path',
        type=str,
        default='./db/ai_insights.db',
        help='Path to the SQLite database file (default: ai_insights.db)'
    )
    parser.add_argument(
        '--data-dir',
        type=str,
        default='./data',
        help='Path to the data directory containing SQL files (default: ./data)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force recreate database (delete existing database)'
    )
    
    args = parser.parse_args()
    
    # Convert to absolute paths
    db_path = os.path.abspath(args.db_path)
    data_dir = os.path.abspath(args.data_dir)
    
    # Check if data directory exists
    if not os.path.exists(data_dir):
        logger.error(f"Data directory does not exist: {data_dir}")
        return 1
    
    # Handle force recreation
    if args.force and os.path.exists(db_path):
        logger.info(f"Removing existing database: {db_path}")
        os.remove(db_path)
    
    # Check if database already exists
    if os.path.exists(db_path) and not args.force:
        response = input(f"Database {db_path} already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            logger.info("Database setup cancelled")
            return 0
        os.remove(db_path)
    
    try:
        setup_database(db_path, data_dir)
        logger.info(f"Database setup completed successfully: {db_path}")
        return 0
    
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main()) 