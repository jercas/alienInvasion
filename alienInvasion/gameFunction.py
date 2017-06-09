#coding=utf-8
#Alien Invasion-游戏逻辑类
#2017.4.25
#v1.0 创建
#v1.1 增添checkEvents()中键盘事件响应,增添形参对象ship —— 以实现飞船移动控制
#     增添updateScreen()中飞船位置更新 —— 以实现飞船位置的持续更新
#v1.2 重构checkEvents(),将其中KEYDOWN与KEYUP事件提出拆解为两个函数方便响应用户操作
#v1.3 重写checkKeydownEvents()和updateScreen(),添加对事件响应和位置更新
#v1.4 重构checkKeydownEvents(),将子弹发射逻辑提出为单独函数,简化按键事件响应函数函数体
#     增添getNumberAliensX() getNumberRow() createAlien() createAlienFlock(),四个函数在屏幕上生成外星人图像
#v1.5 重构createAliensFlock(),将计算行可容纳外星人数量和创建外星人并计算右移位置逻辑提出为两个函数
#v1.6 增添checkFlockEdge()和changeFlockDirection(),以实现外星人移动时碰触屏幕边缘下移并调整移动方向
#     在updateBullet(),添加碰撞检验调用（pygame.sprite.groupcollide(group1, group2, dokill1, dokill2, collided = None)）
#                      添加循环重写外星人逻辑（当外星人被消灭殆尽时）
#v1.7 重构updateBullet(),将子弹同外星人碰撞检查逻辑 和 循环重写外星人逻辑（过关）提出为独立函数体checkBulletAlienCollisions
#v1.8 增添shipHit(),处理飞船同外星人碰撞之后的逻辑处理（包括屏幕暂停播放爆炸动画,使飞船重新置底居中,清空子弹与外星人并重新绘制一批外星人编组）
#     增添checkAliensBottom(),处理外星人触底屏幕的情况
#v1.9 增添checkEvents()中,监测鼠标按键逻辑
#     增添checkPlayButton(),处理PLAY按钮触发后的游戏状态重置情况
#     优化checkPlayButton(),使该函数正确处理点击play重置游戏状态后的各项参数情况（所有参数初始化）,
#                           并将play按钮置于游戏活动状态不可触发,且在游戏活动状态隐藏光标
#v2.0 增添restartGame(),将重新开始/游戏结束时的数据、状态重置清空逻辑提出
#v2.1 修改checkBulletAlienCollisions(),增添击中外星人加分逻辑,动态更新计分板
#v.21 重构checkPlayButton(),将其中的游戏开局初始化逻辑提出为独立函数体startGame()
#     增添checkKeyDownEvent()中,按下小键盘Enter键开始游戏逻辑
#     优化checkBulletAlienCollisions(),优化子弹击中多个外星人时的加分逻辑
#v2.2 增添checkHighestScore(),判断当前得分是否超过最高分,如是更新最高分
import pygame
import sys
from bullet import  Bullet
from alien import Alien
from random import randint
#导入time模块,调用其中的sleep()使游戏（进程）暂停
from time import sleep
#导入json模块,保存数据
import json

def checkEvents(aiSettings,screen,status,playButton,ship,aliens,bullets,scoreBoard):
	"""监测键盘和鼠标事件,识别到退出操作时调用系统sys模块exit()函数退出"""
	for event in pygame.event.get():
		"""
		常用事件集：	
		事件 			产生途径 						参数
		QUIT 			用户按下关闭按钮 					none
		ATIVEEVENT 		Pygame被激活或者隐藏 				gain, state
		KEYDOWN 		键盘被按下 						unicode, key, mod
		KEYUP 			键盘被放开 						key, mod
		MOUSEMOTION 	鼠标移动 						pos, rel, buttons
		MOUSEBUTTONDOWN 鼠标按下 						pos, button
		MOUSEBUTTONUP 	鼠标放开 						pos, button
		JOYAXISMOTION 	游戏手柄(Joystick or pad)移动 	joy, axis, value
		JOYBALLMOTION 	游戏球(Joy ball)?移动 			joy, axis, value
		JOYHATMOTION 	游戏手柄(Joystick)?移动 			joy, axis, value
		JOYBUTTONDOWN 	游戏手柄按下 						joy, button
		JOYBUTTONUP 	游戏手柄放开 						joy, button
		VIDEORESIZE 	Pygame窗口缩放 					size, w, h
		VIDEOEXPOSE 	Pygame窗口部分公开(expose)? 		none
		USEREVENT 		触发了一个用户事件 				code
		"""
		#监测到QUIT事件,如点击退出或alt+f4时退出程序
		if event.type == pygame.QUIT:
			filename = 'highestScore.json'
			with open(filename,'w')as file_object:
				json.dump(status.highestScore,file_object)
			sys.exit()
		#监测到KEYDOWN事件,调用响应按键函数处理
		elif event.type == pygame.KEYDOWN:
			checkKeydownEvents(event,aiSettings,status,screen,ship,aliens,bullets,scoreBoard)
		#监测到KEYUP事件,调用响应松开函数处理
		elif event.type == pygame.KEYUP:
			checkKeyupEvents(event,ship)
		#监测到MOUSEBUTTONDOWN事件,调用PLAY按键函数处理
		elif event.type == pygame.MOUSEBUTTONDOWN:
			#获取mouse单击处的X,Y坐标
			mouseX,mouseY = pygame.mouse.get_pos()
			checkPlayButton(aiSettings,screen,status,playButton,ship,aliens,bullets,mouseX,mouseY,scoreBoard)


def checkKeydownEvents(event,aiSettings,status,screen,ship,aliens,bullets,scoreBoard):
	"""响应按键"""
	# 判断按键类型,快捷键ESC——退出,keypadEnter——开始,左右按键——置不同飞船移动标志为True
	if event.key == pygame.K_ESCAPE:
		filename = 'highestScore.json'
		with open(filename, 'w')as file_object:
			json.dump(status.highestScore, file_object)
		sys.exit()
	elif event.key == pygame.K_KP_ENTER:
		if not status.gameActive:
			startGame(aiSettings, screen, status, ship, aliens, bullets,scoreBoard)
	elif event.key == pygame.K_RIGHT:
		ship.movingRight = True
	elif event.key == pygame.K_LEFT:
		ship.movingLeft = True
	# 监测到子弹发射,创建一颗子弹加入编组bullets中监测到子弹发射,创建一颗子弹加入编组bullets中
	elif event.key == pygame.K_SPACE:
		fireBullets(aiSettings,screen,ship,bullets)


def fireBullets(aiSettings,screen,ship,bullets):
	# 判断屏幕上子弹是否已达最大数额,否则不可再继续射击（即增加子弹数）
	if len(bullets) < aiSettings.bulletAllowed:
		newBullet = Bullet(aiSettings, screen, ship)
		bullets.add(newBullet)


def checkKeyupEvents(event,ship):
	"""响应松开"""
	# 判断按键类型,置不同飞船移动标志为True
	if event.key == pygame.K_RIGHT:
		ship.movingRight = False
	elif event.key == pygame.K_LEFT:
		ship.movingLeft = False


def checkPlayButton(aiSettings,screen,status,playButton,ship,aliens,bullets,mouseX,mouseY,scoreBoard):
	"""响应PLAY按钮"""
	# rect.collidepoint()检测鼠标单击位置是否在rect的范围内
	buttonClick = playButton.rect.collidepoint(mouseX,mouseY)
	# 只有在游戏非活动状态时点击play button区域才可用
	if buttonClick and  not status.gameActive:
		startGame(aiSettings, screen, status, ship, aliens, bullets,scoreBoard)


def checkHighestScore(status,scoreBoard):
	"""判断当前得分是否超过最高分,如是更新最高分"""
	if status.score > status.highestScore:
		status.highestScore = status.score
		scoreBoard.prepareHighestScore()


def checkBulletAlienCollisions(aiSettings,screen,status,ship,aliens,bullets,scoreBoard):
	"""判断子弹击中外星人逻辑和循环重写外星人编组"""
	# 调用sprite.groupcollide()判断两个不同元组间的元素碰撞（rect位置重叠）
	# 返回一个字典,以classA(bullets)为Key classB(aliens)为Value的键值对
	# 后两个实参True,为判断两元组对象rect重叠后,分别在其各自的sprite编组中删除两个对象
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	# 根据返回字典判断碰撞是否存在,存在着说明击中-加分
	if collisions:
		# 遍历返回的字典,不漏掉任何一个发生碰撞的外星人对象
		for aliens in collisions.values():
			# len(aliens)即发生碰撞的外星人数
			status.score += aiSettings.alienPoints * len(aliens)
			scoreBoard.prepareScore()
		# 每当有得分更新后调用checkHighestScore,判断是否需要对最高分进行更新
		checkHighestScore(status,scoreBoard)
	# 判断外星人编组是否为空（即外星人消灭完毕）
	if len(aliens) == 0:
		# 如是,删除现有子弹 并 重新调用 creatAliensFlock绘制一批外星人（理解为简单意义上的 LEVEL 2）
		# 外星人 LEVEL 2 具体移动速度或者血量加成、模型变化等设定暂定
		# LEVEL UP
		status.level += 1
		scoreBoard.prepareLevel()
		bullets.empty()
		aiSettings.increaseSpeed()
		createAliensFlock(aiSettings, screen, ship, aliens)


def updateBullets(aiSettings,screen,status,ship,aliens,bullets,scoreBoard):
	"""子弹刷新,负责子弹位置刷新和子弹超限删除,形参获取 子弹对象"""
	# 子弹位置更新
	bullets.update()
	# 删除已消失的子弹
	for bullet in bullets.sprites():
		# 子弹矩形模型下标小于0,证明子弹已飞出屏幕将其从精灵编组中删去,避免继续消耗内存和处理能力
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	#判断子弹是否击中目标,若为最后一个目标刷新外星人队列
	checkBulletAlienCollisions(aiSettings,screen,status,ship,aliens,bullets,scoreBoard)

def getNumberAliensX(aiSettings,alienWidth):
	"""计算每行可容纳的外星人数量"""
	# 外星人间隔为两倍外星人宽度且屏幕两端均需留出一个外星人宽度,故行可用空间 = 总宽度 - 2*外星人宽度（即单个外星人占宽）
	availableSpaceX = aiSettings.screenWidth - (2 * alienWidth)
	# 行可容纳外星人数 = 行可用空间 / （2*外星人宽度）, 用int强制类型转换使结果为整数
	numberAlienX = int(availableSpaceX / (2 * alienWidth))
	return numberAlienX


def getNumberRow(aiSettings,shipHeight,alienHeight):
	"""计算屏幕可容纳多少行外星人"""
	# 以屏幕高度减去第一行外星人上边距（外星人图像高度）、飞船高度、以及外星人群与飞船距离（外星人高度两倍）,故列可用空间 = 总高度 - 飞船高度 - 3倍外星人高度
	availableSpaceY = (aiSettings.screenHeight - shipHeight - (3 * alienHeight))
	# 可容纳行数 = 列可用空间 / （2*外星人高度）,用int强制类型转换使结果为整数
	numberRow = int(availableSpaceY / (2 * alienHeight))
	return numberRow


def createAlien(aiSettings,screen,aliens,alienNumber,rowNumber):
	alien = Alien(aiSettings, screen)
	# 通过计算x坐标,将其加入当前行,并将每个外星人往右推一个外星人宽的距离
	alien.floatX = alien.rect.width  + 2 * alien.rect.width  * alienNumber
	# 通过计算y坐标,将其加入新列,并将每个外星人往下推一个外星人高的距离
	alien.floatY = alien.rect.height + 2 * alien.rect.height * rowNumber
	# 获取推移后外星人初始位置
	alien.rect.x = alien.floatX
	alien.rect.y = alien.floatY
	aliens.add(alien)


def createAliensFlock(aiSettings, screen, ship, aliens):
	"""创建外星人群"""
	# 创建一个外星人
	alien = Alien(aiSettings,screen)
	# 计算一行可容纳外星人数量
	# 由外星人矩形模块获取其宽度及高度,由飞船矩形模块获取其高度
	alienWidth 	= alien.rect.width
	alienHeight = alien.rect.height
	shipHeight  = ship.rect.height
	# 获取行可容纳外星人数量
	numberAlienX = getNumberAliensX(aiSettings,alienWidth)
	# 获取可容纳行数
	numberRow    = getNumberRow(aiSettings,shipHeight,alienHeight)

	# 不断创建多行外星人
	for  rowNumber in range(numberRow):
		for alienNumber in range(numberAlienX):
			# 不断创建外星人加入每一行中
			# 随机创建
			randomAlienNumber = randint(1,7)
			randomRowNumber = randint(0,2)
			createAlien(aiSettings,screen,aliens,randomAlienNumber,randomRowNumber)

			# 规则创建
			# createAlien(aiSettings, screen, aliens, alienNumber, rowNumber)


def checkFlockEdge(aiSettings,aliens):
	"""判断外星人是否碰触屏幕边缘,并调用响应函数"""
	# 逐一遍历外星人编组中的外星人
	for alien in aliens.sprites():
		# 调用alien类内部函数判断是否碰触边缘
		if alien.checkEdge():
			# 如有碰触,调用下移转向函数changeFlockDirection并立即跳出循环
			changeFlockDirection(aiSettings,aliens)
			break


def changeFlockDirection(aiSettings,aliens):
	"""对整个外星人群进行下移并转向"""
	# 逐一遍历外星人编组中的外星人
	for alien in aliens.sprites():
		# 下移外星人
		alien.rect.y += aiSettings.alienDropSpeedFactor
	# 1→-1  -1→1 修改外星人移动方向标识,调整外星人移动方向
	aiSettings.alienMoveDirection *= -1

def checkAliensBottom(aiSettings,status,screen,ship,aliens,bullets,scoreBoard):
	"""处理外星人触底逻辑"""
	# 获取游戏屏幕的外接矩形
	screenRect = screen.get_rect()
	# 逐一检查外星人编组中是否有外星人触底
	for alien in aliens.sprites():
		if alien.rect.bottom >= screenRect.bottom:
			# 如有触底,调用shipHit()视作飞船被碰撞,跳出循环不再检测余下编组元素情况
			shipHit(aiSettings,status,screen,ship,aliens,bullets,scoreBoard)
			break


def shipHit(aiSettings,status,screen,ship,aliens,bullets,scoreBoard):
	"""处理外星人和飞船碰撞后的逻辑"""
	# 尚有可用飞船数
	if status.shipLeft > 0:
		# 可用飞船数减一
		status.shipLeft -= 1
		# 飞船图标减一
		scoreBoard.prepareShips()
		# 重开下条命
		restartGame(aiSettings,screen,ship,aliens,bullets)
		# 暂停游戏一秒
		sleep(1.0)
	else:
		# 无可用飞船,游戏结束置游戏状态为非活动
		status.gameActive = False
		# 在非活动状态显示光标
		pygame.mouse.set_visible(True)


def startGame(aiSettings,screen,status,ship,aliens,bullets,scoreBoard):
	# 隐藏光标,向set_visible传递False将隐藏光标
	pygame.mouse.set_visible(False)
	# 重置游戏动态数据
	aiSettings.init_dynamic_settings()
	# 重置游戏统计信息
	status.resetStatus()
	# 重置所有计分板图像
	scoreBoard.prepareScore()
	scoreBoard.prepareHighestScore()
	scoreBoard.prepareLevel()
	scoreBoard.prepareShips()
	# 单击PLAY,游戏运行状态开始
	status.gameActive = True
	# 重开下局游戏
	restartGame(aiSettings, screen, ship, aliens, bullets)



def restartGame(aiSettings,screen,ship,aliens,bullets):
	# 清空外星人和子弹编队
	aliens.empty()
	bullets.empty()
	# 绘制一批外星人编队
	createAliensFlock(aiSettings, screen, ship, aliens)
	# 将飞船置底居中
	ship.centerShip()


def updateAliens(aiSettings,status,screen,ship,aliens,bullets,scoreBoard):
	"""外星人刷新,负责外星人位置刷新"""
	# 是否有碰触屏幕边缘情况？
	checkFlockEdge(aiSettings,aliens)
	# 外星人位置更新
	aliens.update()
	# 监测外星人和飞船间的碰撞
	if pygame.sprite.spritecollideany(ship,aliens):
		print("Mayday Mayday!")
		shipHit(aiSettings,status,screen,ship,aliens,bullets,scoreBoard)
	# 每次刷新外星人都检测有无外星人触底发生
	checkAliensBottom(aiSettings,status,screen,ship,aliens,bullets,scoreBoard)


def updateScreen(aiSettings,screen,status,ship,aliens,bullets,playButton,scoreBoard):
	"""在用户操作时不断刷新屏幕,三个形参分别获取 游戏设置,屏幕surface对象,飞船对象"""
	# 每次循环时都重绘屏幕
	screen.fill(aiSettings.backgroundColor)

	# 绘制子弹,对子弹精灵元组逐一调用draw.rect()进行绘制
	# 无图像编组元素 绘制法
	for bullet in bullets.sprites():
		bullet.drawBullet()
		#pygame.draw.rect(bullet.screen, bullet.color, bullet.rect)

	# 绘制飞船
	ship.blitme()

	# 绘制外星人,对编组调用 draw() pygame会自动绘制编组的每个元素,绘制位置由image的属性rect决定
	# 有图像编组元素 绘制法
	aliens.draw(screen)

	# 绘制计分板
	scoreBoard.showScore()

	# 如果游戏处于非活动状态,绘制Play按钮
	if not status.gameActive:
		playButton.drawButton()

	# 让最近绘制的屏幕可见
	pygame.display.flip()