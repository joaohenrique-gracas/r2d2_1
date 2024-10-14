import mediapipe as mp
from motor_control import stopMotors, rotate_robot

# Inicialização do MediaPipe para detecção de mãos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Variável de controle para modo de rastreamento
tracking = False

# Funções para detecção de gestos específicos
def detect_open_hand(hand_landmarks):
    """
    Detectar se a mão está aberta.
    Critério: O dedo mínimo (pinky) e o polegar estão estendidos.
    """
    finger_tips = [8, 12, 16, 20]  # Índices das pontas dos dedos
    open_fingers = sum([hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y for tip in finger_tips])
    return open_fingers == 5  # Todos os dedos levantados

def detect_closed_fist(hand_landmarks):
    """
    Detectar se o punho está fechado.
    Critério: Todas as pontas dos dedos estão abaixo das juntas dos dedos.
    """
    finger_tips = [8, 12, 16, 20]  # Índices das pontas dos dedos
    closed_fingers = sum([hand_landmarks.landmark[tip].y > hand_landmarks.landmark[tip - 2].y for tip in finger_tips])
    return closed_fingers == 4  # Todos os dedos fechados

def detect_two_fingers_up(hand_landmarks):
    """
    Detectar se dois dedos estão levantados (sinal de paz).
    Critério: O indicador e o dedo médio estão levantados, enquanto o anular e mínimo estão abaixados.
    """
    index_up = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
    middle_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
    ring_down = hand_landmarks.landmark[16].y > hand_landmarks.landmark[14].y
    pinky_down = hand_landmarks.landmark[20].y > hand_landmarks.landmark[18].y
    return index_up and middle_up and ring_down and pinky_down

# Função para processar gestos e interagir com o sistema de controle
def process_gestures(frame):
    global tracking

    # Conversão de BGR para RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Processamento da imagem para detectar mãos
    hand_results = hands.process(rgb_frame)

    # Verificar se há mãos detectadas
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            # Mão aberta -> Iniciar rastreamento
            if detect_open_hand(hand_landmarks):
                tracking = True
                print("Modo de rastreamento ativado")
            
            # Punho fechado -> Parar rastreamento
            elif detect_closed_fist(hand_landmarks):
                tracking = False
                stopMotors()
                print("Modo de rastreamento desativado")

            # Dois dedos levantados -> Girar no próprio eixo
            elif detect_two_fingers_up(hand_landmarks):
                rotate_robot()
                print("Girando no próprio eixo")

    return tracking
