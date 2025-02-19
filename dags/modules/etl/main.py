import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from modules.database import init_db
from modules.extract_data import *
from modules.etl.load import load_main_data_to_db, load_index_data_to_db
from modules.etl.transform import *


if __name__ == "__main__":
    init_db()
    handler = KaggleDataHandler(dataset_name="carrie1/ecommerce-data")
    # handler.download_kaggle_data()
    df = handler.extract_data()
    
    load_main_data_to_db(df)
    load_index_data_to_db()
