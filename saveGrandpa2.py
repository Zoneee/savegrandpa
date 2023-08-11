import random


class Grandpa:
    # 初始化方法，用于设置对象的初始属性
    def __init__(self, save, survive, day, bros):
        self.save = save
        self.survive = survive
        self.day = day
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
totaldays = 5000


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
    custom_print('模拟结束')
    custom_print('{:=<20}'.format('='))
    for i in days:
        bros_filters = [gp for gp in results if gp.bros == i]
        d = len(bros_filters)
        if d == 0:
            d = 1
        custom_print('{1:=<20}行动模式：每天{0}行动一次，每次行动{0}人。{1:=<20}'.format(i, '='))

        for i in days:
            filters = [gp for gp in bros_filters if gp.day == i and gp.save]
            p = len(filters)/d
            custom_print('第{}昼，救出概率为：{:0>5.2f}%'.format(
                i, (p)*100))


'''
bug: bros>1 时，存活率与bros值分布过于规律
        for i in days:
            filters = [gp for gp in bros_filters if gp.day <=
                       i and gp.survive]  # 第7天活着的第7-1天肯定活着，所以要一起统计
            p = len(filters)/d
            custom_print('第{}夜，存活概率为：{:0>5.2f}%'.format(
                i, (p)*100))
'''


def intro():
    '''
    输出一些提示
    '''
    with open('output.txt', 'w') as f:  # 重置输出
        pass
    custom_print('模拟葫芦娃救爷爷，求出葫芦娃第几天去救爷爷的成功率最大')
    custom_print('模拟次数：{}'.format(totaldays))
    custom_print('{:=<20}'.format('='))


def simNGame(n):
    for i in range(n):
        simOneGame(1)
        simOneGame(2)
        simOneGame(3)
        simOneGame(4)
        simOneGame(5)
        simOneGame(6)
        pass


def simOneGame(bros):
    '''
    7天视作一局
    bros=1 代表每天排一人营救
    bros=3 代表跳过前两天，第三天排三人营救
    默认没救出爷爷，爷爷存活
    '''

    '''
    行动顺序
    每n天白天进行营救
    不论是否执行营救，都在当天晚进行轮盘赌
    
    救
    没救出》判断死亡
    救出》无动作
    '''
    gp = Grandpa(False, True, 0, bros)
    results.append(gp)
    start, stop, step = 1, 8, bros
    for i in range(start, stop):
        gp.day = i
        if i % bros == 0:  # 凑齐人数
            if morningAction(bros):
                gp.save = True
                break

            if i+step > len(days):  # 下次步长超过最后一天则强制出兵，强制出兵则无需执行夜晚行动，拯救失败以为着必死
                gp.day = len(days)
                bros = len(days)-i
                if morningAction(bros):
                    gp.save = True
                    break
                else:
                    gp.survive = False
                    break

        if nightAction(i):
            gp.survive = False
            break


def bronNBros(n):
    c = 1/len(days)
    return c*n


def morningAction(bros):
    return saveGrandpa(bros)


def nightAction(day):
    return killGrandpa(day)


def saveGrandpa(bros):
    c = 1/len(days)
    p = c*bros
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
