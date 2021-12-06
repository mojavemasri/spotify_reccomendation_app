from apihelper import apihelper
from helper import helper
class enterRecord():
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
