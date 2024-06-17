from ultralytics import YOLO
import cv2
import os
from datetime import datetime

model = YOLO("train3.pt")

if not os.path.exists("Ejecucion"):
    os.makedirs("Ejecucion")

execution_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
execution_path = os.path.join("Ejecucion", execution_time)
os.makedirs(execution_path)

cap = cv2.VideoCapture(1)
frame_count = 0


while True:

    ret, frame = cap.read()
    if not ret:
        break

    resultados = model.predict(frame, imgsz = 640, conf=0.7)

    if resultados[0].boxes.shape[0] > 0:
        anotaciones = resultados[0].plot()

        # Guardar capturas en la carpeta de la ejecución
        frame_filename = os.path.join(execution_path, f"frame_{frame_count:04d}.png")
        cv2.imwrite(frame_filename, anotaciones)
        frame_count += 1
    else:
        anotaciones = frame

    cv2.imshow("Deteccion Movimiento Anomalo", anotaciones)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()