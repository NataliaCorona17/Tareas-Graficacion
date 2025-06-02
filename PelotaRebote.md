```python
import cv2 as cv
import numpy as np

ancho = 1000
alto = 500
radio = 20
x = ancho // 2
y = alto // 2
velocidad_x = 10
velocidad_y = 7

while True:
    img = np.ones((alto, ancho, 3), dtype=np.uint8) * 255

    if x + radio > ancho or x - radio < 0:
        velocidad_x *= -1
    if y + radio > alto or y - radio < 0:
        velocidad_y *= -1

    x += velocidad_x
    y += velocidad_y

    cv.circle(img, (int(x), int(y)), radio, (0, 255, 0), -1)
    cv.imshow('Pelota Rebotando', img)

    if cv.waitKey(20) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()

```