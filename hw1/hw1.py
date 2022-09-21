# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
import ga
import os

if __name__ == '__main__':
    for _ in range(1):
        startCounter = time.time()
        with open('exmp6', 'r') as f:
            rawData = f.readlines()
        # f = open("C:\\Users\\bai\\Code\\Python\\hw1_561\\exmp3", 'r')
        dataSize = int(rawData[0])
        pointSet = []
        for i in range(1, dataSize + 1):
            x, y, z = rawData[i].split(' ')
            pointSet.append([int(x), int(y), int(z)])
        greatestAnswers = []
        # question_numbers_set = random.sample(range(0, 1000), 50)
        distanceMap = ga.buildDistanceMap(pointSet)
        popNum = 300
        generation = 3000
        mutatePoss = 0.1
        selectRate = 0.3
        possibilities = ga.getSelectPossibility(popNum)
        # middleAnswers = ga.createRandomApproxAnswers(len(pointSet), howMany=popNum)
        middleAnswers = ga.createGreadyInitialAnswers(distanceMap, popNum)
        for i in range(generation):
            middleAnswers = ga.selectAnswer(distanceMap, middleAnswers, selectRate, possibilities)
            middleAnswers = ga.mutate(middleAnswers, mutatePoss)
            circleDistances = ga.getCircleDistances(distanceMap, middleAnswers)
            greatestAnswers.append(middleAnswers[circleDistances.index(min(circleDistances))])
            print(str(i) + f'/{generation}')

        greatestCircleDistances = ga.getCircleDistances(distanceMap, greatestAnswers)
        greatestCircleDistances.sort()
        # posRecorder = {value: idx for idx, value in enumerate(greatestCircleDistances)}
        print(greatestCircleDistances)
        with open('output.txt', 'w') as f:
            for pointInd in greatestAnswers[0]:
                data = str(pointSet[pointInd])[1:-1].replace(',', '')
                f.write(data + '\n')
            data = str(pointSet[greatestAnswers[0][0]])[1:-1].replace(',', '')
            f.write(data + '\n')
        totalTime = time.time() - startCounter
        with open('recorderReverseMutate2.txt', 'a') as f:
            f.write(str(popNum) + ' ' + str(generation) + ' ' + str(mutatePoss) + ' ' + str(
                greatestCircleDistances[0]) + ' ' +str(selectRate)+' '+ str(totalTime) + ' ' + os.path.basename(__file__) + ga.stra + '\n')
