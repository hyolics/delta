import os
import logging
# import kaggle
import pandas as pd

class KaggleDataHandler:
    def __init__(self, dataset_name: str, data_path: str = "./data", file_name: str = "data.csv"):
        """
        :param dataset_name: Kaggle 數據集名稱（如 'carrie1/ecommerce-data'）
        :param data_path: 存放數據的資料夾
        :param file_name: CSV 文件名稱
        """
        self.dataset_name = dataset_name
        self.data_path = data_path
        self.file_path = os.path.join(data_path, file_name)

        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def download_kaggle_data(self):
        try:
            logging.info("Authenticating Kaggle API...")
            # kaggle.api.authenticate()

            # os.makedirs(self.data_path, exist_ok=True)

            logging.info(f"Downloading dataset: {self.dataset_name} ...")
            # kaggle.api.dataset_download_files(self.dataset_name, path=self.data_path, unzip=True)

            logging.info("Download completed successfully!")
        except Exception as e:
            logging.error(f"Error while downloading data: {e}")

    def extract_data(self):
        try:
            if os.path.exists(self.file_path):
                df = pd.read_csv(self.file_path, encoding="ISO-8859-1", dtype={'CustomerID': str, 'InvoiceID': str})
                logging.info(f"Read CSV successfully, total records: {len(df)}")
                return df
            else:
                logging.error("CSV file not found!")
                return None
        except Exception as e:
            logging.error(f"Error while reading CSV: {e}")
            return None

if __name__ == "__main__":
    handler = KaggleDataHandler(dataset_name="carrie1/ecommerce-data")
    handler.download_kaggle_data()
    df = handler.extract_data()
