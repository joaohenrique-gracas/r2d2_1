import cv2
import mediapipe as mp
from motor_control import setMotorSpeed, stopMotors, gradual_pwm_control
from gesture_control import process_gestures

# Inicialização do MediaPipe para detecção de rostos
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection()

# Variáveis de controle
face_position = None

# Função para detectar rostos e mãos
def process_frame(frame):
    global face_position

    # Processar os gestos das mãos
    tracking = process_gestures(frame)

    # Se o modo de rastreamento estiver ativado, detectar rostos
    if tracking:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_results = face_detection.process(rgb_frame)

        if face_results.detections:
            for detection in face_results.detections:
                bboxC = detection.location_data.relative_bounding_box
                face_position = int(bboxC.xmin * frame.shape[1] + bboxC.width * frame.shape[1] / 2)
                control_motors_based_on_face_position(face_position)

    return frame

# Função para controlar os motores com base na posição do rosto
def control_motors_based_on_face_position(face_position):
    window_center = 320  # Valor para centralização da tela
    center_buffer = 10
    kp = 50 / 320
    error = window_center - face_position
    pwmOut = kp * error

    if face_position < window_center - center_buffer:
        # Rosto à esquerda
        gradual_pwm_control(50 + pwmOut, 50)
    elif face_position > window_center + center_buffer:
        # Rosto à direita
        gradual_pwm_control(50, 50 + pwmOut)
    else:
        # Rosto centralizado
        gradual_pwm_control(50, 50)
