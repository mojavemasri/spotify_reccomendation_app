import random
import math
import numpy as np
import csv
import requests
import json
import ast

class helper():

    #takes in a spotify url and an item type and returns if it is a valid url
    # 1: track
    # 2: album
    # 3: artist
    # 4: playlist
    @staticmethod
    def checkURL(url, itemtype):
        if not url[0:25] == 'https://open.spotify.com/':
            return False
        elif itemtype == 1:
            if not url[25:30] == "track":
                return False
            else:
                return True
        elif itemtype == 2:
            if not url[25:30] == "album":
                return False
            else:
                return True
        elif itemtype == 3:
            if not url[25:31] == "artist":
                return False
            else:
                return True
        elif itemtype == 4:
            if not url[25:33] == "playlist":
                return False
            else:
                return True
        else:
            return False

    #its in the name lol
    @staticmethod
    def convertURLtoURI(url):
        if url[25:30] == "track" or url[25:30] == "album":
            return url[32:url.index(?)]
        elif url[25:31] == "artist":
            return url[33:url.index(?)]
        elif url[25:33] == "playlist":
            return url[35:url.index(?)]
        else:
            return ""

    #gets a url from user and returns the ID
    # 1: track
    # 2: album
    # 3: artist
    # 4: playlist
    @staticmethod
    def getURLFromUser(itemtype):
        while True
            url = input("Enter url:")
            if helper.checkURL(url, itemtype):
                break
            else:
                print("Invalid url, please try again")
        return convertURLtoURI(url)

    #takes in a spotify url and an item type and returns if it is a valid url
    # ITEM TYPES
    # 1: track
    # 2: album
    # 3: artist
    # 4: playlist
    # 5: genre
    # SEARCH TYPES
    # 1: name


    @staticmethod
    def searchDB(searchTerm, itemtype):
        queryItem = ""
        searchItem = ""
        if itemtype == 1:
            queryItem = 'track'
        elif itemtype == 2:
            queryItem = 'album'
        elif itemtype == 3:
            queryItem = 'artist'
        elif itemtype == 4:
            queryItem = 'playlist'
        elif itemtype == 5:
            queryItem = 'genre'
        searchItem = queryItem + "Name"
        query = ''''''
        queryResult = []
        #implement query
        return queryResult


    # function checks for user input given a list of choices
    @staticmethod
    def get_choice(lst):
        choice = input("Enter choice number: ")
        while choice.isdigit() == False:
            print("Incorrect option. Try again")
            choice = input("Enter choice number: ")

        while int(choice) not in lst:
            print("Incorrect option. Try again")
            choice = input("Enter choice number: ")
        return int(choice)
    
