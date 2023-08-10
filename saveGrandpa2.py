import random


class Grandpa:
    # 初始化方法，用于设置对象的初始属性
    def __init__(self, save, survive, day):
        self.save = save
        self.survive = survive
        self.day = day


results = []
days = [1, 2, 3, 4, 5, 6, 7]

# 模拟次数
totaldays = 50000


def main():
    intro()
    simNGame(totaldays)
    printResult()


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
    print('模拟结束')
    print('{:=<20}'.format('='))
    for i in days:
        filters = [gp for gp in results if gp.day == i and gp.save]
        p = len(filters)/len(results)
        print('第{}天，救出概率为：{}%'.format(
            i, (p)*100))

    for i in days:
        filters = [gp for gp in results if gp.day >=
                   i and gp.survive]  # 第7天活着的第7-1天肯定活着，所以要一起统计
        p = len(filters)/len(results)
        print('第{}天，存活概率为：{}%'.format(
            i, (p)*100))


def intro():
    '''
    输出一些提示
    '''
    print('模拟葫芦娃救爷爷，求出葫芦娃第几天去救爷爷的成功率最大')
    print('模拟次数：{}'.format(totaldays))
    print('{:=<20}'.format('='))


def simNGame(n):
    for i in range(n):
        simOneGame()


def simOneGame():
    '''
    7天视作一局
    默认没救出爷爷，爷爷存活
    '''

    '''
    救
    没救出》判断死亡
    救出》无动作
    '''
    gp = Grandpa(False, True, 0)
    results.append(gp)
    for i in days:
        gp.day = i
        if saveGrandpa(i):
            gp.save = True
            break
        else:
            if killGrandpa(i):
                gp.survive = False
                break


def saveGrandpa(day):
    c = 1/len(days)
    p = c*day
    r = random.random()
    # print('救出概率：{}>>>>实际概率：{}'.format(p, r))
    return r < p


def killGrandpa(day):
    c = len(days)
    d = abs(c-day+1)  # 每天空弹夹-1
    if d == 0:  # 解决除数为0问题
        d = 1
    p = 1/d
    r = random.random()
    # print('存活概率：{}>>>>实际概率：{}'.format(1-p, 1-r))
    return r < p


main()
