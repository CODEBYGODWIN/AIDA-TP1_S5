import pytest
import pandas as pd
import os
import sys

# Add the project root to sys.path to allow importing from 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.risk_analysis import count_at_risk_clients

def test_count_at_risk_clients():
    sample_path = "tests/risk_sample.csv"
    assert os.path.exists(sample_path)
    
    df = pd.read_csv(sample_path)
    count = count_at_risk_clients(df)
    assert count == 2
