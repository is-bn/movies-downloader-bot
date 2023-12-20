import requests
from bs4 import BeautifulSoup

def search_movies(query):
    movies_list = []
    movies_details = {}
    website = BeautifulSoup(requests.get(f"https://mkvcinemas.skin/?s={query.replace(' ', '+')}").text, "html.parser")
    movies = website.find_all("a", {'class': 'ml-mask jt'})
    for movie in movies:
        if movie:
            movies_details["id"] = f"link{movies.index(movie)}"
            movies_details["title"] = movie.find("span", {'class': 'mli-info'}).text
            movies_details["link"] = movie['href'] # Store the direct link to the movie
            movies_list.append(movies_details)
            movies_details = {}
    return movies_list

def get_movie(query):
    movie_details = {}
    movie_page_link = BeautifulSoup(requests.get(f"{query}").text, "html.parser") # Use the direct link
    if movie_page_link:
        title = movie_page_link.find("div", {'class': 'mvic-desc'}).h3.text
        movie_details["title"] = title
        img = movie_page_link.find("div", {'class': 'mvic-thumb'})['data-bg']
        movie_details["img"] = img
        links = movie_page_link.find_all("a", {'rel': 'noopener', 'data-wpel-link': 'internal'})
        final_links = {}
        for i in links:
            final_links[f"{i.text}"] = i['href'] # Store the direct links without shortening
        movie_details["links"] = final_links
    return movie_details
