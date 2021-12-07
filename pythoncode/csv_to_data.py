#take all the data from the file as specified and turn it into a 2D array with each row a record
#then convert everything into the 4 table values then insert

#however what we really want is tuples but well get to that in a second
import csv
import mysql.connector
import random
from db_operations import db_operations
from apihelper import apihelper
from modifyRecord import modifyRecord
def convertDate(date):
    if len(date) == 4:
        return (date+"-01-01")
    else:
        if len(date) > 5:
            if date[4] == "-":
                return date + "-01"
        if int(date[-2:-1]+date[-1]) < 22:
            datetemp = "20"
        else:
            datetemp = "19"
        datetemp = datetemp + date[-2:-1]+date[-1]
        date = date[0:-3]
        if date.index('/') == 1:
            datetemp = datetemp + "-0"+date[0]
            date = date[2:-1] + date[-1]
        elif date.index('/') == 2:
            datetemp = datetemp + "-"+date[0:2]
            date = date[3:-1] + date[-1]
        if len(date) == 1:
            datetemp = datetemp + "-0"+ date
        else:
            datetemp = datetemp + "-" + date
        return datetemp


def array2d(filename):
    rs = []
    f = open(filename,"r")
    records = f.readlines()
    for i in range(len(records)):
        if i != 0:
            inst = records[i].split(',')
            inst.append(i)
            id = ord(inst[6][0])
            inst.append(id)
            rs.append(inst)
    return rs

#lst is list of indices that will be used for that particular tuple
#data is the array in question
def toTuples(lst, data):
    table = []
    for i in range(len(data)):
        temp = []
        for j in range(len(lst)):
            x = data[i]
            d = lst[j]
            temp.append(x[d])
        table.append(tuple(temp))
    table = clean(table)
    return table

#if a list has duplicate entries it will be removed here
def clean(data):
    cleaned = []
    for i in data:
        unique = True
        for j in cleaned:
            if i == j:
                unique = False
        if unique:
            cleaned.append(i)
    return cleaned


def genreartistalbumtrackinput():
    dbop = db_operations()
    cursor = dbop.getCursor()
    connection = dbop.getConnection()
    dupList = []
    counter = 0
    genreList = []
    with open('../csvs/genres.csv', 'r') as fr:
        reader = csv.reader(fr)
        firstRow = True
        for row in reader:

            if firstRow:
                firstRow = False
            else:
                insertGenre = row[1][1:-1] + row[1][-1]
                if "\'" in insertGenre:
                    insertGenre = insertGenre.replace("\'", "\\\'")
                    print(insertGenre)

                query = f'''INSERT INTO genre(genreName) Value (\'{insertGenre}\')'''

                #print(query)
                try:
                    cursor.execute(query)
                    genreList.append([row[0], insertGenre])
                except mysql.connector.Error as e:
                    if e.errno == 1062:
                        for r in genreList:
                            if r[1] == insertGenre:
                                dupList.append([counter, r[0]])
                        print(f"DUPLICATE ENTRY: {insertGenre}")
            counter += 1

    #UNCOMMENT TO COMMIT DATABASES
    #connection.commit()
    #query = '''SELECT Count(*) FROM genre'''
    #print(dupList)
    #cursor.execute(query)
    counter = 0
    fr.close()
    with open('../csvs/artists.csv', 'r') as fr:
        reader = csv.reader(fr)
        firstRow = True
        for row in reader:
            if firstRow:
                firstRow = False
            else:
                insertArtist = row
                #insertArtists = row[1][1:-1] + row[1][-1]
                if "\'" in insertArtist[1]:
                    insertArtist[1] = insertArtist[1].replace("\'", "\\\'")
                    print(f"\,{insertArtist}")
                query = f'''INSERT INTO artist(artistID, artistName, artistPopularity)
                Value (\'{insertArtist[0]}\', \'{insertArtist[1]}\', {insertArtist[2]});'''


                #print(query)
                try:
                    cursor.execute(query)
                except mysql.connector.Error as e:
                    if e.errno == 1062:
                       print(f"DUPLICATE ENTRY: {insertArtist}")
                    else:
                       print(insertArtist[1])
                       print(f"{e.msg}")
            counter += 1
    #UNCOMMENT TO COMMIT DATABASES
    #connection.commit()
    #query = '''SELECT Count(*) FROM genre'''
    #print(dupList)
    #cursor.execute(query)

    counter = 0
    fr.close()
    with open('../csvs/albums.csv', 'r') as fr:
        reader = csv.reader(fr)
        firstRow = True
        for row in reader:
            if firstRow:
                firstRow = False
            else:
                insertAlbum = row
                #insertArtists = row[1][1:-1] + row[1][-1]
                if "\'" in insertAlbum[2]:
                    insertAlbum[2] = insertAlbum[2].replace("\'", "\\\'")
                    #print(f"\,{insertAlbum}")

                #print(f"COMPARING {insertAlbum[-1]},{convertDate(insertAlbum[-1])}")
                insertAlbum[-1] = convertDate(insertAlbum[-1])
                query = f'''INSERT INTO album(albumID, artistID, albumName, numTracks, albumType, releaseDate)
                Value (\'{insertAlbum[0]}\', \'{insertAlbum[1]}\', \'{insertAlbum[2]}\', {insertAlbum[3]}, \'{insertAlbum[4]}\', \'{insertAlbum[5]}\');'''
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
            counter += 1
    #UNCOMMENT TO COMMIT DATABASES
    #connection.commit()

    fr.close()
    with open('../csvs/tracks.csv', 'r') as fr:
        reader = csv.reader(fr)
        firstRow = True
        for row in reader:
            if firstRow:
                firstRow = False
            else:
                insertTrack = row
                #insertArtists = row[1][1:-1] + row[1][-1]
                if "\'" in insertTrack[4]:
                    insertTrack[4] = insertTrack[4].replace("\'", "\\\'")
                    print(f"\,{insertTrack}")
                query = f'''INSERT INTO track(trackID , albumID, artistID, trackName, trackLength, trackPopularity, explicit)
                Value (\'{insertTrack[1]}\', \'{insertTrack[2]}\', \'{insertTrack[3]}\', \'{insertTrack[4]}\', {insertTrack[5]}, {insertTrack[6]}, {insertTrack[7]});'''


                #print(query)
                try:
                    cursor.execute(query)
                except mysql.connector.Error as e:
                    if e.errno == 1062:
                       print(f"DUPLICATE ENTRY: {insertTrack}")
                    else:
                       print(insertTrack[1])
                       print(f"{e.msg}")
            counter += 1
    query = '''SELECT Count(*) FROM track'''
    cursor.execute(query)
    print(cursor.fetchone())

    #UNCOMMENT TO COMMIT DATABASES
    #connection.commit()
    counter = 0
    fr.close()

def playlistInput():
    dbop = db_operations()
    cursor = dbop.getCursor()
    connection = dbop.getConnection()
    counter = 0
    with open('../csvs/playlists.csv', 'r') as fr:
        reader = csv.reader(fr)
        firstRow = True
        for row in reader:
            if firstRow:
                firstRow = False
            else:
                insertPlaylist = row
                #insertArtists = row[1][1:-1] + row[1][-1]
                if "\'" in insertPlaylist[1]:
                    insertPlaylist[1] = insertPlaylist[1].replace("\'", "\\\'")
                    print(f"\,{insertPlaylist}")
                query = f'''INSERT INTO playlist(playlistID , playlistName, numTracks)
                Value (\'{insertPlaylist[0]}\', \'{insertPlaylist[1]}\', {insertPlaylist[2]});'''


                print(query)
                try:
                    cursor.execute(query)
                except mysql.connector.Error as e:
                    if e.errno == 1062:
                       print(f"DUPLICATE ENTRY: {insertPlaylist}")
                    else:
                       print(insertPlaylist[1])
                       print(f"{e.msg}")
            counter += 1
    connection.commit()
    query = '''SELECT Count(*) FROM track'''
    cursor.execute(query)
    print(cursor.fetchone())
    #NEED TO GET NEW AUTH TOKEN BEFORE DOING THIS STEP
    playlistArr = []
    apihelp = apihelper('BQBy6wJH8UCY5pIapCVunXyZvHhifhbNYgjS2oQ4AufHonEPJwooiM4CKQns3uErrhGk6AeDsbFLy9Mk73rP91BvSexalux9Aj3rct19W8TkuUFEvO6fJ-z1wddW7BMjh7CD5PgeOCUnUGqh9CkAcSvI0EzU-xhCMWGcAXfUrC4')
    with open('../csvs/playlistTrackJunction.csv', 'r') as fr:
        reader = csv.reader(fr)
        firstRow = True
        for row in reader:
            if firstRow:
                firstRow = False
            else:
                insertpt = row
                inList = False
                for p in playlistArr:
                    #print(f"\'{p}\' = \'{row[1].strip()}\'")
                    if p == row[1].strip():
                        inList = True
                        break
                if not inList:
                    playlistTrackList = apihelp.returnPlaylistTracks(row[1].strip())
                    countPlaylist = 0
                    #insertArtists = row[1][1:-1] + row[1][-1]
                    for tDict in playlistTrackList:
                        tID = tDict["id"]
                        query = f'''INSERT INTO ptjunction(playlistID , trackID, trackPlace)
                        Value (\'{row[1].strip()}\', \'{tID}\', {countPlaylist});'''
                        countPlaylist += 1
                        print(query)
                        try:
                            cursor.execute(query)
                        except mysql.connector.Error as e:
                            if e.errno == 1062:
                               print(f"DUPLICATE ENTRY: {insertpt}")
                            else:
                               print(f"{e.msg}")
                    playlistArr.append(row[1].strip())

            counter += 1
    connection.commit()
    query = '''SELECT * FROM ptjunction'''
    cursor.execute(query)
    line = cursor.fetchone()
    while line:
        print(line)
        line = cursor.fetchone()
    #UNCOMMENT TO COMMIT DATABASES
    #connection.commit()
    counter = 0
    fr.close()

def gaInput():
    dbop = db_operations()
    loopdbop = db_operations()
    executeDB = db_operations()
    executecursor = executeDB.getCursor()
    executeconnection = executeDB.getConnection()
    cursor = dbop.getCursor()
    connection = dbop.getConnection()
    apihelp =  apihelper('BQCJ2e14X1Ecgb46elZaPEXiYRPGAETidpXHZd2ZKYqXt4cJFwHQZetI1SU5_nkwx0yVJsiBUtNmeL6zIzq_oSaWzW5AL-E6cxT0EUiAIJw9RqzQkYARNudx1rCu-c3JVctm6BQpzK0Jr_UBoMo7CSMkhyPzFgqsOhWvEG2UFZE')
    query = '''SELECT artistID FROM artist'''
    cursor.execute(query)
    line = cursor.fetchone()
    queryList = []
    counter = 0
    while line:
        if counter%10 == 0:
            print(f"i = {counter}")
        counter += 1
        artistID = line[0]
        artistDict = apihelp.getArtistDict(line[0])
        for g in artistDict["genres"]:
            genreName = g
            if "\'" in genreName:
                genreName = genreName.replace("\'", "\\\'")
                print(genreName)
            genreID = modifyRecord.getGenreID(genreName, loopdbop)
            query = f'''Insert INTO gajunction(genreID, artistID, gaUNIQUEID)
            VALUES ({genreID}, \'{artistID}\', \'{genreID}{artistID}\');'''
            if counter%10 == 0:
                print(query)
            try:
                executecursor.execute(query)
                executeconnection.commit()
            except mysql.connector.Error as e:
                if e.errno == 1062:
                   print(f"DUPLICATE ENTRY: {artistID}")
                else:
                   print("INVALID")
                   print(f"{e.msg}")
        line = cursor.fetchone()
        #print(line)

def featureInput():
    dbop = db_operations()
    cursor = dbop.getCursor()
    connection = dbop.getConnection()
    counter = 0
    with open('../csvs/audioFeatureListNew.csv', 'r') as fr:
        reader = csv.reader(fr)
        firstRow = True
        for row in reader:
            if firstRow:
                firstRow = False
            else:
                insertAttrs = row
                #insertArtists = row[1][1:-1] + row[1][-1]
                if "\'" in insertAttrs[1]:
                    insertAttrs[1] = insertAttrs[1].replace("\'", "\\\'")
                    #print(f"\,{insertAttrs}")
                query = f'''INSERT INTO track_ATTRIBUTES(trackID, danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, valence)
                VALUES (\'{insertAttrs[0]}\', \'{insertAttrs[1]}\',\'{insertAttrs[2]}\',\'{insertAttrs[3]}\',\'{insertAttrs[4]}\',\'{insertAttrs[5]}\',\'{insertAttrs[6]}\',\'{insertAttrs[7]}\',\'{insertAttrs[8]}\');'''


                print(query)
                try:
                    cursor.execute(query)
                except mysql.connector.Error as e:
                    if e.errno == 1062:
                       print(f"DUPLICATE ENTRY: {insertAttrs}")
                    else:
                       print(insertAttrs[1])
                       print(f"{e.msg}")
            counter += 1
    connection.commit()
    query = '''SELECT Count(*) FROM track'''
    cursor.execute(query)
    print(cursor.fetchone())
    fr.close()

featureInput()
