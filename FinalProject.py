import requests
import json
import unittest
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

API_KEY = 'f0cf7dff'

def load_json(filename):
    try:    
        with open(filename, "r") as fh:
            data_content = json.load(fh)
            return data_content
    except:
        return {}

def write_json(dict, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(dict, file, indent=4)
        print(f"JSON data has been successfully written to {filename}.")
    except:
        print("error opening or converting json file")
        
def get_music_data(song):
    '''
    creates API request
    ARGUMENTS: 
        title: title of the movie you're searching for 

    RETURNS: 
        tuple with the response text and url OR None if the 
        request was unsuccesful
    '''


    url = ""

    response = requests.get(url)
    print(response)

    if response.status_code == 200:
        response_dict = json.loads(response.text)
        if response_dict["Response"] == "False":
            return None
        return (response_dict, url)
    else:
        # print(f"Error: {response.status_code} {response.reason}")
        return None
    


    
def main():
    '''
    Note that your cache file will be called 
    cache.json and will be created in your current directory

    Make sure you are in the directory you want to be work in 
    prior to running
    '''
    #######################################
    # DO NOT CHANGE THIS 
    # this code loads in the list of movies and 
    # removes whitespace for you!
    with open('/Users/vaivaraisys/Desktop/SI206/206FinalProject/songdata.txt', 'r') as f: 
        songs = f.readlines()
        
    for i in range(len(songs)): 
        songs[i] = songs[i].strip()
    
    # resp = 
    # print(resp)
        
    # DO NOT CHANGE THIS 
    #######################################
    print(get_music_data("passionfruit-104"))