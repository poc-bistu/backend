import board
import amazons
import timer


class Room():
    def __init__(self, boardtype, boardargs, totaltime):

        # 初始化棋盘，计时器， 玩家列表， 比赛状态
        self.__board = board.Board()
        self.__timmer = timer.Timer(totaltime)
        self.__status = 0
        self.player = []

        # 根据其中覆盖原棋盘

        if boardtype == None:
            pass
        elif boardtype == 'amazons':
            self.__board = amazons.Amazons(boardargs[0], boardargs[1])
        else:
            pass

    # 加入玩家
    def addplayer(self, player):
        # 初始化玩家ID列表，支持12个玩家。
        idList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

        # 初始化搜寻ID
        playerNum = len(self.player)

        # 通过ID 找寻玩家，这样会更方便一些
        for searchID in idList:
            flag = 1
            for i in range(playerNum):
                if self.player[i]['id'] == searchID:
                    flag = 0

            if flag == 1:
                self.player.append({'id': searchID, 'player': None})
        '''
        ⬆️ 上面还缺少玩家这个类的实例。
        '''

    # 删除玩家
    def removeplayer(self, id):
        playerNum = len(self.player)
        for i in range(playerNum):
            if self.player[i]['id'] == id:
                self.player.pop(i)

        return 1

    # 开始游戏，并开始计时
    def start(self):
        self.__status = 1
        pass

    # 获取比赛状态
    def status(self):
        return {'status': self.__status, 'message': None}

    # 移动棋子
    def move(self, player, location, *kw):
        return self.__board.fire(player, location, *kw)








