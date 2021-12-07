import random
from apihelper import apihelper
from db_operations import db_operations
class reccomendation():

#NEW ATTRIBUTES
#danceability
#energy
#speechiness
#acousticness
#instrumentalness
#liveness
#valence
#artistPopularity


    def __init__(self, playlist, maxpopularity, minpopularity, maxartistpopularity, \
    minartistpopularity, vibechoice):
        self.playlist = playlist
        self.samplePoolList, self.samplePool, self.sampleSize = initializeSamplePool(maxpopularity, minpopularity, maxartistpopularity, minartistpopularity, vibechoice)

    @staticmethod
    def initializeSamplePool(maxpopularity, minpopularity, maxartistpopularity,minartistpopularity, vibechoice):
        dbop = db_operations()
        cursor = dbop.getCursor()
        if vibechoice == 1:
            query = f'''SELECT tA.trackID, tA.danceability, tA.energy, tA.speechiness, tA.acousticness, tA.instrumentalness, tA.liveness, tA.valence, a.artistPopularity
                        FROM (track_ATTRIBUTES tA
                       INNER JOIN tracks t ON tA.trackID = t.trackID) INNER JOIN artist a ON t.artistID = artistID
                       WHERE t.trackPopularity <= {maxpopularity} AND t.trackPopularity >= {minpopularity}
                       AND a.aristPopularity <= {maxartistpopularity} AND a.artistPopularity >= {minartistpopularity}
                       AND tA.danceability >= 0.55 AND tA.valence >= 0.5
                       LIMIT 1000;
                    '''
        elif vibechoice == 2:
            query = f'''SELECT tA.trackID, tA.danceability, tA.energy, tA.speechiness, tA.acousticness, tA.instrumentalness, tA.liveness, tA.valence, a.artistPopularity
                        FROM (track_ATTRIBUTES tA
                       INNER JOIN tracks t ON tA.trackID = t.trackID) INNER JOIN artist a ON t.artistID = artistID
                       WHERE t.trackPopularity <= {maxpopularity} AND t.trackPopularity >= {minpopularity}
                       AND a.aristPopularity <= {maxartistpopularity} AND a.artistPopularity >= {minartistpopularity}
                       AND tA.energy <= 0.55 AND tA.valence <= 0.5
                       LIMIT 1000;
                    '''
        elif vibechoice == 3:
            query = f'''SELECT tA.trackID, tA.danceability, tA.energy, tA.speechiness, tA.acousticness, tA.instrumentalness, tA.liveness, tA.valence, a.artistPopularity
                        FROM (track_ATTRIBUTES tA
                       INNER JOIN tracks t ON tA.trackID = t.trackID) INNER JOIN artist a ON t.artistID = artistID
                       WHERE t.trackPopularity <= {maxpopularity} AND t.trackPopularity >= {minpopularity}
                       AND a.aristPopularity <= {maxartistpopularity} AND a.artistPopularity >= {minartistpopularity}
                       AND tA.energy >= 0.72
                       LIMIT 1000;
                    '''
        elif vibechoice == 4:
            query = f'''SELECT tA.trackID, tA.danceability, tA.energy, tA.speechiness, tA.acousticness, tA.instrumentalness, tA.liveness, tA.valence, a.artistPopularity
                        FROM (track_ATTRIBUTES tA
                       INNER JOIN tracks t ON tA.trackID = t.trackID) INNER JOIN artist a ON t.artistID = artistID
                       WHERE t.trackPopularity <= {maxpopularity} AND t.trackPopularity >= {minpopularity}
                       AND a.aristPopularity <= {maxartistpopularity} AND a.artistPopularity >= {minartistpopularity}
                       AND tA.energy <= 0.55 AND tA.valence >= 0.5
                       LIMIT 1000;
                    '''
        cursor.execute(query)
        masterRef = cursor.fetchall()
        sampleSize = len(masterRef)
        initsamplePoolList = []
        initsamplePool = {}
        for m in masterRef:
            initsamplePoolList.append(m[0])
            tempattributeList = []
            firstVal = True
            for a in m:
                if firstVal:
                    tempID = a
                    firstVal = False
                else:
                    tempattributeList.append(a)
            initsamplePool[tempID] = tempattributeList
        #QUERY THAT RETURNS track ATTRIBUTES ARTIST POPULARITY, and NUM ITEMS RETURNED
        #LIMIT AT 1000
        #NORMALIZE ARTIST POPULARITY BY /100
        return initsamplePoolList, initsamplePool, sampleSize


    #USED TO GENERATE INITIAL SOLUTIONS
    def genPop(popSize, numItems):
      population = []
      for _ in range(popSize):
        temp = []
        for _ in range(numItems):
          tempID = samplePoolList[random.randint(0,self.sampleSize-1)]
          for k in self.playlist:
            if tempID == k:
              tempID = samplePoolList[random.randint(0,self.sampleSize-1)]
          temp.append(tempID)
        population.append(temp)
      return population



    #SELECTS RANDOM SOLUTTIONS FROM POPULATION
    #FIXED
    def roulette_selection(population, numParents):
      parentSelect = []
      numParents = int(numParents)
      for _ in range (numParents):
        parentSelect.append(population.pop(random.randint(0,len(population)-1)))
      return parentSelect


    def simpleCrossover(p1,p2):

      c1 = []
      c2 = []
      plength = len(p1)
      #print(random.randint(0,1))
      if p1[0] > 0.5:
        index1 = random.randint(plength // 2,plength-1)
        index2 = random.randint(0, index1-1)
        for i in range(plength):
          if i < index1:
            c1.append(p1[i])
            c2.append(p2[i])
          elif i < index2:
            c1.append(p2[i])
            c2.append(p1[i])
          else:
            c1.append(p1[i])
            c2.append(p2[i])
      else:
        index = random.randint(0,plength-1)
        for i in range(plength):
          if i < index:
            c1.append(p1[i])
            c2.append(p2[i])
          else:
            c1.append(p2[i])
            c2.append(p1[i])

      return c1,c2

    def simpleMutation(sol, mut, playlist):
      for i in range(len(sol)):
        if random.random() < mut:
          sol[0][i] = simpleMutateVal(playlist)

        if random.random() < mut:
          sol[1][i] = simpleMutateVal(playlist)
      return sol

    def simpleMutateVal(playlist):
      validMut = False
      while not validMut:
        tempVal = self.samplePoolList[random.randint(0,self.sampleSize-1)]
        validMut = True
        for k in playlist:
          if tempVal == k:
            validMut = False
            break
      return tempVal

    def generateChildren(numParents, population, mut, numChildren, playlistItemsIndex):
      #print(f"Population length = {len(population)}")
      #print(f"numParents = {numParents}")

      parentList = population
      childPopulation = []
      iterRange = numParents -2
      if len(population) < numParents:
        iterRange = len(population) - 1
        #print(f"iterRange: {iterRange}")
      for i in range(iterRange):
        p1 = parentList[i]
        p2 = parentList[i+1]
        sol = simpleCrossover(p1,p2)
        mutsol= simpleMutation(sol,mut, playlistItemsIndex)
        childPopulation.append(mutsol[0])
        childPopulation.append(mutsol[1])
      childPopulation = roulette_selection(childPopulation, numChildren)
      population = childPopulation + population

      return population


    def checkDupID(sol, playlistIndexes, sampleSize):
      for j in range(len(sol)):
        for i in range(len(sol)):
          if sol[j] == playlistIndexes[i] or (sol[j] == sol[i] and not i == j):
            sol[j] = random.randint(0, sampleSize-1)
      return sol



    def tournament_survival(population, numSurvive, playlist, playlistAvg, weight, sampleSize, playlistVars):
      newpop = []
      playlistAvg = avgVal(playlistIndices)
      if len(population) < numSurvive:
        numSurvive = len(population)
      for i in range(numSurvive):
        ind1 = random.randint(0,len(population)-1)
        ind2 = random.randint(0,len(population)-1)
        newpop.append(winner(population[ind1], population[ind2], playlistAvg, weight, playlistVars))
      return newpop


    def winner(s1, s2, playlistAvg, weight, playlistVars):
      v1 = calcVal(s1, playlistAvg, weight, playlistVars)
      v2 = calcVal(s2, playlistAvg, weight, playlistVars)
      if v1 > v2:
        return s1
      else:
        return s2

    def avgVal(sol):
      avgList = [0,0,0,0,0,0,0]
      numtracks = len(sol)
      for s in sol:
          for i in range(len(samplePool[s])):
              avgList[i] += ((samplePool[s][i])/numtracks)
      return avgList

    def calcVal(sol, playlistAvg, weight, playlistVars):
      avgTestSol = avgVal(sol)
      avgVar = findVar(sol)
      diffList = compareVectors(playlistAvg, avgTestSol, weight)
      varList = compareVectors(avgVar, playlistVars, [0,0,0,0,0,0,0])#CAN BE REPLACED WITH WEIGHT
      return(calcDistance(diffList)+calcDistance(avgVar))

    def compareVectors(s1, s2, weight):
      diffList = []
      if not len(s1) == len(s2):
        return -1
      if not len(s1) == len(weight):
        return -1
      for i in range(len(s2)):
        #print(f"i = {i}")
        tempDiff = s1[i] - s2[i]
        if s2[i] != 0:
          tempDiff /= s2[i]
        tempDiff = math.exp(-1*(tempDiff**2))
        #print(weight[i])
        tempDiff *= weight[i]
        diffList.append(tempDiff)
      return diffList


    def findVar(sol):
      varList = [0,0,0,0,0,0,0]
      avgVals = avgVal(sol)
      numtracks = len(sol)
      for s in sol:
          for i in range(len(samplePool[s])):
              varList[i] += (((samplePool[s][i] - avgVal[i])**2)/(numtracks-1))
      return varList


    def calcDistance(diffList):
      sum = 0
      for d in diffList:
        sum += (d**2)
      sum = sum**0.5
      return sum


    def normalizeArr(vector):
      distance = calcDistance(vector)
      for i in range(len(vector)):
        vector[i] /= distance
      return vector


    @staticmethod
    def prettyPrint(sol):
        counter = 0
      for track in sol:
        #QUERY TO GET track NAME AND ARTIST NAME GIVEN track ID
        print(f"Track {counter}: {respDict['artists'][0]['name']} - {respDict['name']}")
        counter+=1

#NEW ATTRIBUTES
#danceability
#energy
#speechiness
#acousticness
#instrumentalness
#liveness
#valence
#artistPopularity
    def runGA():
        print(trackList)
        print("--------INITIAL PLAYLIST----------\n")
        prettyPrint(self.playlist)
        NUM_TRIALS = 500
        MUT_RATE = 0.1
        POP_SIZE = 2000
        NUM_PARENTS = 200
        NUM_CHILDREN = (NUM_PARENTS/2)
        BASE_POP = 1000
        FIRSTCONVERG = 1.2
        AFTERCONVERG = 1.04
        bestVal = 0
        bestSol = []
        MAX_RESETS = 100
        ACCURACY = 1.4
        currBestSol = []
        varPlaylist = findVar(self.playlist)
        #['danceability', 'energy', 'speechiness', 'acousticness', 'liveness', 'valence','artistPopularity']
        WEIGHT = [0.5,0.5,0.5,0.5,0.5,0.5,0.5]
        print(varPlaylist)
        for w in range(len(WEIGHT)):
          if varPlaylist[w] < 0.002:
            WEIGHT[w] *= 500
          else:
            WEIGHT[w] *= (varPlaylist[w] ** -1)
        WEIGHT = normalizeArr(WEIGHT)
        print(WEIGHT)
        #print(pop)
        updatepop = genPop(BASE_POP, 10)
        updatepop = roulette_selection(updatepop, NUM_PARENTS)
        updatepop = generateChildren(NUM_PARENTS, pop, MUT_RATE, NUM_CHILDREN, playlist)
        playlistAvg = avgVal(self.playlist)
        print(pop)
        resetcounter = 0
        currConverg = FIRSTCONVERG

        while(bestVal < ACCURACY or resetcounter >= MAX_RESETS):
          #bestVal = 0
          #bestSol = []
          resetcounter += 1
          currBestVal = 0
          currBestSol = []
          for i in range(NUM_TRIALS):
            updatepop = tournament_survival(updatepop, BASE_POP, playlistInit, playlistAvg, WEIGHT, SAMPLE_SIZE, varPlaylist)
            random.shuffle(updatepop)
            updatepop = generateChildren(NUM_PARENTS, updatepop, MUT_RATE, NUM_CHILDREN, playlist)
            if(i%10 == 0):
              print(f"i == {i}")
              convNum = 0
              for k in range(len(updatepop)):
                updatepop[k] = checkDupID(updatepop[k], playlistIndexes, SAMPLE_SIZE)
              for sol in updatepop:
                temp = calcVal(sol, playlistAvg, WEIGHT, varPlaylist)
                #print(temp)

                if temp > bestVal:
                  bestVal = temp
                  currBestVal = temp
                  print(f"BESTVAL: {temp}, i = {i}")
                  bestSol = sol
                  currBestSol = sol
                elif temp > currBestVal:
                  currBestVal = temp
                  currBestSol = sol
                  print(f"{temp}, i = {i}")
                elif temp == bestVal or temp == currBestVal:
                  convNum += 1
              print(f"convRate = {convNum/len(updatepop)}")
              if convNum * 2 >= len(updatepop) and not currBestSol == bestSol:
                print("ADDING THE SPECIAL SAUCE 10x")
                for x in range(10):
                  updatepop.append(bestSol)
              elif convNum * currConverg >= len(updatepop):
                print(f"RESETTING AT {i}, convNum == {convNum}, len(updatepop) == {len(updatepop)}")
                currConverg = AFTERCONVERG
                break

            if i == NUM_TRIALS-1:
              print(f"Conv num: {convNum}")

          print("Adding new Pop, BEST SOLUTION: ")
          print(bestSol)
          prettyPrint(bestSol)
          pop = genPop((POP_SIZE*2), 10, playlistInit)
          #print(pop)
          pop.append(bestSol)
          pop = roulette_selection(pop, (NUM_PARENTS*2))

          random.shuffle(pop)
          pop = generateChildren((NUM_PARENTS*2), pop, MUT_RATE, (NUM_CHILDREN*2), playlist)
          print(len(updatepop))
          updatepop = pop
          print(len(updatepop))

        for sol in updatepop:
          temp = calcVal(sol, playlistAvg, WEIGHT, varPlaylist)
          #print(temp)
          if temp > bestVal:
            bestVal = temp
            print(f"BESTVAL: {temp}")
            print(sol)
            bestSol = sol

        print("-------SIMILAR PLAYLIST--------")
        prettyPrint(bestSol)
