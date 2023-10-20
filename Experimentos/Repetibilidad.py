from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time as tm
import socket
import threading 

#EDITAR               
#robots=["192.168.1.104","192.168.1.106","192.168.1.105"]    
robots=["192.168.1.104","192.168.1.105","192.168.1.106"]
intento = 4


UDP_IP_TX =""
UDP_PORT_TX = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP

##---------------------------------------------------------
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)

UDP_IP_RX = "192.168.1.100"# ip del computador que recibe datos (mismo que el que corre este script)
UDP_PORT_RX = 1234

print("Su IP es: ", IPAddr)

#UDP
sock_RX = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_RX.bind((UDP_IP_RX, UDP_PORT_RX))

file_name = "FINAL_V2"+str(intento)+".csv"  # archivo csv
texto = open(file_name,'w')
texto.write('Robot,Delta_muestra,Input_d,d_ref,vel_ref,Input_vel,Input_theta,Output_d,Output_vel,Output_theta'+'\n')
texto.close()



def GetData(file_name,):

    while True:
            data, addr = sock_RX.recvfrom(4096)
            testo = str(data.decode('utf-8'))
            texto = open(file_name, "a")
            data, addr = sock_RX.recvfrom(4096)
            texto.write(testo+'\n')
            texto.close()
 

calibrar=input("¿Calibrar? (S/N)")

if (calibrar == "S"):
    #calibrar
    for ip in reversed(robots):
        UDP_IP_TX = ip
        UDP_PORT_TX = 1111
        MESSAGE = "E/calibrar/1"
        sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
        print("message:", MESSAGE, "IP:", UDP_IP_TX)
        tm.sleep(0.2)
    input("Presione enter cuando la calibración esté completa")
"""
for i in range(len(robots)):

    UDP_IP_TX = robots[i]
    MESSAGE = "E/cv_p/" + str(100)#str(50000.3)
    print(MESSAGE, UDP_IP_TX)   
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
    MESSAGE = "E/cv_i/" + str(282)#600.3)
    print(MESSAGE, UDP_IP_TX)   
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
    MESSAGE = "E/cv_d/" + str(0)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
    print(MESSAGE, UDP_IP_TX)   


    UDP_IP_TX = robots[i]
    MESSAGE = "E/cd_p/" + str(8)#20000)
    print(MESSAGE, UDP_IP_TX)   
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
    MESSAGE = "E/cd_i/" + str(20)
    print(MESSAGE, UDP_IP_TX)   
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
    MESSAGE = "E/cd_d/" + str(0.1)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
    print(MESSAGE, UDP_IP_TX)   

    UDP_IP_TX = robots[i]
    MESSAGE = "E/co_p/" + str(2000)
    print(MESSAGE, UDP_IP_TX)   
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
    MESSAGE = "E/co_i/" + str(4500)
    print(MESSAGE, UDP_IP_TX)   
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
    MESSAGE = "E/co_d/" + str(60)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
    print(MESSAGE, UDP_IP_TX)   


"""

tm.sleep(2)
     
######INICIAR
UDP_IP_TX = robots[0]
UDP_PORT_TX = 1111
MESSAGE = "E/parar/no"
sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))

"""
######ALINEAR            
for i in range(len(robots)-1):
    UDP_IP_TX = robots[i+1]
    dist =10
    MESSAGE = "E/cd_ref/" + str(dist)
    print(MESSAGE, UDP_IP_TX)
    #sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))


tm.sleep(3)
"""
#iniciar monitoreo
dataCollector1 = threading.Thread(target=GetData, args=(file_name,))
dataCollector1.start()
#####################################ETAPA 1####################################################
#velocidad 20, distancia predecesor 10
UDP_IP_TX = robots[0]
UDP_PORT_TX = 1111        
MESSAGE = "E/cv_ref/" + str(round(20))
print(MESSAGE)
sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))

for i in range(len(robots)-1):
            UDP_IP_TX = robots[i+1]
            dist =15
            MESSAGE = "E/cd_ref/" + str(dist)
            print(MESSAGE, UDP_IP_TX)
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
        
tm.sleep(30) 

######################################ETAPA 2###################################
#velocidad 15 distancia 10
UDP_IP_TX = robots[0]
UDP_PORT_TX = 1111        
MESSAGE = "E/cv_ref/" + str(round(25))
print(MESSAGE)
sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))

for i in range(len(robots)-1):
            UDP_IP_TX = robots[i+1]
            dist =15
            MESSAGE = "E/cd_ref/" + str(dist)
            print(MESSAGE, UDP_IP_TX)
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
        
tm.sleep(30)

######################################ETAPA 2###################################
#velocidad 15 distancia 10
UDP_IP_TX = robots[0]
UDP_PORT_TX = 1111        
MESSAGE = "E/cv_ref/" + str(round(15))
print(MESSAGE)
sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))

for i in range(len(robots)-1):
            UDP_IP_TX = robots[i+1]
            dist =15
            MESSAGE = "E/cd_ref/" + str(dist)
            print(MESSAGE, UDP_IP_TX)
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
        
tm.sleep(30)

UDP_IP_TX = robots[0]
UDP_PORT_TX = 1111
MESSAGE = "E/parar/si"
sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
