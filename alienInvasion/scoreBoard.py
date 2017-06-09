#coding = utf-8
#Alien Invasion-计分板类
#2017.5.8
#v1.0 创建
#v1.1 添加最高分积分板显示prepareHighestScore(),逻辑类同计分板显示方式
#     添加等级显示prepareLevel(),逻辑类同计分板显示方式
#v1.2 导入Group类和Ship类创建飞船编组

#导入pygame中font模块用以将文字渲染为图像
import pygame.font
from pygame.sprite import Group
from ship import Ship

class ScoreBoard():
    """<<alien invasion>> 用于创建游戏中的计分板"""
    def __init__(self,aiSettings,screen,status):
        """初始化得分统计相关属性"""
        self.aiSettings = aiSettings
        self.screen     = screen
        self.status     = status

        # 获取屏幕rect对象
        self.screenRect = screen.get_rect()

        # 设置文本颜色
        self.textColor = (30,30,30)
        # 创建文本对象font,设置字体来渲染文本,None--默认字体,48--文本字号
        self.font = pygame.font.SysFont(None,48)

        # 初始化计分板、最高分、等级、飞船图像
        self.prepareScore()
        self.prepareHighestScore()
        self.prepareLevel()
        self.prepareShips()


    def prepareScore(self):
        """将得分文本转换为图像"""
        # 将gameStatus类中存储的初始化分数变量由 int→str,并使其圆整化
        # round(),使小数精确到小数点后多少位,其中小数位数由第二实参指定（当为负数时round()将圆整到最近的10,100,1000等整数倍）
        roundedScore = int(round(self.status.score,-1))
        # 字符串格式设置指令,将数值转换为字符串时在其中千分位插入逗号
        scoreStr = "{:,}".format(roundedScore)
        # 调用font类中render()将文本渲染为图像,分别指定所需渲染文本、是否抗锯齿以及文本和背景颜色
        self.scoreImage = self.font.render(scoreStr,True,self.textColor,self.aiSettings.backgroundColor)
        # 获取刚转换的文本图像（即计分板图像）的rect对象
        self.scoreRect = self.scoreImage.get_rect()
        # 设置计分板图像位置,置于屏幕右上角
        self.scoreRect.right = self.screenRect.right - 20
        self.scoreRect.top = 20


    def prepareHighestScore(self):
        """将最高分文本转换为图像"""
        roundedHighestScore = int(round(self.status.highestScore, -1))
        highestScoreStr = "{:,}".format(roundedHighestScore)
        self.highestScoreImage = self.font.render(highestScoreStr, True, self.textColor, self.aiSettings.backgroundColor)
        self.highestScoreRect = self.highestScoreImage.get_rect()
        # 设置最高分图像位置,置于屏幕顶部中央
        self.highestScoreRect.centerx = self.screenRect.centerx
        self.highestScoreRect.top = 20


    def prepareLevel(self):
        """将等级文本转换为图像"""
        self.levelImage = self.font.render(str(self.status.level), True, self.textColor, self.aiSettings.backgroundColor)
        self.levelRect = self.levelImage.get_rect()
        # 设置最高分图像位置,置于计分板图像下方
        self.levelRect.right = self.screenRect.right - 20
        self.levelRect.top = self.scoreRect.bottom+10


    def prepareShips(self):
        """显示剩余的飞船数"""
        # 创建飞船编组
        self.ships = Group()
        # 遍历飞船编组,依次在屏幕左上角生成飞船图像以表示可用飞船数
        for shipNumber in range(self.status.shipLeft):
            ship = Ship(self.aiSettings,self.screen)
            ship.rect.x = 10 + shipNumber * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)


    def showScore(self):
        """显示计分板"""
        self.screen.blit(self.scoreImage,self.scoreRect)
        self.screen.blit(self.highestScoreImage,self.highestScoreRect)
        self.screen.blit(self.levelImage,self.levelRect)
        self.ships.draw(self.screen)