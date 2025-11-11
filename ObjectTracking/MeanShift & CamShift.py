import numpy as np
import cv2
import os

# Obtener la ruta absoluta al directorio del proyecto
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
haarcascade_path = os.path.join(project_dir, 'resources', 'haarcascades', 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(haarcascade_path)

# Verificar que el clasificador se cargó correctamente
if face_cascade.empty():
    print("Error: No se pudo cargar el clasificador Haar Cascade")
    exit()

# Esperar un poco para que la cámara se estabilice
print("Preparando cámara... Asegúrate de que tu rostro esté visible")
for _ in range(30):
    cap.read()

# Intentar detectar el rostro varias veces
face_detected = False
max_attempts = 50
attempts = 0
window_created = False

while not face_detected and attempts < max_attempts:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo leer el frame de la cámara")
        cap.release()
        exit()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_rectangles = face_cascade.detectMultiScale(
        gray, 
        scaleFactor=1.1, 
        minNeighbors=5, 
        minSize=(100, 100)
    )
    
    if len(face_rectangles) > 0:
        face_detected = True
        print("¡Rostro detectado!")
    else:
        attempts += 1
        cv2.putText(frame, "Buscando rostro...", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Deteccion', frame)
        window_created = True
        cv2.waitKey(1)

if not face_detected:
    print("Error: No se detectó ningún rostro después de varios intentos")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Solo destruir la ventana si fue creada
if window_created:
    cv2.destroyWindow('Deteccion')

(face_x, face_y, w, h) = tuple(face_rectangles[0])

track_window = (face_x, face_y, w, h)

# Region of interest
roi = frame[face_y:face_y + h, face_x:face_x + w]

hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

# Crear máscara para ignorar valores muy oscuros y muy brillantes
mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))

# Histograma con máscara
roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])

cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

print("Iniciando tracking... Presiona 'q' para salir")

frame_count = 0

while True:
    ret, frame = cap.read()

    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Crear máscara para el back projection
        mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
        
        # Aplicar máscara al back projection
        dst = cv2.bitwise_and(dst, dst, mask=mask)

        # Aplicar MeanShift
        ret, track_window = cv2.meanShift(dst, track_window, term_crit)

        x, y, w, h = track_window
        
        # Dibujar el rectángulo de seguimiento
        img2 = cv2.rectangle(frame.copy(), (x, y), (x + w, y + h), (0, 255, 0), 3)
        
        # Dibujar un punto en el centro
        center_x = x + w // 2
        center_y = y + h // 2
        cv2.circle(img2, (center_x, center_y), 5, (0, 0, 255), -1)
        
        # Mostrar información
        cv2.putText(img2, f"Tracking: ({center_x}, {center_y})", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow('MeanShift Tracking', img2)
        
        # Opcional: mostrar el back projection para debug
        # cv2.imshow('Back Projection', dst)

        key = cv2.waitKey(30) & 0xFF

        if key == ord('q'):
            break
            
        frame_count += 1
    else:
        break

print(f"Tracking finalizado. Total de frames procesados: {frame_count}")
cap.release()
cv2.destroyAllWindows()
