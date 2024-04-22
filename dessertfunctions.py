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

def set_up_desserts_table(desserts_tuple, cur, conn):
    integer_key_mapping = {}
    number_letter_tuples = generate_number_letter_tuples()
    cur.execute(
        "DROP TABLE IF EXISTS desserts"
        )

    cur.execute(
        "CREATE TABLE desserts (Integer_Key INTEGER, Starting_Letter TEXT, Desserts TEXT UNIQUE)"
        )
    for dessert in desserts_tuple:
        starting_letter = dessert[0].lower()
        # print("Starting Letter:", starting_letter)
        
        # print("ASCII Value of starting letter:", ord(starting_letter))
        # print("ASCII Value of 'a':", ord('a'))
        
        index = ord(starting_letter.lower()) - ord('a')
        # print("Calculated Index:", index)
        
        if 0 <= index < len(number_letter_tuples):
            integer_key = number_letter_tuples[index][0]
            integer_key_mapping[starting_letter] = integer_key
            cur.execute("INSERT OR IGNORE INTO desserts (Integer_Key, Starting_Letter, Desserts) VALUES (?, ?, ?)", (integer_key_mapping[starting_letter], starting_letter, dessert))
        else:
            print("Index out of range:", index)

    conn.commit()
    
    # for desserts in desserts_tuple:
    #     starting_letter = desserts[0].lower() 
    #     if starting_letter not in integer_key_mapping:
    #         integer_key = number_letter_tuples[ord(starting_letter) - ord('a')][0]
    #         integer_key_mapping[starting_letter] = integer_key
    #     cur.execute("INSERT OR IGNORE INTO desserts (Integer_Key, Starting_Letter, Desserts) VALUES (?, ?, ?)", (integer_key_mapping[starting_letter], starting_letter, desserts))

    
    # conn.commit()

def main():
    desserts_list = retrieve_desserts()
    generate_number_letter_tuples()
    cur, conn = set_up_database("food_data.db")
    set_up_desserts_table(desserts_list, cur, conn)

main()