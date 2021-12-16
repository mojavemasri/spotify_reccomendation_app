import random
import math
from apihelper import apihelper
from db_operations import db_operations
from modifyRecord import modifyRecord
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
    minartistpopularity, vibechoice, apihelp):
        self.playlist = playlist
        self.samplePoolList, self.samplePool, self.sampleSize = reccomendation.initializeSamplePool(maxpopularity, minpopularity, maxartistpopularity, minartistpopularity, vibechoice, playlist, apihelp)
        print(f"sampleSize: {self.sampleSize}")
    @staticmethod
    def initializeSamplePool(maxpopularity, minpopularity, maxartistpopularity,minartistpopularity, vibechoice, playlist,apihelp):
        dbop = db_operations()
        cursor = dbop.getCursor()
        if vibechoice == 1:
            query = f'''SELECT tA.trackID, tA.danceability, tA.energy, tA.speechiness, tA.acousticness, tA.instrumentalness, tA.liveness, tA.valence, a.artistPopularity
                        FROM (track_ATTRIBUTES tA
                       INNER JOIN track t ON tA.trackID = t.trackID) INNER JOIN artist a ON t.artistID = a.artistID
                       WHERE t.trackPopularity <= {maxpopularity} AND t.trackPopularity >= {minpopularity}
                       AND a.artistPopularity <= {maxartistpopularity} AND a.artistPopularity >= {minartistpopularity}
                       AND tA.danceability >= 0.55 AND tA.valence >= 0.5
                       LIMIT 1000;
                    '''
        elif vibechoice == 2:
            query = f'''SELECT tA.trackID, tA.danceability, tA.energy, tA.speechiness, tA.acousticness, tA.instrumentalness, tA.liveness, tA.valence, a.artistPopularity
                        FROM (track_ATTRIBUTES tA
                       INNER JOIN track t ON tA.trackID = t.trackID) INNER JOIN artist a ON t.artistID = a.artistID
                       WHERE t.trackPopularity <= {maxpopularity} AND t.trackPopularity >= {minpopularity}
                       AND a.artistPopularity <= {maxartistpopularity} AND a.artistPopularity >= {minartistpopularity}
                       AND tA.energy <= 0.55 AND tA.valence <= 0.5
                       LIMIT 1000;
                    '''
        elif vibechoice == 3:
            query = f'''SELECT tA.trackID, tA.danceability, tA.energy, tA.speechiness, tA.acousticness, tA.instrumentalness, tA.liveness, tA.valence, a.artistPopularity
                        FROM (track_ATTRIBUTES tA
                       INNER JOIN track t ON tA.trackID = t.trackID) INNER JOIN artist a ON t.artistID = a.artistID
                       WHERE t.trackPopularity <= {maxpopularity} AND t.trackPopularity >= {minpopularity}
                       AND a.artistPopularity <= {maxartistpopularity} AND a.artistPopularity >= {minartistpopularity}
                       AND tA.energy >= 0.72 AND tA.danceability >= 0.55
                       LIMIT 1000;
                    '''
        elif vibechoice == 4:
            query = f'''SELECT tA.trackID, tA.danceability, tA.energy, tA.speechiness, tA.acousticness, tA.instrumentalness, tA.liveness, tA.valence, a.artistPopularity
                        FROM (track_ATTRIBUTES tA
                       INNER JOIN track t ON tA.trackID = t.trackID) INNER JOIN artist a ON t.artistID = a.artistID
                       WHERE t.trackPopularity <= {maxpopularity} AND t.trackPopularity >= {minpopularity}
                       AND a.artistPopularity <= {maxartistpopularity} AND a.artistPopularity >= {minartistpopularity}
                       AND tA.energy <= 0.55 AND tA.valence >= 0.3
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
                    tempattributeList.append(float(a))
            tempattributeList[-1] = float(tempattributeList[-1])/100
            initsamplePool[tempID] = tempattributeList
        for p in playlist:
            if not p in initsamplePool.keys():
                query = f'''SELECT tA.trackID, tA.danceability, tA.energy, tA.speechiness, tA.acousticness, tA.instrumentalness, tA.liveness, tA.valence, a.artistPopularity
                            FROM (track_ATTRIBUTES tA
                           INNER JOIN track t ON tA.trackID = t.trackID) INNER JOIN artist a ON t.artistID = a.artistID
                           WHERE t.trackID = \'{p}\''''
                #print(p)

                cursor.execute(query)
                temptrackInfo = cursor.fetchall()
                #print(f"p = {p}")
                #print(temptrackInfo)
                if temptrackInfo == []:
                    #print("no attributes found")
                    modifyRecord.insertAttributes(p, apihelp)
                    cursor.execute(query)
                    temptrackInfo = cursor.fetchall()
                    #print(f"newTrackInfo: {temptrackInfo}")
                temptrackInfo = temptrackInfo[0]
                firstTrack = True
                initsamplePoolList.append(temptrackInfo[0])
                tempattributeList = []
                for t in temptrackInfo:
                    if firstTrack:
                        tempID = t
                        firstTrack = False
                        continue
                    else:
                        tempattributeList.append(float(t))
                tempattributeList[-1] = float(tempattributeList[-1])/100
                initsamplePool[tempID] = tempattributeList
        #QUERY THAT RETURNS track ATTRIBUTES ARTIST POPULARITY, and NUM ITEMS RETURNED
        #LIMIT AT 1000
        #NORMALIZE ARTIST POPULARITY BY /100
        return initsamplePoolList, initsamplePool, sampleSize


    #USED TO GENERATE INITIAL SOLUTIONS
    def genPop(self, popSize, numItems):
      population = []
      for _ in range(popSize):
        temp = []
        for _ in range(numItems):
          tempID = self.samplePoolList[random.randint(0,self.sampleSize-1)]
          for k in self.playlist:
            if tempID == k:
              tempID = self.samplePoolList[random.randint(0,self.sampleSize-1)]
          temp.append(tempID)
        population.append(temp)
      return population



    #SELECTS RANDOM SOLUTTIONS FROM POPULATION
    #FIXED
    def roulette_selection(self, population, numParents):
      parentSelect = []
      numParents = int(numParents)
      for _ in range (numParents):
        parentSelect.append(population.pop(random.randint(0,len(population)-1)))
      return parentSelect


    def simpleCrossover(self,p1,p2):

      c1 = []
      c2 = []
      plength = len(p1)
      #print(random.randint(0,1))
      if random.random() > 0.5:
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

    def simpleMutation(self,sol, mut, playlist):
      for i in range(len(sol)):
        if random.random() < mut:
          sol[0][i] = self.simpleMutateVal(playlist)

        if random.random() < mut:
          sol[1][i] = self.simpleMutateVal(playlist)
      return sol

    def simpleMutateVal(self,playlist):
      validMut = False
      while not validMut:
        tempVal = self.samplePoolList[random.randint(0,self.sampleSize-1)]
        validMut = True
        for k in playlist:
          if tempVal == k:
            validMut = False
            break
      return tempVal

    def generateChildren(self, numParents, population, mut, numChildren, playlist):
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
        sol = self.simpleCrossover(p1,p2)
        mutsol= self.simpleMutation(sol,mut, playlist)
        childPopulation.append(mutsol[0])
        childPopulation.append(mutsol[1])
      childPopulation = self.roulette_selection(childPopulation, numChildren)
      population = childPopulation + population

      return population


    def checkDupID(self, sol, playlist, sampleSize):
      for j in range(len(sol)):
        for p in range(len(sol)):
          if sol[j] == p:
            sol[j] = self.samplePoolList(random.randint(0, sampleSize-1))
      return sol



    def tournament_survival(self, population, numSurvive, playlistAvg, weight, sampleSize, playlistVars):
      newpop = []
      playlistAvg = self.avgVal(self.playlist)
      if len(population) < numSurvive:
        numSurvive = len(population)
      for i in range(numSurvive):
        ind1 = random.randint(0,len(population)-1)
        ind2 = random.randint(0,len(population)-1)
        newpop.append(self.winner(population[ind1], population[ind2], playlistAvg, weight, playlistVars))
      return newpop


    def winner(self, s1, s2, playlistAvg, weight, playlistVars):
      v1 = self.calcVal(s1, playlistAvg, weight, playlistVars)
      v2 = self.calcVal(s2, playlistAvg, weight, playlistVars)
      if v1 > v2:
        return s1
      else:
        return s2


    def avgVal(self, sol):
      avgList = [0,0,0,0,0,0,0,0]
      numtracks = len(sol)
      for s in sol:
          for i in range(len(self.samplePool[s])):
              #print(len(self.samplePool[s]))
              #print(len(avgList))
              avgList[i] += ((self.samplePool[s][i])/numtracks)
      return avgList

    def calcVal(self, sol, playlistAvg, weight, playlistVars):
      wavg = 0.5
      wvar = 0.25
      avgTestSol = self.avgVal(sol)
      avgVar = self.findVar(sol)
      diffList = reccomendation.compareVectors(playlistAvg, avgTestSol, weight)
      varList = reccomendation.compareVectors(avgVar, playlistVars, weight)#CAN BE REPLACED WITH WEIGHT
      return(((wavg*reccomendation.calcDistance(diffList))+(wvar*reccomendation.calcDistance(varList)))/(wavg+wvar))

    @staticmethod
    def compareVectors(s1, s2, weight):
      diffList = []
      if not len(s1) == len(s2):
        print(f"len(s1): {len(s1)}")
        print(f"len(s2): {len(s2)}")
        return -1
      if not len(s1) == len(weight):
        print(f"len(s1): {len(s1)}")
        print(f"len(weight): {len(weight)}")
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

    def findVar(self, sol):
      varList = [0,0,0,0,0,0,0,0]
      avgVals = self.avgVal(sol)
      numtracks = len(sol)
      for s in sol:
          for i in range(len(self.samplePool[s])):
              varList[i] += (((self.samplePool[s][i] - avgVals[i])**2)/(numtracks-1))
      return varList

    @staticmethod
    def calcDistance(diffList):
      sum = 0
      #print(diffList)
      for d in diffList:
        sum += (d**2)
      sum = sum**0.5
      return sum

    @staticmethod
    def normalizeArr(vector):
      distance = reccomendation.calcDistance(vector)
      for i in range(len(vector)):
        vector[i] /= distance
      return vector


    @staticmethod
    def prettyPrint(sol):
        dbop = db_operations()
        cursor = dbop.getCursor()
        counter = 1
        for track in sol:
            query = f'''SELECT t.trackName, a.artistName FROM
                    track t INNER JOIN artist a on t.artistID = a.artistID
                    WHERE t.trackID = \'{track}\';'''
            cursor.execute(query)
            result = cursor.fetchall()[0]
            print(f"Track {counter}: {result[1]} - {result[0]}")
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
    def runGA(self):
        #print(trackList)
        print("--------INITIAL PLAYLIST----------\n")
        reccomendation.prettyPrint(self.playlist)
        NUM_TRIALS = 300
        MUT_RATE = 0.1
        POP_SIZE = 1000
        NUM_PARENTS = 200
        NUM_CHILDREN = (NUM_PARENTS/2)
        BASE_POP = 1000
        MAX_CONVERG = 0.96
        MAX_VAL = 0.995
        FIRSTCONVERG = 1.2
        AFTERCONVERG = 1.04
        bestVal = 0
        bestSol = []
        MAX_RESETS = 5
        ACCURACY = -10000
        currBestSol = []
        varPlaylist = self.findVar(self.playlist)
        #['danceability', 'energy', 'speechiness', 'acousticness', 'liveness', 'valence','artistPopularity']
        WEIGHT = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
        #print(varPlaylist)
        for w in range(len(WEIGHT)):
          if varPlaylist[w] < 0.002:
            WEIGHT[w] *= 500
          else:
            WEIGHT[w] *= (varPlaylist[w] ** -1)
        WEIGHT = reccomendation.normalizeArr(WEIGHT)
        #print(WEIGHT)
        #print(pop)
        updatepop = self.genPop(BASE_POP, 10)
        updatepop = self.roulette_selection(updatepop, NUM_PARENTS)
        updatepop = self.generateChildren(NUM_PARENTS, updatepop, MUT_RATE, NUM_CHILDREN, self.playlist)
        playlistAvg = self.avgVal(self.playlist)
        #print(updatepop)
        resetcounter = 0
        currConverg = FIRSTCONVERG

        while(resetcounter <= MAX_RESETS):
          #bestVal = 0
          #bestSol = []
          resetcounter += 1
          currBestVal = 0
          currBestSol = []
          for i in range(NUM_TRIALS):
            updatepop = self.tournament_survival(updatepop, BASE_POP, playlistAvg, WEIGHT, self.sampleSize, varPlaylist)
            random.shuffle(updatepop)
            updatepop = self.generateChildren(NUM_PARENTS, updatepop, MUT_RATE, NUM_CHILDREN, self.playlist)
            if(i%10 == 0):
              print(f"i == {i}")
              convNum = 0
              for k in range(len(updatepop)):
                updatepop[k] = self.checkDupID(updatepop[k], self.playlist, self.sampleSize)
              for sol in updatepop:
                temp = self.calcVal(sol, playlistAvg, WEIGHT, varPlaylist)
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
              if (convNum/len(updatepop)) >= MAX_CONVERG:
                  print(f"RESETTING AT {i}")
                  break
              if convNum * 2 >= len(updatepop) and not currBestSol == bestSol:
                print("ADDING THE SPECIAL SAUCE 10x")
                for x in range(10):
                  updatepop.append(bestSol)
              elif convNum  >= len(updatepop):
                print(f"RESETTING AT {i}, convNum == {convNum}, len(updatepop) == {len(updatepop)}")
                currConverg = AFTERCONVERG
                break

            if i == NUM_TRIALS-1:
              print(f"Conv num: {convNum}")
          if bestVal >= MAX_VAL:
              break
          print("Adding new Pop, BEST SOLUTION: ")
          print(bestSol)
          reccomendation.prettyPrint(bestSol)
          pop = self.genPop((POP_SIZE*2), 10)
          #print(pop)
          pop.append(bestSol)
          pop = self.roulette_selection(pop, (NUM_PARENTS*2))

          random.shuffle(pop)
          pop = self.generateChildren((NUM_PARENTS*2), pop, MUT_RATE, (NUM_CHILDREN*2), self.playlist)
          print(len(updatepop))
          updatepop = pop
          print(len(updatepop))

        for sol in updatepop:
          temp = self.calcVal(sol, playlistAvg, WEIGHT, varPlaylist)
          #print(temp)
          if temp > bestVal:
            bestVal = temp
            print(f"BESTVAL: {temp}")
            print(sol)
            bestSol = sol

        print("-------SIMILAR PLAYLIST--------")
        reccomendation.prettyPrint(bestSol)
