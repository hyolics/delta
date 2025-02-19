import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from load import load_data_to_db
from modules.database import init_db
from modules.extract_data import *


if __name__ == "__main__":
    init_db()
    
    handler = KaggleDataHandler(dataset_name="carrie1/ecommerce-data")
    handler.download_kaggle_data()
    df = handler.extract_data()
    
    load_data_to_db(df)