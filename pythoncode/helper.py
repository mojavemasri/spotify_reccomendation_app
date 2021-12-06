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
    #given the artist dictionary, returns a list of genres the artist falls under
    @staticmethod
    def getGenreInfo(genreDict):
      g = genreDict["genres"]
      return g

    #given the track dictionary, returns the corresponding album info
    @staticmethod
    def getAlbumInfo(trackDict):
      alb = []
      alb.append(trackDict["album"]["id"])
      alb.append(trackDict["artists"][0]["id"])
      alb.append(trackDict["album"]["name"])
      alb.append(trackDict["album"]["total_tracks"])
      alb.append(trackDict["album"]["album_type"])
      alb.append(trackDict["album"]["release_date"])
      return alb

    #given the artist dictionary and the track dictionary, returns corresponding artist info
    @staticmethod
    def getArtistInfo(trackDict, artistDict):
      art = []
      art.append(trackDict["artists"][0]["id"])
      art.append(trackDict["artists"][0]["name"])
      art.append(artistDict["popularity"])
      return art

    #given the track dictionary, returns corresponding track info
    @staticmethod
    def getTrackInfo(trackDict):
      t = []
      t.append(trackDict["id"])
      t.append(trackDict["album"]["id"])
      t.append(trackDict["artists"][0]["id"])
      t.append(trackDict["name"])
      t.append(trackDict["duration_ms"])
      t.append(trackDict["popularity"])
      t.append(trackDict["explicit"])
      return t


    #given a spotify track ID, it will return the database track id
    #needs to be integrated into database
    @staticmethod
    def getTrackID(track):
      with open('tracks.csv', 'r') as fr:
        line = fr.readline()
        line = fr.readline()
        count = 0
        while line:
          #if count%1000 == 0:
          #  print(f"line {count}")
          #count += 1
          tempID = line[line.index(',')+1:line.index(',') +23]
          #print(tempID)
          if track == tempID:
            fr.close()
            return line[0:line.index(',')-1]
          line = fr.readline()
      fr.close()
    #given a genre name, it will return the genreID
    #needs to be integrated into database
    #when we integrate into the database we will remove the second arguement
    @staticmethod
    def getGenreID(g, genreArr):

      with open('genres.csv', 'r') as fr:
        line = fr.readline()
        line = fr.readline()
        count = 0
        while line:
          #if count%1000 == 0:
          #  print(f"line {count}")

          tempID = line[3:-1]+line[-1]
          if g == tempID:
            return count
          count += 1
          line = fr.readline()
      fr.close()
      for ga in genreArr:
        if ga == g:
          return count
        count += 1
      return count

    #given the track dictionary, it will determine whether or not it is a unique album
    #this one can be written better
    #needs to be integrated into database
    #when we integrate into the database we will remove the second arguement
    @staticmethod
    def uniqueAlbum(tempdict, albumArr):
      album = tempdict["album"]["id"]
      for a in albumArr:
        if a[0] == album:
          return False
      with open('tracks.csv', 'r') as fr:
        line = fr.readline()
        line = fr.readline()
        count = 0
        while line:
          #if count%1000 == 0:
          #  print(f"line {count}")
          #count += 1
          tempID = line[0:22]
          if album == tempID:
            return False
          line = fr.readline()
      fr.close()
      return True


    #given the track dictionary, it will determine whether or not it is a unique artist
    #this one can be written better
    #needs to be integrated into database
    #when we integrate into the database we will remove the second arguement
    @staticmethod
    def uniqueArtist(tempdict, artistArr):

      artist = tempdict["artists"][0]["id"]
      for a in artistArr:
        if a[0] == artist:
          return False
      with open('artists.csv', 'r') as fr:
        line = fr.readline()
        line = fr.readline()
        count = 0
        while line:
          #if count%1000 == 0:
          #  print(f"line {count}")
          #count += 1
          tempID = line[0:22]
          if artist == tempID:
            return False
          line = fr.readline()
      fr.close()
      return True

    #given the genre name, it will determine whether or not it is a unique genre
    #needs to be integrated into database
    #when we integrate into the database we will remove the second arguement
    @staticmethod
    def uniqueGenre(genre, genreArr):
      for g in genreArr:
        if g[0] == genre:
          return False
      with open('genres.csv', 'r') as fr:
        line = fr.readline()
        line = fr.readline()
        count = 0
        while line:
          #if count%1000 == 0:
          #  print(f"line {count}")
          #count += 1
          tempID = line[3:-1]+line[-1]
          if genre == tempID:
            return False
          line = fr.readline()
      fr.close()
      return True

    #given the spotify trackID, it will determine whether or not it is a unique track
    #needs to be integrated into database
    #when we integrate into the database we will remove the second arguement
    @staticmethod
    def uniqueTrack(track, trackArr):
      for t in trackArr:
        if t[1] == track:
          return False
      with open('tracks.csv', 'r') as fr:
        line = fr.readline()
        line = fr.readline()
        count = 0
        while line:
          #if count%1000 == 0:
          #  print(f"line {count}")
          #count += 1
          tempID = line[line.index(',')+1:line.index(',') +23]
          #print(tempID)
          if track == tempID:
            return False
          line = fr.readline()
      fr.close()
      return True


    #given the spotify playlistID, it will determine whether or not it is a unique playlist
    #needs to be integrated into database
    @staticmethod
    def uniquePlaylist(playlist):
      with open('playlists.csv', 'r') as fr:
        line = fr.readline()
        line = fr.readline()
        count = 0
        while line:
          #if count%1000 == 0:
          #  print(f"line {count}")
          #count += 1
          tempID = line[0:22]
          if playlist == tempID:
            return False
          line = fr.readline()
      fr.close()
      return True


    #WE NEED TO REWRITE THE FOLLOWING IN TERMS OF OUR DATABASE:
    #addPlaylistToDatabase(MOVED TO enterRecord)
    #getTrackID
    #getGenreID
    #uniqueAlbum
    #uniqueArtist
    #uniqueGenre
    #uniqueTrack
    #uniquePlaylist
