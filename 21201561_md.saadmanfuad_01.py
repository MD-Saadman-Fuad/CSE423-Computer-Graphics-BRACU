#Two Tasks are given in the same py file


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

#task 1


# class Raindrop:
#     def __init__(self, x, y, speed):
#         self.x = x
#         self.y = y
#         self.speed = speed
#
# rain_direction = 0
# day = False
#
# raindrops = []
# for i in range(100):
#     x = random.uniform(500, 0)
#     y = random.uniform(0, 500)
#     speed = random.uniform(2, 6)
#     raindrops.append(Raindrop(x, y, speed))
#
# def update_raindrop_position():
#     for i in raindrops:
#         i.x += rain_direction
#         i.y -= i.speed
#         if(i.y < 0):
#             i.y = random.uniform(0, 500)
#             i.x = random.uniform(0, 500)
#
# def rerender(i):
#     glutPostRedisplay()
#     glutTimerFunc(16, rerender, 0)
#
# def draw_points(x, y, s):
#     glPointSize(s) #pixel size. by default 1 thake
#     glBegin(GL_POINTS)
#     glVertex2f(x,y) #jekhane show korbe pixel
#     glEnd()
# def draw_line(x1, y1, x2, y2):
#     glPointSize(100)
#     glLineWidth(4)
#     glBegin(GL_LINES)
#     glVertex2f(x1, y1)
#     glVertex2f(x2, y2)
#     glEnd()
#
# def draw_square(x1, y1, x2, y2, x3, y3, x4, y4):
#     glPointSize(5)
#     glLineWidth(10)
#     glBegin(GL_QUADS)
#     glVertex2f(x1, y1)
#     glVertex2f(x2, y2)
#     glVertex2f(x3, y3)
#     glVertex2f(x4, y4)
#     glEnd()
#
#
# def iterate():
#     glViewport(0, 0, 500, 500)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
#     glMatrixMode (GL_MODELVIEW)
#     glLoadIdentity()
#
# def specialKeyListener(key, x, y):
#     global rain_direction
#
#     if(key == GLUT_KEY_RIGHT):
#         rain_direction += 1
#
#     if(key == GLUT_KEY_LEFT):
#         rain_direction -= 1
#
# def keyboardListener(key, x, y):
#     global day
#     if(key == b"d"):
#         day = True
#
#     if(key == b"n"):
#         day = False
#
# def showScreen():
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glLoadIdentity()
#     iterate()
#
#     if(day == True):
#         glClearColor(1, 1, 1, 1)
#         glColor3f(0, 0, 0)
#     else:
#         glClearColor(0, 0, 0, 1)
#         glColor3f(1, 1, 1)
#
#     #Drawing the house
#     draw_line(100, 250, 250, 400) #/
#     draw_line(250, 400, 400, 250) #\
#     draw_line(100, 250, 400, 250) #-
#     # draw_line(110, 250, 390, 250)
#     draw_points(265, 100, 5)
#     draw_line(110, 50, 390, 50) #_
#     draw_line(110, 250, 110, 50) #h_l
#     draw_line(390, 250, 390, 50) #h_r
#     draw_line(225, 150, 225, 50) #d_l
#     draw_line(223, 150, 276, 150) #d_u
#     draw_line(275, 150, 275, 50) #d_r
#     # draw_square(130, 200, 130, 150, 180, 150, 180, 200)
#     # draw_line(350, 200, 350, 150)
#     # draw_square(320, 200, 320, 150, 370, 150, 370, 200)
#
#     # draw_line(320, 200, 370, 150)
#     draw_line(320, 200, 320, 150) #l
#     draw_line(370, 150, 370, 200) #r
#     draw_line(320, 175, 370, 175) #-
#     draw_line(320, 200, 370, 200) #u
#     draw_line(370, 150, 320, 150) #d
#     draw_line(345, 200, 345, 150) #|
#
#
#     update_raindrop_position()
#
#     for i in raindrops:
#         if(day == True):
#             glColor3f(0, 0, 1.0)
#         else:
#             glColor3f(1, 1, 1)
#         draw_line(i.x, i.y, i.x, i.y + 20)
#     glutSwapBuffers()
#
# glutInit()
# glutTimerFunc(0, rerender, 0)
# glutInitDisplayMode(GLUT_RGBA)
# glutInitWindowSize(500, 500)
# glutInitWindowPosition(0, 0)
# wind = glutCreateWindow(b"Task 1")
# glutDisplayFunc(showScreen)
# glutSpecialFunc(specialKeyListener)
# glutKeyboardFunc(keyboardListener)
#
# glutMainLoop()

#task 2

points = []
speed = 1
play = True
blink = False

def mouseListener(button, state, x, y):
    global blink
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        color = [random.random(), random.random(), random.random(), 1]
        direction = random.choice([(1, 1), (-1, 1), (1, -1), (-1, -1)])
        point = [x, 500-y, direction[0], direction[1], color]
        points.append(point)
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if blink:
            blink = False
        else:
            blink = True

def keyboardListener(key, x, y):
    global speed, play
    if key == b' ':
        if play:
            play = False
        else:
            play = True
    elif key == GLUT_KEY_UP:
        speed += 1
    elif key == GLUT_KEY_DOWN:
        if speed > 1:
            speed -= 1
        else:
            speed = 1

def draw_points(x, y, size, color):
    glColor4f(color[0], color[1], color[2], color[3])
    glPointSize(size)
    glEnable(GL_POINT_SMOOTH)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glLoadIdentity()
    iterate()

    for p in points:
        draw_points(p[0], p[1], 10, p[4])
    glutSwapBuffers()

def animate(balls):
    if play:
        for p in points:
            p[0] += p[2]*speed
            p[1] += p[3]*speed
            if blink:
                p[4][3] = (p[4][3]+0.1)%1
            if p[0] > 500 or p[0] < 0:
                p[2] *= -1
            if p[1] > 500 or p[1] < 0:
                p[3] *= -1

    glutTimerFunc(30, animate, "balls")
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Task 2") #window name
glutDisplayFunc(showScreen)
glutIdleFunc(animate("balls"))
glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(keyboardListener)
glutMainLoop()
