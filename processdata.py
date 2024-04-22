
import requests
import json
import unittest
import os
import sqlite3
import random
import string
from bs4 import BeautifulSoup 
# from mealfunctions import set_up_meal_table
# from dessertfunctions import set_up_desserts_table
from mealfunctions import set_up_database


def meal_dessert_data(cur, conn):
    cur.execute(
        "SELECT desserts.Desserts, meal_names.Meal_name FROM desserts INNER JOIN meal_names ON desserts.Integer_Key = meal_names.Integer_Key AND desserts.Starting_Letter = meal_names.Starting_Letter"
    )
    meal_dessert_data = cur.fetchall()
    # print(meal_dessert_data)
    return meal_dessert_data

def calculate_most_letter_meals(meal_dessert_data):
    # cur.execute("SELECT Starting_Letter, COUNT(*) AS Meal_Count FROM meal_names GROUP BY Starting_Letter ORDER BY Meal_Count DESC LIMIT 1")
    # most_common_letter = cur.fetchone()
    # print(most_common_letter)
    letter_count = {}
    for dessert, meal in meal_dessert_data:
        dessert_letter = dessert[0].lower()
        meal_letter = meal[0].lower()
        
        if dessert_letter in letter_count:
            letter_count[dessert_letter] += 1
        else:
            letter_count[dessert_letter] = 1
        
        if meal_letter in letter_count:
            letter_count[meal_letter] += 1
        else:
            letter_count[meal_letter] = 1
    
    most_common_letter = max(letter_count, key=letter_count.get)
    # print(most_common_letter)
    return most_common_letter

def main(): 
    cur, conn = set_up_database("food_data.db")
    meal_dessert_data(cur, conn)
    calculate_most_letter_meals(meal_dessert_data)
main()
    
