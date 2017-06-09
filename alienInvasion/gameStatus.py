#coding = utf-8
#Alien gameStatus-统计数据类
#2017.5.3
#v1.0 创建
#v1.1 增添分数参数记录玩家当前得分
import json
class GameStatus():
    """<<alien invasion>> 跟踪游戏统计数据"""
    def __init__(self,aiSettings):
        """初始化游戏统计数据"""
        self.aiSettings = aiSettings

        # 游戏启动标识,游戏一开始处于非活动状态,通过主流程中点击 play 开始游戏
        self.gameActive = False

        # 游戏最高得分
        try:
            filename = 'highestScore.json'
            with open(filename)as file_object:
                self.highestScore = json.load(file_object)
        except FileNotFoundError:
            self.highestScore = 0


        # 重新初始化游戏数据
        self.resetStatus()


    def resetStatus(self):
        """初始化游戏过程中的可变统计数据"""
        self.shipLeft = self.aiSettings.shipLimit
        self.score = 0
        self.level = 1
