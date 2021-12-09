import db_operations

class printRecord:

    def __init__(self):
        self.dbop = db_operations.db_operations()
        self.cursor = self.dbop.getCursor()
        self.connection = self.dbop.getConnection()

    @staticmethod
    def printSimpleTrack( trackID):
        dbop = db_operations.db_operations()
        cursor = dbop.getCursor()
        connection = dbop.getConnection()
        query = f'''
                    SELECT trackID, trackName, a.artistName FROM track
                    INNER JOIN artist a ON track.artistID = a.artistID
                    WHERE trackID = \'{trackID}\';
                '''
        cursor.execute(query)
        track = cursor.fetchone()
        print(f"{track[0]}, {track[1]} by {track[2]}")
        return track

    @staticmethod
    def printSimpleAlbum(albumID):
        dbop = db_operations.db_operations()
        cursor = dbop.getCursor()
        connection = dbop.getConnection()
        query = f'''
                    SELECT albumID, albumName, art.artistName FROM album INNER JOIN artist art on album.artistID = art.artistID
                    WHERE albumID = \'{albumID}\'
                '''
        cursor.execute(query)
        album = cursor.fetchone()
        #print(album)
        print(f"{album[0]}, {album[1]} by {album[2]}")
        return album

    @staticmethod
    def printSimpleArtist(artistID):
        dbop = db_operations.db_operations()
        cursor = dbop.getCursor()
        connection = dbop.getConnection()
        query = f'''
                    SELECT artistID, artistName FROM artist
                    WHERE artistID = \'{artistID}\'
                '''
        cursor.execute(query)
        artist = cursor.fetchone()
        print(f"{artist[0]}, {artist[1]}")
        return artist

    @staticmethod
    def printSimpleGenre(genreID):
        dbop = db_operations.db_operations()
        cursor = dbop.getCursor()
        connection = dbop.getConnection()
        query = f'''
                    SELECT genreID, genreName FROM genre
                    WHERE genreID = \'{genreID}\'
                '''
        cursor.execute(query)
        genre = cursor.fetchone()
        print(f"{genre[0]}, {genre[1]}")
        return genre

    @staticmethod
    def printSimplePlaylist(self, playlistID):
        dbop = db_operations.db_operations()
        cursor = dbop.getCursor()
        connection = dbop.getConnection()
        query = f'''
                    SELECT playlistID, playlistName FROM playlist
                    WHERE playlistID = \'{playlistID}\'
                '''
        cursor.execute(query)
        playlist = cursor.fetchone()
        print(f"{playlist[0]}, {playlist[1]}")
        return playlist


    @staticmethod
    def printFancyTrack(trackID):
        dbop = db_operations.db_operations()
        cursor = dbop.getCursor()
        connection = dbop.getConnection()
        query = f'''
                    SELECT trackID, trackName, art.artistName, alb.albumName, alb.releaseDate FROM (track
                    INNER JOIN artist art ON track.artistID = art.artistID)
                    INNER JOIN album alb ON track.albumID = alb.albumID
                    WHERE trackID = \'{trackID}\';
                '''
        cursor.execute(query)
        track = cursor.fetchone()
        print("============SONG INFO================")
        print(f"trackID: {track[0]}")
        print(f"Name: {track[1]}")
        print(f"Artist: {track[2]}")
        print(f"Album: {track[3]}")
        print(f"Release Date: {track[4]}")

        query = f'''
            SELECT genreName FROM genre
            WHERE genreID IN (
            SELECT genreID FROM gajunction
            WHERE artistID IN (
            SELECT artistID FROM track
            WHERE trackID =  \'{trackID}\'
            )
            );'''
        cursor.execute(query)
        genres = cursor.fetchall()
        if len(genres) > 0:
            print("Artist Genres: ")
            for g in genres:
                print(g[0])
        return track

    @staticmethod
    def printFancyGenre(genreID):
        dbop = db_operations.db_operations()
        cursor = dbop.getCursor()
        connection = dbop.getConnection()
        query = f'''
                    SELECT genreID, genreName FROM genre
                    WHERE genreID = \'{genreID}\';
                '''
        cursor.execute(query)
        track = cursor.fetchone()
        print("===========GENRE INFO===========")
        print(f"genreID: {track[0]}")
        print(f"Name: {track[1]}")

        query = f'''
                    SELECT artistName FROM artist
                    WHERE artistID IN (
                    SELECT artistID FROM gajunction
                    WHERE genreID = \'{genreID}\')
                    LIMIT 60;
                '''
        cursor.execute(query)
        genreArtists = cursor.fetchall()
        print("Artists within this Genre:")
        for ga in genreArtists:
            print(ga[0])

    @staticmethod
    def printFancyAlbum(albumID):
        dbop = db_operations.db_operations()
        cursor = dbop.getCursor()
        connection = dbop.getConnection()
        query = f'''
                    SELECT albumID, albumName, art.artistName, alb.releaseDate FROM artist
                    INNER JOIN album alb ON artist.artistID = alb.artistID
                    WHERE albumID = \'{albumID}\';
                '''
        cursor.execute(query)
        album = cursor.fetchone()
        print("=======ALBUM INFO=========")
        print(f"albumID: {album[0]}")
        print(f"Name: {album[1]}")
        print(f"Artist Name: {album[2]}")
        print(f"Release Date: {album[3]}")

        print("Tracks: ")
        query = f'''
                    SELECT trackID FROM track
                    WHERE albumID = \'{albumID}\';
                '''
        cursor.execute(query)
        tracks = cursor.fetchall()
        for t in tracks:
            printRecord.printSimpleTrack(t[0])

    def printFancyPlaylist(self, playlistID):
        data = self.printSimplePlaylist(playlistID)
        print(f'''playlistName:{data[1]}
playlistID:{data[0]}
numTracks:{data[2]}
               ''')
