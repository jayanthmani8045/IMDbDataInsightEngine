import streamlit as st

st.set_page_config(
    page_title="IMDb Scraper & Visualizer",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 IMDb Scraper & Visualizer")

st.markdown("""
This application allows you to scrape movie data directly from IMDb search result pages and visualize the collected data.

### How It Works
1.  **Data Collection:** Navigate to the `Data Collection` page to input an IMDb search URL and the corresponding genre. The app uses Selenium to scrape the data, which is then stored for analysis.
2.  **Data Visualization:** Go to the `Data Visualization` page to create and compare various graphs based on the data you've collected.

### Technologies Used
- **Streamlit:** For creating the interactive web application.
- **Selenium:** For automating the web browser to scrape data.
- **Pandas:** For data manipulation and storage.
- **Matplotlib & Seaborn:** For creating data visualizations.
""")