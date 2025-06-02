```python
import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Función para determinar la letra según la posición de los dedos
def reconocer_letra(hand_landmarks, frame):
    h, w, _ = frame.shape  # Tamaño de la imagen
    
    # Obtener coordenadas de los puntos clave en píxeles
    dedos = [(int(hand_landmarks.landmark[i].x * w), int(hand_landmarks.landmark[i].y * h)) for i in range(21)]
    
    # Obtener posiciones clave (puntas de los dedos)
    pulgar, indice, medio, anular, meñique, base_medio = dedos[4], dedos[8], dedos[12], dedos[16], dedos[20], dedos[9]
    #PARA CIRCULO
    pp, ip, mp, ap, mep = dedos[4], dedos[8], dedos[12], dedos[16], dedos[20]

    # Mostrar los números de los landmarks en la imagen
    for i, (x, y) in enumerate(dedos):
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)  # Puntos verdes
        cv2.putText(frame, str(i), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    # Dibujar coordenadas del pulgar
    cv2.putText(frame, f'({int(pulgar[0])}, {int(pulgar[1])})', (pulgar[0], pulgar[1] - 15), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (23, 0, 0), 2, cv2.LINE_AA)

    # Calcular distancias en píxeles
    distancia_pulgar_indice = np.linalg.norm(np.array(pulgar) - np.array(indice))
    distancia_indice_medio = np.linalg.norm(np.array(indice) - np.array(medio))
    distancia_pulgar_medio = np.linalg.norm(np.array(pulgar) - np.array(base_medio))
    #PARA CIRCULO
    distancia_pp_ip = np.linalg.norm(np.array(pp) - np.array(ip))
    distancia_pp_mp = np.linalg.norm(np.array(pp) - np.array(mp))
    distancia_pp_ap = np.linalg.norm(np.array(pp) - np.array(ap))
    distancia_pp_mep = np.linalg.norm(np.array(pp) - np.array(mep))
    promedio = (distancia_pp_ip + distancia_pp_mp + distancia_pp_ap + distancia_pp_mep) / 4
    cv2.circle(frame, [pulgar[0] + 50, pulgar[1] + 50], int(promedio), (0, 255, 0), -1)
    # Lógica para reconocer algunas letras
    if distancia_pulgar_medio < 30:
        return "B"  # Seña de la letra A (puño cerrado con pulgar al lado)
    elif indice[1] < medio[1] and medio[1] < anular[1] and anular[1] < meñique[1]:
        return "A"  # Seña de la letra B (todos los dedos estirados, pulgar en la palma)
    elif distancia_pulgar_indice < 150:
        return "C"  # Seña de la letra C (mano en forma de "C")
    elif pulgar[1] > medio[1] and indice[1] < pulgar[1]:
        return "D"
    elif medio[1] < indice[1] and medio[1] < anular[1] and medio[1] < meñique[1] and pulgar[1] < indice[1]:
        return "FUCK YOU >:("
    return "Desconocido"
    

# Captura de video en tiempo real
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir a RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar la imagen con MediaPipe
    results = hands.process(frame_rgb)

    # Dibujar puntos de la mano y reconocer letras
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Identificar la letra
            letra_detectada = reconocer_letra(hand_landmarks, frame)

            # Mostrar la letra en pantalla
            cv2.putText(frame, f"Letra: {letra_detectada}", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
    
    # Mostrar el video
    cv2.imshow("Reconocimiento de Letras", frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()

```