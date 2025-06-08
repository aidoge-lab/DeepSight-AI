#!/usr/bin/env python3
"""
Database Test Script

This script tests the SQLite database to ensure it was set up correctly
and contains the expected data.

Usage:
    python test_database.py [--db-path database.db]
"""

import argparse
import logging
import sqlite3
from typing import Any, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_database_connection(db_path: str) -> sqlite3.Connection:
    """Test database connection and return the connection object."""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
        logger.info(f"Successfully connected to database: {db_path}")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Failed to connect to database: {e}")
        raise


def test_table_structure(conn: sqlite3.Connection) -> Dict[str, Any]:
    """Test the table structure and return table information."""
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    table_info = {}

    for table in tables:
        table_name = table["name"]
        logger.info(f"Testing table: {table_name}")

        # Get table schema
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        # Get row count
        cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
        row_count = cursor.fetchone()["count"]

        table_info[table_name] = {
            "columns": len(columns),
            "row_count": row_count,
            "column_details": [
                {
                    "name": col["name"],
                    "type": col["type"],
                    "nullable": not col["notnull"],
                    "primary_key": bool(col["pk"]),
                }
                for col in columns
            ],
        }

        logger.info(f"  - {len(columns)} columns, {row_count} rows")

    return table_info


def test_data_integrity(conn: sqlite3.Connection) -> None:
    """Test data integrity and run some basic queries."""
    cursor = conn.cursor()

    logger.info("Running data integrity tests...")

    # Test ai_models table if it exists
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='ai_models'"
    )
    if cursor.fetchone():
        logger.info("Testing ai_models table...")

        # Test for non-null model names
        cursor.execute(
            "SELECT COUNT(*) as count FROM ai_models WHERE model IS NULL OR model = ''"
        )
        null_models = cursor.fetchone()["count"]
        if null_models > 0:
            logger.warning(f"Found {null_models} rows with null/empty model names")
        else:
            logger.info("✓ All model names are non-null and non-empty")

        # Test for valid publication dates
        cursor.execute(
            "SELECT COUNT(*) as count FROM ai_models WHERE publication_date IS NOT NULL"
        )
        valid_dates = cursor.fetchone()["count"]
        logger.info(f"✓ {valid_dates} rows have valid publication dates")

        # Test for parameter ranges
        cursor.execute(
            "SELECT MIN(parameters) as min_params, MAX(parameters) as max_params FROM ai_models WHERE parameters IS NOT NULL"
        )
        param_range = cursor.fetchone()
        if param_range["min_params"] and param_range["max_params"]:
            logger.info(
                f"✓ Parameter range: {param_range['min_params']:,} to {param_range['max_params']:,}"
            )

        # Test for organization data
        cursor.execute(
            "SELECT COUNT(DISTINCT organization) as org_count FROM ai_models WHERE organization IS NOT NULL"
        )
        org_count = cursor.fetchone()["org_count"]
        logger.info(f"✓ {org_count} unique organizations")

        # Test for frontier models
        cursor.execute(
            "SELECT COUNT(*) as count FROM ai_models WHERE frontier_model = 1"
        )
        frontier_count = cursor.fetchone()["count"]
        logger.info(f"✓ {frontier_count} frontier models")


def run_sample_queries(conn: sqlite3.Connection) -> None:
    """Run sample queries to demonstrate database functionality."""
    cursor = conn.cursor()

    logger.info("Running sample queries...")

    # Check if ai_models table exists
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='ai_models'"
    )
    if not cursor.fetchone():
        logger.info("ai_models table not found, skipping sample queries")
        return

    # Top 5 models by parameters
    logger.info("Top 5 models by parameter count:")
    cursor.execute(
        """
        SELECT model, organization, parameters 
        FROM ai_models 
        WHERE parameters IS NOT NULL 
        ORDER BY parameters DESC 
        LIMIT 5
    """
    )

    for row in cursor.fetchall():
        logger.info(
            f"  - {row['model']} ({row['organization']}): {row['parameters']:,} parameters"
        )

    # Models by publication year
    logger.info("Models by publication year:")
    cursor.execute(
        """
        SELECT strftime('%Y', publication_date) as year, COUNT(*) as count
        FROM ai_models 
        WHERE publication_date IS NOT NULL 
        GROUP BY strftime('%Y', publication_date)
        ORDER BY year DESC
        LIMIT 5
    """
    )

    for row in cursor.fetchall():
        logger.info(f"  - {row['year']}: {row['count']} models")

    # Top organizations by model count
    logger.info("Top organizations by model count:")
    cursor.execute(
        """
        SELECT organization, COUNT(*) as model_count
        FROM ai_models 
        WHERE organization IS NOT NULL 
        GROUP BY organization
        ORDER BY model_count DESC
        LIMIT 5
    """
    )

    for row in cursor.fetchall():
        logger.info(f"  - {row['organization']}: {row['model_count']} models")


def main():
    """Main function to run database tests."""
    parser = argparse.ArgumentParser(
        description="Test SQLite database setup and data integrity"
    )
    parser.add_argument(
        "--db-path",
        type=str,
        default="./db/ai_insights.db",
        help="Path to the SQLite database file (default: ai_insights.db)",
    )

    args = parser.parse_args()

    logger.info(f"Testing database: {args.db_path}")

    try:
        # Test database connection
        conn = test_database_connection(args.db_path)

        # Test table structure
        table_info = test_table_structure(conn)

        if not table_info:
            logger.warning("No tables found in the database")
            return 1

        # Test data integrity
        test_data_integrity(conn)

        # Run sample queries
        run_sample_queries(conn)

        # Summary
        total_tables = len(table_info)
        total_rows = sum(info["row_count"] for info in table_info.values())

        logger.info(f"Database test completed successfully!")
        logger.info(f"Summary: {total_tables} tables, {total_rows} total rows")

        conn.close()
        return 0

    except Exception as e:
        logger.error(f"Database test failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
