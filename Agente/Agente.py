import socket
IP = "127.0.0.1"
PORT = 1161
BUFFERSIZE = 1024

def verificarComunidad(request):
	with open('snmpd.conf') as c_conf: 
		contenido = c_conf.read()
		permisos = contenido[:contenido.index('community')]
		comunidad = contenido[contenido.index(' ')+1:]
		if permisos == "rw":
			if request[:request.find(' ')] in comunidad:
				return True
			else:
				return False
		else:
			return False

def verificaOID(oid):
	with open('mib.txt') as mib:
		lineas_mib = mib.readlines()
		for linea in lineas_mib:
			if linea.find(oid):
				return True
		return False

def obtenerOID(oid):
	with open('mib.txt') as mib:
		lineas_mib = mib.readlines()
		for linea in lineas_mib:
			if oid in linea:
				return linea

def getRequest(request):
	if verificarComunidad(request):
		oid = request[request.find(' ')+1:]
		oid = oid[2:]
		if verificaOID(oid):
			getResponse = obtenerOID(oid)
			SNMPDaemonSocket.sendto(str.encode(getResponse), addr)			
		else:
			SNMPDaemonSocket.sendto(str.encode("E: OID no reconocido"), addr)
	else:
		SNMPDaemonSocket.sendto(str.encode("E: comunidad no reconocida"), addr)

def modificarOID(oid_a_cambiar):
	info_nueva = oid_a_cambiar[oid_a_cambiar.find(' ')+1:]
	oid_a_cambiar= oid_a_cambiar[:oid_a_cambiar.find(' ')+1]
	nuevas_lineas = []
	with open('mib.txt','r') as mib:
		lineas_mib = mib.readlines()
		for linea in lineas_mib:
			if oid_a_cambiar in linea:
				info_cambiar = linea[linea.find('=')+2:]
				new_line = linea.replace(info_cambiar,info_nueva)
				print("linea reemplazada {}".format(new_line))
				nuevas_lineas.append(new_line+'\n')
			else:
				nuevas_lineas.append(linea)

	with open('mib.txt', 'w') as outfile:
		for line in nuevas_lineas:
			outfile.write(line)

def setrequest(request):
	if verificarComunidad(request):
		oid_a_cambiar = request[request.find(' ')+1:]
		oid_a_cambiar = oid_a_cambiar[2:]
		if verificaOID(oid_a_cambiar):
			#oid = obtenerOID(oid_a_cambiar)
			modificarOID(oid_a_cambiar)
			SNMPDaemonSocket.sendto(str.encode("OID modificado, verifique con get"), addr)
		else:
			SNMPDaemonSocket.sendto(str.encode("E: OID no encontrado"), addr)
	else:
		SNMPDaemonSocket.sendto(str.encode("E: comunidad no reconocida"), addr)


SNMPDaemonSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SNMPDaemonSocket.bind((IP,PORT))
print("Server UDP up and listening")

while True:
	print('\nwaiting to receive message')
	request, addr = SNMPDaemonSocket.recvfrom(BUFFERSIZE)
	request = str(request, 'utf-8')

	if request[:3].upper() == 'GET':
		comunidad = request[request.find(' ')+1:]
		getRequest(comunidad)

	elif request[:3	].upper() == 'SET':
		comunidad = request[request.find(' ')+1:]
		setrequest(comunidad)
	else:
		SNMPDaemonSocket.sendto(str.encode("E: comando no reconocido"), addr)