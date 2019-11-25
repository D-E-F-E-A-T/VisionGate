from funcoesMQTT import escutar
from ../controlarHardware.tirarFoto import ligarLED
from ../controlarHardware.tirarFoto import desligarLED

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
