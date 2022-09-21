import math
import random

stra = ' 加了贪心优化'

def createRandomApproxAnswers(numOfPoint, howMany):
    randomAnswers = [[j for j in range(0, numOfPoint)] for _ in range(howMany)]
    for i in range(howMany):
        random.shuffle(randomAnswers[i])
    return randomAnswers


def createGreadyInitialAnswer(distanceMap):
    anAnswer = [0]
    anAnswerSet = {0}
    while len(anAnswer) != len(distanceMap[0]):
        minDis = math.inf
        minIdx = anAnswer[-1]
        for i in range(len(distanceMap[anAnswer[-1]])):
            if distanceMap[anAnswer[-1]][i] < minDis and i not in anAnswerSet:
                minDis = distanceMap[anAnswer[-1]][i]
                minIdx = i
        anAnswer.append(minIdx)
        anAnswerSet.add(minIdx)
    return anAnswer

def createGreadyInitialAnswers(distanceMap,howMany):
    gready = createGreadyInitialAnswer(distanceMap)
    return [gready for _ in range(howMany)]

def getCircleDistances(distanceMap, approxAnswerList):
    circleDistances = []
    n = len(approxAnswerList[0])
    for i in range(len(approxAnswerList)):
        sum = 0
        for j in range(n):
            if j == n - 1:
                sum += distanceMap[approxAnswerList[i][j]][approxAnswerList[i][0]]
            else:
                sum += distanceMap[approxAnswerList[i][j]][approxAnswerList[i][j + 1]]
        circleDistances.append(sum)
    return circleDistances


def selectAnswer(distanceMap, approxAnswerList, selectRate, possibilities):
    result = []
    answerLen = len(approxAnswerList[0])
    circleDistances = getCircleDistances(distanceMap, approxAnswerList)
    # sorted answers
    sortedDis = sorted(circleDistances)
    # for example: 50 ans,25pairs
    for i in range(len(approxAnswerList) // 2):
        temp = []
        # choose a pair of parents
        for j in range(2):
            # ############按概率取样
            rand = random.uniform(0, selectRate)
            for k in range(len(possibilities)):
                if k == 0:
                    if rand < possibilities[k]:
                        temp.append(approxAnswerList[circleDistances.index(sortedDis[k])].copy())
                        break
                else:
                    if rand >= possibilities[k - 1] and rand < possibilities[k]:
                        temp.append(approxAnswerList[circleDistances.index(sortedDis[k])].copy())
                        break
        # exchange information
        randStart = random.randint(0, answerLen - 2)
        randEnd = random.randint(randStart, answerLen - 1)
        pos1_recorder = {value: idx for idx, value in enumerate(temp[0])}
        pos2_recorder = {value: idx for idx, value in enumerate(temp[1])}

        for j in range(randStart, randEnd):
            val1, val2 = temp[0][j], temp[1][j]
            pos1, pos2 = pos1_recorder[val2], pos2_recorder[val1]
            temp[0][j], temp[0][pos1] = temp[0][pos1], temp[0][j]
            temp[1][j], temp[1][pos2] = temp[1][pos2], temp[1][j]
            pos1_recorder[val1], pos1_recorder[val2] = pos1, j
            pos2_recorder[val1], pos2_recorder[val2] = j, pos2

        result.append(temp[0])
        result.append(temp[1])
    return result


def getSelectPossibility(numOfAnswers):
    possibilities = []
    diff = 2 / numOfAnswers / numOfAnswers
    for i in range(numOfAnswers // 2 - 1, -1, -1):
        possibilities.append(1 / numOfAnswers + diff * i)
    for i in range(0, numOfAnswers // 2):
        possibilities.append(1 / numOfAnswers - diff * i)
    for i in range(1, numOfAnswers):
        possibilities[i] += possibilities[i - 1]
    return possibilities


def mutate(middleAnswers, poss):
    answerLen = len(middleAnswers[0])
    for i in range(len(middleAnswers)):
        if random.random() < poss:
            # random.shuffle(middleAnswers[i])
            index1 = random.randint(0, answerLen - 2)
            index2 = random.randint(index1, answerLen - 1)
            # middleAnswers[i][index1], middleAnswers[i][index2] = middleAnswers[i][index2], middleAnswers[i][index1]
            mutateSeg = middleAnswers[i][index1:index2]
            mutateSeg.reverse()
            middleAnswers[i] = middleAnswers[i][:index1] + mutateSeg + middleAnswers[i][index2:]
    return middleAnswers


def getDistance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)


def buildDistanceMap(pointSet):
    n = len(pointSet)
    distanceMap = [[0 for _1 in range(n)] for _2 in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            distanceMap[i][j] = distanceMap[j][i] = getDistance(pointSet[i], pointSet[j])
    return distanceMap


if __name__ == '__main__':
    for _ in range(1):
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
        distanceMap = buildDistanceMap(pointSet)
        gready = createGreadyInitialAnswer(distanceMap)
        print(createGreadyInitialAnswers(distanceMap,100))
