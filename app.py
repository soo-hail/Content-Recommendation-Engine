import os
import time
import pickle
import psycopg2
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
from dotenv import load_dotenv

# LOAD FUNCTION THAT FETCHES-POSTER FOR MOVIES.
from src.utils import fetch_poster

# Load Environment Variables from .env file
load_dotenv()

# PostgreSQL Connection
conn = psycopg2.connect(
    dbname=os.getenv('POSTGRES_DB_NAME'),
    user=os.getenv('POSTGRES_DB_USER'),
    password=os.getenv('POSTGRES_DB_PASSWORD'),
    host=os.getenv('POSTGRES_DB_HOST'),
    port=os.getenv('POSTGRES_DB_PORT')
)

cursor = conn.cursor()

# PAGE CONFIGURATION FOR FULL-SCREEN LAYOUT
st.set_page_config(
    page_title="OTT Platform",
    page_icon="🎥",
    layout="wide"
)

with st.sidebar:
    selected = option_menu(
        menu_title="",
        options=[
            "Search", "Home", "Trending", "Favorites", "Genres", "Live Shows",
            "Watchlist", "History",  # Additional options
            "Settings", "Help & Support", "About"
        ],  
        icons=[
            "search", "house", "fire", "heart", "tags", "tv",
            "list-task", "clock-history",  
            "gear", "info-circle", "question-circle"
        ],  
        menu_icon="cast",  # Menu header icon
        default_index=1  # Highlight the second option by default
    )

if selected == 'Search':
    # LOAD THE PROCESSED-DATA(AS DATAFRAME) AND CONSINE-SIMILARITY MATRIX.
    with open('src/components/artifacts/movie_data.pkl', 'rb') as f:
        df, cosine_sim = pickle.load(f)
    
    # FUNCTION TO GET MOVIE-RECOMENDATION.
    def get_recommendations(title, cosine_sim = cosine_sim):
        
        idx = df[df['original_title'].str.lower() == title.lower()].index[0] # GET INDEX(ROW-NUMBER) OF THE MOVIE.
        sim_scores = list(enumerate(cosine_sim[idx])) # GET ALL THE SIMILARITY-SCORES OF A GIVEN MOVIE WITH OTHER MOVIES.
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse = True) # SORT SIMILARITY SCORES. 
        sim_scores = sim_scores[1:13]  # GET TOP 12 MOVIES
        movie_indices = [i[0] for i in sim_scores]
        
        return df['original_title'].iloc[movie_indices] # RETRIVES TITLES OF MOVIES FROM THE DATA-FRAME USING PROVIDED INDEICES OF MOVIES.
    
    # SETUP USER-INTERFACE USING STREAMLIT.    
    st.title('Movie Recommendation Engine')

    selected_movie = st.selectbox("Select a movie:", df['original_title'].values)        
            
    if st.button('Recommend'):
        # GET RECOMMENDED MOVIES BASED ON SELECTED-MOVIES.
        recommendations = get_recommendations(selected_movie)
        st.write("Top 12 recommended movies:")

        for i in range(0, 10, 6): # LOOP TO ITERATE 2 ROWS(BECAUSE IT INCREMENTS BY 5).
            # CREATE 5 COLUMNS FOR EACH ROW.
            cols = st.columns(6)
            
            for col, idx in zip(cols, range(i, i + 6)): # LOOP TO ITERATE COLUMNS IN A ROW.
                # IDX ---> REPRESENTS INDEX OF RECOMMENDED MOVIES IN 'recommendations'
                if idx < len(recommendations):
                    movie_index = recommendations.index[idx]
                    movie_title = recommendations.iloc[idx]
                    movie_id = df.loc[movie_index, 'id']
                    
                    poster_url = fetch_poster(movie_id)
                    
                    with col:
                        st.image(poster_url, width = 150)
                        st.write(movie_title)
elif selected == "Home":
    # HOME PAGE
    # LOAD DATA-FRAME FROM pickle FILE.
    with open('src/components/artifacts/genres_data.pkl', 'rb') as f:
        genres_df = pickle.load(f)
    
    input_movie = st.text_input('Watch Movie')
    
    genres_list = genres_df['genres'].unique()
    genres_list = genres_list[(genres_list != None) & (genres_list != 'TV Movie') & (genres_list != 'Foreign')]

    if input_movie:
        # FETCH MOVIE-TITLE FROM MOVIE-ID.
        input_movie = int(input_movie)
        title = genres_df[genres_df['id'] == input_movie]['original_title'].iloc[0]
        
        # ADD DATA TO THE DATA-BASE.
        cursor.execute('''
            INSERT INTO user_history (userId, movieId, title, rating) VALUES (%s, %s, %s, %s)
        ''', (1, input_movie, title, 4.5))
        
        conn.commit()
        
    # DISPLAY MOVIE POSTERS IN HOME-PAGE.
    for genre in genres_list:
        st.subheader(f"{genre} Movies")
        
        # Filter movies by genre and pick 10 random movies (or all if less than 10)
        # genre_movies = genres_df[genres_df['genres'] == genre]['id'].drop_duplicates().head(10).tolist()
        genre_movies = genres_df[genres_df['genres'] == genre]['id'].drop_duplicates().sample(n=10).tolist()
        
        # Create columns for displaying posters
        cols = st.columns(10)
        
        for col, movie_id in zip(cols, genre_movies):
            with col: 
              
                # Fetch and display the poster for each movie
                st.image(fetch_poster(movie_id), width=130)
                st.markdown(
                    f"""
                    <p style="margin-bottom: 0.2rem;">TMDB {movie_id}</p>
                    <p style="margin-top: 0; margin-bottom: 0.5rem;">{genres_df[genres_df['id'] == movie_id]['original_title'].iloc[0]}</p>
                    """,
                    unsafe_allow_html=True
                )
                
    
elif selected == 'Trending':
    # TRENDING PAGE
    st.title("Trending Page")
    st.write("Check out the trending content!")

elif selected == 'Favorites':
    # FAVORITES PAGE
    st.title("Favorites")
    st.write("Here are your favorite movies and shows!")

elif selected == 'Genres':
    # GENRES PAGE
    st.title("Genres")
    st.write("Explore movies and shows by genres!")

elif selected == 'Watchlist':
    # WATCHLIST PAGE
    st.title("Watchlist")
    st.write("Movies and shows in your watchlist!")

elif selected == 'History':
    
    st.title('Watch History')
    st.write('Your Watch History')
    
    # FETCH THE MOVIES FROM DATA-BASE.
    cursor.execute('SELECT * FROM user_history')
    rows = cursor.fetchall()
    
    # EXTRACT ALL MOVIE-IDS
    movie_ids = [row[2] for row in rows]
    movie_ids.reverse()
    
    # DISPLAY MOVIES
    for i in range(0, len(movie_ids), 6):
        cols = st.columns(6)
        
        for col, idx in zip(cols, range(i, i + 6)):
            if idx < len(movie_ids):
                with col:
                    st.image(fetch_poster(movie_ids[idx]), width = 150)
    

elif selected == 'Settings':
    # SETTINGS PAGE
    st.title("Settings")
    st.write("Adjust your preferences here!")

elif selected == 'Help & Support':
    # HELP & SUPPORT PAGE
    st.title("Help & Support")
    st.write("How can we assist you?")

elif selected == 'About':
    # ABOUT PAGE
    st.title("About")
    st.write("Learn more about this platform!")
    
    
    
cursor.close()
conn.close()