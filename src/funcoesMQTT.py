# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt

MQTT_ADDRESS = 'mqtt.fluux.io' #Endereço do broker
MQTT_PORT = 1883 #Porta do broker
MQTT_TIMEOUT = 180 #Tempo máximo sem resposta

MQTT_TOPIC = "+/VisionGate/#" #Tópico
MQTT_MSGS = [0] #Mensagens recebidas

#Callback - conexao ao broker realizada
def on_connect(client, userdata, flags, rc):
    #faz subscribe automatico no topico
    client.subscribe(MQTT_TOPIC)

#Callback - mensagem recebida do broker
def on_message(client, userdata, msg):
    mensagem = str(msg.payload) 
    
    MQTT_MSGS.append(str(msg.payload))
    mensagem = MQTT_MSGS[(len(MQTT_MSGS) -1)]

    callToAction = ['abrir', 'fechar', 'BDok', 'BDnot']
    if mensagem in callToAction:
        client.disconnect()

#Callback - mensagem publicada
def on_publish(client, userdata, mid):
    print("Enviado")

def enviarPlaca(msg):
    client = mqtt.Client()
    client.on_publish = on_publish
    
    client.connect(MQTT_ADDRESS, MQTT_PORT)
    result, mid = client.publish('VisionGate/StreamChannel', msg)

def escutar():
    client = mqtt.Client()
    
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.connect(MQTT_ADDRESS, MQTT_PORT)
    client.subscribe("VisionGate/#")

    client.loop_forever()
    return MQTT_MSGS[(len(MQTT_MSGS) -1)]
    