from helper import helper
from apihelper import apihelper
from printRecords import printRecords

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
    ''')
    typechoice = helper.get_choice([1,2,3,4,5])
    if typechoice == 1:
        print('''
        Would you like to:
        1)Enter the Spotify url to display your track
        2)Enter the name of the song and search for it''')
        searchChoice = helper.get_choice([1,2,3,4,5])
        if searchChoice == 1:

    elif typechoice == 2:
    elif typechoice == 3:
    elif typechoice == 4:
    elif typechoice == 5:

def editlibrary():

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
    #elif choice == 2:
    #elif choice == 3:
    #elif choice == 4:
    elif choice == 5:
        authToken = textRequestToken()
        apihelp = apihelper(authToken)
    elif choice == 6:
        exitmessage()
        break
