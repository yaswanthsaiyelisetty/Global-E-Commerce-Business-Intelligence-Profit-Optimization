import pandas as pd
import numpy as np
import sqlite3
import json
import os
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

# Base Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'global_ecommerce_sales.csv')
CLEAN_DATA_PATH = os.path.join(BASE_DIR, 'cleaned_data', 'cleaned_ecommerce_sales.csv')
DB_PATH = os.path.join(BASE_DIR, 'database', 'ecommerce_sales.db')
INSIGHTS_PATH = os.path.join(BASE_DIR, 'app', 'insights.json')

def load_and_clean_data():
    df = pd.read_csv(DATA_PATH)
    
    # Drop duplicates
    df = df.drop_duplicates()
    
    # Convert dates
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    
    # Safely convert numeric columns
    num_cols = ['Quantity', 'Unit_Price', 'Discount_Percent', 'Total_Sales', 'Shipping_Cost', 'Profit']
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Fill missing values
    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())
        
    cat_cols = ['Customer_Name', 'Customer_Segment', 'Country', 'Region', 'Product_Category', 'Product_Name', 'Payment_Method']
    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0]).str.strip()
        
    return df

def feature_engineering(df):
    df['Year'] = df['Order_Date'].dt.year
    df['Month'] = df['Order_Date'].dt.month
    df['Month_Name'] = df['Order_Date'].dt.month_name()
    df['Quarter'] = df['Order_Date'].dt.quarter
    
    df['Revenue_Per_Order'] = df['Total_Sales']
    df['Profit_Margin'] = df['Profit'] / df['Total_Sales']
    df['Shipping_Cost_Ratio'] = df['Shipping_Cost'] / df['Total_Sales']
    df['Discount_Value'] = df['Quantity'] * df['Unit_Price'] * (df['Discount_Percent'] / 100)
    df['Gross_Sales'] = df['Quantity'] * df['Unit_Price']
    df['Net_Sales_After_Shipping'] = df['Total_Sales'] - df['Shipping_Cost']
    
    df['Order_Size'] = pd.cut(df['Quantity'], bins=[0, 2, 5, float('inf')], labels=['Low', 'Medium', 'High'])
    df['Profit_Status'] = np.where(df['Profit'] > 0, 'Profitable', 'Loss-Making')
    
    df['Discount_Level'] = pd.cut(df['Discount_Percent'], bins=[-1, 0, 10, 20, 100], labels=['No Discount', 'Low', 'Medium', 'High'])
    
    return df

def save_to_db(df):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql('sales', conn, if_exists='replace', index=False)
    
    targets = pd.DataFrame({
        'Region': ['North America', 'Europe', 'Asia Pacific', 'Middle East & Africa', 'South America'],
        'Sales_Target': [250000, 200000, 220000, 150000, 130000],
        'Profit_Target': [45000, 35000, 40000, 25000, 20000]
    })
    targets.to_sql('region_targets', conn, if_exists='replace', index=False)
    conn.close()

def generate_insights(df):
    # KPIs
    kpis = {
        'total_revenue': float(df['Total_Sales'].sum()),
        'total_profit': float(df['Profit'].sum()),
        'total_orders': int(df['Order_ID'].nunique()),
        'avg_order_value': float(df['Total_Sales'].mean()),
        'profit_margin': float((df['Profit'].sum() / df['Total_Sales'].sum()) * 100),
        'total_shipping_cost': float(df['Shipping_Cost'].sum())
    }
    
    # Sales by Region
    sales_by_region = df.groupby('Region')['Total_Sales'].sum().to_dict()
    
    # Profit by Category
    profit_by_category = df.groupby('Product_Category')['Profit'].sum().to_dict()
    
    # Monthly Sales (aggregating by month number)
    monthly_sales_df = df.groupby('Month')['Total_Sales'].sum().reset_index()
    monthly_sales_df = monthly_sales_df.sort_values('Month')
    monthly_sales = monthly_sales_df['Total_Sales'].tolist()
    
    # Payment Method Distribution
    payment_methods = df['Payment_Method'].value_counts().to_dict()
    
    # Top Products
    top_products = df.groupby(['Product_Name', 'Product_Category']).agg({
        'Total_Sales': 'sum',
        'Profit': 'sum'
    }).reset_index().sort_values('Total_Sales', ascending=False).head(5).to_dict('records')
    
    # Target Achievement
    region_sales = df.groupby('Region')[['Total_Sales', 'Profit']].sum().reset_index()
    targets = pd.DataFrame({
        'Region': ['North America', 'Europe', 'Asia Pacific', 'Middle East & Africa', 'South America'],
        'Sales_Target': [250000, 200000, 220000, 150000, 130000],
        'Profit_Target': [45000, 35000, 40000, 25000, 20000]
    })
    achievement = pd.merge(region_sales, targets, on='Region')
    achievement['Achievement_Percent'] = (achievement['Total_Sales'] / achievement['Sales_Target']) * 100
    achievement['Status'] = np.where(achievement['Achievement_Percent'] >= 100, 'Target Met', 'Underperforming')
    target_achievement = achievement[['Region', 'Sales_Target', 'Total_Sales', 'Achievement_Percent', 'Status']].to_dict('records')
    
    insights = {
        'kpis': kpis,
        'sales_by_region': sales_by_region,
        'profit_by_category': profit_by_category,
        'monthly_sales': monthly_sales,
        'payment_method_distribution': payment_methods,
        'top_products': top_products,
        'target_achievement': target_achievement,
        'recommendations': [
            "Increase marketing investment in high-profit regions like North America.",
            "Reduce excessive discounting if it consistently lowers profit margins.",
            "Optimize shipping costs in regions where the shipping cost ratio is high.",
            "Promote products with high profit margins instead of focusing purely on top-line sales.",
            "Improve performance in underachieving regions using localized targeting and offers.",
            "Encourage preferred payment methods to improve overall checkout completion rates."
        ]
    }
    
    with open(INSIGHTS_PATH, 'w') as f:
        json.dump(insights, f, indent=4)

def main():
    print("Loading and cleaning data...")
    df = load_and_clean_data()
    
    print("Feature engineering...")
    df = feature_engineering(df)
    
    print("Saving cleaned data...")
    df.to_csv(CLEAN_DATA_PATH, index=False)
    
    print("Saving to database...")
    save_to_db(df)
    
    print("Generating insights.json...")
    generate_insights(df)
    
    print("Data processing pipeline complete.")

if __name__ == "__main__":
    main()
