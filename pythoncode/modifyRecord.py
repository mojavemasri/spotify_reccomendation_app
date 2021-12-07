from apihelper import apihelper
from helper import helper
from db_operations import db_operations

class modifyRecord():
    #given a playlist id or url, it will figure out what is new in the list(new track, new artist, etc)
    #and it will add each new record to a list
    #we still need to add this to a database
    @staticmethod
    def addPlaylistToDatabase(playlist, apihelp):
      if playlist[0:10] == 'https://op':
        playlistID = playlist[34:56]
      else:
        playlistID = playlist
      playlistArr = apihelp.returnPlaylistTracks(playlist)
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
        #print(t)
        if uniqueTrack(t, trackArr):
            addTrackToDatabase(t, apihelp)
        ptjunction.append([playlistID, t, counter])
        counter += 1
      playlistDict = apihelp.getPlaylistDict(playlist)
      playlistInfo = [playlistID, playlistDict["name"], str(len(playlistDict["tracks"]["items"]))]
      print(f"Playlist info: {playlistInfo}")
      #add items HERE to their respective databases. genreid,trackid,ptjunction, and gajunction should be autoincrement so u should take that into consideration
      #--------------------------------
      #QUERY STATEMENT FOR PLAYLIST, PT JUNCTION
      #--------------------------------
      #this return statement wont be necessary if u r already adding the items to the database
      return[playlistInfo, trackArr, albumArr, artistArr, genreArr, gajunction, ptjunction]

    @staticmethod
    def addTrackToDatabase(trackID, apihelp):
        if uniqueTrack(trackID):
            trackdict = apihelp.getTrackDict(trackID)
            tempt = getTrackInfo(trackdict)
            insertAttributes(trackdict["id"], apihelp)
            albumID = trackdict["album"]["id"]
            if uniqueAlbum(albumID):
              tempalb = getAlbumInfo(trackdict)
              artistID = trackdict["artist"][0]["id"]
              if uniqueArtist(artistID):
                tempartistdict = apihelp.getArtistDict(trackdict["artists"][0]["id"])
                tempart = getArtistInfo(trackdict, tempartistdict)
                for g in tempartistdict['genres']:
                  if uniqueGenre(g):
                    #query statement for inserting genre g
                    #genreArr.append(g)
                  #querystatement for inserting gajunction [tempdict["artists"][0]["id"], getGenreID(g, genreArr)]
                  #gajunction.append([tempdict["artists"][0]["id"], getGenreID(g, genreArr)])
                #query statement to insert tempart
                #artistArr.append(tempart)
              #querystatement to insert tempalb
              #albumArr.append(tempalb)
            #querystatement to insert trackid

            #EXECUTE ALL THE ABOVE QUERY STATEMENTS
        else:
            pass

    @staticmethod
    def addAlbumToDatabase(albumID, apihelp):
        albumDict = apihelp.getAlbumDict(albumID)
        for track in albumDict['items']:
            addTrackToDatabase(track)

    @staticmethod
    def insertAttributes(trackID, apihelp):
        attrList = apihelp.getAudioAttributes(trackID)
        #QUERY TO INSERT ATTR LIST

    @staticmethod
    def updatePlaylist(playlistID, apihelp):
        hardDeletePlaylist(playlistID, apihelp)
        addPlaylistToDatabase(playlistID, apihelp)


    @staticmethod
    def hardDeletePlaylist(playlistID, apihelp):
        #query to remove all values from ptjunction where playlistID = playlistID
        #query to remove playlist from the playlist function where playlistID = playlistID
        pass

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
    def getGenreID(genre):
      dbop = db_operations()
      cursor = dbop.getCursor()
      query = f'''Select genreID from genre
                WHERE genreName = \'{genre}\'
                LIMIT 1;'''
      cursor.execute(query)
      ID = cursor.fetchone()
      return ID

    #given the track dictionary, it will determine whether or not it is a unique album
    #this one can be written better
    #needs to be integrated into database
    #when we integrate into the database we will remove the second arguement
    @staticmethod
    def uniqueAlbum(albumID):
      dbop = db_operations()
      cursor = dbop.getCursor()
      query = f'''Select Count(*) from album
                WHERE albumID = \'{albumID}\';'''
      cursor.execute(query)
      count = cursor.fetchone()
      if count[0] == 0:
          return True
      else:
          return False


    #given the track dictionary, it will determine whether or not it is a unique artist
    #this one can be written better
    #needs to be integrated into database
    #when we integrate into the database we will remove the second arguement
    @staticmethod
    def uniqueArtist(artistID):
      dbop = db_operations()
      cursor = dbop.getCursor()
      query = f'''Select Count(*) from artist
                WHERE artist = \'{artistID}\';'''
      cursor.execute(query)
      count = cursor.fetchone()
      if count[0] == 0:
          return True
      else:
          return False

    #given the genre name, it will determine whether or not it is a unique genre
    #needs to be integrated into database
    #when we integrate into the database we will remove the second arguement
    @staticmethod
    def uniqueGenre(genre):
      dbop = db_operations()
      cursor = dbop.getCursor()
      query = f'''Select Count(*) from genre
                WHERE genreName = \'{genre}\';'''
      cursor.execute(query)
      count = cursor.fetchone()
      if count[0] == 0:
          return True
      else:
          return False

    #given the spotify trackID, it will determine whether or not it is a unique track
    #needs to be integrated into database
    #when we integrate into the database we will remove the second arguement
    @staticmethod
    def uniqueTrack(trackID):
      dbop = db_operations()
      cursor = dbop.getCursor()
      query = f'''Select Count(*) from track
                WHERE trackID = \'{trackID}\';'''
      cursor.execute(query)
      count = cursor.fetchone()
      if count[0] == 0:
          return True
      else:
          return False


    #given the spotify playlistID, it will determine whether or not it is a unique playlist
    #needs to be integrated into database
    @staticmethod
    def uniquePlaylist(playlist):
      dbop = db_operations()
      cursor = dbop.getCursor()
      query = f'''Select Count(*) from playlist
                WHERE playlistID = \'{playlist}\';'''
      cursor.execute(query)
      count = cursor.fetchone()
      if count[0] == 0:
          return True
      else:
          return False
    #WE NEED TO REWRITE THE FOLLOWING IN TERMS OF OUR DATABASE:
    #addPlaylistToDatabase(MOVED TO modifyRecord)
    #getTrackID
    #getGenreID
    #uniqueAlbum
    #uniqueArtist
    #uniqueGenre
    #uniqueTrack
    #uniquePlaylist
    #hardDeletePlaylist
