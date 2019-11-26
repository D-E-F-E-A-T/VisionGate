from funcoesMQTT import escutar
from eventosHardware import ligarLED
from eventosHardware import desligarLED
mensagem = escutar()

if mensagem == "abrir":
    ligarLED()
    #seja bem vindo
elif mensagem == "BDok":
    ligarLED()
    #seja bem vindo <nome>

elif mensagem == "fechar":
    desligarLED()

elif mensagem == "BDnot":
    desligarLED()
    #A placa não foi encontrada no banco de dados
