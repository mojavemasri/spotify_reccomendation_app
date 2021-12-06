import random
import math
import numpy as np
import csv
import requests
import json
import ast

class helper():

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


    #given a playlist id or url, it will figure out what is new in the list(new track, new artist, etc)
    #and it will add each new record to a list
    #we still need to add this to a database
    @staticmethod
    def addPlaylistToDatabase(playlist):

      if playlist[0:10] == 'https://op':
        playlistID = playlist[34:56]
      else:
        playlistID = playlist
      playlistArr = returnPlaylistTracks(playlist)
      print(playlistArr)
      gajunction = []
      ptjunction = []
      trackArr = []
      albumArr = []
      artistArr = []
      genreArr = []
      playlistInfo = []
      counter = 0
      for tempdict in playlistArr:

        t = tempdict['id']
        if tempdict["is_local"]:
          continue
        print(t)
        if uniqueTrack(t, trackArr):
          tempt = getTrackInfo(tempdict)
          if uniqueAlbum(tempdict, albumArr):
            tempalb = getAlbumInfo(tempdict)
            if uniqueArtist(tempdict, artistArr):
              tempartistdict = getArtistDict(tempdict["artists"][0]["id"])
              tempart = getArtistInfo(tempdict, tempartistdict)
              for g in tempartistdict['genres']:
                if uniqueGenre(g, genreArr):
                  genreArr.append(g)
                gajunction.append([tempdict["artists"][0]["id"], getGenreID(g, genreArr)])
              artistArr.append(tempart)
            albumArr.append(tempalb)
          trackArr.append(tempt)
        ptjunction.append([playlistID, t, counter])
        counter += 1
      playlistDict = getPlaylistDict(playlist)
      playlistInfo = [playlistID, playlistDict["name"], str(len(playlistDict["tracks"]["items"]))]
      print(f"Playlist info: {playlistInfo}")
      #add items HERE to their respective databases. genreid,trackid,ptjunction, and gajunction should be autoincrement so u should take that into consideration
      #--------------------------------




      #--------------------------------
      #this return statement wont be necessary if u r already adding the items to the database
      return[playlistInfo, trackArr, albumArr, artistArr, genreArr, gajunction, ptjunction]

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
    #addPlaylistToDatabase
    #getTrackID
    #getGenreID
    #uniqueAlbum
    #uniqueArtist
    #uniqueGenre
    #uniqueTrack
    #uniquePlaylist
