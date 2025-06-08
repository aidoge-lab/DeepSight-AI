#!/usr/bin/env python3
"""
AI Models Database Query Examples

This script demonstrates how to query the AI models database
with various useful queries for analysis and insights.

Usage:
    python query_examples.py [--db-path database.db]
"""

import sqlite3
import argparse
import pandas as pd
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIModelsQuery:
    """Class for querying the AI models database."""
    
    def __init__(self, db_path: str):
        """Initialize with database path."""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
    
    def __del__(self):
        """Close database connection."""
        if hasattr(self, 'conn'):
            self.conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a query and return results as list of dictionaries."""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_models_by_year(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get model counts by publication year."""
        query = """
        SELECT 
            strftime('%Y', publication_date) as year,
            COUNT(*) as model_count
        FROM ai_models 
        WHERE publication_date IS NOT NULL 
        GROUP BY strftime('%Y', publication_date)
        ORDER BY year DESC
        LIMIT ?
        """
        return self.execute_query(query, (limit,))
    
    def get_largest_models(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the largest models by parameter count."""
        query = """
        SELECT 
            model,
            organization,
            parameters,
            publication_date,
            domain
        FROM ai_models 
        WHERE parameters IS NOT NULL 
        ORDER BY parameters DESC
        LIMIT ?
        """
        return self.execute_query(query, (limit,))
    
    def get_models_by_organization(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get model counts by organization."""
        query = """
        SELECT 
            organization,
            COUNT(*) as model_count
        FROM ai_models 
        WHERE organization IS NOT NULL 
        GROUP BY organization
        ORDER BY model_count DESC
        LIMIT ?
        """
        return self.execute_query(query, (limit,))
    
    def get_frontier_models(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get all frontier models."""
        query = """
        SELECT 
            model,
            organization,
            publication_date,
            parameters,
            domain,
            notability_criteria
        FROM ai_models 
        WHERE frontier_model = 1
        ORDER BY publication_date DESC
        LIMIT ?
        """
        return self.execute_query(query, (limit,))
    
    def get_models_by_domain(self, domain: str = None) -> List[Dict[str, Any]]:
        """Get models by domain (e.g., 'Language', 'Vision', 'Multimodal')."""
        if domain:
            query = """
            SELECT 
                model,
                organization,
                publication_date,
                parameters,
                domain,
                task
            FROM ai_models 
            WHERE domain LIKE ?
            ORDER BY publication_date DESC
            """
            return self.execute_query(query, (f'%{domain}%',))
        else:
            # Get domain distribution
            query = """
            SELECT 
                domain,
                COUNT(*) as model_count
            FROM ai_models 
            WHERE domain IS NOT NULL
            GROUP BY domain
            ORDER BY model_count DESC
            LIMIT 15
            """
            return self.execute_query(query)
    
    def get_training_cost_analysis(self) -> List[Dict[str, Any]]:
        """Analyze training costs and compute requirements."""
        query = """
        SELECT 
            model,
            organization,
            publication_date,
            parameters,
            training_compute_flop,
            training_compute_cost_usd,
            training_time_hours,
            training_hardware
        FROM ai_models 
        WHERE training_compute_cost_usd IS NOT NULL
        ORDER BY training_compute_cost_usd DESC
        LIMIT 20
        """
        return self.execute_query(query)
    
    def get_recent_models(self, days: int = 365) -> List[Dict[str, Any]]:
        """Get models published in the last N days."""
        query = """
        SELECT 
            model,
            organization,
            publication_date,
            parameters,
            domain,
            notability_criteria
        FROM ai_models 
        WHERE publication_date >= date('now', '-{} days')
        ORDER BY publication_date DESC
        """.format(days)
        return self.execute_query(query)
    
    def search_models(self, search_term: str) -> List[Dict[str, Any]]:
        """Search for models by name, organization, or description."""
        query = """
        SELECT 
            model,
            organization,
            publication_date,
            parameters,
            domain,
            abstract
        FROM ai_models 
        WHERE model LIKE ? 
           OR organization LIKE ?
           OR abstract LIKE ?
        ORDER BY publication_date DESC
        LIMIT 50
        """
        search_pattern = f'%{search_term}%'
        return self.execute_query(query, (search_pattern, search_pattern, search_pattern))


def print_results_table(results: List[Dict[str, Any]], title: str):
    """Print results in a formatted table."""
    if not results:
        print(f"\n{title}: No results found")
        return
    
    print(f"\n{title}:")
    print("=" * len(title))
    
    # Convert to pandas DataFrame for better formatting
    df = pd.DataFrame(results)
    
    # Format large numbers
    for col in df.columns:
        if 'parameters' in col.lower() or 'cost' in col.lower():
            df[col] = df[col].apply(lambda x: f"{x:,}" if pd.notnull(x) and isinstance(x, (int, float)) else x)
    
    print(df.to_string(index=False, max_rows=20))


def main():
    """Main function to run example queries."""
    parser = argparse.ArgumentParser(
        description="Query examples for AI models database"
    )
    parser.add_argument(
        '--db-path',
        type=str,
        default='ai_insights.db',
        help='Path to the SQLite database file (default: ai_insights.db)'
    )
    
    args = parser.parse_args()
    
    try:
        db = AIModelsQuery(args.db_path)
        
        print("🤖 AI Models Database Query Examples")
        print("=====================================")
        
        # 1. Models by year
        results = db.get_models_by_year(10)
        print_results_table(results, "📅 Models by Publication Year")
        
        # 2. Largest models
        results = db.get_largest_models(10)
        print_results_table(results, "🔢 Largest Models by Parameter Count")
        
        # 3. Top organizations
        results = db.get_models_by_organization(10)
        print_results_table(results, "🏢 Top Organizations by Model Count")
        
        # 4. Frontier models
        results = db.get_frontier_models(15)
        print_results_table(results, "🚀 Recent Frontier Models")
        
        # 5. Domain distribution
        results = db.get_models_by_domain()
        print_results_table(results, "🎯 Models by Domain")
        
        # 6. Language models specifically
        results = db.get_models_by_domain('Language')[:10]
        print_results_table(results, "💬 Recent Language Models")
        
        # 7. Training cost analysis
        results = db.get_training_cost_analysis()
        print_results_table(results, "💰 Most Expensive Models to Train")
        
        # 8. Recent models (last year)
        results = db.get_recent_models(365)[:15]
        print_results_table(results, "🆕 Models from Last Year")
        
        # 9. Search example
        print(f"\n🔍 Search Example: Models related to 'GPT'")
        results = db.search_models('GPT')[:10]
        print_results_table(results, "GPT-related Models")
        
        print(f"\n✅ Query examples completed successfully!")
        print(f"Database: {args.db_path}")
        
    except Exception as e:
        logger.error(f"Error running queries: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 