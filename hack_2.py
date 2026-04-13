import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

# -------------------------------
# CSV Parser
# -------------------------------
class CSVParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        return pd.read_csv(self.file_path)


# -------------------------------
# Data Cleaner
# -------------------------------
class DataCleaner:
    def clean(self, df):
        df['description'] = df['description'].astype(str).str.upper()
        df['description'] = df['description'].str.replace(r'[^A-Z0-9 ]', '', regex=True)

        # Date validation
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        if df['date'].isna().sum() > 0:
            print("⚠️ Invalid dates removed")

        # Amount validation
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        if df['amount'].isna().sum() > 0:
            print("⚠️ Invalid amounts removed")

        # Type validation
        df['type'] = df['type'].str.lower()
        valid_types = ['credit', 'debit']
        if (~df['type'].isin(valid_types)).sum() > 0:
            print("⚠️ Invalid types removed")

        df = df.dropna()
        df = df[df['type'].isin(valid_types)]

        return df


# -------------------------------
# Categorizer
# -------------------------------
class Categorizer:
    def categorize(self, desc):
        if "SALARY" in desc or "BONUS" in desc:
            return "Income"
        elif "RENT" in desc:
            return "Rent"
        elif any(x in desc for x in ["SWIGGY","ZOMATO","DOMINOS","STARBUCKS","GROCERY"]):
            return "Food"
        elif any(x in desc for x in ["UBER","OLA"]):
            return "Travel"
        elif any(x in desc for x in ["AMAZON","FLIPKART"]):
            return "Shopping"
        elif any(x in desc for x in ["ELECTRICITY","WATER","RECHARGE"]):
            return "Bills"
        elif any(x in desc for x in ["NETFLIX","SPOTIFY","PRIME"]):
            return "Entertainment"
        elif any(x in desc for x in ["APOLLO","MEDPLUS","HOSPITAL"]):
            return "Healthcare"
        elif "LIC" in desc:
            return "Insurance"
        elif "TRANSFER" in desc:
            return "Transfer"
        elif "INTEREST" in desc:
            return "Interest"
        else:
            return "Other"


# -------------------------------
# NEW: Database Manager
# -------------------------------
class DatabaseManager:
    def __init__(self, db_name="expenses.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                date TEXT,
                description TEXT,
                amount REAL,
                type TEXT,
                category TEXT
            )
        ''')
        self.conn.commit()

    def insert_data(self, df):
        df.to_sql("transactions", self.conn, if_exists='replace', index=False)
        print("✅ Data saved to database")

    def fetch_data(self):
        return pd.read_sql_query("SELECT * FROM transactions", self.conn)


# -------------------------------
# Analytics
# -------------------------------
class Analytics:
    def __init__(self, df):
        self.df = df

    def total_income(self):
        return np.sum(self.df[self.df['type'] == 'credit']['amount'])

    def total_expense(self):
        return np.sum(self.df[self.df['type'] == 'debit']['amount'])

    def category_summary(self):
        return self.df.groupby('category')['amount'].sum()

    def plot_line(self):
        summary = self.category_summary()
        plt.figure()
        plt.plot(summary.index, summary.values, marker='o')
        plt.title("Line Chart")
        plt.xticks(rotation=45)
        plt.savefig("line_chart.png")
        plt.close()

    def plot_bar(self):
        summary = self.category_summary()
        plt.figure()
        plt.bar(summary.index, summary.values)
        plt.title("Bar Chart")
        plt.xticks(rotation=45)
        plt.savefig("bar_chart.png")
        plt.close()

    def plot_pie(self):
        summary = self.category_summary()
        plt.figure()
        plt.pie(summary.abs().values, labels=summary.index, autopct='%1.1f%%')
        plt.title("Pie Chart")
        plt.savefig("pie_chart.png")
        plt.close()

    def plot_histogram(self):
        plt.figure()
        plt.hist(self.df['amount'], bins=10)
        plt.title("Histogram")
        plt.savefig("histogram.png")
        plt.close()

    def plot_box(self):
        plt.figure()
        plt.boxplot(self.df['amount'])
        plt.title("Box Plot")
        plt.savefig("boxplot.png")
        plt.close()


# -------------------------------
# Main Class
# -------------------------------
class ExpenseManager:
    def __init__(self, file_path):
        self.parser = CSVParser(file_path)
        self.cleaner = DataCleaner()
        self.categorizer = Categorizer()
        self.db = DatabaseManager()   # NEW

    def run(self):
        df = self.parser.load_data()
        df = self.cleaner.clean(df)

        df['category'] = df['description'].apply(self.categorizer.categorize)

        # Save to database
        self.db.insert_data(df)

        # Fetch again (optional but good practice)
        df = self.db.fetch_data()

        analytics = Analytics(df)

        print("Total Income:", analytics.total_income())
        print("Total Expense:", analytics.total_expense())
        print("\nCategory Summary:\n", analytics.category_summary())

        analytics.plot_line()
        analytics.plot_bar()
        analytics.plot_pie()
        analytics.plot_histogram()
        analytics.plot_box()

        df.to_csv("output.csv", index=False)
        print("\n✅ Data saved in CSV + Database + Graphs generated!")


# -------------------------------
# Run
# -------------------------------
if __name__ == "__main__":
    app = ExpenseManager("transactions.csv")
    app.run()