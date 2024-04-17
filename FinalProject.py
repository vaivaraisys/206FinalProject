import requests
import json
import unittest
import os
import sqlite3


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
        
def get_meal_data(area):
    '''
    creates API request
    ARGUMENTS: 
        title: title of the movie you're searching for 

    RETURNS: 
        tuple with the response text and url OR None if the 
        request was unsuccesful
    '''


    url = f"https://www.themealdb.com/api/json/v1/1/filter.php?a={area}"

    response = requests.get(url)
    print(response)

    if response.status_code == 200:
        response_dict = json.loads(response.text)
        # if response_dict["Response"] == "False":
        #     return None
    else:
        return None
    name_id_list = []
    for meal, meal_details in response_dict.items():
        # print(meal_details) 
        for meal_data in meal_details:
            # print(meal_data)  
            meal_name = meal_data["strMeal"]
            # print(meal_name)   
            meal_id = meal_data["idMeal"]   
            # print(meal_id)
            meal_info = (meal_name, meal_id)
            name_id_list.append(meal_info)
    # print(name_id_list)
        # for meal_detail in meal_details:
            # print(meal_detail)
    return (response_dict, name_id_list, url)

    
def cache_meal_data(areas):
    # cache_content = load_json(areas)
    meal_detail = get_meal_data(areas)
    json_content = write_json(meal_detail, "area_meals.json")

def set_up_database(db_name):
    """
    Sets up a SQLite database connection and cursor.

    Parameters
    -----------------------
    db_name: str
        The name of the SQLite database.

    Returns
    -----------------------
    Tuple (Cursor, Connection):
        A tuple containing the database cursor and connection objects.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn


def get_drink_data(drink):

    url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink}"

    response = requests.get(url)
    print(response)

    if response.status_code == 200:
        response_dict = json.loads(response.text)
        # if response_dict["Response"] == "False":
        #     return None
        return (response_dict, url)
    else:
        # print(f"Error: {response.status_code} {response.reason}")
        return None
    
def cache_music_data(songs, file_name):
    cache_content = load_json(file_name)
    successes = 0
    total_music = len(songs)

    for song in songs:
        song_detail = get_music_data(song)
        if song_detail != None:
            response_details, requested_url = get_music_data(song)
            if requested_url not in list(cache_content.keys()):
                successes += 1
                cache_content[requested_url] = response_details
    if successes > 0:
        write_json(cache_content, file_name)
    percent_found = int(successes/total_music) * 100
    # print(f"Cached data for {percent_found}% of movies")
    return f"Cached data for {percent_found}% of movies"


    
def main():
    '''
    Note that your cache file will be called 
    cache.json and will be created in your current directory

    Make sure you are in the directory you want to be work in 
    prior to running
    '''

    
    # resp = 
    # print(resp)
        
    # DO NOT CHANGE THIS 
    #######################################
    print(get_music_data("passionfruit-104"))
    print(cache_music_data(songs, "songdata.txt"))