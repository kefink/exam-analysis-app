import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64

st.set_page_config(page_title="Teacher Exam Results Analysis", layout="wide")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

image_path = 'jm.jpg'

img_base64 = get_base64_of_bin_file(image_path)

st.markdown(
    f"""
    <style>
        .main {{
            background-image: url("data:image/jpg;base64,{img_base64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .main-title {{
            font-size: 36px;
            color: #2E86C1;
            text-align: center;
            font-weight: bold;
            margin-bottom: 20px;
        }}
        .sidebar .sidebar-content {{
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
        }}
        .reportview-container .main .block-container {{
            padding-top: 20px;
            padding-bottom: 20px;
            padding-left: 20px;
            padding-right: 20px;
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
        }}
        .stButton > button {{
            color: white;
            background-color: #2E86C1;
            border-radius: 10px;
            border: none;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">Teacher Exam Results Analysis</div>', unsafe_allow_html=True)

st.markdown("""
This dashboard is designed to help teachers easily analyze exam results from uploaded CSV files.
You can view summary statistics, filter data, and visualize exam performance trends.
""")

uploaded_file = st.file_uploader("Upload Exam Results CSV File", type="csv")

def load_data(file):
    try:
        data = pd.read_csv(file)
        return data
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def plot_data(data, x_col, y_col, plot_type):
    plt.figure(figsize=(10, 5))
    if plot_type == "Line Plot":
        sns.lineplot(data=data, x=x_col, y=y_col)
    elif plot_type == "Bar Plot":
        sns.barplot(data=data, x=x_col, y=y_col)
    elif plot_type == "Scatter Plot":
        sns.scatterplot(data=data, x=x_col, y=y_col)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

if uploaded_file is not None:
    df = load_data(uploaded_file)

    if df is not None:
        st.subheader("Data Preview")
        st.write(df.head())

        st.subheader("Data Summary")
        st.write(df.describe())

        st.subheader("Filter Data")
        columns = df.columns.tolist()
        selected_column = st.selectbox("Select column to filter by", columns)
        unique_values = df[selected_column].unique()
        selected_value = st.selectbox("Select value", unique_values)

        filtered_df = df[df[selected_column] == selected_value]
        st.write(filtered_df)

        st.subheader("Plot Data")
        x_column = st.selectbox("Select x-axis column", columns)
        y_column = st.selectbox("Select y-axis column", columns)
        plot_type = st.selectbox("Select plot type", ["Line Plot", "Bar Plot", "Scatter Plot"])

        if st.button("Generate Plot"):
            plot_data(filtered_df, x_column, y_column, plot_type)
    else:
        st.warning("No data to display. Please upload a valid CSV file.")

else:
    st.write("Waiting for file upload...")
