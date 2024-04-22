import requests
import json
import unittest
import os
import sqlite3
import random
import string
from bs4 import BeautifulSoup 
from mealfunctions import generate_number_letter_tuples
from mealfunctions import set_up_database

#Getting drinks id and instructions on how to make the drink
def get_drink_data():
    alphabet = [chr(i) for i in range(65, 91)]
    name_id_list = []

    for letter in alphabet:
        url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={letter}"

        response = requests.get(url)
        # print(response)

        if response.status_code == 200:
            response_dict = json.loads(response.text)
            # print(response_dict)
        else:
            # print(f"Error: {response.status_code} {response.reason}")
            return None

        for drink, drink_details in response_dict.items():
            if drink_details == None:
                continue
            else:
            # print(meal_details) 
                for drink_data in drink_details:
                    # print(meal_data)  
                    drink_instructions = drink_data["strInstructions"]
                    # print(meal_name)   
                    drink_id = drink_data["idDrink"]   
                    # print(meal_id)
                    drink_info = (drink_id, drink_instructions)
                    name_id_list.append(drink_info)
    # print(name_id_list)
        # for meal_detail in meal_details:
            # print(meal_detail)
    return name_id_list
    # return (response_dict, name_id_list, url)

#same thing: create i variable/counter/accumulator that calls the next 25 after breaking

# set up table for drinks ****(NOT WORKING)****
def set_up_drink_table(drink_dict, cur, conn):
    integer_key_mapping = {}
    # counter = 0
    number_letter_tuples = generate_number_letter_tuples()
    # print(number_letter_tuples)
    cur.execute(
        "DROP TABLE IF EXISTS drinks"
        )

    cur.execute(
        "CREATE TABLE drinks (Integer_Key INTEGER, Starting_Letter TEXT, Drink_Instructions TEXT UNIQUE, Drink_ID INTEGER)"
        )
    
    for (drink_id, drink_instructions) in drink_dict:
        starting_letter = drink_instructions[0].lower()
        # print("Starting Letter:", starting_letter)
        
        # print("ASCII Value of starting letter:", ord(starting_letter))
        # print("ASCII Value of 'a':", ord('a'))
        
        index = ord(starting_letter.lower()) - ord('a')
        # print("Calculated Index:", index)
        
        if 0 <= index < len(number_letter_tuples):
            integer_key = number_letter_tuples[index][0]
            integer_key_mapping[starting_letter] = integer_key
            cur.execute("INSERT OR IGNORE INTO drinks (Integer_Key, Starting_Letter, Drink_Instructions, Drink_ID) VALUES (?, ?, ?, ?)", (integer_key_mapping[starting_letter], starting_letter, drink_instructions, drink_id))
        else:
            print("Index out of range:", index)

    conn.commit()



def main():
    drink_dict = get_drink_data()
    generate_number_letter_tuples()
    cur, conn = set_up_database("food_data.db")
    set_up_drink_table(drink_dict, cur, conn)

main()


