## 导入相关模块
import random
import pygame
import sys
from pygame.locals import *

windows_width = 800
windows_height = 600  # 游戏窗口的大小
cell_size = 20  # 贪吃蛇身体方块大小,注意身体大小必须能被窗口长宽整除

''' #初始化区
由于我们的贪吃蛇是有大小尺寸的, 因此地图的实际尺寸是相对于贪吃蛇的大小尺寸而言的
'''
map_width = int(windows_width / cell_size)
map_height = int(windows_height / cell_size)

# 颜色定义
white = (255, 255, 255)
black = (0, 0, 0)
gray = (230, 230, 230)
dark_gray = (40, 40, 40)
DARKGreen = (0, 155, 0)
Green = (0, 255, 0)
Red = (255, 0, 0)
blue = (0, 0, 255)
dark_blue = (0, 0, 139)

FOOD_color = [(10, (255, 100, 100)), (20, (100, 255, 100)), (30, (100, 100, 255))]  # 食物颜色
# FOOD_jpg = ["sb0102.jpg","sh01.jpg"]
BG_COLOR = black  # 游戏背景颜色


# 定义方向
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

HEAD = 0  # 贪吃蛇头部下标
score_add = []


def running_game(screen, snake_speed_clock, num):
    change_speed = 0  # 定义改变速度
    start_speed = 2  # 贪吃蛇的原始速度+2
    startx = random.randint(20, map_width - 20)  # 开始位置
    starty = random.randint(10, map_height - 10)
    snake_coords = [{'x': startx, 'y': starty},  # 初始贪吃蛇
                    {'x': startx - 1, 'y': starty},
                    {'x': startx - 2, 'y': starty}]
    direction = RIGHT  # 开始时向右移动
    food = get_random_location()  # 实物随机位置
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()  #退出游戏
            elif event.type == KEYDOWN:  # and 判断是否输入了反方向
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_SPACE:
                    pygame.mixer.music.pause()
                    pause(screen)
                    pygame.mixer.music.play()
                elif event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_1:  # 按“1”加速,一局加速不超过10
                    if change_speed < 10:
                        change_speed += 1
                elif event.key == K_2:  # 按“2”减速，减速次数不能超过加速5次
                    if change_speed > -5 and len(snake_coords) > 8:
                        change_speed -= 1
        move_snake(direction, snake_coords)  # 移动蛇
        ret = snake_is_alive(snake_coords)   #调用snake_is_alive方法判断蛇是否活着
        music = pygame.mixer.Sound("7896.wav")
        if not ret:
            music.play()
            pygame.mixer.music.stop()
            break  # 蛇跪了. 游戏结束
        snake_is_eat_food(snake_coords, food)  # 判断蛇是否吃到食物
        screen.fill(BG_COLOR)    # 上面定义了黑色为背景颜色，通过fill铺满背景颜色
        draw_grid(screen)      # 画出来背景中的网格
        draw_snake(screen, snake_coords)     # 画出蛇 和蛇的颜色
        draw_food(screen, food)    # 加载出蛇要吃的食物
        draw_score(screen, len(snake_coords) - 3)    #画成绩
        pygame.display.update()    # 刷新
        # 控制速度
        if len(snake_coords) < 40:    # 如果蛇的长度少于40
            snake_speed = change_speed + len(snake_coords) // 2 + start_speed   #每吃一个食物蛇的速度加2
            draw_speed(screen, change_speed + len(snake_coords) // 2 + start_speed)    #把蛇的速度花在游戏画面中
            pygame.display.update()    #每秒更新
        else:
            snake_speed = 10  # 长度到达40时，若一直按减速，则看到速度最小为10
            draw_speed(screen, 10)    #游戏画面中的速度停在10
            pygame.display.update()   #每秒更新
        snake_speed_clock.tick(snake_speed)   # 蛇存在的时间
    keep_rangking(len(snake_coords) - 4, num)   # 保存游戏结束之后玩家吃到了多少个食物
    show_gameover_info(screen, len(snake_coords) - 4, num)   # 游戏结束并且蛇的长度保存



# 将食物画出来
def draw_food(screen, food):   #定义两个参数，一个是场景，一个是食物
    x = food['x'] * cell_size
    y = food['y'] * cell_size
    fd = pygame.image.load(("icecream-09.jpg"))    # 加载食物图片
    food_style = pygame.Rect(x, y, cell_size, cell_size)  # 食物在游戏运行后显示大小个位置
    screen.blit(fd, food_style)     # 在场景中生成食物

    # fd = pygame.image.load(("h.jpg"))  # 加载食物图片
    # food_style = pygame.Rect(x, y, cell_size, cell_size)  # 食物在游戏运行后显示大小个位置
    # screen.blit(fd, food_style)  # 在场景中生成食物

    # fd = pygame.image.load(("sb0102.jpg"))  # 加载食物图片
    # food_style = pygame.Rect(x, y, cell_size, cell_size)  # 食物在游戏运行后显示大小个位置
    # screen.blit(fd, food_style)  # 在场景中生成食物


    # appleRect = pygame.Rect(x, y, cell_size, cell_size)
    # food_style = FOOD_color[random.randint(0, 2)]
    # pygame.draw.rect(screen, food_style[1], appleRect)


# 将贪吃蛇画出来
def draw_snake(screen, snake_coords):
    for coord in snake_coords:
        x = coord['x'] * cell_size
        y = coord['y'] * cell_size
        '''wormSegmentRect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(screen, dark_blue, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(  # 蛇身子里面的第二层亮绿色
            x + 4, y + 4, cell_size - 8, cell_size - 8)
        pygame.draw.rect(screen, blue, wormInnerSegmentRect)'''
        sk = pygame.image.load('sh01.jpg')
        wormSegmentRect = pygame.Rect(x, y, cell_size, cell_size)
        screen.blit(sk, wormSegmentRect)


# 画网格
def draw_grid(screen):
    for x in range(0, windows_width, cell_size):  # draw 水平 lines
        pygame.draw.line(screen, dark_gray, (x, 0), (x, windows_height))
    for y in range(0, windows_height, cell_size):  # draw 垂直 lines
        pygame.draw.line(screen, dark_gray, (0, y), (windows_width, y))


# 移动贪吃蛇
def move_snake(direction, snake_coords):
    if direction == UP:
        newHead = {'x': snake_coords[HEAD]['x'], 'y': snake_coords[HEAD]['y'] - 1}
    elif direction == DOWN:
        newHead = {'x': snake_coords[HEAD]['x'], 'y': snake_coords[HEAD]['y'] + 1}
    elif direction == LEFT:
        newHead = {'x': snake_coords[HEAD]['x'] - 1, 'y': snake_coords[HEAD]['y']}
    elif direction == RIGHT:
        newHead = {'x': snake_coords[HEAD]['x'] + 1, 'y': snake_coords[HEAD]['y']}
    snake_coords.insert(0, newHead)


# 判断蛇死了没
def snake_is_alive(snake_coords):
    tag = True
    if snake_coords[HEAD]['x'] == -1 or snake_coords[HEAD]['x'] == map_width or snake_coords[HEAD]['y'] == -1 or snake_coords[HEAD]['y'] == map_height: #判断蛇是否碰壁
        tag = False
        # 蛇碰壁啦
    for snake_body in snake_coords[1:]:  # 遍历蛇身体部分
        if snake_body['x'] == snake_coords[HEAD]['x'] and snake_body['y'] == snake_coords[HEAD]['y']:
            tag = False  # 蛇碰到自己身体啦
    return tag


# 判断贪吃蛇是否吃到食物
def snake_is_eat_food(snake_coords, food):  # 如果是列表或字典，那么函数内修改参数内容，就会影响到函数体外的对象。
    if snake_coords[HEAD]['x'] == food['x'] and snake_coords[HEAD]['y'] == food['y']:
        food['x'] = random.randint(0, map_width - 1)
        food['y'] = random.randint(0, map_height - 1)  # 食物位置重新设置
    else:
        del snake_coords[-1]  # 如果没有吃到实物, 就向前移动, 那么尾部一格删掉


# 食物随机生成
def get_random_location():
    return {'x': random.randint(0, map_width - 1), 'y': random.randint(0, map_height - 1)}

# 开始信息显示
def show_start_info(screen):
    font = pygame.font.Font('myfont.ttf', 40)
    tip = font.render('按任意键开始游戏', True, (255, 0, 0))
    tip1 = font.render('author:bzx', True, white)
    gamestart = pygame.image.load('start.png').convert()  # 图
    # 片自适应设置
    screen.blit(tip1, (550, 750))
    screen.blit(gamestart, (0, 0))
    screen.blit(tip, (325, 270))
    pygame.display.update()
    while True:  # 键盘监听事件
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()  # 终止程序
            elif event.type == KEYDOWN:
                if (event.key == K_ESCAPE):  # 终止程序
                    terminate()  # 终止程序
                elif event.key == K_SPACE:
                    pause = True
                    pygame.quit()
                    quit()
                else:
                    return  # 结束此函数, 开始游戏


# 游戏结束信息显示
def show_gameover_info(screen, score, num):
    font = pygame.font.Font('myfont.ttf', 40)
    tip = font.render('ESC退出游戏, 按任意键重新开始游戏~', True, (255, 255, 0))
    # 创建一个和串窗口一样大小的图片
    start = pygame.image.load('over.png')
    # 设定显示的背景图和位置
    screen.blit(start, (0, 40))
    screen.blit(tip, (60, 100))
    pygame.display.update()
    while True:  # 键盘监听事件
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()  # 终止程序
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # 终止程序
                    terminate()  # 终止程序
                elif event.key == K_3:  # 按“3”加速,排行榜
                    show_ranking(screen, score, num)
                    pygame.display.update()
                else:
                    return  # 结束此函数, 重新开始游戏


# 画成绩
def draw_score(screen, score):
    font = pygame.font.Font('myfont.ttf', 30)
    scoreSurf = font.render('得分: %s' % score, True, Green)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (windows_width - 120, 10)
    screen.blit(scoreSurf, scoreRect)


# 画速度
def draw_speed(screen, speed):
    font = pygame.font.Font('myfont.ttf', 30)
    speedSurf = font.render('速度: %s' % speed, True, Green)
    speedRect = speedSurf.get_rect()
    speedRect.topleft = (windows_width - 800, 10)
    screen.blit(speedSurf, speedRect)


score_list = {}


# 保存排名
def keep_rangking(score, num):
    score_list['次数'] = num
    score_list['分数'] = score
    global score_add
    score_add.append(score_list)
    print(score_add[num - 1])


# 显示本局游戏信息
def show_ranking(screen, score, num):
    for i in range(num):
        font = pygame.font.Font('myfont.ttf', 30)
        # scoreSurf = font.render('第{: ^}次得分为: {: ^10}'.format(num,score), True, Green)
        scoreSurf = font.render('%s' % (score_add[num - 1]), True, Green)
        scoreRect = scoreSurf.get_rect()
        rang = pygame.image.load('rangking.jpg')
        screen.blit(rang, (0, 0))
        scoreRect.topleft = (windows_width - 520, 100)
        screen.blit(scoreSurf, scoreRect)


# 程序暂停
def pause(screen):
    '''
    start = pygame.image.load('start.png')
    screen.blit(start,(290, 150))
    pygame.display.update()
    '''
    font = pygame.font.Font('myfont.ttf', 40)
    tem = font.render('游戏暂停, 按“空格”键重新开始游戏~', True, (255, 255, 0))
    screen.blit(tem, (150, 260))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    return

# 程序终止
def terminate():
    pygame.quit()
    sys.exit()


# 主函数
def main():
    pygame.init()  # 模块初始化
    pygame.mixer.init()  #音乐模块初始化
    snake_speed_clock = pygame.time.Clock()  # 创建Pygame时钟对象
    screen = pygame.display.set_mode((windows_width, windows_height), 0, 32)  #
    screen.fill(white)
    pygame.display.set_caption("贪吃蛇大作战")  # 设置标题
    show_start_info(screen)  # 欢迎信息


    num = 0
    while True:
        pygame.mixer.music.load("7895.wav")
        pygame.mixer.music.play()
        num += 1
        running_game(screen, snake_speed_clock, num)


# show_gameover_info(screen, len(snake_coords) - 3, num)

if __name__ == '__main__':
    main()

