```python
import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt, gluNewQuadric, gluCylinder, gluDisk, gluSphere
import sys
import math
import cv2
import mediapipe as mp

# === Variables globales ===
camera_pos = [4.0, 3.0, 8.0]
camera_target = [0.0, 1.0, 0.0]
camera_up = [0.0, 1.0, 0.0]

camera_speed = 0.03
prev_hand_x, prev_hand_y = None, None
prev_zoom_distance = None

# Movimiento del hongo
t = 0.0
jump_amplitude = 1.3
base_height = 3.6

def init():
    glClearColor(0.5, 0.8, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    light_position = [10.0, 10.0, 10.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

def draw_ground():
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.5, 0.2)
    glVertex3f(-10, 0, 10)
    glVertex3f(10, 0, 10)
    glVertex3f(10, 0, -10)
    glVertex3f(-10, 0, -10)
    glEnd()

def draw_grass():
    glColor3f(0.5, 0.9, 0.5)
    blade_height = 0.25
    num_blades = 120

    glBegin(GL_LINES)
    for i in range(num_blades):
        x = (i % 12) - 6 + (i * 0.05)
        z = (i // 12) - 5 + (i * 0.04)
        glVertex3f(x, 0.0, z)
        glVertex3f(x, blade_height, z)
    glEnd()

def draw_pipe():
    quadric = gluNewQuadric()
    glPushMatrix()
    glColor3f(0.1, 0.63, 0.2)
    glTranslatef(0.0, 0.0, 0.0)
    glRotatef(-90, 1, 0, 0)
    base_radius = 1.0
    base_height_local = base_radius * 3.0
    top_height = 0.6
    gluDisk(quadric, 0.0, base_radius, 32, 1)
    gluCylinder(quadric, base_radius, base_radius, base_height_local, 32, 32)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.1, 0.63, 0.2)
    glTranslatef(0.0, base_height_local, 0.0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quadric, 1.3, 1.3, top_height, 32, 32)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.0, 0.0, 0.0)
    glTranslatef(0.0, base_height_local, 0.0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quadric, 1.0, 1.0, top_height, 32, 32)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.1, 0.63, 0.2)
    glTranslatef(0.0, base_height_local + top_height, 0.0)
    glRotatef(-90, 1, 0, 0)
    gluDisk(quadric, 1.0, 1.3, 32, 1)
    glPopMatrix()

def draw_mushroom(moving=True, pos_x=0.0, pos_y=None, pos_z=0.0):
    global t
    quadric = gluNewQuadric()
    if moving:
        y_position = base_height + math.sin(t) * jump_amplitude
    else:
        y_position = pos_y if pos_y is not None else 0.0

    glPushMatrix()
    glTranslatef(pos_x, y_position, pos_z)

    # Tallo
    glColor3f(0.96, 0.87, 0.7)
    radius = 0.4
    height = 0.8
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    gluDisk(quadric, 0.0, radius, 32, 1)
    gluCylinder(quadric, radius, radius, height, 32, 32)
    glTranslatef(0.0, 0.0, height)

    # Sombrero
    glRotatef(90, 1, 0, 0)
    glTranslatef(0.0, 0.0, -radius * 0.3)
    glColor3f(1.0, 0.0, 0.0)
    cap_radius = radius * 1.5
    gluSphere(quadric, cap_radius, 32, 32)

    # Mancha superior
    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)
    glTranslatef(0.0, cap_radius * 0.95, 0.0)
    gluSphere(quadric, radius * 0.3, 16, 16)
    glPopMatrix()

    for i in range(5):
        angle = (2 * 3.14159 / 5) * i
        x = cap_radius * 0.7 * math.cos(angle)
        z = cap_radius * 0.7 * math.sin(angle)
        y = cap_radius * 0.5
        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)
        glTranslatef(x, y, z)
        gluSphere(quadric, radius * 0.4, 16, 16)
        glPopMatrix()

    if moving:
        # Ojos
        eye_radius = radius * 0.15
        eye_y = cap_radius * -0.9
        eye_z = cap_radius * 0.9

        glPushMatrix()
        glColor3f(0.0, 0.0, 0.0)
        glTranslatef(-eye_radius * 2, eye_y, eye_z)
        gluSphere(quadric, eye_radius, 16, 16)
        glPopMatrix()

        glPushMatrix()
        glColor3f(0.0, 0.0, 0.0)
        glTranslatef(eye_radius * 2, eye_y, eye_z)
        gluSphere(quadric, eye_radius, 16, 16)
        glPopMatrix()

    glPopMatrix()
    glPopMatrix()

def update_jump():
    global t
    t += 0.3

def draw_cloud(x, y, z):
    quadric = gluNewQuadric()
    glColor3f(1.0, 1.0, 1.0)

    # Cuerpo de la nube: varias esferas
    offsets = [(-0.6, 0.0, 0.0), (0.0, 0.2, 0.0), (0.6, 0.0, 0.0)]
    radii =   [0.5,             0.7,             0.5]  # Tamaño de cada esfera

    for (dx, dy, dz), radius in zip(offsets, radii):
        glPushMatrix()
        glTranslatef(x + dx, y + dy, z + dz)
        gluSphere(quadric, radius, 16, 16)
        glPopMatrix()


def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
              camera_target[0], camera_target[1], camera_target[2],
              camera_up[0], camera_up[1], camera_up[2])
    
    draw_ground()
    draw_grass()

        # Nubes en el cielo
    draw_cloud(-3.0, 6.0, -4.0)
    draw_cloud(2.0, 6.5, -3.0)
    draw_cloud(4.0, 5.8, 3.0)
    draw_cloud(-5, 7, -5)
    draw_cloud(3, 6.5, -4)
    draw_cloud(-3, 6.8, 4)
    draw_cloud(4.5, 7.2, 3)
    draw_cloud(0, 7.5, 0)


    draw_pipe()
    
    # Hongo que salta (con cara)
    draw_mushroom(moving=True, pos_x=0.0, pos_y=None, pos_z=0.0)

    # Hongos estáticos (sin cara)
    draw_mushroom(moving=False, pos_x=-2.0, pos_y=0.8, pos_z=2.0)     # Original
    draw_mushroom(moving=False, pos_x=3.0,  pos_y=0.8, pos_z=-1.5)    # Extra 1
    draw_mushroom(moving=False, pos_x=-4.0, pos_y=0.8, pos_z=-3.0)    # Extra 2
    draw_mushroom(moving=False, pos_x=1.5,  pos_y=0.8, pos_z=3.5)     # Extra 3

    # Hongos en orillas (dentro del piso)
    draw_mushroom(moving=False, pos_x=-6, pos_y=0.8, pos_z=-5)    # Orilla 1 (esquina izq)
    draw_mushroom(moving=False, pos_x=6,  pos_y=0.8, pos_z=5)     # Orilla 2 (esquina der)
    draw_mushroom(moving=False, pos_x=6,  pos_y=0.8, pos_z=-5)    # Orilla 3 (posterior der)
    draw_mushroom(moving=False, pos_x=-6,  pos_y=0.8, pos_z=5)     # Orilla 2 (esquina der)

    glfw.swap_buffers(window)


def update_camera_with_hand(hand_x, hand_y, frame_width, frame_height):
    global prev_hand_x, prev_hand_y, camera_pos, camera_target
    if prev_hand_x is not None and prev_hand_y is not None:
        dx = (hand_x - prev_hand_x) / frame_width
        angle = dx * 50
        radius = math.sqrt((camera_pos[0] - camera_target[0]) ** 2 + (camera_pos[2] - camera_target[2]) ** 2)
        theta = math.atan2(camera_pos[2] - camera_target[2], camera_pos[0] - camera_target[0])
        theta -= math.radians(angle)
        camera_pos[0] = camera_target[0] + radius * math.cos(theta)
        camera_pos[2] = camera_target[2] + radius * math.sin(theta)

    prev_hand_x = hand_x
    prev_hand_y = hand_y

def update_zoom_with_pinch(landmarks, frame_width, frame_height):
    global prev_zoom_distance, camera_pos, camera_target
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    x1, y1 = int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height)
    x2, y2 = int(index_tip.x * frame_width), int(index_tip.y * frame_height)
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    if prev_zoom_distance is not None:
        diff = distance - prev_zoom_distance
        zoom_speed = 0.5
        direction = [
            camera_target[i] - camera_pos[i]
            for i in range(3)
        ]
        length = math.sqrt(sum(d**2 for d in direction))
        if length != 0:
            direction = [d / length for d in direction]
            for i in range(3):
                camera_pos[i] -= direction[i] * diff * zoom_speed

    prev_zoom_distance = distance

def main():
    global window
    if not glfw.init():
        sys.exit()

    width, height = 800, 600
    window = glfw.create_window(width, height, "Escena con Hongo", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        glfw.terminate()
        return

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils

    while not glfw.window_should_close(window):
        update_jump()
        draw_scene()

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                h, w, _ = frame.shape
                cx = int(handLms.landmark[0].x * w)
                cy = int(handLms.landmark[0].y * h)
                update_camera_with_hand(cx, cy, w, h)
                update_zoom_with_pinch(handLms.landmark, w, h)
                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Camara - Movimiento de Mano", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        glfw.poll_events()

    cap.release()
    cv2.destroyAllWindows()
    glfw.terminate()

if __name__ == "__main__":
    main()

```