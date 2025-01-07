import requests

# FETCH MOVIE POSTERS FROM TMDB-API
def fetch_poster(movie_id):
    api_key = '7b995d3c6fd91a2284b4ad8cb390c7b8'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
        
    try:
        # REQUEST
        response = requests.get(url)
            
        # FETCH-POSTER PATH.
        data = response.json()
        poster_path = data['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
            
        return full_path
    except Exception as e:
        pass