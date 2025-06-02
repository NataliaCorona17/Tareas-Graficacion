```python
import cv2 as cv   #importa openCv
import numpy as np  # Importa Numpy

#img = cv.imread ('Duo.jpg',1)
img = np.ones ((300,300), dtype = np.uint8) * 250

#img2 = cv.cvtColor (img, cv.COLOR_BGR2GRAY)
#img3 = cv.cvtColor (img, cv.COLOR_BGR2RGB)
#img4 = cv.cvtColor (img, cv.COLOR_BGR2HSV)
#img5 = cv.cvtColor (img2, cv.COLOR_GRAY2BGR) 
#img6 = cv.cvtColor (img, cv.COLOR_BGR2XYZ) 
#img7 = cv.cvtColor (img, cv.COLOR_BGR2Luv) 
#img8 = cv.cvtColor (img, cv.COLOR_HLS2BGR)
#img9 = cv.cvtColor (img, cv.COLOR_Lab2RGB)
#img10 = cv.cvtColor (img, cv.COLOR_RGB2YCrCb)
#cv.imshow('img2a',img2)
#cv.imshow('B&W',img2)
#cv.imshow('RGB',img3)
#cv.imshow('HSV',img4)
#cv.imshow('G2BGR',img5)
#cv.imshow('XYZ',img6)
#cv.imshow('Luv',img7)
#cv.imshow('BGR',img8)
#cv.imshow('RGB',img9)
#cv.imshow('YCrCb',img10)

import cv2 as cv
import numpy as np

img = np.ones((300, 300), dtype=np.uint8) * 255


for i in range(60, 80):
    for j in range(60, 80):
        img[i, j] = 0
for i in range(60, 80):
    for j in range(80, 100):
        img[i, j] = 0
for i in range(60, 80):
    for j in range(160, 180):
        img[i, j] = 0
for i in range(60, 80):
    for j in range(180, 200):
        img[i, j] = 0
for i in range(80, 100):
    for j in range(40, 60):
        img[i, j] = 0
for i in range(80, 100):
    for j in range(100, 120):
        img[i, j] = 0
for i in range(100, 120):
    for j in range(120, 140):
        img[i, j] = 0
for i in range(80, 100):
    for j in range(200, 220):
        img[i, j] = 0
for i in range(80, 100):
    for j in range(140, 160):
        img[i, j] = 0
for i in range(100, 120):
    for j in range(220, 240):
        img[i, j] = 0
for i in range(100, 120):
    for j in range(20, 40):
        img[i, j] = 0
for i in range(120, 140):
    for j in range(20, 40):
        img[i, j] = 0
for i in range(120, 140):
    for j in range(220, 240):
        img[i, j] = 0
for i in range(140, 160):
    for j in range(200, 220):
        img[i, j] = 0
for i in range(160, 180):
    for j in range(180, 200):
        img[i, j] = 0
for i in range(180, 200):
    for j in range(160, 180):
        img[i, j] = 0
for i in range(200, 220):
    for j in range(140, 160):
        img[i, j] = 0
for i in range(220, 240):
    for j in range(120, 140):
        img[i, j] = 0
for i in range(200, 220):
    for j in range(100, 120):
        img[i, j] = 0
for i in range(180, 200):
    for j in range(80, 100):
        img[i, j] = 0
for i in range(160, 180):
    for j in range(60, 80):
        img[i, j] = 0
for i in range(140, 160):
    for j in range(40, 60):
        img[i, j] = 0



cv.imshow ('img2b',img)
cv.waitKey (0)
cv.destroyAllWindows

```