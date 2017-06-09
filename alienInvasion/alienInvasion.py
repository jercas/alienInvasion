# coding = utf-8
# Alien Invasion-主程序
# 2017.4.24
# v1.0 创建主流程函数,绘制Python窗口,监测事件;设置背景
# v1.1 创建Settings类 —— 重构主程序,将'游戏设置'提出单独成类,避免各种设置在主代码中亢余的情况
#     创建Ship类,负责飞船的行为控制
# v1.2 创建gameFunction类,负责游戏运行具体函数 —— 重构主程序,将'事件响应'操作提出到gameFunction模块checkEvents()中(原因同上)
#											  —— 重构主程序,将'屏幕刷新'操作提出到gameFunction模块updateScreen()中(原因同上)
#      在主流程中实例化子弹对象,附加对子弹的事件响应和位置更新
# v1.3 添加子弹删除逻辑,优化游戏运行 —— 重构主程序,将'删除过限子弹'和'刷新子弹位置'操作提出到gameFunction模块updateBullets()中（原因同上）
#      在主流程中实例化外星人对象,添加updateScrenn()形参,以在屏幕上刷新外星人位置
#      在主流程中添加外星人图像刷新函数调用updateAliens()
# v1.4 重构主流程逻辑,将主流程分为活动状态 和 非活动状态
#      checkEvent()事件监测函数可在 非活动状态下运行,以响应用户ese或单击X按钮退出游戏
#      updateScreen()屏幕刷新函数可在 非活动状态下运行,以在gameover玩家是否选择重新开始游戏时刷新屏幕与鼠标位置
#      ship.update()、updateBullets()、updateAliens()只可在 活动状态下运行,当游戏暂停或结束时停止刷新这三者对象的位置
# v1.5 在主流程中创建Button实例,创建PLAY button
#      在主流程中创建scoreBoard，创建计分板

# 导入Pygame模块
import pygame
# 导入settings模块,以调用Settings类初始化/修改游戏设置
from settings import Settings
# 导入ship模块,以创建飞船并调用飞船操作控制
from ship import Ship
# 导入alien模块,以创建外星人并调用外星人移动控制
from alien import Alien
# 导入gameFunction模块,以调用游戏逻辑控制等
import gameFunction
# 导入pygame.sprite模块,调用其中Group类将子弹存储为一个编组进行统一处理
from pygame.sprite import Group
# 导入gameStatus模块,调用其中GameStatus类存储并调用游戏统计数据
from gameStatus import GameStatus
# 导入button模块,调用其中Button类创建按钮
from button import Button
# 导入scoreBoard模块,调用其中的ScoreBoard类创建计分板
from scoreBoard import ScoreBoard
"""
#导入sys模块,以调用exit()函数退出
import sys 
v1.2中剔除,因事件响应操作提出到gameFunction中的checkEvents()函数中进行,主程序中不再需要直接调用sys
"""

def runGame():
	"""<<alien invasion>>主函数"""
	# 初始化游戏
	pygame.init()
	# 创建Settings类对象访问游戏设置
	aiSettings = Settings()
	# 创建一个屏幕对象
	screen = pygame.display.set_mode((aiSettings.screenWidth, aiSettings.screenHeight))
	"""
	set_mode会返回一个Surface对象，代表了在桌面上出现的那个窗口，三个参数第一个为元祖，代表分辨率（必须）；
	第二个是一个标志位，具体意思见下表，如果不用什么特性，就指定0；第三个为色深。
	标志位 	功能
	FULLSCREEN 	创建一个全屏窗口
	DOUBLEBUF 	创建一个“双缓冲”窗口，建议在HWSURFACE或者OPENGL时使用
	HWSURFACE 	创建一个硬件加速的窗口，必须和FULLSCREEN同时使用
	OPENGL 		创建一个OPENGL渲染的窗口
	RESIZABLE 	创建一个可以改变大小的窗口
	NOFRAME 	创建一个没有边框的窗口
	"""
	# 创建一个统计数据存储对象,并初始化游戏部分动态参数
	status = GameStatus(aiSettings)
	# 创建一个飞船对象
	ship = Ship(aiSettings, screen)
	# 创建一组外星人序列
	aliens = Group()
	# 创建一组子弹序列
	bullets = Group()
	# 创建PLAY按钮
	playButton = Button(aiSettings,screen,'Play')
	# 创建计分板
	scoreBoard = ScoreBoard(aiSettings,screen,status)
	# 设置窗口标题
	pygame.display.set_caption("Alien Invasion By JerCas丶Ety")

	# 开始游戏主循环
	"""
	无限循环，直到用户跳出。在这个主循环里做的事情就是不停地画背景和更新光标位置，
	虽然背景是不动的，我们还是需要每次都画它， 否则鼠标覆盖过的位置就不能恢复正常了。
	"""
	while True:
		# 1.检查玩家输入-2.更新飞船位置-3.更新所有未消失子弹位置并删除已消失子弹位置-4.根据以上更新后的screen对象位置刷新重新绘制屏幕
		gameFunction.checkEvents(aiSettings,screen,status,playButton,ship,aliens,bullets,scoreBoard)
		# 游戏处于活动状态时 才刷新三者对象位置
		if status.gameActive:
			# 飞船位置更新,！！！必须置于屏幕刷新语句前,以便实现飞船位置更新后再刷新屏幕而将更新后的新位置刷新到屏幕上以实现视觉上的位置移动
			ship.update()
			gameFunction.updateBullets(aiSettings,screen,status,ship,aliens,bullets,scoreBoard)
			gameFunction.updateAliens(aiSettings,status,screen,ship,aliens,bullets,scoreBoard)
		gameFunction.updateScreen(aiSettings,screen,status,ship,aliens,bullets,playButton,scoreBoard)

runGame()
