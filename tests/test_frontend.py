import pandas as pd
from src.backend.database import Base, get_db
from src.backend.models import Education, FormalEducation
from src.backend.main import app

def test_data_filtering():
    #mock data
    data = {'Countries and Areas': ['USA', 'Ghana'], 'Value': [10, 20]}
    df = pd.DataFrame(data)

    #test logic
    filtered_df = df[df['Countries and Areas'].isin(['USA'])]
    assert len(filtered_df) == 1
    assert filtered_df.iloc[0]['Countries and Areas'] == 'USA'