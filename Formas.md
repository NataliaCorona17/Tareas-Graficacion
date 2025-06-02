```python
import cv2 as cv
import numpy as np

img = np.ones((500, 500, 3), dtype=np.uint8) * 255

# Cabeza
cv.circle(img, (250, 150), 50, (255, 255, 255), -1)
cv.circle(img, (250, 150), 45, (0, 0, 0), 2)

# Cuerpo (arriba)
cv.circle(img, (250, 250), 70, (255, 255, 255), -1)
cv.circle(img, (250, 250), 65, (0, 0, 0), 2)

# Cuerpo (abajo)
cv.circle(img, (250, 350), 90, (255, 255, 255), -1)
cv.circle(img, (250, 350), 85, (0, 0, 0), 2)

# Ojos
cv.circle(img, (230, 130), 10, (0, 0, 0), -1)
cv.circle(img, (270, 130), 10, (0, 0, 0), -1)

# Nariz
cv.circle(img, (250, 140), 5, (255, 165, 0), -1)

# Boca
cv.ellipse(img, (250, 160), (15, 5), 0, 0, 360, (0, 0, 0), -1)

# Botones
cv.circle(img, (250, 280), 5, (0, 0, 0), -1)
cv.circle(img, (250, 310), 5, (0, 0, 0), -1)

# Brazos
cv.line(img, (200, 250), (150, 200), (0, 0, 0), 3)
cv.line(img, (300, 250), (350, 200), (0, 0, 0), 3)

cv.imshow('Hombre de Nieve', img)
cv.waitKey(0)
cv.destroyAllWindows()

```