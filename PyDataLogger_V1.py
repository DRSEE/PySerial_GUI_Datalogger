import serial
import serial.tools.list_ports
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.scrolledtext as st
import _thread
import sys
import rx_threading
import pathlib
from re import search


####INIT####
serialPort = rx_threading.SerialPort()
arduino_port = ""  #Default COM
baud = 0           #Default baud
tab = [1]
tab.remove(1)
liste = [1]
liste.remove(1)
tab_baud = (1200,1800,2400,4800,7200,9600,19200,38400,57600,115200,128000) #list of baudrate available
tab_file_format = ('.txt','.csv')

isopen = False


def show_ports():
    global strPort
    global tab
    global numConnection
    ports = serial.tools.list_ports.comports()
    numConnection = len(ports)
    for i in range(0,numConnection):
        port = ports[i]
        strPort = str(port)
        var = len(strPort)
        var = var - 5
        strPort = strPort[:-var]
        tab.append(strPort)
        print(strPort)

def reset_ports():
    tab.clear()
    show_ports()
    box['values']=(tab)

def open_com():
    global ret_box,ret_box_baud,isopen
    if ( (len(box.get()) == 0) or (len(box_baud.get()) == 0)):
        print("null parameter")
    else:
        if button_activate.cget("text") == 'Activer la com':
            isopen = True
            ret_box = box.get()
            ret_box_baud = box_baud.get()
            arduino_port = ret_box
            baud = ret_box_baud
            serialPort.Open(arduino_port,baud)
            scroll_input_data.configure(state ='normal')
            button_activate.config(text='Fermer la com')
        else:
            isopen = False
            serialPort.Close()
            scroll_input_data.configure(state ='disabled')
            button_activate.config(text='Activer la com')

def quitter():
    main.destroy()

def delete_data():
    if isopen == True:
        scroll_input_data.delete('1.0',END)
        liste.clear()
    else:
        liste.clear()
        scroll_input_data.configure(state ='normal')
        scroll_input_data.delete('1.0',END) 
        scroll_input_data.configure(state ='disabled')
        

        
def export_file():
        global ret_file_name,ret_format_file
        #b_export["state"] = DISABLED
        if ((len(nom_fichier.get()) == 0) or (len(scroll_input_data.get('1.0',END))== 0)):
            print("null parameter")
        else:
            ret_file_name = nom_fichier.get()
            ret_format_file = format_fichier.get() 
            FileName = (ret_file_name+""+ret_format_file) 
            file_check = pathlib.Path(FileName)
            print(FileName)
            if file_check.exists():
                scroll_input_data.configure(state ='normal')
                nom_fichier.delete(0,END)
                scroll_input_data.insert('1.0',"Fichier déjà existant \n")
                scroll_input_data.configure(state ='disabled')
            else:
                print("Création du fichier")
                print(liste[::-1])
                file = open(FileName,"a")
                for item in liste:
                    item = item.replace('\r\n','')
                    file.write("%s\n" % item)
                file.close()
                scroll_input_data.configure(state = 'normal')
                scroll_input_data.insert('1.0',"Création du fichier \n")
                scroll_input_data.configure(state = 'disabled')
            

show_ports()
##################[GUI]############################   

#Init page
main=Tk()
main.geometry("800x400+350+400")
main.title("Serial Data Logger By DRS")
main.iconbitmap('icon
                .ico')
main.resizable(False, False)
main['bg']= 'snow3'

#Menu principal
menu = Menu(main)
sousmenu= Menu(menu, tearoff=0)
menu.add_cascade(label="Menu",menu=sousmenu)
sousmenu.add_command(label="Quitter", command=quitter)
main.config(menu = menu)
#Menu Com
frame_config_com = Frame(main,width='195',height='200', relief='ridge', borderwidth=1,bg='snow2')
frame_config_com.pack(anchor='nw',padx="2",pady="2")
title_com = Label(frame_config_com,text="Paramètre de communication",bg='snow2',font=('bold',10))
title_com.pack()
title_com.place(x=8,y=0)
    #Bouton activation com & reset 
button_activate = Button(frame_config_com, text="Activer la com",command=open_com)
button_activate.pack()
button_activate.place(x=15,y=150)

button_delete = Button(frame_config_com,text="Reset data",command=delete_data)
button_delete.pack()
button_delete.place(x=115,y=150)
    #Menu déroulant choix com
box = ttk.Combobox(frame_config_com,width=15)
box['values']=(tab)

if numConnection >1:
    box.set(tab[1])
else:
    box.set(tab[0])

box.pack()
box.place(x=5,y=55)
    #Menu déroulant choix baudrate
box_baud = ttk.Combobox(frame_config_com,width=15)
box_baud['values']=(tab_baud)
box_baud.set(tab_baud[5]) #set default baudrate -> element 5 -> 9600
box_baud.pack()
box_baud.place(x=5,y=110)

    #Bouton com actualiser
b_rst = Button(main,text="Actualiser",command=reset_ports)
b_rst.pack(pady="5",padx="5")
b_rst.place(x=128,y=55)
    #Texte menu déroulant

title_com = Label(frame_config_com,text="Port COM:",bg='snow2')
title_com.pack()
title_com.place(x=4,y=34)

title_baud = Label(frame_config_com,text="Baudrate:",bg='snow2')
title_baud.pack()
title_baud.place(x=4,y=89)

#Menu print Serial data
frame_show_data = Frame(main, width='599',height='399',relief='groove',borderwidth=1)
frame_show_data.pack(pady="10",padx="4")
frame_show_data.place(x=200,y=0)
frame_show_data.configure(background="snow2")
title_data = Label(frame_show_data,text="Serial Data",bg='snow2')
title_data.pack()
title_data.place(x=280,y=0)
#sous menu print Serial data

scroll_input_data = st.ScrolledText(master=frame_show_data,width=72,height=23,relief='flat',borderwidth=1)
scroll_input_data.pack()
scroll_input_data.place(x=3,y=20)


def ReceivedData(message):
    global str_message
    str_message = message.decode("utf-8")
    scroll_input_data.insert('1.0',str_message)
    liste.append(str_message)



serialPort.startThread(ReceivedData)
        
def actualisation():
    main.after(250,actualisation)


#Menu Export files
frame_export_file = Frame(main,width='195',height='200',relief='ridge',borderwidth=1,bg='snow2')
frame_export_file.pack(anchor='sw',padx="2",pady="2")

title_file = Label(frame_export_file,text="Export fichier Datalogger",bg='snow2',font=('bold',10))
title_file.pack()
title_file.place(x=18,y=0)
    #Saisie nom fichier
nom_fichier = Entry(frame_export_file,width='15')
nom_fichier.pack()
nom_fichier.place(x=5,y=55)

title_nom_fichier = Label(frame_export_file,text="Nom du fichier:",bg='snow2')
title_nom_fichier.pack()
title_nom_fichier.place(x=4,y=34)

    #Saisie format fichier
format_fichier = ttk.Combobox(frame_export_file,width=15)
format_fichier['values']=(tab_file_format)
format_fichier.set(tab_file_format[1])
format_fichier.pack()
format_fichier.place(x=5,y=110)

title_format = Label(frame_export_file,text="Format d'export",bg='snow2')
title_format.pack()
title_format.place(x=4,y=89)

    #Bouton export fichier

b_export = Button(frame_export_file,text="Export Data",command=export_file)
b_export.pack()
b_export.place(x=60,y=140)


main.after(500, actualisation)
main.mainloop()
#########################[END GUI]##############################
