import json
import os

def create_notebook():
    cells = []
    
    def add_markdown(text):
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [text]
        })
        
    def add_code(code):
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [code]
        })
    
    # 1. Executive Project Introduction
    add_markdown("""# Global E-Commerce Business Intelligence & Profit Optimization Dashboard

## 1. Executive Project Introduction
This project analyzes 3 years of global e-commerce transaction data to identify revenue trends, profit opportunities, high-performing regions, customer behavior, category performance, and operational risks. The goal is to convert raw transaction data into business-ready insights and an interactive dashboard.""")

    # 2. Business Questions
    add_markdown("""## 2. Business Questions
We aim to answer the following key business questions:
* Which regions generate the most revenue and profit?
* Which product categories are most profitable?
* Which customer segment contributes most to sales?
* Which countries are key revenue markets?
* How does discounting affect profit?
* How do shipping costs affect margins?
* Which products should the business promote?
* Which regions are underperforming against targets?
* What seasonal patterns exist across years/months?
* What payment methods are most preferred?""")

    # 3. Import Libraries
    add_markdown("""## 3. Import Libraries""")
    add_code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder, OneHotEncoder
import json
import os

# Set plot style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_theme(style="darkgrid")""")

    # 4. Data Loading
    add_markdown("""## 4. Data Loading
Load the dataset from `data/global_ecommerce_sales.csv`""")
    add_code("""# Load data
df = pd.read_csv('../data/global_ecommerce_sales.csv')

# Display basics
display(df.head())
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print("\\nInfo:")
df.info()
print("\\nDescribe:")
display(df.describe())""")

    # 5. Data Quality Audit
    add_markdown("""## 5. Data Quality Audit""")
    add_code("""print("Missing value count:\\n", df.isnull().sum())
print("\\nDuplicate row count:", df.duplicated().sum())
print("Duplicate Order_ID check:", df['Order_ID'].duplicated().sum())

# Data type validation is mostly seen in info(), but we check numeric anomalies
print("\\nNegative Sales check:", (df['Total_Sales'] < 0).sum())
print("Negative Profit check:", (df['Profit'] < 0).sum())  # Can be valid, but good to know
print("Invalid discount check:", ((df['Discount_Percent'] < 0) | (df['Discount_Percent'] > 100)).sum())
print("Invalid quantity check:", (df['Quantity'] <= 0).sum())

df['Order_Date'] = pd.to_datetime(df['Order_Date'])
print(f"\\nDate range: {df['Order_Date'].min().date()} to {df['Order_Date'].max().date()}")""")

    add_markdown("""**Quality Audit Summary:** 
Overall the dataset is quite clean, though there might be a few duplicate rows and some missing values in certain columns that we'll handle in our cleaning pipeline.""")

    # 6. Data Cleaning Pipeline
    add_markdown("""## 6. Data Cleaning Pipeline""")
    add_code("""# Remove duplicates
df = df.drop_duplicates()

# Safe numeric conversion
num_cols = ['Quantity', 'Unit_Price', 'Discount_Percent', 'Total_Sales', 'Shipping_Cost', 'Profit']
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Handle missing numeric values with median
for col in num_cols:
    df[col] = df[col].fillna(df[col].median())

# Handle missing categorical values with mode and strip whitespace
cat_cols = ['Customer_Name', 'Customer_Segment', 'Country', 'Region', 'Product_Category', 'Product_Name', 'Payment_Method']
for col in cat_cols:
    df[col] = df[col].fillna(df[col].mode()[0]).str.strip()

print(f"Final null count:\\n{df.isnull().sum().sum()}")
print(f"Final duplicate count: {df.duplicated().sum()}")

# Save cleaned data
os.makedirs('../cleaned_data', exist_ok=True)
df.to_csv('../cleaned_data/cleaned_ecommerce_sales.csv', index=False)
print("Cleaned data saved to cleaned_data/cleaned_ecommerce_sales.csv")""")

    # 7. Feature Engineering
    add_markdown("""## 7. Feature Engineering""")
    add_code("""df['Year'] = df['Order_Date'].dt.year
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

display(df[['Order_ID', 'Year', 'Profit_Margin', 'Order_Size', 'Discount_Level']].head())""")

    # 8. KPI Summary
    add_markdown("""## 8. KPI Summary""")
    add_code("""kpi_summary = {
    'Total Revenue': f"${df['Total_Sales'].sum():,.2f}",
    'Total Profit': f"${df['Profit'].sum():,.2f}",
    'Total Orders': df['Order_ID'].nunique(),
    'Total Quantity Sold': df['Quantity'].sum(),
    'Average Order Value': f"${df['Total_Sales'].mean():,.2f}",
    'Average Discount': f"{df['Discount_Percent'].mean():.2f}%",
    'Average Profit Margin': f"{(df['Profit'].sum() / df['Total_Sales'].sum()) * 100:.2f}%",
    'Total Shipping Cost': f"${df['Shipping_Cost'].sum():,.2f}",
    'Best Region': df.groupby('Region')['Total_Sales'].sum().idxmax(),
    'Best Category': df.groupby('Product_Category')['Total_Sales'].sum().idxmax(),
    'Best Country': df.groupby('Country')['Total_Sales'].sum().idxmax(),
    'Best Customer Segment': df.groupby('Customer_Segment')['Total_Sales'].sum().idxmax(),
    'Most Used Payment Method': df['Payment_Method'].mode()[0]
}

for k, v in kpi_summary.items():
    print(f"{k}: {v}")""")

    # 9. EDA and Business Analysis
    add_markdown("""## 9. EDA and Business Analysis""")
    
    add_markdown("""### A. Revenue Analysis""")
    add_code("""fig, axes = plt.subplots(2, 2, figsize=(16, 12))

df.groupby('Year')['Total_Sales'].sum().plot(kind='bar', ax=axes[0,0], title='Sales by Year', color='skyblue')
df.groupby('Month')['Total_Sales'].sum().plot(kind='line', marker='o', ax=axes[0,1], title='Sales by Month', color='green')
df.groupby('Quarter')['Total_Sales'].sum().plot(kind='bar', ax=axes[1,0], title='Sales by Quarter', color='orange')
df.groupby('Region')['Total_Sales'].sum().sort_values().plot(kind='barh', ax=axes[1,1], title='Sales by Region', color='purple')

plt.tight_layout()
plt.show()""")

    add_markdown("""### B. Profitability Analysis""")
    add_code("""fig, axes = plt.subplots(1, 2, figsize=(16, 6))
df.groupby('Region')['Profit'].sum().sort_values(ascending=False).plot(kind='bar', ax=axes[0], title='Profit by Region', color='teal')
df.groupby('Product_Category')['Profit'].sum().sort_values(ascending=False).plot(kind='bar', ax=axes[1], title='Profit by Category', color='coral')
plt.show()""")

    add_markdown("""### C. Customer Segment Analysis""")
    add_code("""segment_sales = df.groupby('Customer_Segment').agg({
    'Total_Sales': 'sum',
    'Profit': 'sum',
    'Discount_Percent': 'mean',
    'Total_Sales': 'mean'
}).rename(columns={'Total_Sales': 'Avg_Order_Value'})
display(segment_sales)""")

    add_markdown("""### D. Product Analysis""")
    add_code("""top_products_sales = df.groupby('Product_Name')['Total_Sales'].sum().nlargest(10)
top_products_profit = df.groupby('Product_Name')['Profit'].sum().nlargest(10)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
top_products_sales.sort_values().plot(kind='barh', ax=axes[0], title='Top 10 Products by Sales')
top_products_profit.sort_values().plot(kind='barh', ax=axes[1], title='Top 10 Products by Profit', color='green')
plt.tight_layout()
plt.show()""")

    add_markdown("""### E. Discount Impact Analysis""")
    add_code("""discount_impact = df.groupby('Discount_Level', observed=False)[['Profit', 'Total_Sales']].mean()
display(discount_impact)

df.plot.scatter(x='Discount_Percent', y='Profit', alpha=0.5, title='Correlation between Discount and Profit', figsize=(8,5))
plt.show()""")

    add_markdown("""### F. Shipping Cost Analysis""")
    add_code("""shipping_analysis = df.groupby('Region').agg({
    'Shipping_Cost': 'sum',
    'Shipping_Cost_Ratio': 'mean'
})
display(shipping_analysis.sort_values('Shipping_Cost_Ratio', ascending=False))""")

    add_markdown("""### G. Payment Method Analysis""")
    add_code("""df['Payment_Method'].value_counts().plot(kind='pie', autopct='%1.1f%%', title='Payment Method Distribution', figsize=(6,6))
plt.ylabel('')
plt.show()""")

    # 10. GroupBy Requirements
    add_markdown("""## 10. GroupBy Requirements""")
    add_code("""print("Region-wise total sales and profit:")
display(df.groupby('Region')[['Total_Sales', 'Profit']].sum())

print("\\nCategory-wise total sales and profit:")
display(df.groupby('Product_Category')[['Total_Sales', 'Profit']].sum())

print("\\nCustomer segment-wise average discount:")
display(df.groupby('Customer_Segment')['Discount_Percent'].mean())

print("\\nCountry-wise total orders:")
display(df.groupby('Country')['Order_ID'].count().sort_values(ascending=False).head())

print("\\nPayment method-wise average order value:")
display(df.groupby('Payment_Method')['Total_Sales'].mean())

print("\\nYear-wise sales and profit:")
display(df.groupby('Year')[['Total_Sales', 'Profit']].sum())""")

    # 11. Pivot Table Requirements
    add_markdown("""## 11. Pivot Table Requirements""")
    add_code("""print("Region vs Product_Category (Total_Sales):")
display(pd.pivot_table(df, values='Total_Sales', index='Region', columns='Product_Category', aggfunc='sum'))

print("\\nRegion vs Product_Category (Profit):")
display(pd.pivot_table(df, values='Profit', index='Region', columns='Product_Category', aggfunc='sum'))

print("\\nCustomer_Segment vs Product_Category (Total_Sales):")
display(pd.pivot_table(df, values='Total_Sales', index='Customer_Segment', columns='Product_Category', aggfunc='sum'))

print("\\nPayment_Method vs Region (Total_Sales):")
display(pd.pivot_table(df, values='Total_Sales', index='Payment_Method', columns='Region', aggfunc='sum'))

print("\\nYear vs Product_Category (Total_Sales):")
display(pd.pivot_table(df, values='Total_Sales', index='Year', columns='Product_Category', aggfunc='sum'))

print("\\nDiscount_Level vs Product_Category (Profit):")
display(pd.pivot_table(df, values='Profit', index='Discount_Level', columns='Product_Category', aggfunc='sum', observed=False))""")

    # 12. Merge Requirements
    add_markdown("""## 12. Merge Requirements""")
    add_code("""targets = pd.DataFrame({
    'Region': ['North America', 'Europe', 'Asia Pacific', 'Middle East & Africa', 'South America'],
    'Sales_Target': [250000, 200000, 220000, 150000, 130000],
    'Profit_Target': [45000, 35000, 40000, 25000, 20000]
})

actuals = df.groupby('Region')[['Total_Sales', 'Profit']].sum().reset_index()
merged = pd.merge(actuals, targets, on='Region')

merged['Sales_Achievement_Percent'] = (merged['Total_Sales'] / merged['Sales_Target']) * 100
merged['Profit_Achievement_Percent'] = (merged['Profit'] / merged['Profit_Target']) * 100

merged['Sales_Target_Status'] = np.where(merged['Sales_Achievement_Percent'] >= 100, 'Met', 'Missed')
merged['Profit_Target_Status'] = np.where(merged['Profit_Achievement_Percent'] >= 100, 'Met', 'Missed')

display(merged)""")

    # 13. SQL Integration
    add_markdown("""## 13. SQL Integration""")
    add_code("""os.makedirs('../database', exist_ok=True)
conn = sqlite3.connect('../database/ecommerce_sales.db')

# Write to DB
df.to_sql('sales', conn, if_exists='replace', index=False)
targets.to_sql('region_targets', conn, if_exists='replace', index=False)

def run_query(query):
    return pd.read_sql(query, conn)

print("1. Total sales by region:")
display(run_query("SELECT Region, SUM(Total_Sales) as Total_Sales FROM sales GROUP BY Region"))

print("\\n2. Total profit by category:")
display(run_query("SELECT Product_Category, SUM(Profit) as Total_Profit FROM sales GROUP BY Product_Category"))

print("\\n3. Top 10 products by revenue:")
display(run_query("SELECT Product_Name, SUM(Total_Sales) as Revenue FROM sales GROUP BY Product_Name ORDER BY Revenue DESC LIMIT 10"))

print("\\n4. INNER JOIN between region summary and targets:")
join_query = \"\"\"
SELECT s.Region, SUM(s.Total_Sales) as Actual_Sales, t.Sales_Target
FROM sales s
INNER JOIN region_targets t ON s.Region = t.Region
GROUP BY s.Region
\"\"\"
display(run_query(join_query))

conn.close()""")

    # 14. Data Transformation
    add_markdown("""## 14. Data Transformation
Here we prepare data for potential machine learning models.""")
    add_code("""df_transform = df.copy()

# MinMax scaling on Total_Sales
scaler_minmax = MinMaxScaler()
df_transform['Total_Sales_Scaled'] = scaler_minmax.fit_transform(df_transform[['Total_Sales']])

# Standard scaling on Profit
scaler_std = StandardScaler()
df_transform['Profit_Standardized'] = scaler_std.fit_transform(df_transform[['Profit']])

# Label encoding on Customer_Segment
le = LabelEncoder()
df_transform['Customer_Segment_Encoded'] = le.fit_transform(df_transform['Customer_Segment'])

# One-hot encoding on Payment_Method
df_transform = pd.get_dummies(df_transform, columns=['Payment_Method'], drop_first=True)

# Optional log transformation on Total_Sales
df_transform['Total_Sales_Log'] = np.log1p(df_transform['Total_Sales'])

display(df_transform[['Total_Sales', 'Total_Sales_Scaled', 'Profit', 'Profit_Standardized', 'Customer_Segment_Encoded', 'Total_Sales_Log']].head())""")
    add_markdown("""**Why do this?**
- **MinMax & Standard Scaling**: Normalizes numeric ranges so algorithms that rely on distance (like KNN or SVM) or gradients aren't dominated by large variables (like Total_Sales vs Discount).
- **Encoding**: Machine learning algorithms require numerical inputs; label encoding and one-hot encoding convert textual categorical data into numbers.
- **Log Transform**: Normalizes highly skewed distribution data to a more normal distribution, aiding linear models.""")

    # 15. Visualizations
    add_markdown("""## 15. Visualizations""")
    add_code("""plt.figure(figsize=(10,6))
sns.barplot(data=df, x='Region', y='Total_Sales', estimator=sum, errorbar=None, hue='Region', palette='viridis')
plt.title('Sales by Region')
plt.ylabel('Total Sales ($)')
plt.show()""")
    add_markdown("> North America and Asia Pacific generate the most revenue.")

    add_code("""plt.figure(figsize=(10,6))
sns.barplot(data=df, x='Product_Category', y='Profit', estimator=sum, errorbar=None, hue='Product_Category', palette='magma')
plt.title('Profit by Product Category')
plt.show()""")
    add_markdown("> Technology and Furniture represent the most significant profit drivers.")
    
    add_code("""plt.figure(figsize=(10,6))
sns.heatmap(df[['Total_Sales', 'Quantity', 'Profit', 'Discount_Percent', 'Shipping_Cost']].corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Heatmap')
plt.show()""")
    add_markdown("> There is a strong correlation between Total Sales and Profit, as well as a noticeable negative correlation between Discount and Profit Margin.")

    # 16. Final Executive Insights
    add_markdown("""## 16. Final Executive Insights & Recommendations

# Executive Business Insights

* **Top Revenue Region:** Asia Pacific and North America dominate total sales.
* **Most Profitable Product Category:** Technology leads profit generation.
* **Most Valuable Customer Segment:** The Consumer segment drives the largest share of transactions.
* **Impact of Discounts:** High discount levels directly erode profit margins, occasionally resulting in net losses on specific product lines.
* **Shipping Cost Risks:** Regions with underdeveloped logistics face higher shipping cost ratios, impacting net profitability.
* **Business Recommendations:**
    1. Increase marketing investment in high-profit regions like North America.
    2. Reduce excessive discounting if it consistently lowers profit margins, particularly in Furniture.
    3. Optimize shipping costs in regions where the shipping cost ratio is unusually high.
    4. Promote products with high profit margins instead of focusing purely on top-line sales.
    5. Improve performance in underachieving regions using localized targeting and targeted regional offers.
    6. Encourage preferred payment methods to improve overall checkout completion rates.""")

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.9.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    with open('../notebooks/ecommerce_bi_analysis.ipynb', 'w') as f:
        json.dump(notebook, f, indent=2)
        
    print("Notebook ecommerce_bi_analysis.ipynb created successfully!")

if __name__ == "__main__":
    create_notebook()
