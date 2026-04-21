import csv
import os
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from pathlib import Path


# Expected structure for business_data.csv
EXPECTED_COLUMNS = [
    'id_client', 'segment', 'region', 'canal_acquisition',
    'nb_commandes', 'chiffre_affaires', 'date_dernier_achat',
    'dernier_achat_jours', 'satisfaction', 'statut_client',
    'risque_churn', 'potentiel_upsell', 'cout_support'
]

COLUMN_TYPES = {
    'id_client': str,
    'segment': str,
    'region': str,
    'canal_acquisition': str,
    'nb_commandes': int,
    'chiffre_affaires': float,
    'date_dernier_achat': str,  # Date as string, will validate format
    'dernier_achat_jours': int,
    'satisfaction': float,
    'statut_client': str,
    'risque_churn': str,
    'potentiel_upsell': float,
    'cout_support': float
}


class CSVValidationError(Exception):
    """Exception raised for CSV validation errors"""
    pass


def validate_file_structure(filepath: str) -> Tuple[bool, List[str]]:
    """
    Validate the structure of a CSV file.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    # Check file existence
    if not os.path.exists(filepath):
        return False, [f"File not found: {filepath}"]
    
    # Check file extension
    if not filepath.lower().endswith('.csv'):
        errors.append(f"File must be CSV format, got: {Path(filepath).suffix}")
    
    # Check file is readable
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            # Check headers exist
            if reader.fieldnames is None:
                return False, ["CSV file has no headers"]
            
            # Remove BOM from column names if present
            headers = [col.strip() for col in reader.fieldnames]
            
            # Check all expected columns are present
            missing_columns = set(EXPECTED_COLUMNS) - set(headers)
            if missing_columns:
                errors.append(f"Missing columns: {', '.join(missing_columns)}")
            
            # Check for unexpected columns
            extra_columns = set(headers) - set(EXPECTED_COLUMNS)
            if extra_columns:
                errors.append(f"Unexpected columns: {', '.join(extra_columns)}")
            
            # Validate rows
            row_errors = []
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (after header)
                row_error = validate_row(row, row_num)
                if row_error:
                    row_errors.extend(row_error)
            
            if row_errors and len(row_errors) <= 5:  # Show first 5 row errors
                errors.extend(row_errors)
            elif row_errors:
                errors.append(f"Found {len(row_errors)} row validation errors (showing first 5)")
                errors.extend(row_errors[:5])
    
    except UnicodeDecodeError:
        errors.append("File encoding error: expected UTF-8")
    except Exception as e:
        errors.append(f"Error reading file: {str(e)}")
    
    return len(errors) == 0, errors


def validate_row(row: Dict[str, str], row_num: int) -> List[str]:
    """
    Validate a single CSV row.
    
    Args:
        row: Dictionary representation of the row
        row_num: Row number for error reporting
        
    Returns:
        List of error messages for this row
    """
    errors = []
    
    for column, expected_type in COLUMN_TYPES.items():
        if column not in row:
            continue
            
        value = row[column].strip()
        
        # Skip validation for empty values (they're optional)
        if not value:
            continue
        
        try:
            if expected_type == int:
                int(value)
            elif expected_type == float:
                float(value)
            elif column == 'date_dernier_achat':
                # Validate date format YYYY-MM-DD
                datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            errors.append(
                f"Row {row_num}: Invalid {expected_type.__name__} in column '{column}': '{value}'"
            )
    
    return errors


def parse_csv(filepath: str) -> List[Dict[str, any]]:
    """
    Parse a CSV file and return list of dictionaries.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        List of dictionaries representing rows
        
    Raises:
        CSVValidationError: If file structure is invalid
    """
    is_valid, errors = validate_file_structure(filepath)
    
    if not is_valid:
        raise CSVValidationError(f"Invalid CSV file: {'; '.join(errors)}")
    
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert types
                converted_row = {}
                for column, expected_type in COLUMN_TYPES.items():
                    if column in row:
                        value = row[column].strip()
                        if not value:
                            # Keep empty values as None
                            converted_row[column] = None
                        elif expected_type == int:
                            converted_row[column] = int(value)
                        elif expected_type == float:
                            converted_row[column] = float(value)
                        else:
                            converted_row[column] = value
                data.append(converted_row)
    except Exception as e:
        raise CSVValidationError(f"Error parsing CSV file: {str(e)}")
    
    return data


def upload_csv(filepath: str, destination_dir: str = '.') -> Tuple[bool, str, Optional[List[Dict]]]:
    """
    Upload and parse a CSV file.
    
    Args:
        filepath: Path to the CSV file to upload
        destination_dir: Directory to store the file (default: current directory)
        
    Returns:
        Tuple of (success, message, parsed_data)
    """
    try:
        # Validate file structure
        is_valid, errors = validate_file_structure(filepath)
        if not is_valid:
            error_msg = "Validation failed: " + "; ".join(errors)
            return False, error_msg, None
        
        # Ensure destination directory exists
        os.makedirs(destination_dir, exist_ok=True)
        
        # Copy file to destination
        filename = os.path.basename(filepath)
        destination_path = os.path.join(destination_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8-sig') as src:
            with open(destination_path, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
        
        # Parse the CSV
        parsed_data = parse_csv(destination_path)
        
        message = f"Successfully uploaded and parsed {filename} ({len(parsed_data)} rows)"
        return True, message, parsed_data
    
    except CSVValidationError as e:
        return False, str(e), None
    except Exception as e:
        return False, f"Upload error: {str(e)}", None


def get_file_summary(parsed_data: List[Dict]) -> Dict:
    """
    Get summary statistics for parsed CSV data.
    
    Args:
        parsed_data: List of dictionaries from parsed CSV
        
    Returns:
        Dictionary with summary information
    """
    if not parsed_data:
        return {"rows": 0, "columns": 0}
    
    summary = {
        "rows": len(parsed_data),
        "columns": len(parsed_data[0]) if parsed_data else 0,
        "column_names": list(parsed_data[0].keys()) if parsed_data else [],
        "sample_row": parsed_data[0] if parsed_data else None
    }
    
    return summary


if __name__ == "__main__":
    # Example usage
    csv_file = "business_data.csv"
    
    print("=" * 60)
    print("CSV FILE VALIDATION AND IMPORT")
    print("=" * 60)
    
    # Validate structure
    print(f"\n1. Validating file structure: {csv_file}")
    is_valid, errors = validate_file_structure(csv_file)
    
    if is_valid:
        print("   ✓ File structure is valid")
    else:
        print("   ✗ File structure validation failed:")
        for error in errors:
            print(f"     - {error}")
        exit(1)
    
    # Parse CSV
    print(f"\n2. Parsing CSV file...")
    try:
        data = parse_csv(csv_file)
        print(f"   ✓ Successfully parsed {len(data)} rows")
    except CSVValidationError as e:
        print(f"   ✗ Error: {e}")
        exit(1)
    
    # Display summary
    print(f"\n3. File summary:")
    summary = get_file_summary(data)
    print(f"   - Total rows: {summary['rows']}")
    print(f"   - Total columns: {summary['columns']}")
    print(f"   - Columns: {', '.join(summary['column_names'])}")
    
    # Display first row
    print(f"\n4. First data row:")
    if data:
        for key, value in data[0].items():
            print(f"   - {key}: {value}")
    
    print("\n" + "=" * 60)
