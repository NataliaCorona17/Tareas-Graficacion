```python
import cv2
import mediapipe as mp
import numpy as np

ver = False

# Inicializar MediaPipe Manos
manos_mp = mp.solutions.hands
dibujo_mp = mp.solutions.drawing_utils
manos = manos_mp.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Funcion para determinar la letra o numero segun la posicion de los dedos
def reconocer_simbolo(lista_manos, fotograma):
    global ver
    alto, ancho, _ = fotograma.shape

    if len(lista_manos) == 1:
        mano = lista_manos[0]

        # Obtener coordenadas de los puntos clave
        dedos = [(int(mano.landmark[i].x * ancho), int(mano.landmark[i].y * alto)) for i in range(21)]
        pulgar, indice, medio, anular, menique, base_medio = dedos[4], dedos[8], dedos[12], dedos[16], dedos[20], dedos[9]

        # Mostrar los numeros de los puntos
        for i, (x, y) in enumerate(dedos):
            cv2.circle(fotograma, (x, y), 5, (0, 255, 0), -1)
            cv2.putText(fotograma, str(i), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        # Dibujar coordenadas del pulgar
        cv2.putText(fotograma, f'({int(pulgar[0])}, {int(pulgar[1])})', (pulgar[0], pulgar[1] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (23, 0, 0), 2, cv2.LINE_AA)

        # Calcular distancias
        distancia_pulgar_indice = np.linalg.norm(np.array(pulgar) - np.array(indice))

        # Logica para reconocer letras y simbolos
        if base_medio[1] < pulgar[1] and medio[1] < indice[1] and medio[1] < anular[1] and anular[1] < menique[1]:
            ver = False
            return "B"
        elif pulgar[1] > medio[1] and indice[1] < pulgar[1] and medio[1] < anular[1] and menique[1] > medio[1] and pulgar[1] < anular[1] and pulgar[1] < menique[1]:
            ver = False
            return "U"
        elif indice[1] < pulgar[1] and indice[1] < medio[1] and indice[1] < anular[1] and indice[1] < menique[1] and pulgar[1] > medio[1]:
            ver = False
            return "L"
        elif indice[0] < pulgar[0] and medio[0] < pulgar[0] and pulgar[1] < indice[1] and pulgar[1] < medio[1]:
            ver = False
            return "8"
        elif indice[0] > pulgar[0] and medio[0] > pulgar[0] and pulgar[1] < indice[1] and pulgar[1] < medio[1]:
            ver = False
            return "13"
        elif distancia_pulgar_indice < 15:
            ver = True
            print(ver)
        elif base_medio[1] > pulgar[1] and medio[1] < indice[1] and medio[1] < anular[1] and anular[1] < menique[1] and ver == True:
            return "44"
        else:
            return "Desconocido"

    elif len(lista_manos) == 2:
        mano1 = lista_manos[0]
        mano2 = lista_manos[1]

        # Coordenadas de indice, medio y anular
        i1 = np.array([mano1.landmark[8].x * ancho, mano1.landmark[8].y * alto])
        i2 = np.array([mano2.landmark[8].x * ancho, mano2.landmark[8].y * alto])

        m1 = np.array([mano1.landmark[12].x * ancho, mano1.landmark[12].y * alto])
        m2 = np.array([mano2.landmark[12].x * ancho, mano2.landmark[12].y * alto])

        a1 = np.array([mano1.landmark[16].x * ancho, mano1.landmark[16].y * alto])
        a2 = np.array([mano2.landmark[16].x * ancho, mano2.landmark[16].y * alto])

        muneca1 = np.array([mano1.landmark[0].x * ancho, mano1.landmark[0].y * alto])
        muneca2 = np.array([mano2.landmark[0].x * ancho, mano2.landmark[0].y * alto])

        # Distancias
        dist_i = np.linalg.norm(i1 - i2)
        dist_m = np.linalg.norm(m1 - m2)
        dist_a = np.linalg.norm(a1 - a2)
        dist_munecas = np.linalg.norm(muneca1 - muneca2)

        if dist_i < 40 and dist_m < 40 and dist_a < 40 and dist_munecas > 100:
            return "CASA"

    return "Desconocido"

# Captura de video
captura = cv2.VideoCapture(0)

while captura.isOpened():
    ret, fotograma = captura.read()
    fotograma = cv2.flip(fotograma, 1)
    if not ret:
        break

    fotograma_rgb = cv2.cvtColor(fotograma, cv2.COLOR_BGR2RGB)
    resultados = manos.process(fotograma_rgb)

    if resultados.multi_hand_landmarks:
        simbolo = reconocer_simbolo(resultados.multi_hand_landmarks, fotograma)

        for puntos_mano in resultados.multi_hand_landmarks:
            dibujo_mp.draw_landmarks(fotograma, puntos_mano, manos_mp.HAND_CONNECTIONS)

            # Dibujar puntos de las manos
            alto, ancho, _ = fotograma.shape
            for i, punto in enumerate(puntos_mano.landmark):
                cx, cy = int(punto.x * ancho), int(punto.y * alto)
                cv2.circle(fotograma, (cx, cy), 5, (0, 255, 0), -1)
                cv2.putText(fotograma, str(i), (cx, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        cv2.putText(fotograma, f"Simbolo: {simbolo}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow("Reconocimiento de Simbolos", fotograma)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

captura.release()
cv2.destroyAllWindows()

```