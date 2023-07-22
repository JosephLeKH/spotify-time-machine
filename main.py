"""
Purpose: This program takes a date from 2000 and compile a Spotify playlist of the Billboard Top 100 songs of that
day in the user's Spotify account.
Tools: BeautifulSoup, Spotipy
"""
import requests
import os
from bs4 import BeautifulSoup
import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth

#Take user's input and scrape the songs and artists from the Billboard Top 100
date = input("Enter the date of the playlist (YYYY-MM-DD) :")
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}").text
soup = BeautifulSoup(response, "html.parser")
songs = [x.getText().strip() for x in soup.select(selector="li h3", class_="c-title")]
artists = [x.getText().strip() for x in soup.find_all(name="span", class_="c-label") if len(x.getText().strip()) > 3]

#Autheticate the API using info from Spotify Developer
auth = SpotifyOAuth(client_id=os.environ["SPOTIFY_ID"], client_secret=os.environ["SPOTIFY_SECRET"],
                    redirect_uri="https://example.com/",
                    scope="playlist-modify-private", cache_path="token.txt", show_dialog=True)

#Create the Spotipy object and user_id for adding playlist
spotify = sp.Spotify(auth_manager=auth)
user_id = spotify.current_user()["id"]

#Create a list of song URLs using the songs and artists
songs_url = []
for i in range(0, 100, 1):
    result = spotify.search(q=f"track: {songs[i]} year:{date[:4]}", limit=1, type="track", market="US")
    if len(songs_url) < 100:
        try:
            songs_url.append(result["tracks"]["items"][0]["uri"])
        except IndexError:
            pass

#Create playlistID and add the list of song URLs to that playlist
playlistID = spotify.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)["uri"]
spotify.user_playlist_add_tracks(user=user_id, playlist_id=playlistID, tracks=songs_url)