import streamlit as st
from streamlit_option_menu import option_menu

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
    # SEARCH PAGE
    st.header("Search Movies and Shows")
    search_query = st.text_input("Search for movies", "", placeholder="Type a movie title...")
    if search_query:
        st.write(f"Results for '{search_query}'")
        # You can add more logic here to fetch and display results based on the search query

elif selected == "Home":
    # HOME PAGE
    st.title("Home Page")
    st.write("Welcome to the Home Page!")

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
    # HISTORY PAGE
    st.title("History")
    st.write("Your watched history!")

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
