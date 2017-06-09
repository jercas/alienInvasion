#coding = utf-8
#Alien Invasion-按钮类
#2017.5.4
#v1.0 创建
# 导入pygame.font模块,可将文本渲染到屏幕上
import pygame.font
class Button():
    """<<alien invasion>> 用于创建游戏中的可点选按键"""
    def __init__(self,aiSettings,screen,msg):
        """初始化按钮的属性"""
        # 获取主流程传入的屏幕surface对象
        self.screen = screen
        # 获取屏幕的外接矩形
        self.screenRect = screen.get_rect()

        # 设置按钮的基本尺寸和其他属性
        self.width = 200
        self.height = 50
        self.buttonColor = (0,255,255)
        self.textColor = (255,255,255)
        # 创建文本对象font,设置字体来渲染文本,None--默认字体,48--文本字号
        self.font = pygame.font.SysFont(None,48)

        # 创建按钮的rect外接矩形对象,并设置位于屏幕居中
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screenRect.center

        # 创建按钮的标签,负责将文字Msg渲染为图像
        self.prepareMsg(msg)


    def prepareMsg(self,msg):
        """负责将文字Msg渲染为图像,并使其居中"""
        # 调用font.render()将存储在参数msg中的文本转换为图像image并存在msgImage中
        # 第二形参为布尔型,指定开启/关闭反锯齿功能（反锯齿使文本边缘更平滑）
        # 第三、四形参指定文本颜色和背景色（此处以按钮颜色来设置image背景色,若背景色未指定则为透明背景）
        self.msgImage = self.font.render(msg,True,self.textColor,self.buttonColor)
        # 此时已经将文本转换成了image对象,故可以直接获取其rect对象
        self.msgImageRect = self.msgImage.get_rect()
        # 使文本图像在按钮之中居中
        self.msgImageRect.center = self.rect.center


    def drawButton(self):
        """绘制一个用颜色填充的按钮,再绘制文本"""
        # 绘制表示按钮的矩形
        self.screen.fill(self.buttonColor,self.rect)
        # 传递图像和该图像关联的rect对象,从而在屏幕上绘制文本图像
        self.screen.blit(self.msgImage,self.msgImageRect)