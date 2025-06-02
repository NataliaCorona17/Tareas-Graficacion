```python
import cv2 as cv
import numpy as np

rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')

cap = cv.VideoCapture(0)

while True:
    ret, img = cap.read()
    if not ret:
        print("Error: No se pudo capturar el video.")
        break
    
    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gris, 1.3, 5)
    
    for (x, y, w, h) in rostros:
        hat_width = int(w * 1.2)
        hat_height = int(h * 0.5)
        brim_height = int(h * 0.15)
        
        hat_x1, hat_x2 = x - int(w * 0.1), x + w + int(w * 0.1)
        hat_y1, hat_y2 = y - hat_height - brim_height, y - brim_height
        
        brim_x1, brim_x2 = x - int(w * 0.2), x + w + int(w * 0.2)
        brim_y1, brim_y2 = y - brim_height, y
        
        cv.rectangle(img, (hat_x1, hat_y1), (hat_x2, hat_y2), (0, 0, 0), -1)
        cv.rectangle(img, (brim_x1, brim_y1), (brim_x2, brim_y2), (0, 0, 0), -1)
        
        tie_top_x1, tie_top_x2 = x + int(w * 0.4), x + int(w * 0.6)
        tie_top_y1, tie_top_y2 = y + h, y + int(h * 1.2)
        tie_bottom_x1, tie_bottom_x2 = x + int(w * 0.3), x + int(w * 0.7)
        tie_bottom_y1, tie_bottom_y2 = y + int(h * 1.2), y + int(h * 1.6)
        
        cv.rectangle(img, (tie_top_x1, tie_top_y1), (tie_top_x2, tie_top_y2), (0, 0, 255), -1)
        cv.rectangle(img, (tie_bottom_x1, tie_bottom_y1), (tie_bottom_x2, tie_bottom_y2), (0, 0, 255), -1)
    
    cv.imshow('Sombrero de Copa y Corbata', img)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

```