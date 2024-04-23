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
        # print(dessert_titles)
        return dessert_titles
    else:
        print("Invalid URL")

def set_up_desserts_table(desserts_tuple, cur, conn, max_items=25):
    number_letter_tuples = generate_number_letter_tuples()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='desserts'")
    table_exists = cur.fetchone() is not None
    if not table_exists:
        cur.execute(
            "CREATE TABLE desserts (Integer_Key INTEGER, Starting_Letter TEXT, Dessert_name TEXT UNIQUE)"
        )
        conn.commit()
    cur.execute("SELECT COUNT(*) FROM desserts")
    current_count = cur.fetchone()[0]
    cur.execute("SELECT Dessert_name FROM desserts")
    
    # gets all of the meals currently in the table as a list of tuples
    existing_dessert_names = set(row[0] for row in cur.fetchall())
    # limits the number of items inserted doesn't exceed the maximum allowed (max items), and ensures that you don't try to insert more items than are desserts_tuple
    num_to_insert = min(max_items, len(desserts_tuple) - current_count)
    #data to be inserted into the database will be stored.
    data_to_insert = []
    #iterates over a chunk of data based on the current count 
    for dessert in desserts_tuple[current_count:current_count + num_to_insert]:
          #checks to make sure there is no duplicated data in the existing data list we make and that the starting letter is valid
        if dessert[0].lower() in string.ascii_lowercase:
                starting_letter = dessert[0].lower()
                integer_key = number_letter_tuples[ord(starting_letter) - ord('a')][0]
                 # if the data is not in the exisiting desserts list, we add it to the list for inserting 
                data_to_insert.append((integer_key, starting_letter, dessert))
                #after the data is inserted we add it to existing desserts list so it does not get duplicated
                existing_dessert_names.add(dessert)
        else:
            print(f"Invalid starting letter: {dessert[0]}")

    if data_to_insert:
        cur.executemany("INSERT OR IGNORE INTO desserts (Integer_Key, Starting_Letter, Dessert_name) VALUES (?, ?, ?)", [(d[0], d[1], d[2]) for d in data_to_insert])

    conn.commit()

def main():
    desserts_list = retrieve_desserts()
    generate_number_letter_tuples()
    cur, conn = set_up_database("food_data.db")
    set_up_desserts_table(desserts_list, cur, conn, max_items=25)

main()