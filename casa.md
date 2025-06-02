```python
import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
import sys

def init():
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Cielo azul claro
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40, 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def draw_cube():
    """Base de la casa (morado)"""
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.6, 1.0)  # Morado

    # Frente
    glVertex3f(-1, 0, 1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)

    # Atrás
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)

    # Izquierda
    glVertex3f(-1, 0, -1)
    glVertex3f(-1, 0, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 1, -1)

    # Derecha
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, 1, -1)

    # Arriba
    glColor3f(0.7, 0.5, 1.0)
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)

    # Abajo (suelo de la casa)
    glColor3f(0.5, 0.4, 0.7)
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(-1, 0, 1)
    glEnd()

def draw_roof():
    """Techo (azul)"""
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.0, 0.4)  # Azul

    # Frente
    glVertex3f(-1, 1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(0, 2, 0)

    # Atrás
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(0, 2, 0)

    # Izquierda
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, 1)
    glVertex3f(0, 2, 0)

    # Derecha
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(0, 2, 0)
    glEnd()

def draw_ground():
    """Pasto verde"""
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.6, 0.0)  # Verde pasto
    glVertex3f(-10, 0, 10)
    glVertex3f(10, 0, 10)
    glVertex3f(10, 0, -10)
    glVertex3f(-10, 0, -10)
    glEnd()

def draw_door():
    """Puerta"""
    glBegin(GL_QUADS)
    glColor3f(0.4, 0.2, 0.0)  # Madera

    glVertex3f(-0.3, 0, 1.01)
    glVertex3f(0.3, 0, 1.01)
    glVertex3f(0.3, 0.6, 1.01)
    glVertex3f(-0.3, 0.6, 1.01)
    glEnd()

def draw_house():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(4, 3, 8, 0, 1, 0, 0, 1, 0)

    draw_ground()
    draw_cube()
    draw_roof()
    draw_door()

    glfw.swap_buffers(window)

def main():
    global window
    if not glfw.init():
        sys.exit()

    width, height = 800, 600
    window = glfw.create_window(width, height, "Casa 3D Personalizada", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    while not glfw.window_should_close(window):
        draw_house()
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()

```