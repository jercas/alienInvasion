#coding=utf-8
#Alien Invasion-飞船类
#2017.4.25
#v1.0 创建
#v1.1 在初始化函数中设置飞船移动标志标明飞船状态,并创建函数update()实现飞船位置变化
#     在Ship类初始化函数中添加形参对象aiSettings以调用setting类中存储的飞船数据(移动速度,弹药量等)
#v1.2 增添centetShip(),以将飞船重新置于屏幕置底居中位置
#v1.3 转换Ship()使其继承Sprite,可以创建飞船编组
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	"""<<alien invasion>> 对飞船的显示,运动进行统一编码"""
	def __init__(self,aiSettings,screen):
		"""初始化飞船并设置其初始位置"""
		super().__init__()
		#接收前台传入的屏幕对象,settings类对象
		self.screen = screen
		self.aiSettings = aiSettings
		
		#加载飞船图像
		self.image = pygame.image.load('image/ship.bmp')

		#获取飞船,游戏屏幕的外接矩形,像处理矩形(rect = rectangle)一样处理游戏元素
		self.rect  =  self.image.get_rect()
		self.screenRect = screen.get_rect()
		
		#将飞船初始化置于屏幕底部中央(下两句语法即为,飞船的底部是屏幕的底部,飞船的中央是屏幕的中央,规定了飞船外接矩形的x,y矩形)
		self.rect.centerx = self.screenRect.centerx
		self.rect.bottom  = self.screenRect.bottom
		
		#飞船移动标志
		self.movingRight = False
		self.movingLeft  = False
		
		#将只能存储整数值的rect中的数值转为浮点数存储在变量中,以便updatte()函数更新飞船位置时更细节化到小数位
		self.floatCenterx = float(self.rect.centerx)

		
	def update(self):
		"""根据飞船移动标志调整飞船的位置"""
		#飞船移动标志为True飞船移动
		if self.movingRight and self.rect.right < self.screenRect.right:
			#更新时更新可以接收浮点数的floatCenterx而非rect.centerx
			#且以settings类中飞船的移动速度变量shipSpeedFactor来作为更新数值
			self.floatCenterx += self.aiSettings.shipSpeedFactor
		if self.movingLeft  and self.rect.left > 0:
			self.floatCenterx -= self.aiSettings.shipSpeedFactor
		#最后根据更新完的浮点数floatCenterx的值更新飞船位置rect.centerx
		self.rect.centerx = self.floatCenterx


	def blitme(self):
		"""在指定位置绘制飞船"""
		#blit函数根据两形参分别获取,绘图图像和绘图位置
		self.screen.blit(self.image,self.rect)


	def centerShip(self):
		self.center = self.screenRect.centerx