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

def set_up_integer_table(cur, conn, num_letter_tup):
    cur.execute(
        "DROP TABLE IF EXISTS Integer_Letter"
    )
    cur.execute(
        "CREATE TABLE integer_letter (Integer_Key INTEGER, Letter TEXT)"
        )
        # print(num_letter_tup)
    for number, letter in num_letter_tup:
        cur.execute(
            "INSERT INTO integer_letter (Integer_Key, Letter) VALUES (?, ?)", (number, letter)
            )
    conn.commit()


def set_up_meal_table(meal_dict, cur, conn, max_items=25):
    number_letter_tuples = generate_number_letter_tuples()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='meal_names'")
    table_exists = cur.fetchone() is not None

    if not table_exists:
        cur.execute(
            "CREATE TABLE meal_names (Integer_Key INTEGER, Starting_Letter TEXT, Meal_name TEXT UNIQUE)"
        )
        cur.execute(
            "CREATE TABLE meal_ids (Integer_Key INTEGER, Starting_Letter TEXT, Meal_id TEXT UNIQUE)"
        )
        conn.commit()

    cur.execute("SELECT COUNT(*) FROM meal_names")
    current_count = cur.fetchone()[0]

    cur.execute("SELECT Meal_name FROM meal_names")
    existing_meal_names = set(row[0] for row in cur.fetchall())

    cur.execute("SELECT Meal_id FROM meal_ids")
    existing_meal_ids = set(row[0] for row in cur.fetchall())

    num_to_insert = min(max_items, len(meal_dict) - current_count)

    data_to_insert = []
    for meal, meal_id in meal_dict[current_count:current_count + num_to_insert]:
        if meal not in existing_meal_names and meal_id not in existing_meal_ids:
            starting_letter = meal[0].lower()
            integer_key = number_letter_tuples[ord(starting_letter) - ord('a')][0]
            data_to_insert.append((integer_key, starting_letter, meal, meal_id))
            existing_meal_names.add(meal)
            existing_meal_ids.add(meal_id)

    if data_to_insert:
        cur.executemany("INSERT OR IGNORE INTO meal_names (Integer_Key, Starting_Letter, Meal_name) VALUES (?, ?, ?)", [(d[0], d[1], d[2]) for d in data_to_insert])
        cur.executemany("INSERT OR IGNORE INTO meal_ids (Integer_Key, Starting_Letter, Meal_id) VALUES (?, ?, ?)", [(d[0], d[1], d[3]) for d in data_to_insert])

    conn.commit()

def main():
    # meal_dict = get_meal_data()
    num_letter_tup = generate_number_letter_tuples()
    # cur, conn = set_up_database("food_data.db")
    # set_up_meal_table(meal_dict, cur, conn)
    meal_dict = get_meal_data()
    generate_number_letter_tuples()
    cur, conn = set_up_database("food_data.db")
    set_up_meal_table(meal_dict, cur, conn, max_items=25)
    set_up_integer_table(cur, conn, num_letter_tup)
main()