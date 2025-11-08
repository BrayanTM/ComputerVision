import cv2
import numpy as np
from matplotlib import cm

# Cargar imagen
carretera = cv2.imread('../resources/img/carretera.png')
copia = np.copy(carretera)

# Crear matrices para segmentación
imagen = np.zeros(carretera.shape[:2], dtype = np.int32)
segmentos = np.zeros(carretera.shape, dtype = np.uint8)

# Función para convertir colores de matplotlib a BGR
def rgb(i):
    x = np.array(cm.tab10(i)[:3]) * 255
    return tuple(x)

# Crear lista de colores
colores = []
for i in range(10):
    colores.append(rgb(i))

# Variables globales
marcador = 10
marcador_actual = 1
marcador_actualizado = False

# Función callback del mouse
def mouse(event, x, y, flags, param):
    global marcador_actualizado, copia, imagen, marcador_actual
    
    if event == cv2.EVENT_LBUTTONDOWN:
        # TRACKEAR
        cv2.circle(imagen, (x, y), 10, (marcador_actual), -1)
        # MOSTRAR
        cv2.circle(copia, (x, y), 10, colores[marcador_actual], -1)
        marcador_actualizado = True

# Configurar ventana y callback
cv2.namedWindow('Carretera')
cv2.setMouseCallback('Carretera', mouse)

# Bucle principal
while True:
    cv2.imshow('Segmentos', segmentos)
    cv2.imshow('Carretera', copia)

    # Capturar tecla presionada
    k = cv2.waitKey(1) & 0xFF
    
    # Cerrar con 'q'
    if k == ord('q'):
        break
    # Borrar colores con 'c'
    elif k == ord('c'):
        copia = carretera.copy()
        imagen = np.zeros(carretera.shape[:2], dtype = np.int32)
        segmentos = np.zeros(carretera.shape, dtype = np.uint8)
    # Actualizar marcador actual con teclas 0-9
    elif k > 0 and chr(k).isdigit():
        marcador_actual = int(chr(k))
    
    # Actualizar marcadores de watershed
    if marcador_actualizado:
        imagen_copia = imagen.copy()
        cv2.watershed(carretera, imagen_copia)
        
        segmentos = np.zeros(carretera.shape, dtype = np.uint8)

        for color_ind in range(marcador):
            segmentos[imagen_copia == (color_ind)] = colores[color_ind]
        marcador_actualizado = False

cv2.destroyAllWindows()