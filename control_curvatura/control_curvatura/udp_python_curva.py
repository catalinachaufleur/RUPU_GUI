"""
_____________________________________________________
|   -Conexion de UDP con la base de datos en MySQL  |
|    -Crear archivo CSV                             |
|---------------------------------------------------|

"""
#Librerias
import sys
#import pymysql
import csv
import socket
#Ajustables
file_name = "monitoreo.csv"  # archivo csv

UDP_IP = "192.168.1.101" # ip del computador que recibe datos (mismo que el que corre este script)
UDP_PORT = 1234
#UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
#creacion de archivo CSV
texto = open(file_name,'w')
#estado = "T,"+String(Input_d)+","+String(d_ref)+","+String(vel_ref)+","+String(Input_vel)+","+String(Input_theta)+","+String(Output_d)+","+String(Output_vel)+","+String(Output_theta);
 
texto.write('Robot,Delta_muestra,Input_d,d_ref,vel_ref,Input_vel,Input_theta,Output_d,Output_vel,Output_theta,curvatura,vel_crucero,curvatura_predecesor,control'+'\n')

texto.close()

while True:
    data, addr = sock.recvfrom(4096) # buffer size is 1024 byte
    testo = str(data.decode('utf-8'))
    lista = testo.split(",")
    texto = open(file_name,"a")
    texto.write(testo+'\n')
    texto.close()
    print(testo)
    
