import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from modules.database import get_db
from modules.elt.models import Invoice


def load_data_to_db(df):
    if df is not None:
        df.rename(columns={
            'InvoiceNo': 'invoice_no',
            'StockCode': 'stock_code',
            'Description': 'description',
            'Quantity': 'quantity',
            'InvoiceDate': 'invoice_date',
            'UnitPrice': 'unit_price',
            'CustomerID': 'customer_id',
            'Country': 'country'
        }, inplace=True)
        
 
        try:
            total = len(df)
            duplicates = sum(df.duplicated())
            print(f"Duplicated data: {duplicates}")

            df.drop_duplicates(inplace=True)

            if len(df) + duplicates != total:
                raise ValueError("Data mismatch after deduplication!")
            
            records = df.to_dict(orient="records")

            with next(get_db()) as db: 
                db.bulk_insert_mappings(Invoice, records)
                db.commit()
                print(f"Inserted {len(records)} records successfully!")
 
        except Exception as e:
            db.rollback()
            print(f"Error inserting data: {e}")
    else:
        print("No data to process!")
        