#RupuControlerV5

import tkinter as tk #PIP
import customtkinter #I

from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #pip
import time as tm

import socket

##-------------------------
import matplotlib.pyplot as plt #descargar
import matplotlib.animation as animation
import threading 
#Librerias
import sys
import paho.mqtt.client as mqtt #descargar #install
import pymysql #descargar
import csv


UDP_IP_TX =""
UDP_PORT_TX = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP

##---------------------------------------------------------
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)

UDP_IP_RX = IPAddr # ip del computador que recibe datos (mismo que el que corre este script)
UDP_PORT_RX = 1234

#UDP
sock_RX = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_RX.bind((UDP_IP_RX, UDP_PORT_RX))

#---------------------------------------------------------
file_name = "monitortest.csv"  # archivo csv
texto = open(file_name,'w')
#estado = "T,"+String(Input_d)+","+String(d_ref)+","+String(vel_ref)+","+String(Input_vel)+","+String(Input_theta)+","+String(Output_d)+","+String(Output_vel)+","+String(Output_theta);
 
texto.write('Robot,Delta_muestra,Input_d,d_ref,vel_ref,Input_vel,Input_theta,Output_d,Output_vel,Output_theta'+'\n')
texto.close()

min_v = 0
max_v = 30

min_d = 5
max_d = 25

gData1 = [[0], [0]]
gData2 = [[0], [0]]
gData3 = [[0], [0]]

flag_save=True

class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.layout()
        """
        En esta sección se crean la pestaña 
        Configuración: Entrada de IP
        Control: Muestra el panel de control
        """
    
    def layout(self):
        self.title("RÜPÜ Controller")
        self.geometry("700x800+0+0") 
        
        self.letras_sugeridas =["L","S","T","O"]
        
        #Tamaño Grilla
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(1,weight=1)
        
        #-----Pestañas-------#
        
        #Definir pestañas principales
        self.tabview=customtkinter.CTkTabview(self)#puede ser un self.frame
        self.tabview.pack(padx=20,pady=20,expand=True,fill='both')
        self.tabview.add("Configuración")
        self.tabview.add("Control")
        
        #----Contenido Tab Configuración---#
        self.tabviewConfig = customtkinter.CTkFrame(self.tabview.tab("Configuración"),fg_color='transparent')
        self.tabviewConfig.pack(padx=0,pady=0,expand=True,fill='both')
       
        #label vacía
        self.empty1 = customtkinter.CTkLabel(self.tabviewConfig, text= "         ", fg_color="transparent")
        self.empty1.grid(row=1, column=0, padx=5, pady=5)
       
        #Ingresar IP Monitor          
        self.monitor_ip_label = customtkinter.CTkLabel(self.tabviewConfig, text= "IP Monitor:", fg_color="transparent")
        self.monitor_ip_label.grid(row=0, column=1, padx=5, pady=5)
        
        self.monitor_ip_entry = customtkinter.CTkEntry(self.tabviewConfig)
        self.monitor_ip_entry.grid(row=0, column=2, padx=5, pady=5)
        self.monitor_ip_entry.insert(customtkinter.END,IPAddr)
        
        #Ingresar Número de Robots
        self.num_label = customtkinter.CTkLabel(self.tabviewConfig, text="Número de robots")
        self.num_label.grid(row=1, column=1, padx=5, pady=5)

        self.entry_num = customtkinter.CTkComboBox(self.tabviewConfig, values=["1", "2","3","4","5","6"])
        self.entry_num.grid(row=1, column=2, padx=5, pady=5)
        self.entry_num.set("1") 
        
        #Lista que guarda IP y Label ingresada
        self.ip_entry_widgets = []
        
        #Botón Ok (Ingresa IP y número de robots)
        self.submit_button = customtkinter.CTkButton(self.tabviewConfig, text="Ok", command=self.create_ip_entries)
        self.submit_button.grid(row=1, column=3, padx=5, pady=5) # Updated column value

        #Botones Calibrar y Controlar
        self.calibrar_button = customtkinter.CTkButton(self.tabviewConfig, width = 80,text="Calibrar", command=self.clickCalibrarButton)
        self.guardar_button = customtkinter.CTkButton(self.tabviewConfig, width = 80,text="Guardar IP", command=self.clickGuardarButton)
        
        #-----------------Contenido Tab Control----------#
        self.tabviewControl = customtkinter.CTkFrame(self.tabview.tab("Control"),fg_color='transparent')
        self.tabviewControl.pack(padx=0,pady=0,expand=True,fill='both')             
        
        self.tabviewControlFrame =customtkinter.CTkFrame(self.tabviewControl,fg_color='transparent')
        self.tabviewControlFrame.grid(row=0,column=0)
        
        self.empty2 = customtkinter.CTkLabel(self.tabviewControlFrame, text= "         ", fg_color="transparent")
        self.empty2.grid(row=0, column=0, padx=5, pady=5)
        
        self.switch_var = customtkinter.StringVar(value="off")
        self.switch = customtkinter.CTkSwitch(self.tabviewControlFrame, text="Estado Robot", command=self.switch_event,variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch.grid(row=0, column=2, padx=10, pady=10)

        self.switchSave_var = customtkinter.StringVar(value="1")
        self.savetext ="Guardar "+ file_name
        self.switchSave = customtkinter.CTkSwitch(self.tabviewControlFrame, text=self.savetext, command=self.switchSave_event,variable=self.switchSave_var, onvalue="1", offvalue="0")
        self.switchSave.grid(row=0, column=3, padx=10, pady=10)
             
             
        #crear lista de letras desplegable
                    
        self.labelRobot = customtkinter.CTkLabel(self.tabviewControlFrame, text="Etiqueta robot:")
        self.labelRobot.grid(row=2, column=2, padx=10, pady=10) 
        
        self.selected_letter = customtkinter.StringVar()

        self.letras_lista=[]
    
        self.letter_combobox = customtkinter.CTkComboBox(self.tabviewControlFrame, values=self.letras_lista,variable=self.selected_letter)
        self.letter_combobox.set("L")
        self.letter_combobox.grid(row=2, column=3, padx=10, pady=10)

        
        # Posicionar los sliders y labels
        labelV = customtkinter.CTkLabel(self.tabviewControlFrame, text="Velocidad")
        sliderV = customtkinter.CTkSlider(self.tabviewControlFrame, from_=min_v, to=max_v, orientation="horizontal",state="normal")
        sliderV.bind("<ButtonRelease-1>", lambda event: self.updateValueV(sliderV.get(),self.getIP(self.letter_combobox.get())))
        self.labelVvalue = customtkinter.CTkLabel(self.tabviewControlFrame, text=str(round(sliderV.get())), fg_color="transparent")
        

        labelV.grid(row=3, column=2, columnspan=1, padx=10, pady=10)
        sliderV.grid(row=3, column=3, padx=10, pady=10)
        self.labelVvalue.grid(row=3, column=5, columnspan=1, padx=10, pady=10)
        

        labelD = customtkinter.CTkLabel(self.tabviewControlFrame, text="Distancia")
        sliderD = customtkinter.CTkSlider(self.tabviewControlFrame, from_=min_d, to=max_d, orientation="horizontal",state="normal")
        sliderD.bind("<ButtonRelease-1>", lambda event: self.updateValueD(sliderD.get(),self.getIP(self.letter_combobox.get())))
        self.labelDvalue = customtkinter.CTkLabel(self.tabviewControlFrame, text=str(round(sliderV.get())), fg_color="transparent")
        
        labelD.grid(row=4, column=2, columnspan=1, padx=10, pady=10)
        sliderD.grid(row=4, column=3, padx=10, pady=10)
        self.labelDvalue.grid(row=4, column=5, columnspan=1, padx=10, pady=10)
        
       
        #######SUB PESTAÑAS CONTROLADOR #####
        self.subTabView=customtkinter.CTkTabview(self.tabviewControl)
        self.subTabView.grid(column=0,padx=10, pady=10,sticky='ew')
        self.subTabView.add("Theta")
        self.subTabView.add("Velocidad")
        self.subTabView.add("Distancia")
        
        self.subTabVel =customtkinter.CTkFrame(self.subTabView.tab("Velocidad"),fg_color='white')
        self.subTabVel.pack(padx=0,pady=0,expand=True,fill='both') 
    
        self.subTabDist =customtkinter.CTkFrame(self.subTabView.tab("Distancia"),fg_color='white')
        self.subTabDist.pack(padx=0,pady=0,expand=True,fill='both') 
    
        self.subTabTheta =customtkinter.CTkFrame(self.subTabView.tab("Theta"),fg_color='white')
        self.subTabTheta.pack(padx=0,pady=0,expand=True,fill='both') 
    
        #----SUBTAB THETA---#
        self.label_P_th = customtkinter.CTkLabel(self.subTabTheta, text="P", fg_color="transparent")
        self.label_P_th.grid(row=0, column=0, padx=10, pady=10)    

        self.entry_P_th =  customtkinter.CTkEntry(self.subTabTheta)
        self.entry_P_th.grid(row=1, column=0, padx=5, pady=5)
        
        self.label_I_th = customtkinter.CTkLabel(self.subTabTheta, text="I", fg_color="transparent")
        self.label_I_th.grid(row=0, column=1, padx=10, pady=10)    

        self.entry_I_th =  customtkinter.CTkEntry(self.subTabTheta)
        self.entry_I_th.grid(row=1, column=1, padx=5, pady=5)
    
        self.label_D_th = customtkinter.CTkLabel(self.subTabTheta, text="D", fg_color="transparent")
        self.label_D_th.grid(row=0, column=2, padx=10, pady=10)    

        self.entry_D_th =  customtkinter.CTkEntry(self.subTabTheta)
        self.entry_D_th.grid(row=1, column=2, padx=5, pady=5)
    
        self.submit_theta_btn =customtkinter.CTkButton(self.subTabTheta, text="Enviar", command=self.submit_theta)
        self.submit_theta_btn.grid(row=2, column=1, padx=5, pady=5)
        
        #----SUBTAB Vel
        self.label_P_vel = customtkinter.CTkLabel(self.subTabVel, text="P", fg_color="transparent")
        self.label_P_vel.grid(row=0, column=0, padx=10, pady=10)    

        self.entry_P_vel =  customtkinter.CTkEntry(self.subTabVel)
        self.entry_P_vel.grid(row=1, column=0, padx=5, pady=5)
        
        self.label_I_vel = customtkinter.CTkLabel(self.subTabVel, text="I", fg_color="transparent")
        self.label_I_vel.grid(row=0, column=1, padx=10, pady=10)    

        self.entry_I_vel =  customtkinter.CTkEntry(self.subTabVel)
        self.entry_I_vel.grid(row=1, column=1, padx=5, pady=5)
    
        self.label_D_vel = customtkinter.CTkLabel(self.subTabVel, text="D", fg_color="transparent")
        self.label_D_vel.grid(row=0, column=2, padx=10, pady=10)    

        self.entry_D_vel =  customtkinter.CTkEntry(self.subTabVel)
        self.entry_D_vel.grid(row=1, column=2, padx=5, pady=5)
    
        self.submit_vel_btn =customtkinter.CTkButton(self.subTabVel, text="Enviar", command=self.submit_vel)
        self.submit_vel_btn.grid(row=2, column=1, padx=5, pady=5)
        
        #----SUBTAB Dist
        self.label_P_Dist = customtkinter.CTkLabel(self.subTabDist, text="P", fg_color="transparent")
        self.label_P_Dist.grid(row=0, column=0, padx=10, pady=10)    

        self.entry_P_Dist =  customtkinter.CTkEntry(self.subTabDist)
        self.entry_P_Dist.grid(row=1, column=0, padx=5, pady=5)
        
        self.label_I_Dist = customtkinter.CTkLabel(self.subTabDist, text="I", fg_color="transparent")
        self.label_I_Dist.grid(row=0, column=1, padx=10, pady=10)    

        self.entry_I_Dist =  customtkinter.CTkEntry(self.subTabDist)
        self.entry_I_Dist.grid(row=1, column=1, padx=5, pady=5)
    
        self.label_D_Dist = customtkinter.CTkLabel(self.subTabDist, text="D", fg_color="transparent")
        self.label_D_Dist.grid(row=0, column=2, padx=10, pady=10)    

        self.entry_D_Dist =  customtkinter.CTkEntry(self.subTabDist)
        self.entry_D_Dist.grid(row=1, column=2, padx=5, pady=5)
    
        self.submit_dist_btn =customtkinter.CTkButton(self.subTabDist, text="Enviar", command=self.submit_dist)
        self.submit_dist_btn.grid(row=2, column=1, padx=5, pady=5)


        self.monitor_button = customtkinter.CTkButton(self.tabviewControlFrame, text="Monitorear Señales", command=self.start_monitoring_vel)
        self.monitor_button.grid(row=8, column=2,columnspan=2, padx=10, pady=10)

    
    #Crea y guarda las entradas de IP y Label
    def submit_theta(self):
        for i in range(len(self.ip_entry_widgets)):
            UDP_IP_TX = self.ip_entry_widgets[i][0].get()
            MESSAGE = "E/co_p/" + str(self.entry_P_th.get())
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
            MESSAGE = "E/co_i/" + str(self.entry_I_th.get())
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
            MESSAGE = "E/co_d/" + str(self.entry_D_th.get())
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
            
    
    def submit_dist(self):
        for i in range(len(self.ip_entry_widgets)):
            UDP_IP_TX = self.ip_entry_widgets[i][0].get()
            MESSAGE = "E/cd_p/" + str(self.entry_P_dist.get())
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
            MESSAGE = "E/cd_i/" + str(self.entry_I_dist.get())
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
            MESSAGE = "E/cd_d/" + str(self.entry_D_dist.get())
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
    
    def submit_vel(self):
        for i in range(len(self.ip_entry_widgets)):
            UDP_IP_TX = self.ip_entry_widgets[i][0].get()
            MESSAGE = "E/cv_p/" + str(self.entry_P_vel.get())
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
            MESSAGE = "E/cv_i/" + str(self.entry_I_vel.get())
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
            MESSAGE = "E/cv_d/" + str(self.entry_D_vel.get())
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
            print(MESSAGE, UDP_IP_TX)      
        
    
    def create_ip_entries(self):
        label_vacia0 = customtkinter.CTkLabel(self.tabviewConfig, text=" ", fg_color="transparent")
        label_vacia0.grid(row=4, column=1, padx=10, pady=10)
            
        num_entries = int(self.entry_num.get())          
        sugerido=len(self.letras_sugeridas)
        for i in range(num_entries-sugerido):
            self.letras_sugeridas.append("")

        for i in range(num_entries):
            ip_label = customtkinter.CTkLabel(self.tabviewConfig, text=f'IP {i + 1}:')
            ip_label.grid(row=i + 3, column=1, padx=5, pady=5)

            ip_entry =  customtkinter.CTkEntry(self.tabviewConfig)
            ip_entry.grid(row=i + 3, column=2, padx=5, pady=5)
            ip_entry.insert(customtkinter.END,'192.168.1.10')
            
            letter_entry = customtkinter.CTkEntry(self.tabviewConfig)
            letter_entry.grid(row=i + 3, column=3, padx=5, pady=5)
            letter_entry.insert(customtkinter.END,self.letras_sugeridas[i])

            self.ip_entry_widgets.append((ip_entry, letter_entry))# [(ip1,letra1),(ip2,letra2),...]

        label_vacia = customtkinter.CTkLabel(self.tabviewConfig, text="", fg_color="transparent")
        label_vacia.grid(row=len(self.ip_entry_widgets) + 4, column=1, padx=5, pady=5)
    
    
            
        self.create_widgets()
            
            
    #Posiciona botones Calibrar y Controlar
    def create_widgets(self):
          
        self.calibrar_button.grid(row=len(self.ip_entry_widgets) + 5, column=1,columnspan=2, padx=5, pady=5)
        self.guardar_button.grid(row=len(self.ip_entry_widgets) + 5, column=3,columnspan=2, padx=5, pady=5)
       
    ######------Funciones de Control --------######    
    
    def clickCalibrarButton(self):
         for i in reversed(range(len(self.ip_entry_widgets))):
            UDP_IP_TX = self.ip_entry_widgets[i][0].get()
            UDP_PORT_TX = 1111
            MESSAGE = "E/calibrar/1"
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
            print("message:", MESSAGE, "IP:", UDP_IP_TX)
            tm.sleep(0.2)

    def clickGuardarButton(self):
        self.letras_lista = [entry[1].get() for entry in self.ip_entry_widgets]

        if len(self.letras_lista)>1:
            self.letras_lista.append("ALL")
    
        self.letter_combobox = customtkinter.CTkComboBox(self.tabviewControlFrame, values=self.letras_lista,variable=self.selected_letter)
        self.letter_combobox.set("L")
        self.letter_combobox.grid(row=2, column=3, padx=10, pady=10)
        #self.tabview.select(self.tabviewControlFrame)

            
        
            
    #Función Iniciar  
    def clickIniciarButton(self):
        UDP_IP_TX = self.ip_entry_widgets[0][0].get()
        UDP_PORT_TX = 1111

        MESSAGE = "E/parar/no"
        sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
        print("message:", MESSAGE, "IP:", UDP_IP_TX)
        tm.sleep(0.5)
        
        for i in range(len(self.ip_entry_widgets)-1):
            UDP_IP_TX = self.ip_entry_widgets[i+1][0].get()
            dist =10
            MESSAGE = "E/cd_ref/" + str(dist)
            print(MESSAGE, UDP_IP_TX)
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))

    # Función botón detener
    def clickStopButton(self):
        UDP_IP_TX = self.ip_entry_widgets[0][0].get()
        UDP_PORT_TX = 1111

        MESSAGE = "E/parar/si"
        sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
        print("message:", MESSAGE, "IP:",UDP_IP_TX)

    def switch_event(self):
        #print("switch toggled, current value:", self.switch_var.get())
        if self.switch_var.get() =="on":
            self.clickIniciarButton()
        else:
            self.clickStopButton()

    def switchSave_event(self):
        if self.switchSave_var.get() =="1":
            flag_save = True
        else:
            flag_save = False
            
            
    def updateValueV(self, value,IP):
        self.labelVvalue.configure(text="")
        self.labelVvalue=customtkinter.CTkLabel(self.tabviewControlFrame, text=str(round(value)), fg_color="transparent")
        self.labelVvalue.grid(row=3, column=5, columnspan=1, padx=10, pady=10)
        
        if IP != "ALL":
            UDP_IP_TX = IP
            UDP_PORT_TX = 1111
        
            MESSAGE = "E/cv_ref/" + str(round(value))
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
            print("message:", MESSAGE, "IP:",IP)
        else:
            for i in range(len(self.ip_entry_widgets)):
                UDP_IP_TX = self.ip_entry_widgets[i][0].get()
                UDP_PORT_TX = 1111
        
                MESSAGE = "E/cv_ref/" + str(round(value))
                print("message:", MESSAGE, "IP:",UDP_IP_TX)

                #sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
               
        
    
    def updateValueD(self, value, IP):
        self.labelDvalue.configure(text="")
        self.labelDvalue.grid(row=4, column=5, columnspan=1, padx=10, pady=10)
        self.labelDvalue.configure(text=str(round(value)))
        
        if IP != "ALL":
            UDP_IP_TX = IP
            UDP_PORT_TX = 1111

            MESSAGE = "E/cd_ref/" + str(round(value))
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
            print("message:", MESSAGE, "IP:",IP)

        else:
            for i in range(len(self.ip_entry_widgets)):
                UDP_IP_TX = self.ip_entry_widgets[i][0].get()
                UDP_PORT_TX = 1111
            

                MESSAGE = "E/cd_ref/" + str(round(value))
                print("message:", MESSAGE, "IP:",UDP_IP_TX)
                #sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP_TX, UDP_PORT_TX))
                
                
    
    def getIP(self,label):
        targetIP=""
        if label != "ALL":
            for entry in self.ip_entry_widgets:
                if entry[1].get() == label:
                    targetIP = entry[0].get()
            return targetIP
        else:
            return "ALL"
        

    def GetData(self, out_data,dato,figure):

        while True:
            data, addr = sock_RX.recvfrom(4096)
            testo = str(data.decode('utf-8'))
            lista = testo.split(",")
            print (self.switchSave_var.get())
            if int(self.switchSave_var.get()) :
                texto = open(file_name, "a")
                texto.write(testo+'\n')
                texto.close()
            #print(self.letter_combobox.get())
            #figure.suptitle("Señal robot " + self.letter_combobox.get(), fontsize=16)
            
            if lista[0] == self.letter_combobox.get():
                out_data[1].append(float(lista[dato]))
                if len(out_data[1]) > 100:
                    out_data[1].pop(0)


    def animate_vel(self):
        
        fig, axes = plt.subplots(3, 1, figsize=(8, 12))
        #fig.suptitle('Señales de monitoreo robot '+ self.letter_combobox.get(), fontsize=14) 
        plt.subplots_adjust(top=0.9, hspace=0.5)  

        lines = []

        for ax in axes:
            line, = ax.plot([], [])
            lines.append(line)

        axes[0].set_title('Velocidad', fontsize=12)
        axes[0].set_xlim(0, 100)
        axes[0].set_ylim(0, 30)

        axes[1].set_title('Distancia predecesor', fontsize=12)
        axes[1].set_xlim(0, 100)
        axes[1].set_ylim(0, 20)

        axes[2].set_title('Ángulo de orientación', fontsize=12)
        axes[2].set_xlim(0, 100)
        axes[2].set_ylim(-1, 1)
        
        """
        for ax in axes:
            ax.set_ylim(0, 30)
            ax.set_xlim(0, 200)
        """
        

        def update_line(num, lines, data):
            for line, d in zip(lines, data):
                line.set_data(range(len(d[1])), d[1])
            return lines
       
        line_ani = animation.FuncAnimation(fig, update_line, fargs=(lines, [gData1, gData2, gData3]),interval=50, blit=True, cache_frame_data=False)

        dataCollector1 = threading.Thread(target=self.GetData, args=(gData1, 5,fig))
        dataCollector2 = threading.Thread(target=self.GetData, args=(gData2, 2,fig))
        dataCollector3 = threading.Thread(target=self.GetData, args=(gData3, 6,fig))

        #dataCollector1.setDaemon(True)

        dataCollector1.start()
        dataCollector2.start()
        dataCollector3.start()


        fig.canvas.manager.window.wm_geometry("+1000+0")
        plt.show()
        
        
        def on_close(event):
            '''dataCollector1.join()  # Esperar a que el hilo termine
            dataCollector2.join()
            dataCollector3.join()
            sys.exit(0)  # Salir del programa'''

        # Configurar el evento de cierre de la ventana
        fig.canvas.mpl_connect('close_event', on_close)
        
        
            

    def start_monitoring_vel(self):
        self.animate_vel()    
    
    
    def on_closing(self):
        self.destroy()
        
customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("light")
app = App()
app.mainloop()