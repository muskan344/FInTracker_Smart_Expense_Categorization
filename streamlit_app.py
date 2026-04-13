import io
from pathlib import Path

import pandas as pd
import streamlit as st

from hack_2 import Analytics, CSVParser, Categorizer, DataCleaner


st.set_page_config(page_title="Expense Analytics Dashboard", layout="wide")
st.title("Expense Analytics Dashboard")


def run_pipeline(uploaded_file):
    """Run existing backend pipeline without changing backend logic."""
    temp_path = Path("uploaded_transactions.csv")
    temp_path.write_bytes(uploaded_file.getbuffer())

    parser = CSVParser(str(temp_path))
    cleaner = DataCleaner()
    categorizer = Categorizer()

    # Read file using pandas after upload (requirement).
    raw_df = pd.read_csv(io.BytesIO(uploaded_file.getvalue()))

    # Use existing backend methods.
    df = parser.load_data()
    df = cleaner.clean(df)
    df["category"] = df["description"].apply(categorizer.categorize)

    analytics = Analytics(df)
    return raw_df, df, analytics


def get_invalid_rows(raw_df):
    """Identify invalid rows using the same validation rules as backend cleaner."""
    temp_df = raw_df.copy()
    temp_df["date_parsed"] = pd.to_datetime(temp_df.get("date"), errors="coerce")
    temp_df["amount_parsed"] = pd.to_numeric(temp_df.get("amount"), errors="coerce")
    temp_df["type_normalized"] = temp_df.get("type").astype(str).str.lower()

    invalid_mask = (
        temp_df["date_parsed"].isna()
        | temp_df["amount_parsed"].isna()
        | ~temp_df["type_normalized"].isin(["credit", "debit"])
    )
    invalid_rows = temp_df.loc[invalid_mask].copy()
    return invalid_rows.drop(columns=["date_parsed", "amount_parsed", "type_normalized"])


st.header("Upload CSV")
uploaded_file = st.file_uploader("Upload your transactions CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        with st.spinner("Processing file and generating analytics..."):
            raw_df, cleaned_df, analytics = run_pipeline(uploaded_file)
            invalid_rows_df = get_invalid_rows(raw_df)

            # Success message after upload and read.
            st.success("File uploaded and processed successfully.")
            if not invalid_rows_df.empty:
                st.warning(
                    f"Warning: {len(invalid_rows_df)} invalid row(s) found in uploaded data. "
                    "They are shown below for review."
                )

            # Generate charts through existing Analytics methods.
            analytics.plot_line()
            analytics.plot_bar()
            analytics.plot_pie()
            analytics.plot_histogram()
            analytics.plot_box()

        st.header("Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Income", f"{analytics.total_income():,.2f}")
        with col2:
            st.metric("Total Expense", f"{analytics.total_expense():,.2f}")

        st.header("Category Summary")
        category_df = analytics.category_summary().reset_index()
        category_df.columns = ["Category", "Amount"]
        st.dataframe(category_df, use_container_width=True)

        # Keep summary report download button.
        summary_report = category_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Summary Report",
            data=summary_report,
            file_name="summary_report.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.header("Charts")
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.subheader("Line Chart")
            st.image("line_chart.png", use_container_width=True)
            st.subheader("Pie Chart")
            st.image("pie_chart.png", use_container_width=True)
            st.subheader("Box Plot")
            st.image("boxplot.png", use_container_width=True)
        with chart_col2:
            st.subheader("Bar Chart")
            st.image("bar_chart.png", use_container_width=True)
            st.subheader("Histogram")
            st.image("histogram.png", use_container_width=True)

        st.header("Data Preview")
        preview_col1, preview_col2 = st.columns(2)
        with preview_col1:
            st.subheader("Uploaded Data")
            st.dataframe(raw_df, use_container_width=True)
            if not invalid_rows_df.empty:
                st.subheader("Invalid Rows (Noted)")
                st.dataframe(invalid_rows_df, use_container_width=True)
        with preview_col2:
            st.subheader("Processed Data")
            st.dataframe(cleaned_df, use_container_width=True)

    except Exception as exc:
        st.error(f"Failed to process file: {exc}")
else:
    st.info("Upload a CSV file to start analysis.")
