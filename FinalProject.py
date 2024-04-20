import requests
import json
import unittest
import os
import sqlite3
import random
import string
from bs4 import BeautifulSoup 

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
def retrieve_desserts():
    dessert_titles = []
    url = "https://en.wikipedia.org/wiki/List_of_desserts"
    resp = requests.get(url)
    if resp.status_code == 200:
        html = resp.text
        soup = BeautifulSoup(html, "html.parser")
        row = soup.find_all('div', class_='div-col')[1]
        name_list = row.find_all('a')
        for name in name_list:
            dessert_name = name.text
            dessert_titles.append(dessert_name)
        #print(len(dessert_titles))
        return dessert_titles
    else:
        print("Invalid URL")
     
def get_meal_data():
    # randomLetter = random.choice(string.ascii_letters)
    # print(randomLetter)
    name_id_list = []
    alphabet = [chr(i) for i in range(65, 91)]
    for letter in alphabet:
        # print(letter)

        url = f"https://www.themealdb.com/api/json/v1/1/search.php?f={letter}"

        response = requests.get(url)
        # print(response)
        if response.status_code == 200:
            response_dict = json.loads(response.text)
            meals = response_dict.get("meals")  # Get the list of meals or None
            if meals is not None:
                for meal_data in meals:
                    meal_name = meal_data["strMeal"]
                    meal_id = meal_data["idMeal"]
                    meal_info = (meal_name, meal_id)
                    name_id_list.append(meal_info)
    # print(name_id_list)
    return name_id_list
        # print(name_id_list)
            # for meal_detail in meal_details:
                # print(meal_detail)
        # return (response_dict, name_id_list, url)



def generate_number_letter_tuples():
    # Create a list of tuples containing numbers and corresponding letters
    number_letter_tuples = [(i, chr(i + 96)) for i in range(1, 27)]
    # print(number_letter_tuples)
    return number_letter_tuples

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
def set_up_meal_table(meal_tuple, cur, conn):
    integer_key_mapping = {}
    counter = 0
    number_letter_tuples = generate_number_letter_tuples()
    cur.execute(
        "DROP TABLE IF EXISTS meals"
        )

    cur.execute(
        "CREATE TABLE meals (Integer_Key INTEGER, Starting_Letter TEXT, Meal TEXT UNIQUE, Meal_ID INTEGER)"
        )
    
    for (meal, meal_id) in meal_tuple:
        starting_letter = meal[0].lower() 
        if starting_letter not in integer_key_mapping:
        # Get the corresponding integer key for the starting letter
            integer_key = number_letter_tuples[ord(starting_letter) - ord('a')][0]
            integer_key_mapping[starting_letter] = integer_key
        cur.execute("INSERT OR IGNORE INTO meals (Integer_Key, Starting_Letter, Meal, Meal_ID) VALUES (?, ?, ?, ?)", (integer_key_mapping[starting_letter], starting_letter, meal, meal_id))

        counter += 1
        if counter == 25:
            conn.commit()
            counter = 0  # Reset the counter for the next batch

    # Commit any remaining data
    if counter > 0:
        conn.commit()
    conn.commit()


#Getting drinks id and instructions on how to make the drink
def get_drink_data():
    alphabet = [chr(i) for i in range(65, 91)]
    name_id_list = []

    for letter in alphabet:
        url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={letter}"

        response = requests.get(url)
        print(response)
        if response.status_code == 200:
            response_dict = json.loads(response.text)
            drinks = response_dict.get("drinks")  # Get the list of meals or None
            if drinks is not None:
                for drink_data in drinks:
                    drink_instructions = drink_data["strInstructions"]
                    drink_id = drink_data["idDrink"]
                    drink_info = (drink_instructions, drink_id)
                    name_id_list.append(drink_info)
    print(name_id_list)
    return name_id_list
    # return (response_dict, name_id_list, url)



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
    meal_dict = get_meal_data()
    # drink_dict = get_drink_data()
    # desserts = retrieve_desserts()
    num_letter_list = generate_number_letter_tuples()
    cur, conn = set_up_database("food_data.db")
    meal_table = set_up_meal_table(meal_dict, cur, conn)
    # country_names = retrieve_countries("AlphabeticalCountries.html")
    # print(meal_dict)
    # cached_meal_data = cache_meal_data()
    # print(cache_meal_data(meals, "songdata.txt"))
main()



