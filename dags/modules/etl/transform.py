import pandas as pd
from datetime import datetime

# for RFM analysis
SEGMENT_MAP = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}


def basic_check(df):
    """Preprocess the data by cleaning and adding necessary columns."""
    df.drop_duplicates(inplace=True)
    if "description" in df.columns:
        df["description"] = df["description"].where(pd.notna(df["description"]), None)
    df["customer_id"] = df["customer_id"].where(pd.notna(df["customer_id"]), None)
    df['invoice_date'] = pd.to_datetime(df['invoice_date'])
    
    df["is_cancelled"] = df["invoice_no"].str.startswith('C').astype(int)
    df['amount'] = round(df['quantity'] * df['unit_price'], 2)
    return df

def rename_raw_data(df):
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
    return df

def compute_overview_index(df):
    """Compute overall transactional and financial overview."""
    cancel_transaction = len(set(df[df['is_cancelled'] == 1]['invoice_no']))
    success_transaction = len(set(df[df['is_cancelled'] == 0]['invoice_no']))
    revenue = df['amount'].sum()
    
    overview = {
        'unique_customers': df["customer_id"].nunique(),
        'unique_transactions': df["invoice_no"].nunique(),
        'success_transaction': success_transaction,
        'cancel_transaction': cancel_transaction,
        'revenue': revenue,
        'avg_revenue_per_transaction': round(revenue / success_transaction,2) if success_transaction else 0,
        'avg_revenue_per_customer': round(revenue / df["customer_id"].nunique(),2) if df["customer_id"].nunique() else 0
    }
    
    return pd.DataFrame([overview])

def per_month(df):
    """Aggregate data by month to analyze transactional trends."""
    df_monthly = df.groupby(df["invoice_date"].dt.to_period("M")).agg(
        {"invoice_no": "nunique","customer_id": "nunique","amount": "sum"}).reset_index()
    df_monthly.columns = ["mon", "unique_transactions","unique_customers","revenue"]
    df_monthly['mon'] = pd.to_datetime(df_monthly['mon'])
    df_monthly['revenue'] = df_monthly['revenue'].round(2)
    return df_monthly

def compute_rfm(df):
    """Compute RFM scores for customers."""
    today_date = datetime(2011, 12, 11)
    df = df.dropna(subset=['customer_id'])
    
    monetary_df = df.groupby('customer_id').agg({'amount': 'sum'}).reset_index()
    monetary_df['amount'] = monetary_df['amount'].round(2)
    monetary_df = monetary_df[monetary_df['amount'] > 0]
    
    df = df[~df['invoice_no'].str.startswith('C')]
    df_filtered = df.groupby('customer_id').agg({
        'invoice_date': lambda x: (today_date - x.max()).days,
        'invoice_no': 'nunique'
    }).reset_index()
    
    rfm = pd.merge(df_filtered, monetary_df, on='customer_id')
    rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
    rfm = rfm[rfm['monetary'] > 0]
    
    # Assign RFM scores
    rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])
    
    # Combine RFM scores to create overall RFM score
    rfm["rfm_score"] = rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str)
    rfm['segment'] = rfm['rfm_score'].replace(SEGMENT_MAP, regex=True)
    
    return rfm

def compute_overview_rfm(df):
    """Compute the percentage of customer segments based on RFM."""
    rfm_overview = compute_rfm(df)
    rfm_overview = rfm_overview['segment'].value_counts(normalize=True).reset_index()
    rfm_overview.columns = ['segment', 'percentage']
    rfm_overview['percentage'] = round(rfm_overview['percentage'] / sum(rfm_overview['percentage']),2)
    return rfm_overview
