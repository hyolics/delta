import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import pandas as pd
from sqlalchemy.orm import Session
from  modules.database import get_db
from  modules.etl.models import *
from  modules.etl.transform import *

COMPUTE_FUNCTIONS = [
    (compute_overview_index, OverviewIndex),
    (per_month, OverviewByMonths),
    (compute_rfm, OverviewRFM),
    (compute_overview_rfm, OverviewSegment)
]

def get_or_create(session: Session, model, defaults=None, **kwargs):
    """Retrieves an existing record or creates a new one."""
    instance = session.query(model).filter_by(**kwargs).first()
    if not instance:
        params = {**kwargs, **(defaults or {})}
        instance = model(**params)
        session.add(instance)
        session.commit()
        session.refresh(instance)
    return instance

def delete_and_insert(session: Session, model, records):
    """Deletes existing records and inserts new ones in bulk."""
    try:
        session.query(model).delete()
        session.bulk_insert_mappings(model, records)
        session.commit()
        print(f"Inserted {len(records)} records into {model} successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error inserting data into {model}: {e}")

def insert_dim_data(session, df, model, unique_cols):
    """Handles inserting dimension table data."""
    existing_records = {getattr(row, unique_cols[0]): row for row in session.query(model)}
    mapping = {}
    
    for values in df[unique_cols].drop_duplicates().values:
        key = values[0]
        if key not in existing_records:
            obj = get_or_create(session, model, **dict(zip(unique_cols, values)))
            existing_records[key] = obj
        mapping[key] = getattr(existing_records[key], unique_cols[0])
    
    return mapping

def load_main_data_to_db(df: pd.DataFrame):
    if df is not None:
        df = rename_raw_data(df)
        df = basic_check(df)
    
        try:
            with next(get_db()) as session:
                product_map = insert_dim_data(session, df, DimProduct, ["stock_code", "description"])        
                df["stock_code"] = df["stock_code"].map(product_map)
                df = df.drop(columns=["description", "amount"], errors='ignore')

                fact_records = df.to_dict(orient="records")
                session.bulk_insert_mappings(FactSales, fact_records)
                session.commit()
                
                print(f"Inserted {len(fact_records)} sales records successfully!")
        except Exception as e:
            session.rollback()
            print(f"Error inserting data: {e}")
    
    else:
        print("No data to process!")


def fetch_data():
    with next(get_db()) as session:
        df = pd.DataFrame([row.__dict__ for row in session.query(FactSales).all()])
        df = basic_check(df)
    return df

def compute_index_data(df, func):
    results = {}
    for compute_func, model in func:
        try:
            result_df = compute_func(df)
            results[model] = result_df.to_dict(orient="records")
        except Exception as e:
            print(f"Error computing {model}: {e}")
    return results

def store_index_data(results):
    with next(get_db()) as session:
        for model, records in results.items():
            try:
                delete_and_insert(session, model, records)
            except Exception as e:
                session.rollback()
                print(f"Error inserting data into {model}: {e}")

def load_index_data_to_db():
    df = fetch_data()
    results = compute_index_data(df, COMPUTE_FUNCTIONS)
    store_index_data(results)
