import requests
import json
class apihelper():
    def __init__(self, authToken):
        self.authToken = authToken
    #gets playlist dictionary from spotify api
    def getPlaylistDict(self, url):
      if url[0:10] == 'https://op':
        ID = url[url.index("playlist/")+9:url.index("?")]
      else:
        ID = url
      playlistIndexes = []
      playlistIDList = []
      trackArr = []
      headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {self.authToken}',
      }
      offsetNum = 0
      while True:
        params = (
          ('market', 'US'),
          ('limit', '20'),
          ('offset', f'{offsetNum}'),
        )
        response = requests.get(f'https://api.spotify.com/v1/playlists/{ID}', headers=headers, params=params)
        if str(response) == '<Response [200]>':
          break
        else:
          print(str(response))
          print("playlistDict")

      results = response.json()
      return results

    #returns a list of playlist track dictionaries from spotify api
    def returnPlaylistTracks(self, url):
      print(url)
      if url[0:10] == 'https://op':
        ID = url[34:56]
      else:
        ID = url
      print(ID)
      playlistIndexes = []
      playlistIDList = []
      trackArr = []
      headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {self.authToken}',
      }
      offsetNum = 0
      while True:
        params = (
          ('market', 'US'),
          ('limit', '20'),
          ('offset', f'{offsetNum}'),
        )
        while True:
          response = requests.get(f'https://api.spotify.com/v1/playlists/{ID}/tracks', headers=headers, params=params)
          if str(response) == '<Response [200]>':
           break
          else:
            print(str(response))
            print(f"ID: {ID}")
            print("playlistTracks")

        offsetNum += 20
        results = response.json()
        #print(f"results: {results}")

        print(results)
        if len(results['items']) == 0:
          break
        for track in results['items']:
          print(track["track"])
          trackArr.append(track["track"])
      return trackArr

    #given a user profile, it will add the first 50 user playlists to the database
    def extractUserPlaylists(self, url):
      ID = url[url.index('user/')+5:url.index('?')]

      headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {self.authToken}',
      }
      params = (
        ('limit', '50'),
        ('offset', '0'),
      )
      while True:
        response = requests.get(f'https://api.spotify.com/v1/users/{ID}/playlists', headers=headers, params=params)
        if str(response) == '<Response [200]>':
         break
        else:
          print(str(response))
          print(f"EXTRACT USER PLAYLIST {ID}")
      results = response.json()
      playlistArr = []
      somecounter = 0
      for playlist in results['items']:
        if uniquePlaylist(playlist['id']):
          p = addPlaylistToDatabase(playlist["id"])
      pass


    #given a spotify track id, this gets the track dictionary from spotify's api
    def getTrackDict(self, songID):
      headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {self.authToken}',
      }


      while True:
        response = requests.get(f'https://api.spotify.com/v1/tracks/{songID}', headers=headers)
        if str(response) == '<Response [200]>':
           break
        else:
          print(f"{str(response)}, {songID}")
      result = response.json()
      return result

    #given an artist id, this gets the artist dictionary from spotify's api
    def getArtistDict(self, artistID):
      headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {self.authToken}',
      }


      while True:
        response = requests.get(f'https://api.spotify.com/v1/artists/{artistID}', headers=headers)
        if str(response) == '<Response [200]>':
           break
        else:
          print(f"{str(response)}, {artistID}")
      result = response.json()
      return result

    #given a track id, get relevant track audio attributes
    def getAudioAttributes(self, trackID):
        import requests

        headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {self.authToken}',
    }

        response = requests.get(f'https://api.spotify.com/v1/audio-features/{trackID}', headers=headers)
        results =  response.json()
        attrList = []
        attrList.append(results["id"])
        attrList.append(results["danceability"])
        attrList.append(results["energy"])
        attrList.append(0)
        attrList.append(results["speechiness"])
        attrList.append(results["acousticness"])
        attrList.append(results["instrumentalness"])
        attrList.append(results["liveness"])
        attrList.append(results["valence"])
        return attrList

    #given an albumID, get the albumDictionary
    def getAlbumDict(self, albumID):
        import requests

        headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {self.authToken}',
        }

        response = requests.get(f'https://api.spotify.com/v1/albums/{albumID}/tracks', headers=headers)
        return(response.json())

    def getAuthToken(self):
        return self.authToken
    #given a test token, returns whether or not it is valid
    @staticmethod
    def testToken(token):
        headers = {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': f'Bearer {token}',
        }
        response = requests.get(f'https://api.spotify.com/v1/artists/2WoVwexZuODvclzULjPQtm', headers=headers)
        if str(response) == '<Response [200]>':
           return True
        elif str(response) == '<Response [401]>':
            return False
        else:
          print(f"{str(response)}")
          print("apihelper.testToken: Returning False")
          return False
