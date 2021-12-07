from apihelper import apihelper
from helper import helper
from db_operations import db_operations

class modifyRecord():
    #given a playlist id or url, it will figure out what is new in the list(new track, new artist, etc)
    #and it will add each new record to a list
    #we still need to add this to a database
    @staticmethod
    def addPlaylistToDatabase(playlist, apihelp):
      dbop = db_operations()
      cursor = dbop.getCursor()
      connection = dbop.getConnection()
      if playlist[0:10] == 'https://op':
        playlistID = playlist[34:56]
      else:
        playlistID = playlist
      if uniquePlaylist(playlist):
          playlistArr = apihelp.returnPlaylistTracks(playlistID)
          playlistDict = apihelp.getPlaylistDict(playlistID)
          playlistInfo = getPlaylistInfo(playlistDict)
          if "\'" in playlistInfo[1]:
              insertPlaylist[1] = insertPlaylist[1].replace("\'", "\\\'")
              print(f"\,{insertPlaylist}")
          query = f'''INSERT INTO playlist(playlistID , playlistName, numTracks)
          Value (\'{playlistInfo[0]}\', \'{playlistInfo[1]}\', {playlistInfo[2]});'''
          print(query)
          try:
              cursor.execute(query)
          except mysql.connector.Error as e:
              if e.errno == 1062:
                 print(f"DUPLICATE ENTRY: {insertPlaylist}")
              else:
                 print(insertPlaylist[1])
                 print(f"{e.msg}")
          print(playlistArr)
          counter = 0
          countPlaylist =0

          for tempdict in playlistArr:
            t = tempdict['id']
            if tempdict["is_local"]:
              continue
            #print(t)
            if uniqueTrack(t):
                addTrackToDatabase(t, apihelp)
            query = f'''INSERT INTO ptjunction(playlistID , trackID, trackPlace)
            Value (\'{playlistID}\', \'{t}\', {countPlaylist});'''
            countPlaylist += 1
            print(query)
            try:
                cursor.execute(query)
            except mysql.connector.Error as e:
                if e.errno == 1062:
                   print(f"DUPLICATE ENTRY: {insertpt}")
                else:
                   print(f"{e.msg}")
            counter += 1
          #add items HERE to their respective databases. genreid,trackid,ptjunction, and gajunction should be autoincrement so u should take that into consideration
          #--------------------------------
          #QUERY STATEMENT FOR PLAYLIST, PT JUNCTION
          #--------------------------------
          #this return statement wont be necessary if u r already adding the items to the database
          #return[playlistInfo, trackArr, albumArr, artistArr, genreArr, gajunction, ptjunction]
          pass

    @staticmethod
    def addTrackToDatabase(trackID, apihelp):
        if uniqueTrack(trackID):
            dbop = db_operations()
            cursor = dbop.getCursor()
            connection = dbop.getConnection()
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

                    if "\'" in g:
                        g = g.replace("\'", "\\\'")
                        print(g)
                    if uniqueGenre(g):
                        query = f'''INSERT INTO genre(genreName) Value (\'{g}\')'''
                        #print(query)
                        try:
                            cursor.execute(query)
                        except mysql.connector.Error as e:
                            if e.errno == 1062:
                                for r in genreList:
                                    if r[1] == g:
                                        dupList.append([counter, r[0]])
                                print(f"DUPLICATE ENTRY: {g}")
                    genreID = getGenreID(g)
                    query = f'''Insert INTO gajunction(genreID, artistID, gaUNIQUEID)
                    VALUES ({genreID}, \'{artistID}\', \'{genreID}{artistID}\');'''
                  #querystatement for inserting gajunction [tempdict["artists"][0]["id"], getGenreID(g, genreArr)]
                  #gajunction.append([tempdict["artists"][0]["id"], getGenreID(g, genreArr)])
                if "\'" in tempArt[1]:
                    tempArt[1] = tempArt[1].replace("\'", "\\\'")
                    print(f"\,{tempArt}")
                query = f'''INSERT INTO artist(artistID, artistName, artistPopularity)
                Value (\'{tempArt[0]}\', \'{tempArt[1]}\', {tempArt[2]});'''
                #print(query)
                try:
                    cursor.execute(query)
                except mysql.connector.Error as e:
                    if e.errno == 1062:
                       print(f"DUPLICATE ENTRY: {insertArtist}")
                    else:
                       print(insertArtist[1])
                       print(f"{e.msg}")
              #insertArtists = row[1][1:-1] + row[1][-1]
              if "\'" in tempalb[2]:
                  tempalb[2] = tempalb[2].replace("\'", "\\\'")
                  #print(f"\,{insertAlbum}")

              #print(f"COMPARING {insertAlbum[-1]},{convertDate(insertAlbum[-1])}")
              tempalb[-1] = helper.convertDate(tempalb[-1])
              query = f'''INSERT INTO album(albumID, artistID, albumName, numTracks, albumType, releaseDate)
              Value (\'{tempalb[0]}\', \'{tempalb[1]}\', \'{tempalb[2]}\', {tempalb[3]}, \'{tempalb[4]}\', \'{tempalb[5]}\');'''
              #print(query)
              try:
                  cursor.execute(query)
              except mysql.connector.Error as e:
                  if e.errno == 1062:
                     continue
                     #print(f"DUPLICATE ENTRY: {insertAlbum}")
                  else:
                     #print(insertAlbum)
                     #print(insertAlbum[-1])
                     print(f"{e.msg}")
            #querystatement to insert trackid

            #insertArtists = row[1][1:-1] + row[1][-1]
            if "\'" in tempt[4]:
                tempt[4] = tempt[4].replace("\'", "\\\'")
                print(f"\,{tempt}")
            query = f'''INSERT INTO track(trackID , albumID, artistID, trackName, trackLength, trackPopularity, explicit)
            Value (\'{tempt[1]}\', \'{tempt[2]}\', \'{tempt[3]}\', \'{tempt[4]}\', {tempt[5]}, {tempt[6]}, {tempt[7]});'''


            #print(query)
            try:
                cursor.execute(query)
            except mysql.connector.Error as e:
                if e.errno == 1062:
                   print(f"DUPLICATE ENTRY: {insertTrack}")
                else:
                   print(insertTrack[1])
                   print(f"{e.msg}")
            connection.commit()
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


#NEEDS TO BE IMPLEMENTED
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

    @staticmethod
    def getPlaylistInfo(playlistDict):
       p = []
       p.append(playlistDict["id"])
       p.append(playlistDict["name"])
       p.append(len(playlistDict["tracks"]["items"]))
       return p
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
      return ID[0]



    @staticmethod
    def getGenreID(genre,dbop):
      cursor = dbop.getCursor()
      query = f'''Select genreID from genre
                WHERE genreName = \'{genre}\'
                LIMIT 1;'''
      cursor.execute(query)
      ID = cursor.fetchone()
      return ID[0]

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
