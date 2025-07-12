import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("2. Visualize Collected Data")

# Check if data exists in session state
if 'movie_df' not in st.session_state or st.session_state.movie_df.empty:
    st.warning("No data to visualize. Please go to the 'Data Collection' page to scrape data first.")
    st.page_link("pages/1_Data_Collection.py", label="Go to Data Collection")
    st.stop()

df = st.session_state.movie_df

# --- Data Cleaning for Visualization ---
# Convert relevant columns to numeric types, handling errors
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

# Clean and convert 'Vote Count'
# CORRECTED LINE: First, convert the column to string type to handle any non-string values
df['Vote Count'] = df['Vote Count'].astype(str).str.replace(r'[()KMB]+', '', regex=True).str.strip()
df['Vote Count'] = pd.to_numeric(df['Vote Count'], errors='coerce')

# Get column lists for selectboxes
numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
all_cols = df.columns.tolist()

# --- Plotting Function ---
def create_plot(plot_type, x_axis, y_axis=None):
    fig, ax = plt.subplots(figsize=(10, 6))
    if plot_type == 'Bar Plot':
        sns.barplot(x=x_axis, y=y_axis, data=df, ax=ax)
    elif plot_type == 'Scatter Plot':
        sns.scatterplot(x=x_axis, y=y_axis, data=df, ax=ax)
    elif plot_type == 'Histogram':
        sns.histplot(data=df, x=x_axis, kde=True, ax=ax)
    elif plot_type == 'Line Plot':
        # Line plots are best with sorted data
        line_data = df.dropna(subset=[x_axis, y_axis]).sort_values(by=x_axis)
        sns.lineplot(x=x_axis, y=y_axis, data=line_data, ax=ax)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

# --- Layout for Two Graphs ---
col1, col2 = st.columns(2)

# --- Graph 1 Controls ---
with col1:
    st.header("Graph 1")
    plot_type1 = st.selectbox("Choose plot type", ["Bar Plot", "Scatter Plot", "Histogram", "Line Plot"], key="plot1")
    
    if plot_type1 == "Histogram":
        x_axis1 = st.selectbox("Choose a column for the Histogram", numeric_cols, key="x1")
        fig1 = create_plot(plot_type1, x_axis1)
        st.pyplot(fig1)
    else:
        x_axis1 = st.selectbox("Choose X-axis", all_cols, key="x1_else")
        y_axis1 = st.selectbox("Choose Y-axis", numeric_cols, key="y1")
        fig1 = create_plot(plot_type1, x_axis1, y_axis1)
        st.pyplot(fig1)

# --- Graph 2 Controls ---
with col2:
    st.header("Graph 2")
    plot_type2 = st.selectbox("Choose plot type", ["Bar Plot", "Scatter Plot", "Histogram", "Line Plot"], key="plot2")

    if plot_type2 == "Histogram":
        x_axis2 = st.selectbox("Choose a column for the Histogram", numeric_cols, key="x2")
        fig2 = create_plot(plot_type2, x_axis2)
        st.pyplot(fig2)
    else:
        x_axis2 = st.selectbox("Choose X-axis", all_cols, key="x2_else")
        y_axis2 = st.selectbox("Choose Y-axis", numeric_cols, key="y2")
        fig2 = create_plot(plot_type2, x_axis2, y_axis2)
        st.pyplot(fig2)