import cv2

def ask_for_tracker():
    print('Bienvenido! ¿Qué API de seguimiento te gustaría utilizar?')
    print('Apreta 1 para BOOSTING:')
    print('Apreta 2 para MIL:')
    print('Apreta 3 para KCF:')
    print('Apreta 4 para TLD:')
    print('Apreta 5 para MEDIANFLOW:')
    choice = input('Selecciona tu método de seguimiento: ')

    if choice == '1':
        tracker = cv2.legacy.TrackerBoosting.create()
    if choice == '2':
        tracker = cv2.legacy.TrackerMIL.create()
    if choice == '3':
        tracker = cv2.legacy.TrackerKCF.create()
    if choice == '4':
        tracker = cv2.legacy.TrackerTLD.create()
    if choice == '5':
        tracker = cv2.legacy.TrackerMedianFlow.create()

    return tracker

tracker = ask_for_tracker()
tracker_name = str(tracker).split()[1]

# Captura de Video
cap = cv2.VideoCapture(0)

# Primer Fotograma
ret, frame = cap.read()

# Region of interest para el primer fotograma
roi = cv2.selectROI(frame, False)

# Inicializar

ret = tracker.init(frame, roi)

while True:
    ret, frame = cap.read()

    success, roi = tracker.update(frame)

    (x, y, w, h) = tuple(map(int, roi))

    if success:
        p1 = (x, y)
        p2 = (x + w, y + h)
        cv2.rectangle(frame, p1, p2, (0, 255, 0), 3)
    else:
        cv2.putText(frame, 'Fallo al detectar!', (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    # Mostrar tracker
    cv2.putText(frame, tracker_name, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Mostrar Resultado
    cv2.imshow(tracker_name, frame)

    # Salir
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()