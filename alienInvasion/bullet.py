#coding = utf-8
#Alien Invasion-子弹类
#2017.4.26
#v1.0 创建
import pygame
#导入Sprite类,使用"精灵"来将子弹元素编组处理
from pygame.sprite import  Sprite

class Bullet(Sprite):
    """<<alien invasion>> 对子弹的显示,运动轨迹进行统一编码"""
    def __init__(self,aiSettings,screen,ship):
        """初始化一个子弹对象和其位置（位于飞船顶端）"""
        #继承Sprite类进行重构,接收前台传入的screen surface对象
        super().__init__()
        self.screen = screen

        #子弹并未有图像基础,需要从空白处开始创建,此与（0,0）处开始创建一个小矩形充当子弹,由Settings类中获取其参数
        #此处不同于有图像基础可直接用pygame.get_rect()获取矩形模型,需调用Rect类初始化生成
        self.rect = pygame.Rect(0,0,aiSettings.bulletWidth,aiSettings.bulletHeight)
        #创建小矩形后,再将其移动到正确位置,即飞船的顶端中间
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #将只能存储整数值的rect中的数值转为浮点数存储在变量中, 以便updatte() 函数更新子弹位置时更细节化到小数位
        self.floatY = float(self.rect.y)

        #导入Settings中Bullet速度,颜色参数
        self.color = aiSettings.bulletColor
        self.speedFactor = aiSettings.bulletSpeedFactor


    def update(self):
        """移动子弹"""
        # 更新时更新可以接收浮点数的floatY而非rect.y
        # 且以settings类中子弹的移动速度变量bulletSpeedFactor来作为更新数值
        self.floatY -= self.speedFactor
        # 最后根据更新完的浮点数floatY的值更新子弹位置rect.y
        self.rect.y = self.floatY


    def drawBullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen,self.color,self.rect)
