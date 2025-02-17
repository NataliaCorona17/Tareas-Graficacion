import cv2 as cv   #importa openCv
import numpy as np  # Importa Numpy

img = cv.imread ('Tomie2.jpg',1)

img2 = cv.cvtColor (img, cv.COLOR_BGR2GRAY)
img3 = cv.cvtColor (img, cv.COLOR_BGR2RGB)
img4 = cv.cvtColor (img, cv.COLOR_BGR2HSV)
img5 = cv.cvtColor (img2, cv.COLOR_GRAY2BGR) 
img6 = cv.cvtColor (img, cv.COLOR_BGR2XYZ) 
img7 = cv.cvtColor (img, cv.COLOR_BGR2Luv) 
img8 = cv.cvtColor (img, cv.COLOR_HLS2BGR)
img9 = cv.cvtColor (img, cv.COLOR_Lab2RGB)

cv.imshow('Original',img)
cv.imshow('B&W',img2)
cv.imshow('RGB',img3)
cv.imshow('HSV',img4)
cv.imshow('G2BGR',img5)
cv.imshow('XYZ',img6)
cv.imshow('Luv',img7)
cv.imshow('BGR',img8)
cv.imshow('RGB',img9)

cv.waitKey (0)
cv.destroyAllWindows