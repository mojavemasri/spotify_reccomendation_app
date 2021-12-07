import db_operations

class printRecord:

    def __init__(self):
        self.dbop = db_operations.db_operations()
        self.cursor = self.dbop.getCursor()
        self.connection = self.dbop.getConnection()

    def printSimpleTrack(self, trackID):
        query = f'''
                    SELECT * FROM track
                    WHERE spotifyTrackID = \'{trackID}\'
                '''
        self.cursor.execute(query)
        track = self.cursor.fetchone()
        print(track)
        return track


    def printSimpleAlbum(self, albumID):
        query = f'''
                    SELECT * FROM album
                    WHERE spotifyAlbumID = \'{albumID}\'
                '''
        self.cursor.execute(query)
        album = self.cursor.fetchone()
        print(album)
        return album


    def printSimpleArtist(self, artistID):
        query = f'''
                    SELECT * FROM artist
                    WHERE spotifyArtistID = \'{artistID}\'
                '''
        self.cursor.execute(query)
        artist = self.cursor.fetchone()
        print(artist)
        return artist


    def printSimpleGenre(self, genreID):
        query = f'''
                    SELECT * FROM genre
                    WHERE genreID = \'{genreID}\'
                '''
        self.cursor.execute(query)
        genre = self.cursor.fetchone()
        print(genre)
        return genre

    def printSimplePlaylist(self, playlistID):
        query = f'''
                    SELECT * FROM playlist
                    WHERE playlistID = \'{playlistID}\'
                '''
        self.cursor.execute(query)
        playlist = self.cursor.fetchone()
        print(playlist)
        return playlist



    def printFancyTrack(self, trackID):
        data = self.printSimpleTrack(trackID)
        print(f'''trackID:{data[0]}
spotifyTrackID:{data[1]}
albumID:{data[2]}
artistID:{data[3]}
trackName:{data[4]}
trackLength:{data[5]}
trackPopularity:{data[6]}
explicit:{data[7]}
               ''')

    def printFancyGenre(self,genreID):
        data = self.printSimpleGenre(genreID)
        print(f'''genreID:{data[0]}
genreName:{data[1]}
               ''')

    def printFancyArtist(self, artistID):
        data = self.printSimplePlaylist(artistID)
        print(f'''spotifyArtistID:{data[1]}
artistID:{data[0]}
artistPopularity:{data[2]}
               ''')


    def printFancyAlbum(self, albumID):
        data = self.printSimpleTrack(albumID)
        print(f'''spotifyAlbumID:{data[0]}
spotifyArtistID:{data[1]}
albumName:{data[2]}
numTracks:{data[3]}
albumType:{data[4]}
releaseDate:{data[5]}
               ''')

    def printFancyPlaylist(self, playlistID):
        data = self.printSimplePlaylist(playlistID)
        print(f'''playlistName:{data[1]}
playlistID:{data[0]}
numTracks:{data[2]}
               ''')
