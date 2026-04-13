# FInTracker_Smart_Expense_Categorization

# 💰 Smart Expense Categorization & Analytics Dashboard

## 🚀 Overview

This project is a complete Expense Tracking System that:

* Reads transaction data from CSV
* Cleans and validates data
* Categorizes expenses using rule-based logic
* Stores data in SQLite database
* Generates analytics and visualizations

---

## 🧠 Features

* CSV Upload & Parsing 📂
* Data Cleaning & Validation 🧹
* Rule-Based Categorization 🏷️
* SQLite Database Storage 🗄️
* Analytics:

  * Total Income
  * Total Expense
  * Category-wise summary
* Graphs:

  * 📊 Bar Chart
  * 🥧 Pie Chart
  * 📈 Line Chart
  * 📉 Histogram
  * 📦 Box Plot
* Streamlit Dashboard UI 🎨

---

## 🏗️ Tech Stack

* Python
* Pandas
* NumPy
* Matplotlib
* SQLite
* Streamlit

---

## 📁 Project Structure

```
hack_2.py              → Backend (processing + analytics)
streamlit_app.py       → Frontend (dashboard)
transactions.csv       → Input data
output.csv             → Processed data
expenses.db            → SQLite database
*.png                  → Generated charts
```

---

## ⚙️ How to Run

### 1. Install dependencies

```
pip install pandas numpy matplotlib streamlit
```

### 2. Run backend (optional)

```
python hack_2.py
```

### 3. Run dashboard

```
streamlit run streamlit_app.py
```

---

## 📊 Generated Graphs

### Histogram

Shows distribution of transaction amounts

### Line Chart

Shows category-wise trend

### Pie Chart

Shows percentage distribution

### Bar Chart

Shows category totals

### Box Plot

Shows spread of amounts (outliers)

---

## 🧠 How It Works

1. CSV is uploaded
2. Data is cleaned (invalid rows removed)
3. Transactions are categorized
4. Data is stored in SQLite database
5. Analytics are calculated
6. Graphs are generated
7. Dashboard displays insights

---

## 🎯 Key Concepts Used

* Data Cleaning
* Rule-Based Classification
* Database Integration
* Data Visualization
* Modular Programming (Classes)

---

## 👥 Team Roles

* Backend Developer → Processing & DB
* Frontend Developer → Dashboard
* Data Engineer → Cleaning & categorization
* Analyst → Insights & graphs

---

## 🌟 Future Improvements

* Machine Learning categorization
* Login system
* Advanced analytics

---

## 📌 Demo Flow

Upload CSV → Process Data → View Stats → Analyze Graphs
