import cv2
import numpy as np

# Cargar la imagen
imagen = cv2.imread("pato.jpg")

# Escalar la imagen (aumentar tamaño)
escala = 2  # Factor de escala
nueva_dim = (imagen.shape[1] * escala, imagen.shape[0] * escala)
imagen_escalada = cv2.resize(imagen, nueva_dim, interpolation=cv2.INTER_CUBIC)

# Filtro de nitidez (kernel)
kernel_nitidez = np.array([[ 0, -1,  0],
                            [-1,  5, -1],
                            [ 0, -1,  0]])

# Aplicar convolución
imagen_hd = cv2.filter2D(imagen_escalada, -1, kernel_nitidez)

# Guardar la imagen
cv2.imwrite("imagen_mejorada.jpg", imagen_hd)

print("Imagen guardada como 'imagen_mejorada.jpg'")
    