"""CSV processing and analysis service."""

import csv
import json
from typing import Dict, List, Any, Optional
from pathlib import Path

from src.core.logging import get_logger
from src.utils.token_counter import count_tokens

logger = get_logger(__name__)


class CSVService:
    """Service for processing and analyzing CSV files."""

    def __init__(self):
        """Initialize CSV service."""
        pass

    def parse_csv(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a CSV file and return structured data.

        Args:
            file_path: Path to the CSV file

        Returns:
            Dictionary containing parsed CSV data
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                rows = list(reader)

                if not rows:
                    raise ValueError("CSV file is empty")

                headers = rows[0]
                data_rows = rows[1:]

                # Basic statistics
                total_rows = len(data_rows)
                total_columns = len(headers)

                # Column analysis
                column_stats = self._analyze_columns(headers, data_rows)

                # Sample data
                sample_data = data_rows[:5] if len(data_rows) > 5 else data_rows

                result = {
                    "headers": headers,
                    "total_rows": total_rows,
                    "total_columns": total_columns,
                    "column_stats": column_stats,
                    "sample_data": sample_data,
                    "file_path": file_path,
                }

                logger.info(f"Parsed CSV: {total_rows} rows, {total_columns} columns")
                return result

        except Exception as e:
            logger.error(f"Error parsing CSV file {file_path}: {e}")
            raise

    def _analyze_columns(
        self, headers: List[str], data_rows: List[List[str]]
    ) -> Dict[str, Any]:
        """
        Analyze columns for data types and statistics.

        Args:
            headers: Column headers
            data_rows: Data rows

        Returns:
            Column analysis dictionary
        """
        column_stats = {}

        for i, header in enumerate(headers):
            column_data = [row[i] if i < len(row) else "" for row in data_rows]

            # Basic stats
            non_empty_count = sum(1 for cell in column_data if cell.strip())
            empty_count = len(column_data) - non_empty_count

            # Try to determine data type
            data_type = self._infer_data_type(column_data)

            # Unique values (limited to first 100 for performance)
            unique_values = list(
                set(cell for cell in column_data[:100] if cell.strip())
            )
            unique_count = len(unique_values)

            column_stats[header] = {
                "data_type": data_type,
                "total_cells": len(column_data),
                "non_empty_cells": non_empty_count,
                "empty_cells": empty_count,
                "unique_values_count": unique_count,
                "sample_unique_values": unique_values[:10],  # First 10 unique values
            }

        return column_stats

    def _infer_data_type(self, column_data: List[str]) -> str:
        """
        Infer the data type of a column.

        Args:
            column_data: List of cell values

        Returns:
            Inferred data type
        """
        if not column_data:
            return "unknown"

        # Check for numeric data
        numeric_count = 0
        date_count = 0

        for cell in column_data[:100]:  # Check first 100 cells
            cell = cell.strip()
            if not cell:
                continue

            # Check if numeric
            try:
                float(cell.replace(",", ""))
                numeric_count += 1
            except ValueError:
                pass

            # Check if date-like (simple heuristic)
            if any(separator in cell for separator in ["-", "/", "."]):
                date_count += 1

        total_checked = min(len(column_data), 100)
        numeric_ratio = numeric_count / total_checked if total_checked > 0 else 0
        date_ratio = date_count / total_checked if total_checked > 0 else 0

        if numeric_ratio > 0.8:
            return "numeric"
        elif date_ratio > 0.5:
            return "date"
        else:
            return "text"

    def generate_summary(self, csv_data: Dict[str, Any]) -> str:
        """
        Generate a natural language summary of CSV data.

        Args:
            csv_data: Parsed CSV data

        Returns:
            Natural language summary
        """
        headers = csv_data["headers"]
        total_rows = csv_data["total_rows"]
        total_columns = csv_data["total_columns"]
        column_stats = csv_data["column_stats"]

        summary_parts = [
            f"This dataset contains {total_rows:,} rows and {total_columns} columns.",
            f"The columns are: {', '.join(headers)}.",
        ]

        # Add column type information
        type_counts = {}
        for col_name, stats in column_stats.items():
            data_type = stats["data_type"]
            type_counts[data_type] = type_counts.get(data_type, 0) + 1

        if type_counts:
            type_summary = []
            for data_type, count in type_counts.items():
                type_summary.append(f"{count} {data_type}")
            summary_parts.append(f"Column types: {', '.join(type_summary)}.")

        # Add data quality information
        total_cells = sum(stats["total_cells"] for stats in column_stats.values())
        total_empty = sum(stats["empty_cells"] for stats in column_stats.values())
        if total_empty > 0:
            empty_percentage = (total_empty / total_cells) * 100
            summary_parts.append(
                f"Data completeness: {100 - empty_percentage:.1f}% of cells contain data."
            )

        return " ".join(summary_parts)

    def extract_text_for_embedding(self, csv_data: Dict[str, Any]) -> List[str]:
        """
        Extract text chunks for embedding from CSV data.

        Args:
            csv_data: Parsed CSV data

        Returns:
            List of text chunks for embedding
        """
        chunks = []
        headers = csv_data["headers"]
        data_rows = csv_data["sample_data"]  # Use sample data for embedding

        # Add header information
        chunks.append(f"Dataset columns: {', '.join(headers)}")

        # Add data summary
        summary = self.generate_summary(csv_data)
        chunks.append(summary)

        # Add sample data as text
        for i, row in enumerate(data_rows[:10]):  # Limit to first 10 rows
            row_text = f"Row {i+1}: {', '.join(str(cell) for cell in row)}"
            chunks.append(row_text)

        return chunks
