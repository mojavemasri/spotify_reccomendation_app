from helper import helper
from apihelper import apihelper
from printRecord import printRecord
from modifyRecord import modifyRecord

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

def textRequestToken():
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

def viewlibrary():
    print('''What would you like to view:
            1) Tracks
            2) Albums
            3) Artists
            4) Genres
            5) Playlists
            6) Users(NOT IMPLEMENTED YET IT WONT LET YOU CHOOSE THIS)
            7) Return to main menu
    ''')
    typechoice = helper.get_choice([1,2,3,4,5,7])
    if typechoice == 1:
        print('''
        Would you like to:
        1)Enter the Spotify url to display your track
        2)Enter the name of the song and search for it''')
        searchChoice = helper.get_choice([1,2])
        if searchChoice == 1:
            trackID = helper.getURLFromUser(1)
            printRecord.printFancyTrack(trackID)
        if searchChoice == 2:
            searchName = input("Enter name:")

            queryResult = searchDB(searchName, 1) #search DB needs to be implemented

            for q in queryResult:
                printRecord.printSimpleTrack(q[0])
            if len(queryResult) == 0:
                print("Sorry, no songs of this record were found. Please try again.")

    elif typechoice == 2:
        print('''
        Would you like to:
        1)Enter the album Spotify url to display your album
        2)Enter an artist Spotify url and print all of their (database) albums
        3)Enter the name of the album and search for it
        4) Return to main menu''')
        searchChoice = helper.get_choice([1,2,3, 4])
        if searchChoice == 1:
            albumID = helper.getURLFromUser(2)
            printRecord.printFancyAlbum(albumID)
        elif searchChoice == 2:
            artistID = helper.getURLFromUser(3)
            #write query to get each album where this artist is the artist
            queryResult = []
            for q in queryResult:
                printRecord.printFancyAlbum(q[0])
        elif searchChoice == 3:
            searchName = input("Enter name:")

            queryResult = searchDB(searchName, 2) #search DB needs to be implemented
            print("SEARCH RESULTS: ")
            for q in queryResult:
                printRecord.printSimpleAlbum(q[0])
            if len(queryResult) == 0:
                print("Sorry, no albums witht this name were found. Please try again.")
    elif typechoice == 3:
        print('''
        Would you like to:
        1)Enter the Spotify url to display your artist
        2)Enter the name of the artist and search for it
        3) Return to main menu''')
        searchChoice = helper.get_choice([1,2, 3])
        if searchChoice == 1:
            artistID = helper.getURLFromUser(3)
            printRecord.printFancyArtist(artistID)
        if searchChoice == 2:
            searchName = input("Enter name:")

            queryResult = searchDB(searchName, 3) #search DB needs to be implemented
            print("SEARCH RESULTS: ")
            for q in queryResult:
                printRecord.printSimpleArtist(q[0])
            if len(queryResult) == 0:
                print("Sorry, no artists with this name were found. Please try again.")
    elif typechoice == 4:
        name = input("Enter a name of a genre to search for it here")
        #WRITE A QUERY THAT DISPLAYS SIMILAR NAMES
        queryResult = []
        print("SEARCH RESULTS: ")
        for q in queryResult:
            printRecord.printSimpleGenre(q[0])
    elif typechoice == 5:
        print('''
        Would you like to:
        1)Enter the Spotify url to display your playlist
        2)Enter the name of the playlist and search for it
        3) Return to main menu''')
        searchChoice = helper.get_choice([1,2])
        if searchChoice == 1:
            playlistID = helper.getURLFromUser(5)
            printRecord.printFancyPlaylist(playlistID)
        if searchChoice == 2:
            searchName = input("Enter name:")

            queryResult = searchDB(searchName, 5) #search DB needs to be implemented
            print("SEARCH RESULTS: ")
            for q in queryResult:
                printRecord.printSimpleArtist(q[0])
            if len(queryResult) == 0:
                print("Sorry, no playlist with this name were found. Please try again.")

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
        1)Enter a song
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
            playlistID = helper.getURLFromUser(4)
            modifyRecord.addPlaylistToDatabase(playlistID, apihelp)
    elif typechoice == 2:
        print('''
        Would you like to:
        1)Update a playlist's name
        2)Update a playlist's content
        3) Return to main menu
        ''')
        updateChoice = helper.get_choice([1,2,3])
        if updateChoice = 1:
            playlistID = helper.getURLFromUser(4)
            #QUERY TO CHANGE PLAYLIST NAME GIVEN ID
        elif updateChoice = 2:
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
        modifyRecord.updatePlaylist(playlistID, apihelp)

def getreccomendations():

def menuoptions():
    print('''Menu Options:
            1) View library
            2) Edit library
            4) Get reccomendations
            5) Input new Authentication Token
            6) Exit
        ''')
    return helper.get_choice([1,2,3,4,5,6])

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
    #elif choice == 3:
    #elif choice == 4:
    elif choice == 5:
        authToken = textRequestToken()
        apihelp = apihelper(authToken)
    elif choice == 6:
        exitmessage()
        break
