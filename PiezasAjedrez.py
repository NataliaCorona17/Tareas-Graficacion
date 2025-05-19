import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
from math import cos, sin

camera_pos = [4.0, 3.0, 8.0]
camera_target = [0.0, 1.0, 0.0]
camera_up = [0.0, 1.0, 0.0]

camera_speed = 0.02
keys = {}

def init():
    glClearColor(0.5, 0.8, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def draw_pawn():
    glPushMatrix()
    glColor3f(0.0, 0.3, 0.8)
    glTranslatef(0.0, 0.0, 0.0)
    glRotatef(-90, 1, 0, 0)  # Rotar para alinear con eje Y

    quad = gluNewQuadric()

    # Base
    gluCylinder(quad, 0.4, 0.4, 0.2, 32, 32)
    gluDisk(quad, 0.0, 0.4, 32, 1)  # Tapar parte de abajo de la base
    glTranslatef(0.0, 0.0, 0.2)
    gluDisk(quad, 0.0, 0.4, 32, 1)  # Tapar parte de arriba de la base

    # Cuerpo
    gluCylinder(quad, 0.3, 0.3, 0.8, 32, 32)
    glTranslatef(0.0, 0.0, 0.8)
    gluDisk(quad, 0.0, 0.3, 32, 1)  # Tapar parte de arriba del cuerpo

    # Cabeza
    gluSphere(quad, 0.4, 32, 32)

    glPopMatrix()

def draw_king():
    glPushMatrix()
    glColor3f(0.0, 0.3, 0.8)
    glTranslatef(1.0, 0.0, 0.0)  # Mover el rey a la derecha del peón
    glRotatef(-90, 1, 0, 0)  # Rotar para alinear con eje Y

    quad = gluNewQuadric()

    # Base del rey
    gluCylinder(quad, 0.4, 0.4, 0.2, 32, 32)
    gluDisk(quad, 0.0, 0.4, 32, 1)
    glTranslatef(0.0, 0.0, 0.2)
    gluDisk(quad, 0.0, 0.4, 32, 1)

    # Cuerpo
    gluCylinder(quad, 0.3, 0.3, 1.0, 32, 32)
    glTranslatef(0.0, 0.0, 1.0)
    gluDisk(quad, 0.0, 0.3, 32, 1)
    # Cabeza
    gluSphere(quad, 0.4, 32, 32)
    # Corona (esferas pequeñas alrededor de la cabeza)
    glPushMatrix()
    for i in range(8):
        angle = i * (360 / 8)
        radians = angle * (3.14159 / 180)
        x = 0.4 * cos(radians)
        y = 0.2 * sin(radians)
        glPushMatrix()
        glTranslatef(x, y, 0.25)
        gluSphere(quad, 0.1, 16, 16)
        glPopMatrix()
    glPopMatrix()

    glPopMatrix()

def draw_ground():
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.5, 0.2)
    glVertex3f(-10, 0, 10)
    glVertex3f(10, 0, 10)
    glVertex3f(10, 0, -10)
    glVertex3f(-10, 0, -10)
    glEnd()

def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
              camera_target[0], camera_target[1], camera_target[2],
              camera_up[0], camera_up[1], camera_up[2])

    draw_ground()
    draw_pawn()
    draw_king()

    

    glfw.swap_buffers(window)

def process_input():
    global camera_pos
    if keys.get(glfw.KEY_W, False):
        camera_pos[2] -= camera_speed
    if keys.get(glfw.KEY_S, False):
        camera_pos[2] += camera_speed
    if keys.get(glfw.KEY_A, False):
        camera_pos[0] -= camera_speed
    if keys.get(glfw.KEY_D, False):
        camera_pos[0] += camera_speed
    if keys.get(glfw.KEY_UP, False):
        camera_pos[1] += camera_speed
    if keys.get(glfw.KEY_DOWN, False):
        camera_pos[1] -= camera_speed

def key_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False

def main():
    global window
    if not glfw.init():
        sys.exit()
    width, height = 800, 600
    window = glfw.create_window(width, height, "Peón de ajedrez en OpenGL", None, None)
    if not window:
        glfw.terminate()
        sys.exit()
    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        process_input()
        draw_scene()
        glfw.poll_events()
    glfw.terminate()

if __name__ == "__main__":
    main()
