# 🎬 IMDb Scraper & Visualizer

This project is an interactive web application built with Streamlit that allows users to dynamically scrape movie data from IMDb search pages and visualize the results. Users can input a URL and genre, collect data in real-time using Selenium, and then create custom, comparative plots to analyze trends in movie ratings, release years, and more.

## ✨ Features

  * **Dynamic Web Scraping**: Utilizes Selenium to scrape data from JavaScript-heavy IMDb pages.
  * **Multi-Page Interface**: A clean, multi-page app layout created with Streamlit.
  * **Persistent Data Collection**: Scrape multiple pages and genres; the data is aggregated and persists across sessions.
  * **Interactive Visualizations**: Generate and compare bar charts, scatter plots, and histograms using Matplotlib and Seaborn.
  * **Robust Error Handling**: Gracefully handles invalid user inputs and potential scraping errors.

-----

## 🛠️ Tech Stack

  * **Backend & Scraping**: Python, Selenium, Pandas
  * **Frontend & Data App**: Streamlit
  * **Data Visualization**: Matplotlib, Seaborn

-----

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

  * Python 3.8 or higher
  * Google Chrome browser installed
  * ChromeDriver (must match your Chrome browser version)
      * Ensure that `chromedriver.exe` (on Windows) or `chromedriver` (on Mac/Linux) is in your system's PATH.

### Installation & Setup

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/jayanthmani8045/IMDbDataInsightEngine.git
    cd IMDbDataInsightEngine
    ```

2.  **Create and activate a virtual environment (Recommended):**

    ```sh
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required libraries:**

    ```sh
    pip install -r requirements.txt
    ```

-----

## usage Usage

To run the Streamlit application, execute the following command in your terminal from the project's root directory:

```sh
streamlit run Home.py
```

Your web browser will automatically open to the application's main page.

1.  Navigate to the **Data Collection** page from the sidebar.
2.  Enter a valid IMDb search URL and the corresponding genre.
3.  Click the "Scrape Data" button and wait for the process to complete.
4.  Navigate to the **Data Visualization** page to create plots from the collected data.

-----

## 📁 Project Structure

The project uses a multi-page app structure recognized by Streamlit:

```
├── Home.py              # The main "About" page
├── scraper.py          # Contains the Selenium scraping function
├── requirements.txt    # Project dependencies
└── pages/
    ├── 1_Data_Collection.py
    └── 2_Data_Visualization.py
```

-----

## 📈 Future Improvements

  * **Asynchronous Scraping**: Implement `asyncio` to speed up the data collection process.
  * **Advanced Filtering**: Add options on the visualization page to filter the DataFrame by year, rating, etc.
  * **Deployment**: Containerize the application with Docker and deploy it to a cloud service like Streamlit Community Cloud or AWS.
