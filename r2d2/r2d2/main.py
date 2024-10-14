import cv2
from tracking_system import process_frame

# Inicialização da câmera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Processar o frame para detecção de rosto e gestos de mão
    processed_frame = process_frame(frame)

    # Exibir o frame processado
    cv2.imshow('Tracking System', processed_frame)

    # Pressionar 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar a câmera e fechar janelas
cap.release()
cv2.destroyAllWindows()
