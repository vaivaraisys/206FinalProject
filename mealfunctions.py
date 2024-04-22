import requests
import json
import unittest
import os
import sqlite3
import random
import string
from bs4 import BeautifulSoup 

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
            # print(response_dict)
                # if response_dict["Response"] == "False":
                #     return None
        # else:
        #     pass
        for meal, meal_details in response_dict.items():
            # print(meal)
            # print(meal_details) 
            if meal_details == None:
                continue
            else:
                for meal_data in meal_details:
                    # print(meal_data)  
                    meal_name = meal_data["strMeal"]
                    # print(meal_name)   
                    meal_id = meal_data["idMeal"]   
                    # print(meal_id)
                    meal_info = (meal_name, meal_id)                    
                    # print(meal_info)
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

# sets up meal data table 
def set_up_meal_table(meal_dict, cur, conn, max_items=25):
    # # print(meal_dict)
    # integer_key_mapping = {}
    # # counter = 0
    # number_letter_tuples = generate_number_letter_tuples()
    # cur.execute(
    #     "DROP TABLE IF EXISTS meal_names"
    #     )
    # cur.execute(
    #     "DROP TABLE IF EXISTS meal_ids"
    #     )

    # cur.execute(
    #     "CREATE TABLE meal_names (Integer_Key INTEGER, Starting_Letter TEXT, Meal_name TEXT UNIQUE)"
    #     )
    # cur.execute(
    #     "CREATE TABLE meal_ids (Integer_Key INTEGER, Starting_Letter TEXT, Meal_id TEXT UNIQUE)"
    #     )
    
    # for (meal, meal_id) in meal_dict:
    #     starting_letter = meal[0].lower() 
    #     if starting_letter not in integer_key_mapping:
    #         integer_key = number_letter_tuples[ord(starting_letter) - ord('a')][0]
    #         integer_key_mapping[starting_letter] = integer_key
    #     cur.execute("INSERT OR IGNORE INTO meal_names (Integer_Key, Starting_Letter, Meal_name) VALUES (?, ?, ?)", (integer_key_mapping[starting_letter], starting_letter, meal))
    #     cur.execute("INSERT OR IGNORE INTO meal_ids (Integer_Key, Starting_Letter, Meal_id) VALUES (?, ?, ?)", (integer_key_mapping[starting_letter], starting_letter, meal_id))

    # conn.commit()

    integer_key_mapping = {}
    # counter = 0
    number_letter_tuples = generate_number_letter_tuples()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS meal_names (Integer_Key INTEGER, Starting_Letter TEXT, Meal_name TEXT UNIQUE)"
        )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS meal_ids (Integer_Key INTEGER, Starting_Letter TEXT, Meal_id TEXT UNIQUE)"
        )
    cur.execute(
        "SELECT COUNT (*) FROM meal_names"
    )
    idx = cur.fetchall()
    idx = idx[0][0]

    cur.execute("SELECT Meal_name FROM meal_names")
    existing_meal_names = set(row[0] for row in cur.fetchall())
    
    cur.execute("SELECT Meal_id FROM meal_ids")
    existing_meal_ids = set(row[0] for row in cur.fetchall())
    
    for i in range(idx, idx + 25):
        for meal, meal_id in meal_dict:
            if meal not in existing_meal_names and meal_id not in existing_meal_ids:
                starting_letter = meal[0].lower() 
                if starting_letter not in integer_key_mapping:
                    integer_key = number_letter_tuples[ord(starting_letter) - ord('a')][0]
                    integer_key_mapping[starting_letter] = integer_key
                cur.execute("INSERT OR IGNORE INTO meal_names (Integer_Key, Starting_Letter, Meal_name) VALUES (?, ?, ?)", (integer_key_mapping[starting_letter], starting_letter, meal))

                cur.execute("INSERT OR IGNORE INTO meal_ids (Integer_Key, Starting_Letter, Meal_id) VALUES (?, ?, ?)", (integer_key_mapping[starting_letter], starting_letter, meal_id))

                existing_meal_names.add(meal)
                existing_meal_ids.add(meal_id)
    
    conn.commit()


def main():
    # meal_dict = get_meal_data()
    # generate_number_letter_tuples()
    # cur, conn = set_up_database("food_data.db")
    # set_up_meal_table(meal_dict, cur, conn)
    meal_dict = get_meal_data()
    generate_number_letter_tuples()
    cur, conn = set_up_database("food_data.db")
    set_up_meal_table(meal_dict, cur, conn, max_items=25)
main()