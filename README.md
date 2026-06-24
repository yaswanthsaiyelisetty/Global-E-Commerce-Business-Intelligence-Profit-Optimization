# Global E-Commerce Business Intelligence & Profit Optimization Dashboard

## Project Overview
The Global E-Commerce Business Intelligence & Profit Optimization Dashboard is an end-to-end data analytics project that translates 3 years of global e-commerce transaction data into actionable business insights. It includes a comprehensive data processing pipeline, SQL analytics integration, exploratory data analysis (EDA), and a highly interactive, responsive web-based executive dashboard.

## Business Problem
Global e-commerce businesses face the challenge of identifying the key drivers of their profitability among vast amounts of transactional data. Excessive discounting, fluctuating shipping costs, and underperforming regional markets can easily erode profit margins despite high top-line revenue. This project aims to pinpoint these operational inefficiencies and recommend strategic business pivots.

## Dataset Description
The dataset (`global_ecommerce_sales.csv`) contains e-commerce transaction records spanning 2023–2025. It includes critical fields such as:
- **Order Details:** Order_ID, Order_Date, Quantity, Unit_Price, Total_Sales, Discount_Percent
- **Customer Details:** Customer_Name, Customer_Segment, Country, Region
- **Product Details:** Product_Category, Product_Name
- **Operational Metrics:** Shipping_Cost, Profit, Payment_Method

## Tools and Technologies
- **Python:** Data processing, cleaning, feature engineering, and KPI generation.
- **Pandas & NumPy:** Data manipulation and transformation.
- **SQLite:** SQL analytics and data storage.
- **Matplotlib & Seaborn:** Data visualization in the Jupyter Notebook.
- **Scikit-learn:** Data transformation for machine learning readiness (Scaling & Encoding).
- **HTML5, CSS3, Vanilla JS:** Frontend development for the web dashboard.
- **Chart.js:** Interactive frontend charts.
- **Vercel:** Static site deployment.

## Skills Implemented
- Data Cleaning and Preprocessing
- Feature Engineering
- SQL Analytics & Aggregations
- Advanced Pandas (GroupBy, Pivot Tables, Merging)
- Exploratory Data Analysis (EDA)
- Executive Dashboards & Data Visualization
- Data Transformation (MinMax/Standard Scaling, One-Hot Encoding)
- Frontend Development (Responsive UI, Async Fetch)

## Folder Structure
```text
Global-Ecommerce-BI-Dashboard/
│
├── data/
│   └── global_ecommerce_sales.csv
├── notebooks/
│   └── ecommerce_bi_analysis.ipynb
├── cleaned_data/
│   └── cleaned_ecommerce_sales.csv
├── database/
│   └── ecommerce_sales.db
├── app/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── insights.json
├── reports/
│   └── executive_summary.md
├── scripts/
│   ├── generate_insights.py
│   └── create_notebook.py
├── README.md
└── requirements.txt
```

## Key KPIs
- Total Revenue
- Total Profit
- Total Orders
- Average Order Value
- Profit Margin
- Total Shipping Cost

## Dashboard Screenshots
*(Placeholder for Dashboard Screenshots)*
![Dashboard Screenshot 1](https://via.placeholder.com/1000x500.png?text=Executive+Dashboard+View)

## Business Insights
1. **Top Revenue Regions:** Asia Pacific and North America dominate global sales.
2. **Profit Drivers:** The Technology and Furniture categories drive the highest profitability.
3. **Margin Risks:** Heavy discounting directly correlates with negative profit margins in certain product categories.
4. **Logistics Impact:** High shipping cost ratios in specific regions drastically reduce net profitability.

## How to Run the Notebook
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Open Jupyter Notebook:
   ```bash
   jupyter notebook notebooks/ecommerce_bi_analysis.ipynb
   ```
5. Run the cells to view the EDA, data cleaning pipeline, and SQL queries.

## How to Run the Dashboard Locally
To view the executive web dashboard:
1. Navigate to the `app/` folder.
2. Serve the folder using a local web server (required for fetching `insights.json`). For example, using Python:
   ```bash
   python -m http.server 8000
   ```
3. Open your browser and go to `http://localhost:8000`.

## How to Deploy on Vercel
This project includes a fully responsive frontend that is ready to be hosted on Vercel.
1. Push this project repository to GitHub.
2. Log in to [Vercel](https://vercel.com/) and click **Add New > Project**.
3. Import your GitHub repository.
4. Set the **Root Directory** to `app`.
5. Leave the framework preset and build commands as default.
6. Click **Deploy**. Your dashboard will be live within seconds.

## Conclusion
This project successfully transformed raw transactional e-commerce data into a sophisticated business intelligence tool. By integrating Python data science workflows, SQL analytics, and a modern frontend dashboard, it provides a comprehensive perspective on business health and operational efficiency, proving readiness for real-world strategic data analysis.
