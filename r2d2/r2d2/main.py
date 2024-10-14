import cv2
import motor_control as motor
import gesture_control as gesture
import tracking_system as tracking

# Variável para ativar/desativar o rastreamento
tracking_face = False

# Captura de vídeo da câmera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

while True:
    ret, image = cap.read()
    if not ret:
        break

    # Processa gestos e rosto
    tracking_face, fingers_up = gesture.process_gestures(image)
    
    if tracking_face:
        motor.execute_tracking(image)
    elif fingers_up:
        motor.rotate_robot_on_axis()
    else:
        motor.stopMotors()

    # Mostra a imagem com as detecções
    cv2.imshow('Deteccao de Rosto e Mao', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Limpeza
cap.release()
cv2.destroyAllWindows()
motor.stopMotors()
