import random
import math
import csv
import requests
import json
import ast
from db_operations import db_operations
class helper:


    def convertDate(date):
        if len(date) == 4:
            return (date+"-01-01")
        else:
            if len(date) > 5:
                if date[4] == "-":
                    return date + "-01"
            if int(date[-2:-1]+date[-1]) < 22:
                datetemp = "20"
            else:
                datetemp = "19"
            datetemp = datetemp + date[-2:-1]+date[-1]
            date = date[0:-3]
            if date.index('/') == 1:
                datetemp = datetemp + "-0"+date[0]
                date = date[2:-1] + date[-1]
            elif date.index('/') == 2:
                datetemp = datetemp + "-"+date[0:2]
                date = date[3:-1] + date[-1]
            if len(date) == 1:
                datetemp = datetemp + "-0"+ date
            else:
                datetemp = datetemp + "-" + date
            return datetemp
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
        elif itemtype == 5:
            if not url[25:29] == "user":
                return False
            else:
                return True
        else:
            return False

    #its in the name lol
    @staticmethod
    def convertURLtoURI(url):
        if url[25:30] == "track" or url[25:30] == "album":
            return url[31:url.index('?')]
        elif url[25:31] == "artist":
            return url[32:url.index('?')]
        elif url[25:33] == "playlist":
            return url[34:url.index('?')]
        else:
            return ""

    #gets a url from user and returns the ID
    # 1: track
    # 2: album
    # 3: artist
    # 4: playlist
    @staticmethod
    def getURLFromUser(itemtype):
        while True:
            url = input("Enter url:")
            if helper.checkURL(url, itemtype):
                break
            else:
                print("Invalid url, please try again")
        URI = helper.convertURLtoURI(url)
        return URI

    @staticmethod
    def getURIFromUser():
        while True:
            uri = input("Enter ID:")
            if len(uri) == 22:
                break
            else:
                print("Invalid ID, please try again")

        return uri
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
        dbop = db_operations()
        cursor = dbop.getCursor()
        searchTerm = searchTerm.strip()
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
        searchItemName = queryItem + "Name"
        searchItemID = queryItem + "ID"
        query = f'''
            SELECT {searchItemID} FROM {queryItem}
            WHERE {searchItemName} LIKE \'%{searchTerm.lower()}%\'
            LIMIT 50;
        '''
        print(query)
        cursor.execute(query)
        queryResult = cursor.fetchall()
        #print(queryResult)
        for i in range(len(queryResult)):
            queryResult[i] = queryResult[i][0]
            #print(queryResult[i])
        #implement query
        if len(queryResult) == 0:
            print("Sorry, no items were found with this name. Please try again with a different search term.")
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
