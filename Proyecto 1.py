import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Función para determinar la letra o número según la posición de los dedos
def reconocer_simbolo(hand_landmarks, frame):
    h, w, _ = frame.shape  # Tamaño de la imagen
    
    # Obtener coordenadas de los puntos clave en píxeles
    dedos = [(int(hand_landmarks.landmark[i].x * w), int(hand_landmarks.landmark[i].y * h)) for i in range(21)]
    
    # Obtener posiciones clave (puntas de los dedos)
    pulgar, indice, medio, anular, meñique, base_medio = dedos[4], dedos[8], dedos[12], dedos[16], dedos[20], dedos[9]

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

    # Lógica para reconocer las letras B, L y U
    if distancia_pulgar_medio < 30:
        return "B"
    elif indice[1] < medio[1] and medio[1] < anular[1] and anular[1] < meñique[1]:
        return "L"
    elif pulgar[1] > medio[1] and indice[1] < pulgar[1] and medio[1] < anular[1] and anular[1] < meñique[1]:
        return "U"
    
    # Lógica mejorada para los números 8 y 13
    if abs(indice[1] - medio[1]) < 20 and pulgar[1] > anular[1] and meñique[1] > anular[1]:  
        return "13"
    elif pulgar[1] < indice[1] and abs(medio[1] - anular[1]) < 20 and meñique[1] > anular[1]:  
        return "8"
    
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

    # Dibujar puntos de la mano y reconocer símbolos
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Identificar la letra o número
            simbolo_detectado = reconocer_simbolo(hand_landmarks, frame)

            # Mostrar el símbolo en pantalla
            cv2.putText(frame, f"Símbolo: {simbolo_detectado}", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Mostrar el video
    cv2.imshow("Reconocimiento de Símbolos", frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
