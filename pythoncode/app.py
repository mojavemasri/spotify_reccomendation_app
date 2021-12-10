from helper import helper
from apihelper import apihelper
from printRecord import printRecord
from modifyRecord import modifyRecord
from db_operations import db_operations
from reccomendation import reccomendation
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
clientID = '78a5356a63c04168858c0e650e53c66b'
clientSecret = 'b7a600370d754ac1a62a10e5e54a29cb'

def startscreen():
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("===============================")
    print("WELCOME TO SPOTIFY RECCOMENDATIONS")
    print("")

def textRequestTokenOld():
    print("To begin, input a spotify authentication token. You can do so at: ")
    print("https://developer.spotify.com/console/get-playlists/")
    token = ""
    while True:
        token = input("Input token: ")
        if apihelper.testToken(token):
            print("Valid token.")
            return token
        else:
            print("Try again. ")
    return ""

def textRequestToken():
    tokenRequester = SpotifyClientCredentials(client_id = clientID, client_secret = clientSecret)
    token = tokenRequester.get_access_token(as_dict = False, check_cache = True)
    print(token)
    return token

def viewlibrary():
    dbop = db_operations()
    cursor = dbop.getCursor()
    connection = dbop.getConnection()
    print('''What would you like to view:
            1) Tracks
            2) Albums
            3) Genres
            4) Playlists
            5) Return to main menu
    ''')
    typechoice = helper.get_choice([1,2,3,4,5])
    if typechoice == 1:
        print('''
        Would you like to:
        1)Enter the Spotify url to display your track
        2)Enter the trackID on the track you want to display
        3)Enter the name of the track and search for it''')
        searchChoice = helper.get_choice([1,2,3])
        if searchChoice == 1:
            trackID = helper.getURLFromUser(1)
            modifyRecord.addTrackToDatabase(trackID, apihelp)
            printRecord.printFancyTrack(trackID)
        if searchChoice == 2:
            trackID = helper.getURIFromUser()
            modifyRecord.addTrackToDatabase(trackID, apihelp)
            printRecord.printFancyTrack(trackID)
        elif searchChoice == 3:
            searchName = input("Enter name:")

            queryResult = helper.searchDB(searchName, 1) #search DB needs to be implemented
            if len(queryResult) == 0:
                print("Sorry, no tracks of this record were found. Please try again.")
            else:
                print(f"SEARCH RESULTS FOR \'{searchName}\'")
                print("====================================")
                print("trackID , trackName")
                for q in queryResult:
                    printRecord.printSimpleTrack(q)


    elif typechoice == 2:
        print('''
        Would you like to:
        1)Enter the album Spotify url to display your album
        2)Enter the name of the album and search for it
        3) Return to main menu''')
        searchChoice = helper.get_choice([1,2,3])
        if searchChoice == 1:
            albumID = helper.getURLFromUser(2)
            modifyRecord.addAlbumToDatabase(albumID, apihelp)
            printRecord.printFancyAlbum(albumID)
        elif searchChoice == 2:
            searchName = input("Enter name:")

            queryResult = helper.searchDB(searchName, 2) #search DB needs to be implemented
            print("SEARCH RESULTS: ")
            for q in queryResult:
                printRecord.printSimpleAlbum(q)
            if len(queryResult) == 0:
                print("Sorry, no albums with this name were found. Please try again.")
    elif typechoice == 3:
        searchName = input("Enter a name of a genre to search for it here")
        print("SEARCH RESULTS: ")
        dbop = db_operations()
        cursor = dbop.getCursor()
        connection = dbop.getConnection()
        query = f'''
                    SELECT g.genreID, g.genreName, COUNT(ga.artistID) FROM gajunction ga
                    INNER JOIN genre g ON g.genreID = ga.genreID
                    WHERE g.genreName LIKE \'%{searchName}%\'
                    GROUP BY g.genreID
                    ORDER BY COUNT(ga.artistID) DESC
                    LIMIT 60;
                '''
        cursor.execute(query)
        queryResult = cursor.fetchall()
        print("genreID, Name, number of artists within genre")
        for q in queryResult:
            print(f"{q[0]}, {q[1]} ({q[2]})")
        print('''
        Would you like to:
        1) Get the artists that make music of a specific genre(search by ID)
        2) Return to main menu''')
        genreChoice= helper.get_choice([1,2])
        if genreChoice == 1:
            genreID = input("Enter genre ID: ")
            printRecord.printFancyGenre(genreID)
    elif typechoice == 4:
        print('''
        Would you like to:
        1)Enter the Spotify url to display your playlist
        2)Enter the ID of the playlist you want to display
        3)Enter the name of the playlist and search for it
        4)Print all playlists
        5)Return to main menu''')
        searchChoice = helper.get_choice([1,2,3,4,5])
        if searchChoice == 1:
            playlistID = helper.getURLFromUser(4)
            modifyRecord.addPlaylistToDatabase(playlistID, apihelp)
            printRecord.printFancyPlaylist(playlistID)
        elif searchChoice == 2:
            playlistID = helper.getURIFromUser(4)
            modifyRecord.addPlaylistToDatabase(playlistID, apihelp)
            printRecord.printFancyPlaylist(playlistID)
        elif searchChoice == 3:
            searchName = input("Enter name:")

            queryResult = helper.searchDB(searchName, 5) #search DB needs to be implemented
            print("SEARCH RESULTS: ")
            for q in queryResult:
                printRecord.printSimpleArtist(q[0])
            if len(queryResult) == 0:
                print("Sorry, no playlist with this name were found. Please try again.")
        elif searchChoice == 4:
            query = '''SELECT playlistID, playlistName FROM playlist'''
            cursor.execute(query)
            queryResults = cursor.fetchall()
            for playlist in queryResults:
                print(f"{playlist[0]}, {playlist[1]}")

    print("Redirecting back to main menu, keep track of any useful information")
    input("Press any key to continue")
    pass

def editlibrary(apihelp):
    print('''
    Would you like to:
    1)Insert a record
    2)Update a record
    3)Delete a record
    4) Return to main menu
    ''')
    typechoice = helper.get_choice([1,2,3])
    if typechoice == 1:
        print('''
        Would you like to:
        1)Enter a track
        2)Enter an album
        3)Enter a playlist
        4) Return to main menu
        ''')
        mediumchoice = helper.get_choice([1,2,3])
        if mediumchoice == 1:
            trackID = helper.getURLFromUser(1)
            modifyRecord.addTrackToDatabase(trackID, apihelp)
        elif mediumchoice == 2:
            albumID = helper.getURLFromUser(2)
            modifyRecord.addAlbumToDatabase(albumID, apihelp)
        elif mediumchoice == 3:
            while True:
                playlistID = helper.getURLFromUser(4)
                modifyRecord.addPlaylistToDatabase(playlistID, apihelp)
                print('''
                Would you like to:
                1)Enter another playlist
                2) Return to main menu
                ''')
                contchoice = helper.get_choice([1,2])
                if contchoice == 2:
                    break
    elif typechoice == 2:
        print('''
        Would you like to:
        1)Update a playlist's name
        2)Update a playlist's content
        3) Return to main menu
        ''')
        updateChoice = helper.get_choice([1,2,3])
        if updateChoice == 1:
            playlistID = helper.getURLFromUser(4)
            #QUERY TO CHANGE PLAYLIST NAME GIVEN ID
        elif updateChoice == 2:
            playlistID = helper.getURLFromUser(4)
            modifyRecord.updatePlaylist(playlistID, apihelp)
    elif typechoice == 3:
        print('''
        Delete is only supported for playlists
        ''')
        print('''
        Would you like to:
        1)Enter the url of the playlist you would like to delete
        2) Return to main menu
        ''')
        updateChoice = helper.get_choice([1,2])
        playlistID = helper.getURLFromUser(4)
        modifyRecord.hardDeletePlaylist(playlistID)

def getreccomendations(apihelp):
    dbop = db_operations()
    cursor = dbop.getCursor()
    print('''Menu Options:
            1) Enter the playlist URL you would like to get reccomendations for
            2) Return to main menu
        ''')
    menu1choice = helper.get_choice([1,2])
    if menu1choice == 1:
        playlistID = helper.getURLFromUser(4)
        print(f"RESULTING ID: {playlistID}")
        modifyRecord.addPlaylistToDatabase(playlistID, apihelp)
        query = f'''
            Select trackID FROM ptjunction
            WHERE playlistID = \'{playlistID}\';
        '''
        cursor.execute(query)
        playlistInput = cursor.fetchall()
        for i in range(len(playlistInput)):
            playlistInput[i] = playlistInput[i][0]
        print('''What is the maximum popularity you would like for the playlist reccs(1-100)
                For reference:
                popularity of HEY YA! by OUTKAST: 81
                popularity of MARIPOSA by RADIANT CHILD: 49
                popularty of OCEANIC FEEL by MOLLY LEWIS: 11
            ''')
        maxpopularity = 101
        while maxpopularity > 100 or maxpopularity < 1:
            maxpopularityinput = input("Enter choice:")
            if maxpopularityinput.isnumeric():
                maxpopularity = round(float(maxpopularityinput))
                if maxpopularity > 100 or maxpopularity < 1:
                    print("Invalid choice, must be between 1-100")
            else:
                print("input a numerical value")
        print(f"Setting maxpopularity as {maxpopularity}...")
        print('''What is the minimum popularity you would like for the playlist reccs(1-100)
                For reference:
                popularity of HEY YA! by OUTKAST: 81
                popularity of MARIPOSA by RADIANT CHILD: 49
                popularty of OCEANIC FEEL by MOLLY LEWIS: 11
            ''')
        minpopularity = 101
        while minpopularity > maxpopularity or minpopularity < 1:
            minpopularityinput = input("Enter choice:")
            if minpopularityinput.isnumeric():
                minpopularity = round(float(minpopularityinput))
                if minpopularity > maxpopularity or maxpopularity < 1:
                    print(f"Invalid input, must be between 1-{maxpopularity}")
            else:
                print("Invalid input, input a numerical value")
        print(f"Setting minpopularity as {minpopularity}...")
        minpopularity = 0
        print('''What is the maximum artist popularity you would like for the playlist reccs(1-100)
                For reference:
                popularity of OUTKAST: 76
                popularity of HIATUS KAIYOTE: 60
                popularty of JAI PAUL: 50
            ''')
        maxartistpopularity = 101
        while maxartistpopularity > 100 or maxartistpopularity < 1:
            maxartistpopularityinput = input("Enter choice:")
            if maxartistpopularityinput.isnumeric():
                maxartistpopularity = round(float(maxartistpopularityinput))
                if maxartistpopularity > 100 or maxartistpopularity < 1:
                    print("Invalid choice, must be between 1-100")
            else:
                print("input a numerical value")
        print(f"Setting maxartistpopularity as {maxartistpopularity}...")
        print('''What is the minimum artist popularity you would like for the playlist reccs(1-100)
                For reference:
                popularity of OUTKAST: 76
                popularity of HIATUS KAIYOTE: 60
                popularty of JAI PAUL: 50
            ''')
        minartistpopularity = 101
        while minartistpopularity > maxartistpopularity or minartistpopularity < 1:
            minartistpopularityinput = input("Enter choice:")
            if minartistpopularityinput.isnumeric():
                minartistpopularity = round(float(minartistpopularityinput))
                if minartistpopularity > maxartistpopularity or maxartistpopularity < 1:
                    print(f"Invalid input, must be between 1-{maxartistpopularity}")
            else:
                print("Invalid input, input a numerical value")
        print(f"Setting minartistpopularity as {minartistpopularity}...")
        print(f'''Would you like a:
                1)Morning shower(danceable and joyous)
                2)Evening Drive playlist(chill and somber)
                3)Night club(high energy)
                4)Picnic music(ethereal and subdued)''')
        vibechoice = helper.get_choice([1,2,3,4])
        reccomendationObj =  reccomendation(playlistInput, maxpopularity, minpopularity, maxartistpopularity, \
        minartistpopularity, vibechoice)
        reccomendedPlaylist = reccomendationObj.runGA()

def menuoptions():
    print('''Menu Options:
            1) View library
            2) Edit library
            3) Get reccomendations
            4) Export CSV
            5) Exit
        ''')
    return helper.get_choice([1,2,3,4,5])

def exportToCSV():
    dbop =  db_operations()
    cursor = dbop.getCursor()
    connection = dbop.getConnection()
    constraint = ";"
    beginning = "SELECT * FROM "
    print('''What would you like to export:
            1) Tracks
            2) Albums
            3) Artists
            4) Genres
            5) Playlists
            6) Return to main menu
    ''')
    typechoice = helper.get_choice([1,2,3,4,5,6])
    while True:
        fname = input("ENTER FILE NAME in .csv form (ex. track.csv)")
        if '.csv' in fname:
            break
        else:
            print("INVALID FILE NAME. PLEASE TRY AGAIN")
    if typechoice == 1:
        tableName = 'track'
        header = ['trackID', 'albumID', 'artistID', 'trackName', 'trackLength', 'trackPopularity', 'explicit']
        print('''Would you like to:
            1) export ALL tracks
            2) export tracks of a specific album(enter albumID)
            3) export a specific artist(enter artistID)
            4) export tracks of a specific genre(enter genreID)
        ''')
        constraintchoice = helper.get_choice([1,2,3,4])
        if constraintchoice == 2:
            albumID = helper.getURIFromUser()
            constraint = f'''WHERE albumID = \'{albumID}\';'''
        elif constraintchoice == 3:
            artistID = helper.getURIFromUser()
            constraint = f'''WHERE artistID = \'{artistID}\';'''
        elif constraintchoice == 4:
            genreID = input("Input genreID: ")
            constraint = f'''WHERE artistID in (
            SELECT artistID FROM gajunction ga INNER JOIN genre g
            on g.genreID = ga.genreID
            WHERE g.genreID = \'{genreID}\';'''
    elif typechoice == 2:
        tableName = 'album'
        header = ['albumID', 'artistID', 'albumName', 'numTracks', 'albumType', 'releaseDate']
    elif typechoice == 3:
        tableName = 'artist'
        header = ['artistID', 'artistName', 'artistPopularity']
    elif typechoice == 4:
        tableName = 'genre'
        header = ['genreID', 'genreName']
    elif typechoice == 5:
        print('''Would you like to:
            1) export ALL playlists
            2) export tracks from a playlist(enter playlistID)
        ''')
        playlistChoice = helper.get_choice([1,2,3,4])
        if playlistChoice == 1:
            tableName = 'playlist'
            header = ['playlistID', 'playlistName', 'numTracks']
        elif playlistChoice == 2:
            tableName = '(ptjunction pt INNER JOIN track on pt.trackID = track.trackID) INNER JOIN playlist p on p.playlistID = pt.playlistID '
            playlistID = helper.getURIFromUser()
            beginning = 'SELECT track.trackID, track.albumID, track.artistID, track.trackName, track.trackLength, p.playlistID, p.playlistName FROM '
            constraint = f'''WHERE pt.playlistID = {playlistID}'''
    query = f'''{beginning} {tableName} {constraint}'''
    cursor.execute(query)
    csvData = cursor.fetchall()
    for i in range(len(csvData)):
        newRow = []
        for ent in csvData[i]:
            newRow.append(ent)
        csvData[i] = newRow

    with open(f"../exportcsvs/{fname}", 'w') as fw:
        csvwriter= csv.writer(fw)
        csvwriter.writerow(header)
        for row in csvData:
            csvwriter.writerow(row)
    print("Successfully exported records. ")
def exitmessage():
    print("Goodbye! Happy Listening!")

startscreen()
authToken = textRequestToken()
apihelp = apihelper(authToken)
while True:
    choice = menuoptions()
    if choice == 1:
        viewlibrary()
    elif choice == 2:
        editlibrary(apihelp)
    elif choice == 3:
        getreccomendations(apihelp)
    elif choice == 4:
        exportToCSV()
    elif choice == 5:
        exitmessage()
        break
