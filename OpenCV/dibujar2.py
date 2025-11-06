import numpy as np
import cv2


# Variables
dibujando = False # True si el ratón está presionado
ix = -1
iy = -1

# Funcion
def dibujar_rect(event, x, y, flags, param):
    
    global ix, iy, dibujando

    if event == cv2.EVENT_LBUTTONDOWN:
        dibujando = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if dibujando == True:
            img[:] = 0 # Limpiar la imagen antes de dibujar el rectángulo
            cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), -1)
    elif event == cv2.EVENT_LBUTTONUP:
        dibujando = False
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), -1)

cv2.namedWindow(winname='Imagen')
cv2.setMouseCallback('Imagen', dibujar_rect)


# Mostrar la imagen con OpenCV
img = np.zeros((512, 512, 3))

while True:
    cv2.imshow('Imagen', img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()