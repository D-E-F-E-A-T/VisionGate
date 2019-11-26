#coding: utf-8
from analisarFoto import analisarImagem
from eventosHardware import *

i = 1
while i >= 1:
	i += 1
	if i == 3:
		print("Aguardando o botão ser pressionado")
	if capturarEvento() == 1:
		print(analisarImagem())
