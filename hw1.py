# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
import random


def create_random_approx_answers(pointSet, howMany):
    randomAnswers = [[j for j in range(0, len(pointSet))] for _ in range(howMany)]
    for i in range(howMany):
        random.shuffle(randomAnswers[i])
    return randomAnswers


def getCircleDistances(pointSet, approxAnswerList):
    circleDistances = []
    n = len(approxAnswerList[0])
    for i in range(len(approxAnswerList)):
        sum = 0
        for j in range(n):
            if j == n - 1:
                sum += getDistance(pointSet[approxAnswerList[i][j]], pointSet[approxAnswerList[i][0]])
            else:
                sum += getDistance(pointSet[approxAnswerList[i][j]], pointSet[approxAnswerList[i][j + 1]])
        circleDistances.append(sum)
    return circleDistances


def selectAnswer(pointSet, approxAnswerList):
    result = []
    answerLen = len(approxAnswerList[0])
    circleDistances = getCircleDistances(pointSet, middle_answers)
    sortedDis = sorted(circleDistances)
    possibilities = getSelectPossibility(sortedDis)
    for i in range(1, len(possibilities)):
        possibilities[i] += possibilities[i - 1]
        # 比如说 50个解，25对
    for i in range(len(approxAnswerList) // 2):
        temp = []
        # 选一对，2个
        for j in range(2):
            # ############按概率取样
            rand = random.uniform(0, 1)
            for k in range(len(possibilities)):
                if k == 0:
                    if rand < possibilities[k]:
                        temp.append(approxAnswerList[circleDistances.index(sortedDis[k])].copy())
                        break
                else:
                    if rand >= possibilities[k - 1] and rand < possibilities[k]:
                        temp.append(approxAnswerList[circleDistances.index(sortedDis[k])].copy())
                        break
        # 交换信息
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

        # 添加到解集
        result.append(temp[0])
        result.append(temp[1])
    return result


def getSelectPossibility(sortedCircleDistances):
    n = len(sortedCircleDistances)
    possibilities = []
    diff = 2 / n / n
    for i in range(n // 2 - 1, -1, -1):
        possibilities.append(1 / n + diff * i)
    for i in range(0, n // 2):
        possibilities.append(1 / n - diff * i)
    return possibilities


def mutate(middleAnswers):
    answerLen = len(middleAnswers)
    for i in range(len(middleAnswers)):
        if random.random() < 0.2:
            random.shuffle(middleAnswers[i])
            index1 = random.randint(0, answerLen - 2)
            index2 = random.randint(index1, answerLen - 1)
            mutateSeg = middleAnswers[i][index1:index2]
            mutateSeg.reverse()
            middleAnswers[i] = middleAnswers[i][:index1] + mutateSeg + middleAnswers[i][index2:]
    return middleAnswers


def getDistance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)

    # Press the green button in the gutter to run the script.
    # C:\\Users\\bai\\Code\\Python\\hw1_561\\exmp1
    # C:\\Users\\bai\\Code\\Python\\hw1_561\\exmp2
    # C:\\Users\\bai\\Code\\Python\\hw1_561\\exmp3


# def toString(list):


if __name__ == '__main__':
    with open('exmp3', 'r') as f:
        rawData = f.readlines()
    # f = open("C:\\Users\\bai\\Code\\Python\\hw1_561\\exmp3", 'r')
    dataSize = int(rawData[0])
    pointSet = []
    for i in range(1, dataSize + 1):
        x, y, z = rawData[i].split(' ')
        x, y, z = int(x), int(y), int(z)
        pointSet.append([x, y, z])
    greatestAnswers = []
    # question_numbers_set = random.sample(range(0, 1000), 50)
    middle_answers = create_random_approx_answers(pointSet, howMany=50)
    # print(sorted(getCircleDistances(pointSet, middle_answers)))
    for i in range(100):
        middle_answers = selectAnswer(pointSet, middle_answers)
        # print(middle_answers)
        # print(sorted(getCircleDistances(pointSet, middle_answers)))
        middle_answers = mutate(middle_answers)
        circleDistance = getCircleDistances(pointSet, middle_answers)
        posRecorder = {value: idx for idx, value in enumerate(circleDistance)}
        circleDistance.sort()
        greatestAnswers.append(middle_answers[posRecorder[circleDistance[0]]])

    greatestCircleDistance = getCircleDistances(pointSet, greatestAnswers)
    posRecorder = {value: idx for idx, value in enumerate(greatestCircleDistance)}
    greatestCircleDistance.sort()
    with open('output.txt', 'w') as f:
        for pointInd in greatestAnswers[0]:
            data = str(pointSet[pointInd])[1:-1].replace(',', '')
            f.write(data + '\n')
        data = str(pointSet[greatestAnswers[0][0]])[1:-1].replace(',', '')
        f.write(data + '\n')
        # for pos in pointSet[pointInd]:
        #
        #     f.write(' '.join(pointSet[pointInd]))
        #     f.write(' '.join(pointSet[greatestAnswers[0][0]]))
