import cv2
import mediapipe as mp
import time

# Inicializar MediaPipe Face Mesh y Face Detection
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_face_detection = mp.solutions.face_detection

face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=2, min_detection_confidence=0.5)
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

cap = cv2.VideoCapture(0)

# Variables para detección de parpadeo
ojo_abierto_contador = 0
parpadeo_detectado = False
ultimo_tiempo = time.time()
mensaje = "Detectando..."

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir imagen a RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detectar rostros
    results_faces = face_detection.process(frame_rgb)
    results_mesh = face_mesh.process(frame_rgb)
    
    if results_faces.detections:
        # Contar los cuadros donde los ojos están abiertos
        ojo_abierto_contador += 1
        tiempo_actual = time.time()
        
        # Si han pasado 3 segundos y no ha habido parpadeo, es una posible foto
        if tiempo_actual - ultimo_tiempo > 3:
            if ojo_abierto_contador > 100:
                mensaje = "Es una foto"
            else:
                mensaje = "Es una persona"
                parpadeo_detectado = True
            ojo_abierto_contador = 0
            ultimo_tiempo = tiempo_actual
    
    # Dibujar la malla facial
    if results_mesh.multi_face_landmarks:
        for face_landmarks in results_mesh.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION,
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1),
                mp_drawing.DrawingSpec(color=(255, 177, 154), thickness=1)
            )
    
    # Mostrar mensaje en pantalla
    cv2.putText(frame, mensaje, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if mensaje == "Es una persona" else (0, 0, 255), 2, cv2.LINE_AA)
    
    # Mostrar la imagen
    cv2.imshow("Salida", frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

