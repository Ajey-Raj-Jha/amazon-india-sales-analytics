# 🛒 Amazon India — A Decade of Sales Analytics 📈

## End-to-End E-Commerce Data Analytics Platform

Amazon India: A Decade of Sales Analytics is an end-to-end data analytics project that transforms **10 years of Amazon India transactional data (2015-2025)** into actionable business insights using **Python, SQL, and Business Intelligence dashboards**.

The project builds a complete **data pipeline from messy raw data to professional analytics dashboards**, demonstrating real-world data science and business intelligence workflows. :contentReference[oaicite:1]{index=1}

---

# 📌 Project Overview

This project focuses on analyzing **nearly 1 million e-commerce transactions** to uncover trends in revenue, customer behavior, product performance, and operational efficiency.

The system includes:

- Advanced **data cleaning pipeline**
- **Exploratory Data Analysis (EDA)**
- **SQL database integration**
- **Interactive BI dashboards**
- **Strategic business insights**

The goal is to transform messy real-world data into a **professional analytics platform for decision making**. :contentReference[oaicite:2]{index=2}

---

# 🎯 Objectives

## Data Engineering

- Clean messy real-world e-commerce data
- Handle missing values and inconsistent formats
- Standardize pricing, dates, and categorical variables

## Data Analysis

- Perform comprehensive **EDA with 20 analytical visualizations**
- Identify **customer behavior patterns**
- Analyze **product and category performance**

## Business Intelligence

- Build **25–30 interactive dashboards**
- Generate **strategic business insights**
- Support **data-driven decision making**

---

# 📊 Dataset Overview

## Dataset Scale

- ~1,000,000 transactions
- Time period: **2015–2025**
- Product catalog: **2000+ products**
- Cities covered: **30+ Indian cities**

The dataset simulates **realistic e-commerce business patterns and challenges**. :contentReference[oaicite:3]{index=3}


### Product Catalog

```
amazon_india_products_catalog.csv
```

Contains product information such as:

- product_id
- product_name
- category
- brand
- base_price
- rating

---

# 🧾 Key Features & Columns

## Transaction Data (45+ columns)

### Identifiers
- transaction_id
- customer_id
- product_id

### Temporal Data
- order_date
- order_month
- order_year
- order_quarter

### Product Information
- product_name
- category
- subcategory
- brand
- product_rating

### Pricing Information
- original_price_inr
- discount_percent
- final_amount_inr
- delivery_charges

### Customer Data
- customer_city
- customer_state
- age_group
- is_prime_member

### Operational Metrics
- payment_method
- delivery_days
- return_status
- customer_rating

### Business Indicators
- is_festival_sale
- festival_name
- customer_spending_tier

---

# 🧹 Data Cleaning Pipeline

The dataset intentionally contains **25% data quality issues** to simulate real-world scenarios. :contentReference[oaicite:4]{index=4}

### Key Cleaning Tasks

- Standardizing multiple **date formats**
- Cleaning **price values with currency symbols**
- Normalizing **customer ratings**
- Standardizing **city names**
- Converting mixed **boolean fields**
- Fixing inconsistent **product categories**
- Cleaning **delivery time data**
- Handling duplicate transactions
- Detecting price outliers
- Standardizing payment methods

---

# 📈 Exploratory Data Analysis

The project includes **20 visualization challenges** designed to analyze business patterns.

### Key EDA Topics

- Revenue growth trends (2015-2025)
- Seasonal sales patterns
- Customer segmentation (RFM analysis)
- Payment method evolution (UPI growth)
- Category-wise performance
- Prime membership impact
- Geographic sales distribution
- Festival sales spikes
- Customer age-group behavior
- Price vs demand correlation

These visualizations provide **deep insights into e-commerce dynamics in India**.

---

# 🗄 SQL Database Integration

## Database Schema

The cleaned data is stored in a relational database with tables such as:

### transactions
Main transaction records

### products
Product catalog and category hierarchy

### customers
Customer segmentation data

### time_dimension
Date dimension table for analytics

---

## SQL Operations

The project implements:

- Data loading pipelines
- Aggregation queries for KPIs
- Multi-table joins for analytics
- Indexing for performance optimization
- Dashboard database connectivity

---

# 📊 Business Intelligence Dashboards

The final system includes **25–30 interactive dashboards**.

## Executive Dashboards

- Revenue growth trends
- Average order value
- Active customers
- Category performance

## Revenue Analytics

- Monthly and yearly revenue patterns
- Category contribution analysis
- Festival sales performance
- Price optimization insights

## Customer Analytics

- RFM segmentation
- Customer lifetime value
- Prime membership behavior
- Customer retention analysis

## Product Analytics

- Product performance rankings
- Brand market share
- Inventory demand trends
- Product lifecycle analysis

## Operations Analytics

- Delivery performance metrics
- Payment method trends
- Return rate analysis
- Customer service performance

---

# ⚙️ Technology Stack

## Programming

Python

## Data Processing

- Pandas
- NumPy

## Visualization

- Matplotlib
- Seaborn

## Database

- SQL
- MySQL / PostgreSQL

## Business Intelligence

- Power BI
- Streamlit


---

# 📈 Expected Outcomes

The project produces:

- Professional **EDA reports**
- Clean production-ready dataset
- Optimized SQL database
- Interactive BI dashboards
- Strategic business insights

These outputs help organizations make **data-driven decisions in e-commerce operations**. :contentReference[oaicite:5]{index=5}

---

# 💡 Business Impact

Insights from the analysis support:

- Revenue optimization strategies
- Customer segmentation and retention
- Product portfolio planning
- Inventory demand forecasting
- Marketing campaign optimization

---

# 👨‍💻 Author

Ajey Jha  
Data Analytics | Data Science | Business Intelligence
