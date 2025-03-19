import numpy as np
import cv2 as cv

# Iniciar la captura de video desde la cámara
cap = cv.VideoCapture(0)

# Parámetros para el flujo óptico Lucas-Kanade
lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

# Leer el primer frame de la cámara
ret, first_frame = cap.read()
if not ret:
    cap.release()
    cv.destroyAllWindows()
    exit()

first_frame = cv.flip(first_frame, 1)
h, w = first_frame.shape[:2]
prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)

# Posición inicial de la pelotita (centro de la imagen)
ball_pos = np.array([[[w // 2, h // 2]]], dtype=np.float32)

# Definir límites del marco azul
margin = 20
frame_top_left = (margin, margin)
frame_bottom_right = (w - margin, h - margin)

while True:
    # Capturar el siguiente frame
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv.flip(frame, 1)
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Calcular el flujo óptico
    new_ball_pos, st, err = cv.calcOpticalFlowPyrLK(prev_gray, gray_frame, ball_pos, None, **lk_params)
    
    if new_ball_pos is not None and st[0][0] == 1:
        a, b = new_ball_pos.ravel()

        cv.putText (frame, f' ({int (a)}, {int (b)})', (int (a-30), int (b-30)), cv.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.7, (0, 25, 235), 2)
        
        # Verificar si la pelota está dentro del marco azul
        if frame_top_left[0] < a < frame_bottom_right[0] and frame_top_left[1] < b < frame_bottom_right[1]:
            ball_pos = new_ball_pos
        else:
            # Si la pelota sale del marco, volver al centro
            ball_pos = np.array([[[w // 2, h // 2]]], dtype=np.float32)

    # Dibujar la pelota roja
    a, b = ball_pos.ravel()
    frame = cv.circle(frame, (int(a), int(b)), 20, (0, 0, 255), -1)
    
    # Dibujar el marco azul
    cv.rectangle(frame, frame_top_left, frame_bottom_right, (255, 0, 0), 5)
    
    cv.imshow('Pelota en movimiento', frame)
    prev_gray = gray_frame.copy()

    # Presionar 'Esc' para salir
    if cv.waitKey(30) & 0xFF == 27:
        break

# Liberar la captura y cerrar las ventanas
cap.release()
cv.destroyAllWindows()

