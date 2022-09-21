# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# 从50个数中挑选10个数，是他们的和最接近50个数总和的0.1倍
import random


def create_random_approx_answers(question_numbers_set, howMany):
    return [random.sample(question_numbers_set, 10) for _ in range(howMany)]


def get_error_levels(approx_answer_list, question_numbers_set):
    error_levels = []
    right_answer = sum(question_numbers_set) / 10
    for item in approx_answer_list:
        distance = abs(right_answer - sum(item))
        if distance == 0:
            # 没有误差错误等级是10（认为最小distance是0.1）
            error_levels.append(10)
        else:
            # 误差越大，错误等级越小
            error_levels.append(1 / distance)
    return error_levels


def choice_selected(old_answers, question_numbers_set):
    # choose good answer from old_answers
    result = []
    error_levels = get_error_levels(old_answers, question_numbers_set)
    #归一
    error_levels_one = [item / sum(error_levels) for item in error_levels]
    #概率化方便用random 取样
    for i in range(1, len(error_levels_one)):
        error_levels_one[i] += error_levels_one[i - 1]
    # 比如说 50个解，25对
    for i in range(len(old_answers) // 2):
        temp = []
        #选一对，2个
        for j in range(2):
            # ############按概率取样
            rand = random.uniform(0, 1)
            for k in range(len(error_levels_one)):
                if k == 0:
                    if rand < error_levels_one[k]:
                        temp.append(old_answers[k])
                        break
                else:
                    if rand >= error_levels_one[k - 1] and rand < error_levels_one[k]:
                        temp.append(old_answers[k])
                        break
        rand = random.randint(0, 6)
        #交换信息
        temp_1 = temp[0][:rand] + temp[1][rand:rand + 3] + temp[0][rand + 3:]
        temp_2 = temp[1][:rand] + temp[0][rand:rand + 3] + temp[0][rand + 3:]
        #添加到解集
        result.append(temp_1)
        result.append(temp_2)
    return result

#变异
def variation(old_answers, question_numbers_set, probability):
    for i in range(len(old_answers)):
        rand = random.uniform(0, 1)
        if rand < probability:
            rand_num = random.randint(0, 9)
            old_answers[i] = old_answers[i][:rand_num] + random.sample(question_numbers_set, 1) + old_answers[i][rand_num + 1:]
    return old_answers


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    question_numbers_set = random.sample(range(0, 1000), 50)
    print("len(question_numbers_set):", len(question_numbers_set))
    middle_answers = create_random_approx_answers(question_numbers_set, howMany=100)
    first_answer = middle_answers[0]
    greatest_answers = []
    for i in range(1000):
        middle_answers = choice_selected(middle_answers, question_numbers_set)
        middle_answers = variation(middle_answers, question_numbers_set, 0.1)
        error_levels = get_error_levels(middle_answers, question_numbers_set)
        index = error_levels.index(max(error_levels))
        greatest_answers.append([middle_answers[index], error_levels[index]])
    greatest_answers.sort(key=lambda x: x[1], reverse=True)
    print("right_answer:", sum(question_numbers_set) / 10)
    print("最优解为：", greatest_answers[0][0])
    print("该和为：", sum(greatest_answers[0][0]))
    print("错误等级为（10最大，越大越好）：", greatest_answers[0][1])
    print("最初解的和为", sum(first_answer))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
