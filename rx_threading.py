import serial
import _thread
import sys

class SerialPort:
    def __init__(self):
        self.ReceiveCallback = None
        self.isopen = False
        self.receivedMessage = None
        self.serialport = serial.Serial()

    def __del__(self):
        try:
            if self.serialport.is_open():
                self.serialport.close()
        except:
            print("Erreur de fermeture du port: ", sys.exc_info()[0] )

    def startThread(self,aReceiveCallback):
        self.ReceiveCallback = aReceiveCallback
        try:
            _thread.start_new_thread(self.SerialReadlineThread, ())
        except:
            print("Erreur de lecture du port: ", sys.exc_info()[0])

    def SerialReadlineThread(self):
        while True:
            try:
                if self.isopen:
                    self.receivedMessage = self.serialport.readline()
                    if self.receivedMessage != "":
                        self.ReceiveCallback(self.receivedMessage)
            except:
                print("Erreur de lecture du port: ", sys.exc_info()[0])

    def Open(self,portcom,baudrate):
        if not self.isopen:
            self.serialport.port = portcom
            self.serialport.baudrate = baudrate
            try:
                self.serialport.open()
                self.isopen = True
            except:
                print("Erreur d'ouverture du port: ", sys.exc_info()[0])


    def Close(self):
        if self.isopen:
            try:
                self.serialport.close()
                self.isopen = False
            except:
                print("Erreur de fermeture du port: ", sys.exc_info()[0])

 



