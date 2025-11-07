import cv2

cap = cv2.VideoCapture(0)

ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

x = ancho // 2
y = alto // 2

w = ancho // 4
h = alto // 4

while True:
    ret, frame = cap.read()

    # gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.rectangle(frame, (x, y), (x + w, y + h), color = (0, 0, 255), thickness = 4)

    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()