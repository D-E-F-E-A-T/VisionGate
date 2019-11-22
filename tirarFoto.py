#coding: utf-8
import RPi.GPIO as GPIO
import cv2

GPIO.setmode(GPIO.BOARD)

#Definindo o pino 18 como entrada
pinButao = 18
GPIO.setup(pinButao, GPIO.IN)

#Iniciando WebCam
video = cv2.VideoCapture("http://192.168.1.3:8081/")

def capturarEvento():
    estadoBotao = False
    #Pegando Status e Frame do vídeo
    ret, frame = video.read()
    #Verificando estado do botão
    if GPIO.input(pinButao):
        cv2.imwrite("imagem.jpg", frame)
	estadoBotao = True 
        return estadoBotao #Caso verdadeiro, salva imagem e retorna True

    else:
	estadoBotao = False
        return estadoBotao #Caso falso, retorna falso
