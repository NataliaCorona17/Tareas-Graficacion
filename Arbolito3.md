```python
import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt, gluNewQuadric, gluCylinder, gluSphere
import sys

# Variables globales para la cámara
camera_pos = [4.0, 3.0, 8.0]  # Posición de la cámara
camera_target = [0.0, 1.0, 0.0]  # Punto al que mira
camera_up = [0.0, 1.0, 0.0]  # Vector hacia arriba

# Variables para el movimiento
camera_speed = 0.02  # Velocidad de movimiento
keys = {}  # Diccionario para controlar el estado de las teclas


def init():
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)  # Campo de visión más amplio
    glMatrixMode(GL_MODELVIEW)


def draw_trunk():
    glPushMatrix()
    glColor3f(0.6, 0.3, 0.1)  # Marrón para el tronco
    glTranslatef(0.0, 0.0, 0.0)  # Posicionar el tronco
    glRotatef(-90, 1, 0, 0)  # Rota para orientar el cilindro verticalmente
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.3, 0.3, 2.0, 32, 32)  # Radio y altura del cilindro
    glPopMatrix()


def draw_foliage():
    glColor3f(0.3, 0.6, 0.3)  # Verde para las hojas
    quadric = gluNewQuadric()

    # Posiciones relativas de las esferas (follaje agrupado)
    offsets = [
        (0.0, 2.0, 0.0),
        (0.6, 2.3, 0.0),
        (-0.6, 2.3, 0.0),
        (0.3, 2.0, 0.6),
        (-0.3, 2.0, -0.6),
        (0.0, 2.6, 0.3),
        (0.0, 2.6, -0.3),
        (0.4, 2.5, 0.4),
        (-0.4, 2.5, -0.4)
    ]

    for offset in offsets:
        glPushMatrix()
        glTranslatef(offset[0], offset[1], offset[2])
        gluSphere(quadric, 0.7, 32, 32)
        glPopMatrix()


def draw_apples():
    glColor3f(1.0, 0.0, 0.0)  # Rojo brillante
    quadric = gluNewQuadric()

    apple_positions = [
        (0.6, 2.4, 0.0),
        (-0.6, 2.3, -0.4),
        (0.0, 2.5, 0.6),
        (0.4, 2.2, -0.5),
        (-0.4, 2.2, 0.5),
        (0.0, 1.8, -0.6)
    ]

    for pos in apple_positions:
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        gluSphere(quadric, 0.3, 16, 16)  # Esferas más grandes
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

    # Cámara
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
              camera_target[0], camera_target[1], camera_target[2],
              camera_up[0], camera_up[1], camera_up[2])

    draw_ground()
    draw_trunk()
    draw_foliage()
    draw_apples()  #Aquí añadimos las manzanas

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

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()

    # Crear ventana
    width, height = 800, 600
    window = glfw.create_window(width, height, "Árbol con Manzanas", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Configurar callback de teclado
    glfw.set_key_callback(window, key_callback)

    # Bucle principal
    while not glfw.window_should_close(window):
        process_input()
        draw_scene()
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
 
 ```