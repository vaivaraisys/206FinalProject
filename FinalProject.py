import requests
import json
import unittest
import os
import sqlite3
import random
import string

# do not think we need this
def load_json(filename):
    try:    
        with open(filename, "r") as fh:
            data_content = json.load(fh)
            return data_content
    except:
        return {}
# do not think we need this
def write_json(dict, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(dict, file, indent=4)
        print(f"JSON data has been successfully written to {filename}.")
    except:
        print("error opening or converting json file")


# create a function that uses beautiful soup to get area names to loop through in the function below here for meals


# gets the meal name and id        
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
    print(name_id_list)
        # for meal_detail in meal_details:
            # print(meal_detail)
    return (response_dict, name_id_list, url)

# Sets up the data base 
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

# sets up meal data table ****(NOT WORKING)*****
def set_up_types_table(meal_tuple, cur, conn):
    type_list = []
    for pokemon in data:
        pokemon_type = pokemon["type"][0]
        if pokemon_type not in type_list:
            type_list.append(pokemon_type)
        if len(pokemon["type"]) > 1:
            pokemon_type = pokemon["type"][1]
            if pokemon_type not in type_list:
                type_list.append(pokemon_type)
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Types (id INTEGER PRIMARY KEY, type TEXT UNIQUE)"
    )
    for i in range(len(type_list)):
        cur.execute(
            "INSERT OR IGNORE INTO Types (id,type) VALUES (?,?)", (i,
                                                                   type_list[i])
        )
    conn.commit()


#Getting drinks id and instructions on how to make the drink
def get_drink_data():
    randomLetter = random.choice(string.ascii_letters)
    print(randomLetter)
    url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={randomLetter}"

    response = requests.get(url)
    print(response)

    if response.status_code == 200:
        response_dict = json.loads(response.text)
        # print(response_dict)
    else:
        # print(f"Error: {response.status_code} {response.reason}")
        return None

    name_id_list = []
    for drink, drink_details in response_dict.items():
        # print(meal_details) 
        for drink_data in drink_details:
            # print(meal_data)  
            drink_instructions = drink_data["strInstructions"]
            # print(meal_name)   
            drink_id = drink_data["idDrink"]   
            # print(meal_id)
            drink_info = (drink_id, drink_instructions)
            name_id_list.append(drink_info)
    print(name_id_list)
        # for meal_detail in meal_details:
            # print(meal_detail)
    return (response_dict, name_id_list, url)



# set up table for drinks ****(NOT WORKING)****
def set_up_types_table(drink_tuple, cur, conn):
    type_list = []
    for pokemon in data:
        pokemon_type = pokemon["type"][0]
        if pokemon_type not in type_list:
            type_list.append(pokemon_type)
        if len(pokemon["type"]) > 1:
            pokemon_type = pokemon["type"][1]
            if pokemon_type not in type_list:
                type_list.append(pokemon_type)
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Types (id INTEGER PRIMARY KEY, type TEXT UNIQUE)"
    )
    for i in range(len(type_list)):
        cur.execute(
            "INSERT OR IGNORE INTO Types (id,type) VALUES (?,?)", (i,
                                                                   type_list[i])
        )
    conn.commit()    


# create a function that makes some sort of calculation


# create a function that makes some sort of visual


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
    meal_dict = get_meal_data("Canadian")
    drink_dict = get_drink_data()
    # print(meal_dict)
    # cached_meal_data = cache_meal_data()
    # print(cache_meal_data(meals, "songdata.txt"))
main()



