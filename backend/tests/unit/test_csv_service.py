"""Unit tests for CSV service."""

import pytest
import tempfile
import os
from src.services.csv_service import CSVService


class TestCSVService:
    """Test cases for CSVService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.csv_service = CSVService()

    def test_parse_csv_valid(self):
        """Test parsing a valid CSV file."""
        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("name,age,city\nJohn,30,NYC\nJane,25,LA\n")
            temp_file = f.name

        try:
            result = self.csv_service.parse_csv(temp_file)

            assert result["headers"] == ["name", "age", "city"]
            assert result["total_rows"] == 2
            assert result["total_columns"] == 3
            assert len(result["sample_data"]) == 2

        finally:
            os.unlink(temp_file)

    def test_parse_csv_empty(self):
        """Test parsing an empty CSV file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            temp_file = f.name

        try:
            with pytest.raises(ValueError, match="CSV file is empty"):
                self.csv_service.parse_csv(temp_file)
        finally:
            os.unlink(temp_file)

    def test_infer_data_type_numeric(self):
        """Test data type inference for numeric data."""
        column_data = ["1", "2", "3", "4", "5"]
        data_type = self.csv_service._infer_data_type(column_data)
        assert data_type == "numeric"

    def test_infer_data_type_text(self):
        """Test data type inference for text data."""
        column_data = ["apple", "banana", "cherry", "date", "elderberry"]
        data_type = self.csv_service._infer_data_type(column_data)
        assert data_type == "text"

    def test_generate_summary(self):
        """Test summary generation."""
        csv_data = {
            "headers": ["name", "age", "city"],
            "total_rows": 100,
            "total_columns": 3,
            "column_stats": {
                "name": {
                    "data_type": "text",
                    "total_cells": 100,
                    "non_empty_cells": 100,
                    "empty_cells": 0,
                },
                "age": {
                    "data_type": "numeric",
                    "total_cells": 100,
                    "non_empty_cells": 95,
                    "empty_cells": 5,
                },
                "city": {
                    "data_type": "text",
                    "total_cells": 100,
                    "non_empty_cells": 98,
                    "empty_cells": 2,
                },
            },
        }

        summary = self.csv_service.generate_summary(csv_data)

        assert "100 rows" in summary
        assert "3 columns" in summary
        assert "name, age, city" in summary
        assert "Data completeness" in summary
