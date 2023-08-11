import random
import itertools


class Grandpa:
    # 初始化方法，用于设置对象的初始属性
    def __init__(self, save, survive, day, bros):
        self.save = save
        self.survive = survive
        self.day = day  # 存活天数
        self.bros = bros


def custom_print(*args, **kwargs):
    # 打开文件以追加模式
    with open('output.txt', 'a', encoding='utf8') as f:
        # 将内容输出到文件
        print(*args, file=f, **kwargs)

    # 将内容输出到控制台
    print(*args, **kwargs)


results = []
days = [1, 2, 3, 4, 5, 6]

# 模拟次数
simnum = 5000


def main():
    intro()
    survivedModes = generateModes()
    for mode in survivedModes:
        results.clear()
        simNGame(simnum, mode)
        printResult()


def generateModes():
    result = []
    for a in range(7):
        for b in range(7):
            for c in range(7):
                for d in range(7):
                    for e in range(7):
                        for f in range(7):
                            for g in range(7):
                                if a + b + c + d + e + f + g == 6:
                                    result.append([a, b, c, d, e, f, g])
    return result


def printResult():
    '''
    输出每日救出概率和存活概率
    救出概率=救出次数/总次数
    存活概率=存活次数/总次数
    '''

    '''
    ==========================================================
    =========注：救出后不能再救，死亡后不能再救======================
    ===========================================================
    '''
    custom_print('模拟结束')
    custom_print('{:=<20}'.format('='))
    computeSurvived()
    computeSaved()
    custom_print('{:*<20}'.format('*'))


def computeSaved():
    custom_print('{1:=<20}救出概率{1:=<20}'.format(1, '='))

    for j in days:
        filters = [gp for gp in results if gp.day == j and gp.save]
        p = len(filters)/simnum
        custom_print('第{}昼，救出概率为：{:0>5.2f}%'.format(
            j, (p)*100))
    pass


def computeSurvived():
    custom_print('{1:=<20}存活概率{1:=<20}'.format(1, '='))
    # formation1()
    formation2()
    pass


def formation1():
    # day1存活人数=活着 && day>=day1
    # day2的人（不论死活）day1一定活着，所以统计day2的存活人数=总人口-day1死亡-day2死亡
    total = len([gp for gp in results if gp.bros == 2])  # 筛选营救模式为2的数据
    custom_print(
        'f1。{1:=<20}行动模式：每天{0}行动一次，每次行动{0}人。{1:=<20}'.format(2, '='))
    for i in days:
        survived = len(
            [gp for gp in results if gp.survive and gp.day >= i and gp.bros == 2])
        p = survived/total
        custom_print('第{}夜，存活概率为：{:0>5.2f}%'.format(i, (p)*100))
    pass


def formation2():
    total = simnum
    dieds = 0
    for i in days:
        # day1的死亡人数
        dayDieds = len(
            [gp for gp in results if gp.day == i and not gp.survive])
        # dayN为止的总死亡人数
        dieds += dayDieds
        surviveds = total-dieds
        p = surviveds/total
        custom_print('第{}夜，存活概率为：{:0>5.2f}%'.format(i, (p)*100))
    pass


def intro():
    '''
    输出一些提示
    '''
    with open('output.txt', 'w') as f:  # 重置输出
        pass
    custom_print('模拟葫芦娃救爷爷，求出葫芦娃第几天去救爷爷的成功率最大')
    custom_print('模拟次数：{}'.format(simnum))
    custom_print('{:=<20}'.format('='))


def simNGame(n, mode):
    '''
    模拟N局游戏
    '''
    custom_print('营救模式：{}'.format(mode))
    for i in range(n):
        simOneGame(mode)
        pass


def simOneGame(mode):
    '''
    模拟一局，6天视作一局

    args:
    mode: 行动模式数组
    '''
    gp = Grandpa(False, True, 0, 0)
    results.append(gp)
    day = 1
    for bros in mode:
        gp.day = day
        gp.bros = bros
        survived, saved = simOneDay(day, bros)
        if saved or not survived:
            gp.save = saved
            gp.survive = survived
            break
        day += 1
    pass


def simOneDay(day, bros):
    '''
    模拟一天

    args：
    day: 第几天
    bros: 当天出发的营救人数

    return
    bool: 人物是否存活
    bool: 人物是否救出
    '''

    if morningAction(bros):
        return True, True

    if nightAction(day):
        return False, False

    return True, False


def bronNBros(n):
    c = 1/len(days)
    return c*n


def morningAction(bros):
    '''
    白天行动：营救

    args:
    bros: 出动人数

    result:
    bool: 营救成功
    '''
    return saveGrandpa(bros)


def nightAction(day):
    '''
    夜晚行动：轮盘赌

    args:
    day: 天数

    result:
    bool: 死亡
    '''
    return killGrandpa(day)


def saveGrandpa(bros):
    c = 1/len(days)
    p = c*bros
    r = random.random()
    # print('救出概率：{}>>>>实际概率：{}'.format(p, r))
    return r < p


def killGrandpa(day):
    c = len(days)
    d = abs(c-day+1)  # 每天弹夹-1，第一天不减
    if d == 0:  # 解决除数为0问题
        d = 1
    p = 1/d  # 中弹概率
    r = random.random()
    # print('存活概率：{}>>>>实际概率：{}'.format(1-p, 1-r))
    return r < p


main()
