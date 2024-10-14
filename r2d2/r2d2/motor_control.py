import RPi.GPIO as GPIO
import time

# Definir pinos GPIO dos motores
leftMotorLPWM = 18   # GPIO 18
leftMotorRPWM = 23   # GPIO 23
rightMotorLPWM = 24  # GPIO 24
rightMotorRPWM = 25  # GPIO 25

# Configurações do PWM
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(leftMotorLPWM, GPIO.OUT)
GPIO.setup(leftMotorRPWM, GPIO.OUT)
GPIO.setup(rightMotorLPWM, GPIO.OUT)
GPIO.setup(rightMotorRPWM, GPIO.OUT)

# Inicialização dos PWM
leftMotorLPWM_pwm = GPIO.PWM(leftMotorLPWM, 1000)
leftMotorRPWM_pwm = GPIO.PWM(leftMotorRPWM, 1000)
rightMotorLPWM_pwm = GPIO.PWM(rightMotorLPWM, 1000)
rightMotorRPWM_pwm = GPIO.PWM(rightMotorRPWM, 1000)

leftMotorLPWM_pwm.start(0)
leftMotorRPWM_pwm.start(0)
rightMotorLPWM_pwm.start(0)
rightMotorRPWM_pwm.start(0)

# Função para controle gradual do PWM
def gradual_pwm_control(leftSpeed, rightSpeed, duration=2):
    """
    Controla a velocidade dos motores para atingir o valor desejado gradualmente em 2 segundos.
    """
    current_left_speed = 0
    current_right_speed = 0
    step_time = 0.1
    steps = int(duration / step_time)
    
    left_step = (leftSpeed - current_left_speed) / steps
    right_step = (rightSpeed - current_right_speed) / steps

    for _ in range(steps):
        current_left_speed += left_step
        current_right_speed += right_step
        
        setMotorSpeed(current_left_speed, current_right_speed)
        time.sleep(step_time)

def setMotorSpeed(leftSpeed, rightSpeed):
    """
    Ajusta a velocidade dos motores.
    Velocidades negativas significam movimento para trás.
    """
    if leftSpeed >= 0:
        leftMotorLPWM_pwm.ChangeDutyCycle(leftSpeed)
        leftMotorRPWM_pwm.ChangeDutyCycle(0)
    else:
        leftMotorLPWM_pwm.ChangeDutyCycle(0)
        leftMotorRPWM_pwm.ChangeDutyCycle(-leftSpeed)

    if rightSpeed >= 0:
        rightMotorLPWM_pwm.ChangeDutyCycle(rightSpeed)
        rightMotorRPWM_pwm.ChangeDutyCycle(0)
    else:
        rightMotorLPWM_pwm.ChangeDutyCycle(0)
        rightMotorRPWM_pwm.ChangeDutyCycle(-rightSpeed)

def stopMotors():
    """
    Para os motores, ajustando as velocidades para zero.
    """
    setMotorSpeed(0, 0)

def rotate_robot():
    """
    Faz o robô girar em seu próprio eixo por um período curto.
    Útil quando o gesto de dois dedos é detectado.
    """
    gradual_pwm_control(50, -50)  # Um motor vai para frente e o outro para trás para girar
    time.sleep(1.5)  # Tempo de rotação ajustável
    stopMotors()
