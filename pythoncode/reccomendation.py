
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
        #QUERY THAT RETURNS SONG ATTRIBUTES ARTIST POPULARITY, and NUM ITEMS RETURNED
        #LIMIT AT 1000
        return initsamplePoolList, initsamplePool, sampleSize

    def genPop(popSize, numItems, playlistItemsIndex,sampleSize):
      population = []
      for _ in range(popSize):
        temp = []
        for i in range(numItems):
          tempInt = random.randint(0,sampleSize-1)
          for k in playlistItemsIndex:
            if tempInt == k:
              tempInt = random.randint(0,sampleSize-1)
          temp.append(tempInt)
        population.append(temp)
      return population

    def roulette_selection(population, numParents):
      popSize = len(population)
      if popSize < numParents:
        return population
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

    def simpleMutation(sol, mut, playlistItemsIndex, sampleSize):
      for i in range(len(sol)):
        if random.random() < mut:
          sol[0][i] = simpleMutateVal(playlistItemsIndex, sampleSize)

        if random.random() < mut:
          sol[1][i] = simpleMutateVal(playlistItemsIndex,sampleSize)
      return sol

    def simpleMutateVal(playlistItemsIndex, sampleSize):
      validMut = False
      while not validMut:
        tempInt = random.randint(0,sampleSize-1)
        validMut = True
        for k in playlistItemsIndex:
          if tempInt == k:
            validMut = False
            break
      return tempInt

    def generateChildren(numParents, population, mut, numChildren, playlistItemsIndex, sampleSize):
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
        mutsol= simpleMutation(sol,mut, playlistItemsIndex, sampleSize)
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



    def tournament_survival(population, numSurvive, playlist, playlistIndices, weight, sampleSize, playlistVars):
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

    def avgVal(solIndices):
      avgList = [0,0,0,0,0,0,0,0,0,0,0,0]
      sol = []
      for s in solIndices:
        #print(s)
        #print(songList[s])
        #print(masterRef[songList[s]])
        #print(f"len master ref: {len(masterRef[songList[s]])}")
        sol.append(masterRef[songList[s]])
      for i in range(len(sol)):
        avgList[0] += sol[i]['danceability']
        avgList[1] += sol[i]['energy']
        avgList[2] += (sol[i]['key'])
        avgList[3] += sol[i]['loudness']
        avgList[4] += sol[i]['mode']
        avgList[5] += sol[i]['speechiness']
        avgList[6] += sol[i]['acousticness']
        avgList[7] += sol[i]['instrumentalness']
        avgList[8] += sol[i]['liveness']
        avgList[9] += sol[i]['valence']
        avgList[10] += sol[i]['tempo']
        avgList[11] += sol[i]['duration_ms']
      for i in range(len(avgList)):
        avgList[i] /= len(sol)
      #print(f"len avg list: {len(avgList)}")
      return avgList

    def calcVal(sol, playlistAvg, weight, playlistVars):
      avgTestSol = avgVal(sol)
      avgVar = findVar(sol, avgTestSol)
      diffList = compareVectors(playlistAvg, avgTestSol, weight)
      varList = compareVectors(avgVar, playlistVars, [1,1,1,1,1,1,1,1,1,1,1,1])
      return(calcDistance(diffList)+calcDistance(avgVar))

    def compareVectors(s1, s2, weight):
      diffList = []
      if not len(s1) == len(s2):
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


    def findVar(playlistIndexes, avgVals):
      varList = [0,0,0,0,0,0,0,0,0,0,0,0]
      sol = []
      for t in playlistIndexes:
        sol.append(masterRef[songList[t]])
      for i in range(len(sol)):
        varList[0] += (sol[i]['danceability'] - avgVals[0])**2
        varList[1] += (sol[i]['energy']- avgVals[1])**2
        varList[2] += ((sol[i]['key'])- avgVals[2])**2
        varList[3] += ((sol[i]['loudness']- avgVals[3])**2)
        varList[4] += (sol[i]['mode']- avgVals[4])**2
        varList[5] += (sol[i]['speechiness']- avgVals[5])**2
        varList[6] += (sol[i]['acousticness']- avgVals[6])**2
        varList[7] += (sol[i]['instrumentalness']- avgVals[7])**2
        varList[8] += (sol[i]['liveness']- avgVals[8])**2
        varList[9] += (sol[i]['valence']- avgVals[9])**2
        varList[10] += (sol[i]['tempo']- avgVals[10])**2
        varList[11] += (sol[i]['duration_ms']- avgVals[11])**2
      for j in range(len(varList)):
        varList[j] /= (len(sol)- 1)
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



    def prettyPrint(sol):
      import requests

      headers = {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': f'Bearer {AuthToken}',
      }

      params = (
          ('market', 'US'),
      )
      counter = 1
      for song in sol:
        #findIndex(songList[song])
        response = requests.get(f'https://api.spotify.com/v1/tracks/{songList[song]}', headers=headers, params=params)

        respDict = response.json()
        print(f"Track {counter}: {respDict['artists'][0]['name']} - {respDict['name']}")
        counter+=1


    def runGA():
        print(songList)
        print("--------INITIAL PLAYLIST----------\n")
        prettyPrint(playlistIndexes)
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
        varPlaylist = findVar(playlistIndexes, avgVal(playlistIndexes))
        #['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence','tempo','duration_ms']
        WEIGHT = [0.5,0.5,0.075,0.075,0.05,0.175,0.7,0.5,0.6,1.2,0.1,0.00025]
        print(varPlaylist)
        for w in range(len(WEIGHT)):
          if varPlaylist[w] < 0.002:
            WEIGHT[w] *= 500
          else:
            WEIGHT[w] *= (varPlaylist[w] ** -1)
        WEIGHT = normalizeArr(WEIGHT)
        print(WEIGHT)

        pop = genPop(POP_SIZE, len(playlistInit), playlistInit, SAMPLE_SIZE)
        #print(pop)
        pop = roulette_selection(pop, NUM_PARENTS)
        updatepop = generateChildren(NUM_PARENTS, pop, MUT_RATE, NUM_CHILDREN, playlistIndexes, SAMPLE_SIZE)


        playlistAvg = avgVal(playlistIndexes)
        print(pop)
        pop = roulette_selection(pop, NUM_PARENTS)
        updatepop = generateChildren(NUM_PARENTS, pop, MUT_RATE, NUM_CHILDREN, playlistIndexes, SAMPLE_SIZE)
        pop = genPop(POP_SIZE, len(playlistInit), playlistInit, SAMPLE_SIZE)
        resetcounter = 0
        currConverg = FIRSTCONVERG

        while(bestVal < ACCURACY or resetcounter >= MAX_RESETS):
          #bestVal = 0
          #bestSol = []
          resetcounter += 1
          currBestVal = 0
          currBestSol = []
          for i in range(NUM_TRIALS):

            updatepop = tournament_survival(updatepop, BASE_POP, playlistInit, playlistIndexes, WEIGHT, SAMPLE_SIZE, varPlaylist)
            random.shuffle(updatepop)
            updatepop = generateChildren(NUM_PARENTS, updatepop, MUT_RATE, NUM_CHILDREN, playlistIndexes, SAMPLE_SIZE)
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
          pop = genPop((POP_SIZE*2), len(playlistInit), playlistInit, SAMPLE_SIZE)
          #print(pop)
          pop.append(bestSol)
          pop = roulette_selection(pop, (NUM_PARENTS*2))

          random.shuffle(pop)
          pop = generateChildren((NUM_PARENTS*2), pop, MUT_RATE, (NUM_CHILDREN*2), playlistIndexes, SAMPLE_SIZE)
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
