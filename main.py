from tirarFoto import capturarEvento
from analisarFoto import analisarImagem

while True:
	if capturarEvento():
		analisarImagem()
		#if analisarImagem != False: implementar Sockets
