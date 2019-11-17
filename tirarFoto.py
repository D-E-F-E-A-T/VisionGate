import RPi.GPIO as GPIO
import cv2

GPIO.setmode(GPIO.BOARD)

#Definindo o pino 18 como entrada
pinButao = 18
GPIO.setup(pinButao, GPIO.IN)

#Iniciando WebCam
video = cv2.VideoCapture(0)

def capturarEvento():
    #Pegando Status e Frame do vídeo
    ret, frame = video.read()
    #Verificando estado do botão
    if GPIO.input(pinButao):
        cv2.imwrite("imagem.jpg", frame)
        return True #Caso verdadeiro, salva imagem e retorna True

    else:
        return False #Caso falso, retorna falso
