```python
import cv2 as cv
import numpy as np

# Cargar la imagen en escala de grises
img = cv.imread('img3.jpg', 0)

# Obtener el tamaño de la imagen
x, y = img.shape

# Definir el factor de escala
scale_x, scale_y = 2, 2

# Crear una nueva imagen para almacenar el escalado
scaled_img = np.zeros((int(x * scale_y), int(y * scale_x)), dtype=np.uint8)

# Aplicar el escalado con interpolación bilineal
for i in range(x):
    for j in range(y):
        scaled_img[i * 2, j * 2] = img[i, j]
        if j * 2 + 1 < y * 2:
            scaled_img[i * 2, j * 2 + 1] = img[i, j]
        if i * 2 + 1 < x * 2:
            scaled_img[i * 2 + 1, j * 2] = img[i, j]
        if i * 2 + 1 < x * 2 and j * 2 + 1 < y * 2:
            scaled_img[i * 2 + 1, j * 2 + 1] = img[i, j]

# Aplicar convolución
kernel = np.ones((3, 3), np.float32) / 9
smoothed_img = np.copy(scaled_img)
for i in range(1, scaled_img.shape[0] - 1):
    for j in range(1, scaled_img.shape[1] - 1):
        region = scaled_img[i-1:i+2, j-1:j+2]
        smoothed_img[i, j] = np.sum(region * kernel)

cv.imshow('Imagen Original', img)
cv.imshow('Imagen Escalada (Suavizada)', smoothed_img)
cv.waitKey(0)
cv.destroyAllWindows()

```