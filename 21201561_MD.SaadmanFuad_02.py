from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import sys


width = 800
height = 600
rocket_width = 25
rocket_height = 35
bullet_radius = 5
radius = 20
max_miss = 3


shooter_pos = 0
bullets = []  # List of bullets: {'x': , 'y': }
falling_circles = []  # List of circles: {'x': , 'y': , 'radius': , 'expanding': True/False, 'color': [r, g, b, a]}
score = 0
missed = 0
game_over = False
play = True
blink = False
misfires = 0

last_frame_time = time.time()

# restart Pause-play exit button set
BUTTON_SIZE = 50
buttons = {
    'restart': {'x': -340, 'y': 260, 'width': 40, 'height': 40,'color': [0.0, 0.0, 1.0, 1.0]},
    'play_pause': {'x': 0, 'y': 260, 'width': 40, 'height': 40, 'color': [0, 1.0, 0.0, 1.0]},
    'exit': {'x': 360, 'y': 260, 'width': 40, 'height': 40,'color': [1.0, 0.0, 0.0, 1.0]}
}


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glPointSize(2.0)
    glEnable(GL_POINT_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-400, 400, -300, 300)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def midpoint_circle(x_center, y_center, radius, color):
    glColor4f(*color)
    glBegin(GL_POINTS)
    x = 0
    y = radius
    d = 1 - radius
    plot_circle_points(x_center, y_center, x, y)
    while x < y:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
        plot_circle_points(x_center, y_center, x, y)
    glEnd()


def plot_circle_points(xc, yc, x, y):
    glVertex2f(xc + x, yc + y)
    glVertex2f(xc - x, yc + y)
    glVertex2f(xc + x, yc - y)
    glVertex2f(xc - x, yc - y)
    glVertex2f(xc + y, yc + x)
    glVertex2f(xc - y, yc + x)
    glVertex2f(xc + y, yc - x)
    glVertex2f(xc - y, yc - x)


def midpoint_line(x1, y1, x2, y2, color):
    glColor4f(*color)
    glBegin(GL_POINTS)
    dx = x2 - x1
    dy = y2 - y1
    steep = abs(dy) > abs(dx)
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
        dx, dy = x2 - x1, y2 - y1
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    dx = x2 - x1
    dy = y2 - y1
    derror = abs(dy) * 2
    error = 0
    y = y1
    ystep = 1 if y2 > y1 else -1
    for x in range(x1, x2 + 1):
        if steep:
            glVertex2f(y, x)
        else:
            glVertex2f(x, y)
        error += derror
        if error > dx:
            y += ystep
            error -= 2 * dx
    glEnd()


def draw_shooter():
    global shooter_pos
    glColor4f(1.0, 0.5, 0.0, 1.0)
    x = shooter_pos
    y = -600 // 2 + 20

    midpoint_line(x - 25, y, x + 25, y, [1.0, 0.5, 0.0, 1.0])  # Bottom
    midpoint_line(x - 15, y, x - 15, y + 25, [1.0, 0.5, 0.0, 1.0])  # l|
    midpoint_line(x + 15, y, x + 15, y + 25, [1.0, 0.5, 0.0, 1.0])  # r|
    midpoint_line(x + 15, y + 25, x, y + 35, [1.0, 0.5, 0.0, 1.0])  # \
    midpoint_line(x - 15, y + 25, x, y + 35, [1.0, 0.5, 0.0, 1.0])  # /
    midpoint_line(x + 15, y + 25, x - 15, y + 25, [1.0, 0.5, 0.0, 1.0])  # -
    midpoint_line(x - 25, y, x - 15, y + 10, [1.0, 0.5, 0.0, 1.0])  # fin
    midpoint_line(x + 25, y, x + 15, y + 10, [1.0, 0.5, 0.0, 1.0])  # fin


def draw_bullets():
    for bullet in bullets:
        midpoint_circle(bullet['x'], bullet['y'], bullet_radius, [1.0, 1.0, 0.0, 1.0])


def draw_falling_circles():
    for circle in falling_circles:

        if circle.get('expanding', False):

            if 'radius_direction' not in circle:
                circle['radius_direction'] = 1  # 1 for expanding, -1 for shrinking
            circle['radius'] += circle['radius_direction'] * 20 * delta_time
            if circle['radius'] >= radius + 10:
                circle['radius_direction'] = -1
            elif circle['radius'] <= radius - 10:
                circle['radius_direction'] = 1
        midpoint_circle(circle['x'], circle['y'], circle['radius'], circle['color'])


def draw_buttons():
    for name, btn in buttons.items():
        midpoint_circle(btn['x'], btn['y'], btn['width'] // 2, btn['color'])

        if name == 'restart':
            x, y = btn['x'], btn['y']
            midpoint_line(x + 10, y, x - 10, y, [0.0, 0.0, 1.0, 1.0])
            midpoint_line(x - 10, y, x , y + 5, [0.0, 0.0, 1.0, 1.0])
            midpoint_line(x - 10, y, x, y - 5, [0.0, 0.0, 1.0, 1.0])
        elif name == 'play_pause':
            if play:
                x, y = btn['x'], btn['y']
                midpoint_line(x - 10, y + 10, x - 10, y - 10, [1.0, 1.0, 1.0, 1.0])
                midpoint_line(x + 10, y - 10, x + 10, y + 10, [1.0, 1.0, 1.0, 1.0])
            else:
                x, y = btn['x'], btn['y']
                midpoint_line(x + 10, y - 10, x - 10, y, [1.0, 1.0, 1.0, 1.0])
                midpoint_line(x - 10, y, x + 10, y + 10, [1.0, 1.0, 1.0, 1.0])
                midpoint_line(x + 10, y - 10, x + 10, y + 10, [1.0, 1.0, 1.0, 1.0])
        elif name == 'exit':
            x, y = btn['x'], btn['y']
            midpoint_line(x - 10, y - 10, x + 10, y + 10, [1.0, 1.0, 1.0, 1.0])
            midpoint_line(x + 10, y - 10, x - 10, y + 10, [1.0, 1.0, 1.0, 1.0])


def render_scene():
    global game_over, score
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    if game_over:
        print(f"Game Over! Final Score: {score}")

        glutLeaveMainLoop()
        return

    draw_buttons()
    draw_shooter()
    draw_bullets()
    draw_falling_circles()

    print(f"Score: {score} | Missed: {missed} | Misfires: {misfires}")

    glutSwapBuffers()


def update():
    global bullets, falling_circles, score, missed, game_over, last_frame_time, delta_time, misfires

    current_time = time.time()
    delta_time = current_time - last_frame_time
    last_frame_time = current_time

    if play and not game_over:

        new_bullets = []
        for bullet in bullets:
            bullet['y'] += 300 * delta_time
            if bullet['y'] < height // 2:
                new_bullets.append(bullet)
            if bullet['y'] >= height // 2:
                misfires += 1
                if misfires >= 3:
                    game_over = True
                    print(f"Score: {score} | Missed: {missed} | Misfires: {misfires}")
                    print("Game Over due to excessive misfires!")

        bullets = new_bullets

        # Update falling circles
        new_falling_circles = []
        for circle in falling_circles:
            circle['y'] -= 60 * delta_time

            if circle.get('expanding', False):
                pass
            if circle['y'] < -height // 2:
                missed += 1
                if missed >= max_miss:
                    game_over = True
            else:
                new_falling_circles.append(circle)
        falling_circles = new_falling_circles

        # Collision detection
        to_remove_bullets = []
        to_remove_circles = []
        for bullet in bullets:
            proj_x, proj_y = bullet['x'], bullet['y']
            for circle in falling_circles:
                circ_x, circ_y = circle['x'], circle['y']
                distance_sq = (proj_x - circ_x) ** 2 + (proj_y - circ_y) ** 2
                if (distance_sq <= (bullet_radius + circle['radius']) ** 2):
                    if circle['expanding'] == True:
                        score += 5
                        to_remove_bullets.append(bullet)
                        to_remove_circles.append(circle)
                        break
                    else:
                        score += 1
                        to_remove_bullets.append(bullet)
                        to_remove_circles.append(circle)
                        break


        # Remove collided bullets and circles
        bullets = [p for p in bullets if p not in to_remove_bullets]
        falling_circles = [c for c in falling_circles if c not in to_remove_circles]

        # Check if any circle hits the shooter
        shooter_y = -height // 2 + rocket_height
        shooter_left = shooter_pos - rocket_width // 2
        shooter_right = shooter_pos + rocket_width // 2
        for circle in falling_circles:
            if (circle['y'] - circle['radius'] <= shooter_y + rocket_height):
                if shooter_left - circle['radius'] <= circle['x'] <= shooter_right + circle['radius']:
                    game_over = True
                    print(f"Score: {score} | Missed: {missed} | Misfires: {misfires}")
                    print("Rocket Crashed!")
                    break

        # creating new circles
        if random.random() < 0.0005:  # rate of circle
            x_pos = random.randint(-width // 2 + radius, width // 2 - radius)
            y_pos = height // 2 - radius
            is_unique = random.random() < 0.1  # rate of unique circle
            color = [random.random(), random.random(), random.random(), 1.0]
            circle = {'x': x_pos, 'y': y_pos, 'radius': radius, 'color': color, 'expanding' : False}
            if is_unique:
                circle['expanding'] = True
            falling_circles.append(circle)
    glutPostRedisplay()



def handle_keys(key, x, y):
    global shooter_pos, bullets, play, game_over, score, missed, misfires

    if key == b'a':
        shooter_pos -= 20
        if shooter_pos - rocket_width // 2 < -width // 2:
            shooter_pos = -width // 2 + rocket_width // 2
    elif key == b'd':
        shooter_pos += 20
        if shooter_pos + rocket_width // 2 > width // 2:
            shooter_pos = width // 2 - rocket_width // 2
    elif key == b' ':
        if not game_over:
            bullet = {'x': shooter_pos, 'y': -height // 2 + rocket_height + bullet_radius}
            bullets.append(bullet)






def handle_mouse(button, state, x, y):
    global blink, play, game_over, score, missed
    if state != GLUT_DOWN:
        return
    ogl_x = x - width // 2
    ogl_y = (height // 2 - y)

    if button == GLUT_LEFT_BUTTON:
        for name, btn in buttons.items():
            if (ogl_x >= btn['x'] - btn['width'] // 2 and ogl_x <= btn['x'] + btn['width'] // 2) and \
                    (ogl_y >= btn['y'] - btn['height'] // 2 and ogl_y <= btn['y'] + btn['height'] // 2):
                if name == 'restart':
                    restart_game()
                elif name == 'play_pause':
                    play = not play
                elif name == 'exit':

                    glutLeaveMainLoop()
                    print(f"Goodbye! Final Score: {score}")
                    return
                break



def animate(ball):
    if play:
        for p in points[:]:
            p[0] += p[2] * speed
            p[1] += p[3] * speed
            if blink:
                p[4][3] = (p[4][3] + 0.1) % 1
            if p[0] > 500 or p[0] < 0:
                p[2] *= -1
            if p[1] > 500 or p[1] < 0:
                p[3] *= -1

        if len(points) > 10:
            points.pop(0)

    glutTimerFunc(50, animate, "ball")
    glutPostRedisplay()


def restart_game():
    global bullets, falling_circles, score, missed, game_over, shooter_pos, misfires
    bullets = []
    falling_circles = []
    score = 0
    missed = 0
    misfires = 0
    game_over = False
    shooter_pos = 0
    print("Starting Over")


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    window = glutCreateWindow(b"Shoot The Circles!")

    init()

    glutDisplayFunc(render_scene)
    glutIdleFunc(update)
    glutKeyboardFunc(handle_keys)
    glutMouseFunc(handle_mouse)

    glutMainLoop()


if __name__ == "__main__":
    main()
