import socket
IP = "192.168.1.79"
PORT = 11161
BUFFERSIZE = 1024

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as GestorSocket:
	print("Gestor SNMP\n---Formato de comando:---\n\nGET nombreComunidad OID\n\nSET nombreComunidad OID_a_cambiar nuevo_valor_OID\n")
	while True:
		request = input('Ingrese comando > ')
		GestorSocket.sendto(request.encode(), (IP,PORT))
		print("en espera de una respuesta")
		response, addr = GestorSocket.recvfrom(BUFFERSIZE)
		response = str(response, 'utf-8')
		if response[0] == "E":
			print(response)
		else:
			print(response)