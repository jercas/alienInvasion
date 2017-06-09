#coding = utf-8
#Alien Invasion-设置类 将游戏设置提出单独成类,避免各种设置在主代码中亢余的情况
#2017.4.24
#v1.0 创建
#v1.1 整合入各项飞船参数(如飞船参数,弹药量等)
#v1.2 重构属性设置逻辑,将设置分为静态属性和动态属性,分为两个函数控制,并添加speedupScale属性调控游戏速度,
#                     并增添函数increaseSpeed()利用speedupScale修改游戏元素速度
class Settings():
	"""<<alien invasion>> 存储所有设置的类"""
	def __init__(self):
		"""初始化游戏的静态设置"""
		# 设置屏幕分辨率
		self.screenWidth = 1200
		self.screenHeight = 600
		# 设置背景色
		self.backgroundColor = (230,230,230)

		# 设置飞船数
		self.shipLimit = 2

		# 设置外星人垂直移动速度
		self.alienDropSpeedFactor = 20

		# 设置子弹参数
		self.bulletSpeedFactor = 3
		self.bulletWidth = 5
		self.bulletHeight = 15
		self.bulletColor = (60,60,60)
		self.bulletAllowed = 5

		# 游戏速度控制参数
		self.speedupScale = 1.5
		# 游戏得分控制参数
		self.scoreScale = 2
		# 声明函数
		self.init_dynamic_settings()


	def init_dynamic_settings(self):
		"""初始化游戏动态设置"""
		# 游戏速度参数
		# 设置外星人水平移动速度
		self.alienSpeedFactor = 1
		# 设置子弹移动速度
		self.bulletSpeedFactor = 3
		# 设置飞船移动速度
		self.shipSpeedFactor = 1.5
		# 设置外星人水平移动方向标识, 1=右移 -1=左移
		self.alienMoveDirection = 1

		#　游戏得分参数
		self.alienPoints = 50


	def increaseSpeed(self):
		"""动态修改游戏参数"""
		# 根据速度控制参数动态增加各对象速度
		self.shipSpeedFactor   *= self.speedupScale
		self.alienSpeedFactor  *= self.speedupScale
		self.bulletSpeedFactor *= self.speedupScale
		# 根据得分控制参数动态增加等级提升时的得分
		self.alienPoints = int(self.alienPoints * self.scoreScale)
		# 在终端窗口显示当前等级分数值
		print(self.alienPoints)
