import streamlit as st  # type: ignore
import pandas as pd
from scraper import scrape_imdb_action_movies
import os

st.title("1. Collect Movie Data")

CSV_FILE = "imdb_data.csv"

def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame()

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

if 'movie_df' not in st.session_state:
    st.session_state.movie_df = load_data()

with st.form(key='scrape_form'):
    url = st.text_input("Enter IMDb Search URL", "https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres=adventure")
    genre = st.text_input("Enter Genre", "Adventure")
    submit_button = st.form_submit_button(label='Scrape Data')

if submit_button:
    if not url or not genre:
        st.warning("Please provide both a URL and a Genre.")
    elif "imdb.com/search/" not in url:
        st.error("Please enter a valid IMDb search URL.")
    else:
        with st.spinner(f"Scraping {genre} movies... please wait."):
            try:
                scraped_df = scrape_imdb_action_movies(url, genre)

                # --- FIX: Check if the DataFrame has data before accessing the 'Title' column ---
                existing_titles = set() # Default to an empty set
                if not st.session_state.movie_df.empty:
                    existing_titles = set(st.session_state.movie_df['Title'].dropna())
                # --- End of Fix ---

                new_movies_df = scraped_df[~scraped_df['Title'].isin(existing_titles)]

                if not new_movies_df.empty:
                    combined_df = pd.concat([st.session_state.movie_df, new_movies_df], ignore_index=True)

                    # Data Cleaning Section
                    combined_df['Year'] = pd.to_numeric(combined_df['Year'], errors='coerce')
                    combined_df['Rating'] = pd.to_numeric(combined_df['Rating'], errors='coerce')
                    vote_count_cleaned = combined_df['Vote Count'].astype(str).str.replace(r'[()KMB]+', '', regex=True).str.strip()
                    combined_df['Vote Count'] = pd.to_numeric(vote_count_cleaned, errors='coerce')

                    save_data(combined_df)
                    st.session_state.movie_df = combined_df
                    st.success(f"Scraping complete. Added {len(new_movies_df)} new movies to the dataset.")
                else:
                    st.info("Scraping complete. No new movies were found to add.")

            except Exception as e:
                st.error(f"An error occurred: {e}")

if not st.session_state.movie_df.empty:
    st.header("Collected Movie Data")
    st.dataframe(st.session_state.movie_df)
else:
    st.info("No data collected yet. Use the form above to start scraping.")