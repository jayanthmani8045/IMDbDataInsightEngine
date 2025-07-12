import streamlit as st
import pandas as pd
from scraper import scrape_imdb_action_movies

st.title("1. Collect Movie Data")

# Initialize the DataFrame in session state if it doesn't exist
if 'movie_df' not in st.session_state:
    st.session_state.movie_df = pd.DataFrame()

# Use a form to get user input
with st.form(key='scrape_form'):
    url = st.text_input("Enter IMDb Search URL", "https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres=action")
    genre = st.text_input("Enter Genre", "Action")
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
                # Append new data to the existing DataFrame in session state
                st.session_state.movie_df = pd.concat([st.session_state.movie_df, scraped_df], ignore_index=True)
                st.success(f"Successfully scraped {len(scraped_df)} movies!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Display the collected data if the DataFrame is not empty
if not st.session_state.movie_df.empty:
    st.header("Collected Movie Data")
    st.dataframe(st.session_state.movie_df)
else:
    st.info("No data collected yet. Use the form above to start scraping.")