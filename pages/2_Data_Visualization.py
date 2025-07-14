import streamlit as st # type: ignore
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go # type: ignore
import numpy as np # type: ignore

st.set_page_config(layout="wide")
st.title("📊 Data Analysis, Visualization, and Filtration")

# --- Initial Check for Data ---
if 'movie_df' not in st.session_state or st.session_state.movie_df.empty:
    st.warning("No data to visualize. Please go to the 'Data Collection' page to scrape data first.")
    st.page_link("pages/1_Data_Collection.py", label="Go to Data Collection")
    st.stop()

df = st.session_state.movie_df.copy()

# --- Helper Function for Data Cleaning ---
def duration_to_minutes(duration_str):
    if isinstance(duration_str, str):
        parts = duration_str.replace('h', '').replace('m', '').split()
        hours = int(parts[0]) if len(parts) > 0 else 0
        minutes = int(parts[1]) if len(parts) > 1 else 0
        return hours * 60 + minutes
    return np.nan # Return NaN for non-string types

# --- Data Pre-processing ---
# This ensures that even if the page reruns, we start with the clean types
df['Duration_minutes'] = df['Duration'].apply(duration_to_minutes)
df.dropna(subset=['Title', 'Year', 'Rating', 'Vote Count', 'Duration_minutes'], inplace=True)

# --- Sidebar Filters ---
st.sidebar.header("Filter Options")

# Genre Filter
genres = df['Genre'].unique()
selected_genres = st.sidebar.multiselect("Select Genre(s)", genres, default=genres)

# Rating Filter
min_rating = st.sidebar.slider("Select Minimum Rating", 
                               min_value=float(df['Rating'].min()), 
                               max_value=float(df['Rating'].max()), 
                               value=float(df['Rating'].min()))

# Vote Count Filter
max_vote = int(df['Vote Count'].max())
min_votes = st.sidebar.slider("Select Minimum Vote Count", 
                              min_value=0, 
                              max_value=max_vote, 
                              value=0,
                              step=1000)

# Duration Filter
max_duration = int(df['Duration_minutes'].max())
duration_range = st.sidebar.slider("Select Duration (in minutes)", 
                                   min_value=0, 
                                   max_value=max_duration, 
                                   value=(0, max_duration))

# --- Apply Filters ---
filtered_df = df[
    (df['Genre'].isin(selected_genres)) &
    (df['Rating'] >= min_rating) &
    (df['Vote Count'] >= min_votes) &
    (df['Duration_minutes'] >= duration_range[0]) &
    (df['Duration_minutes'] <= duration_range[1])
]

# --- Main Page Display ---
st.header("Filtered Movie Results")
st.write(f"Displaying **{len(filtered_df)}** movies based on your filters.")
st.dataframe(filtered_df.drop(columns=['Duration_minutes']))

# --- Tabs for Visualizations ---
tab1, tab2, tab3, tab4 = st.tabs(["🏆 Top Movies & Genre Leaders", "📊 Genre Analysis", "📈 Rating & Duration Analysis", "🔍 Correlation"])

with tab1:
    st.subheader("Top 10 Movies")
    col1, col2 = st.columns(2)
    with col1:
        st.write("By Rating")
        top_rated = filtered_df.sort_values(by="Rating", ascending=False).head(10)
        st.dataframe(top_rated[['Title', 'Rating', 'Vote Count']])
    with col2:
        st.write("By Voting Counts")
        top_voted = filtered_df.sort_values(by="Vote Count", ascending=False).head(10)
        st.dataframe(top_voted[['Title', 'Vote Count', 'Rating']])
    
    st.subheader("Top-Rated Movie by Genre")
    genre_leaders = filtered_df.loc[filtered_df.groupby('Genre')['Rating'].idxmax()]
    st.dataframe(genre_leaders[['Genre', 'Title', 'Rating']])

with tab2:
    st.subheader("Genre Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Most Popular Genres by Total Votes")
        genre_votes = filtered_df.groupby('Genre')['Vote Count'].sum().sort_values(ascending=False)
        fig_pie = go.Figure(data=[go.Pie(labels=genre_votes.index, values=genre_votes.values, hole=.3)])
        fig_pie.update_layout(title_text='Genre Popularity by Votes')
        st.plotly_chart(fig_pie)
    with col2:
        st.write("Genre Distribution (Count of Movies)")
        genre_counts = filtered_df['Genre'].value_counts()
        st.bar_chart(genre_counts)

with tab3:
    st.subheader("Rating and Duration Insights")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Rating Distribution")
        fig_hist, ax_hist = plt.subplots()
        sns.histplot(filtered_df['Rating'], kde=True, ax=ax_hist)
        ax_hist.set_title('Distribution of Movie Ratings')
        st.pyplot(fig_hist)
    with col2:
        st.write("Average Duration by Genre")
        avg_duration = filtered_df.groupby('Genre')['Duration_minutes'].mean().sort_values()
        fig_bar, ax_bar = plt.subplots()
        avg_duration.plot(kind='barh', ax=ax_bar)
        ax_bar.set_title('Average Movie Duration (minutes) by Genre')
        st.pyplot(fig_bar)

    st.subheader("Duration Extremes")
    shortest_movie = filtered_df.loc[filtered_df['Duration_minutes'].idxmin()]
    longest_movie = filtered_df.loc[filtered_df['Duration_minutes'].idxmax()]
    col_short, col_long = st.columns(2)
    with col_short:
        st.metric("Shortest Movie", f"{int(shortest_movie['Duration_minutes'])} mins", delta=shortest_movie['Title'], delta_color="off")
    with col_long:
        st.metric("Longest Movie", f"{int(longest_movie['Duration_minutes'])} mins", delta=longest_movie['Title'], delta_color="off")

with tab4:
    st.subheader("Correlation Analysis")
    fig_scatter, ax_scatter = plt.subplots(figsize=(10,6))
    sns.scatterplot(data=filtered_df, x='Vote Count', y='Rating', hue='Genre', ax=ax_scatter, alpha=0.7)
    ax_scatter.set_title('Rating vs. Vote Count')
    ax_scatter.set_xscale('log') # Use a log scale for better visualization of vote counts
    st.pyplot(fig_scatter)

    st.subheader("Average Ratings Heatmap")
    try:
        heatmap_data = filtered_df.groupby('Genre')['Rating'].mean().reset_index()
        fig_heatmap, ax_heatmap = plt.subplots()
        sns.heatmap(heatmap_data.set_index('Genre'), annot=True, fmt=".1f", cmap="viridis", ax=ax_heatmap)
        ax_heatmap.set_title('Average Rating by Genre')
        st.pyplot(fig_heatmap)
    except Exception as e:
        st.warning(f"Could not generate heatmap: {e}")