#coding=utf-8
#Alien Invasion-外星人类
#2017.4.24
#v1.0 创建
#     添加update()更新外星人移动后的图像
#     添加checkEdge()判断外星人是否移动到屏幕边缘
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """<<alien invasion>> 对外星人的显示,运动进行统一编码"""
    def __init__(self,aiSettings,screen):
        """初始化外星人并设置其初始位置"""
        """继承Sprite类进行初始化以实现编组外星人统一操作"""
        super().__init__()
        # 接收前台传入的屏幕对象,settings类对象
        self.screen = screen
        self.aiSettings = aiSettings

        #加载外星人图像
        self.image = pygame.image.load("image/alien.bmp")

        #获取外星人外接矩形
        self.rect  = self.image.get_rect()

        #初始化外星人位置
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #存储外星人准确位置
        self.floatX = float(self.rect.x)


    def checkEdge(self):
        """判断外星人是否移动到屏幕边缘,是的话返回True"""
        screenRect = self.screen.get_rect()
        if self.rect.right >= screenRect.right:
            return True
        elif self.rect.left <= 0 :
            return True


    def update(self):
        """更新外星人移动位置"""
        # 更新时更新可以接收浮点数的floatX而非rect.x
        # 且以settings类中外星人的移动速度变量alienSpeedFactor来作为更新数值
        # 根据setting类中外星人移动方向标识alienMoveDirection更新外星人位置（右移时为正增大X，左移时为负缩小X）
        self.floatX += ( self.aiSettings.alienSpeedFactor * self.aiSettings.alienMoveDirection )
        self.rect.x = self.floatX


    def blitme(self):
        """在指定位置绘制外星人"""
        # blit函数根据两形参分别获取,绘图图像和绘图位置
        self.screen.blit(self.image,self.rect)
