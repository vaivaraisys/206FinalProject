from processdata import *
from mealfunctions import *
from drinkfunctions import *
from dessertfunctions import *
import requests
import json
import unittest
import os
import sqlite3
import random
import string
from bs4 import BeautifulSoup 
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('_mpl-gallery-nogrid')

def meal_pie_chart():
    meal_tuple = get_meal_data()
    letter_count = {}
    for meal, meal_id in meal_tuple:
        starting_letter = meal[0].lower()
        letter_count[starting_letter] = letter_count.get(starting_letter, 0) + 1
    
    letters = list(letter_count.keys())
    counts = list(letter_count.values())
    
    fig, ax = plt.subplots()
    ax.pie(counts, labels=letters, autopct='%1.1f%%', startangle=90)
    ax.axis('equal') 

    plt.savefig("meal_barchart")
    plt.title('Distribution of Meals by Starting Letter', y= 1.1)
    plt.show()

def meal_bar_graph():
    meal_tuple = get_meal_data()
    meal_count = {}
    
    for meal, meal_id in meal_tuple:
        starting_letter = meal[0].lower()
        if starting_letter in meal_count:
            meal_count[starting_letter] += 1
        else:
            meal_count[starting_letter] = 1
   
    letters = list(meal_count.keys())
    counts = list(meal_count.values())

    plt.bar(letters, counts, color="red")
    
    plt.xlabel('Starting Letter')
    plt.ylabel('Number of Meals')
    plt.title('Number of Meals by Starting Letter')
    
    plt.savefig("meal_barchart")
    plt.show()

def desserts_pie_chart():
    desserts_list = retrieve_desserts()
    letter_count = {}
    for dessert in desserts_list:
        starting_letter = dessert[0].lower()
        letter_count[starting_letter] = letter_count.get(starting_letter, 0) + 1
    
    letters = list(letter_count.keys())
    counts = list(letter_count.values())
    
    fig, ax = plt.subplots()
    ax.pie(counts, labels=letters, autopct='%1.1f%%', startangle=90)
    ax.axis('equal') 

    plt.title('Distribution of Desserts by Starting Letter', y= 1.1)
    plt.show()

def desserts_bar_graph():
    desserts_list = retrieve_desserts()
    letter_count = {}
    
    for dessert in desserts_list:
        starting_letter = dessert[0].lower()
        if starting_letter in letter_count:
            letter_count[starting_letter] += 1
        else:
            letter_count[starting_letter] = 1
   
    letters = list(letter_count.keys())
    counts = list(letter_count.values())

    plt.bar(letters, counts, color="red")
    
    plt.xlabel('Starting Letter')
    plt.ylabel('Number of Dessserts')
    plt.title('Number of Deesserts by Starting Letter')
    

    plt.show()



def main():
    meal_pie_chart()
    # meal_bar_graph()
    # desserts_pie_chart()
    # desserts_bar_graph()
main()




