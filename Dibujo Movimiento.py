import cv2 as cv
import numpy as np
import time

width = 500
height = 500

def create_blank_image():
    return np.ones((height, width, 3), dtype=np.uint8) * 255

center_x = width // 2
center_y = height // 2

# Altura del salto
amplitude = 50

speed = 2

cv.namedWindow('Hombre de Nieve', cv.WINDOW_NORMAL)

frame_count = 0

while True:
    img = create_blank_image()

    # Posición vertical
    y_offset = int(amplitude * np.sin(frame_count * speed * 0.01))

    # Cabeza
    cv.circle(img, (center_x, center_y + y_offset - 100), 50, (255, 255, 255), -1)
    cv.circle(img, (center_x, center_y + y_offset - 100), 45, (0, 0, 0), 2)

    # Cuerpo (arriba)
    cv.circle(img, (center_x, center_y + y_offset), 70, (255, 255, 255), -1)
    cv.circle(img, (center_x, center_y + y_offset), 65, (0, 0, 0), 2)

    # Cuerpo (abajo)
    cv.circle(img, (center_x, center_y + y_offset + 100), 90, (255, 255, 255), -1)
    cv.circle(img, (center_x, center_y + y_offset + 100), 85, (0, 0, 0), 2)

    # Ojos
    cv.circle(img, (center_x - 20, center_y + y_offset - 120), 10, (0, 0, 0), -1)
    cv.circle(img, (center_x + 20, center_y + y_offset - 120), 10, (0, 0, 0), -1)

    # Nariz
    cv.circle(img, (center_x, center_y + y_offset - 110), 5, (255, 165, 0), -1)

    # Boca
    cv.ellipse(img, (center_x, center_y + y_offset - 90), (15, 5), 0, 0, 360, (0, 0, 0), -1)

    # Botones
    cv.circle(img, (center_x, center_y + y_offset + 20), 5, (0, 0, 0), -1)
    cv.circle(img, (center_x, center_y + y_offset + 50), 5, (0, 0, 0), -1)

    # Brazos
    cv.line(img, (center_x - 50, center_y + y_offset), (center_x - 100, center_y + y_offset - 50), (0, 0, 0), 3)
    cv.line(img, (center_x + 50, center_y + y_offset), (center_x + 100, center_y + y_offset - 50), (0, 0, 0), 3)

    cv.imshow('Hombre de Nieve', img)

    frame_count += 1 

    key = cv.waitKey(1)
    
    if key == ord('q'):
        break

cv.destroyAllWindows()
