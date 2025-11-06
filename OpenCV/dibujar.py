"""
Dibujar círculos en una imagen con OpenCV al hacer clic con el ratón.
Clic izquierdo para un círculo verde, clic derecho para un círculo rojo.
"""

import numpy as np
import cv2

# Funcion 

def dibujar_circulo(event, x, y, flags, param):
    
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 100, (0, 255, 0), -1)
    elif event == cv2.EVENT_RBUTTONDOWN:
        cv2.circle(img, (x, y), 100, (0, 0, 255), -1)

cv2.namedWindow(winname='Imagen')
cv2.setMouseCallback('Imagen', dibujar_circulo)

# Mostrar la imagen con OpenCV
img = np.zeros((512, 512, 3))

while True:
    cv2.imshow('Imagen', img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()