# -*- coding: cp1252 -*-
"""
_____________________________________________________
|   -Conexion de UDP con la base de datos en MySQL  |
|    -Crear archivo CSV                             |
|---------------------------------------------------|

"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
#Librerias
import sys
import paho.mqtt.client as mqtt
import pymysql
import csv
import socket
#Ajustables
file_name = "C:\\Users\\56975\\Documents\\Catalina\\ELO308-Codes\\ELO308-Codes\\monitoreo.csv"  # archivo csv

UDP_IP = "192.168.1.102" # ip del computador que recibe datos (mismo que el que corre este script)
UDP_PORT = 1234

#UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

#creacion de archivo CSV
texto = open(file_name,'w')
#estado = "T,"+String(Input_d)+","+String(d_ref)+","+String(vel_ref)+","+String(Input_vel)+","+String(Input_theta)+","+String(Output_d)+","+String(Output_vel)+","+String(Output_theta);
 
texto.write('Robot,Delta_muestra,Input_d,d_ref,vel_ref,Input_vel,Input_theta,Output_d,Output_vel,Output_theta'+'\n')

texto.close()

gData = []
gData.append([0])
gData.append([0])
j=0
#Configuramos la gr�fica
fig = plt.figure()
ax = fig.add_subplot(111)
hl, = plt.plot(gData[0], gData[1])
plt.ylim(0, 30)
plt.xlim(0,200)

def GetData(out_data,señal):
    while True:
        data, addr = sock.recvfrom(4096) # buffer size is 1024 byte
        testo = str(data.decode('utf-8'))
        lista = testo.split(",")
        texto = open(file_name,"a")
        texto.write(testo+'\n')
        texto.close()
        #print(testo)
        column = 0
        print (lista[0],lista[señal])
        if lista[0]=='L':
            out_data[1].append( float(lista[5]) )
            i=0
            if len(out_data[1]) > 200:
                out_data[1].pop(0)
            


# Funci�n que actualizar� los datos de la gr�fica
# Se llama peri�dicamente desde el 'FuncAnimation'
def update_line(num, hl, data):
    hl.set_data(range(len(data[1])), data[1])
    return hl,

# Configuramos la funci�n que "animar�" nuestra gr�fica
line_ani = animation.FuncAnimation(fig, update_line, fargs=(hl, gData),
    interval=50, blit=False)

# Configuramos y lanzamos el hilo encargado de leer datos del serial
dataCollector = threading.Thread(target = GetData, args=(gData,5,))
dataCollector.start()
plt.show()

#dataCollector.join()
            
