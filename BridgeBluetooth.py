# -*- coding: utf-8 -*-
#!/usr/bin/env python
import glob

from BridgeConf import *
from bluetooth 	import *
import time
import threading 
from BridgeJoint import *
from BridgeInput import*
from BridgeControl import*


import wx
from wx.lib.wordwrap import wordwrap
#from wx.lib.pubsub import setuparg1 #evita problemi con py2exe
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub as Publisher



class BluetoothClass:
    def __init__(self, Bridge, Conf, Coord):

        self.Bridge = Bridge
        self.Conf   = Conf
        self.Coord  = Coord
        self.ConnectionError= False


    def InputRecognition(self,data):

        self.data=data
        print "* Bluetooth Received: ", self.data

        if self.data[0:3].lower()=="ini": #la stringa inviata dall'app quando si preme il pulsante ini è : "Init-nome utente-interfaccia di controllo"
            #print "SATUS!!",self.Bridge.Status

            if self.Bridge.Status ==IDLE:
                FileName=self.data.split("-")[1]+'.ini' 
                self.Conf.Patient.Loaded = False
                self.Conf.ReadPatientFile(FileName) #leggo il file dell'utente selezionato

                if not self.Conf.Patient.Loaded:
                    self.SendMessage("Error reading file")
                
                else:
                    self.Bridge.Control.Input= self.data.split("-")[2] #imposto l'interfaccia di controllo
                    print self.Bridge.Control.Input
                    wx.CallAfter(Publisher.sendMessage, "ChangeButton", case = "init")
                    self.InitSystem() #avvio l'inizializzazione
            else:
                status = "BStatus:"+str(self.Bridge.Status)
                self.SendMessage(status)
                print "current Status: ", self.Bridge.Status

        elif self.data[0:2]== "ok": #la stringa "ok" arriva quando l'utente schiaccia sul pulsante "DONE" del dialog donning dall'app
            if not __debug__:
                self.Bridge.Status = REST_POSITION 
                wx.CallAfter(Publisher.sendMessage, "UpdateControlInfo")
            else:
                self.SendMessage("Rest Position") # se sono in debug comunico di aver comunque effettuato la rest position per poter passare alla schermata di controllo sull'app
                wx.CallAfter(Publisher.sendMessage, "ChangeButton", case = "ready")
                wx.CallAfter(Publisher.sendMessage, "UpdateControlInfo")
                print "ho inviato stringa rest position"

        elif self.data[0:5] =="Contr": #stringa che l'app invia quando è premuto il pulsante PLAY
            if self.Bridge.Status ==READY:

                if not __debug__:
                    " Verifica ROM giunti paziente & Run update threads "
                    threads_list = threading.enumerate()
                    for i in range(0, self.Bridge.JointsNum):
                        self.Bridge.Joints[i].Jmin = self.Bridge.Patient.Jmin[i]
                        self.Bridge.Joints[i].Jmax = self.Bridge.Patient.Jmax[i]

                        if not "JointUpdateThread" + str(i) in threads_list:
                            print 'JointUpdateThread: ', i
                            self.Bridge.JointUpdateThreads[i].start()
                self.Bridge.Status = RUNNING
                self.SendMessage("Running Ok")
                if self.Bridge.Control.Input=="Joystick":

                    time.sleep(0.2)
                    self.SendMessage("Axis-joy:" + str(self.Bridge.Joystick.Mode))

                wx.CallAfter(Publisher.sendMessage, "ChangeButton", case = "enable control")
                wx.CallAfter(Publisher.sendMessage, "UpdateControlInfo")


            elif self.Bridge.Status == RUNNING:
                self.SendMessage("Already Running")
            print "status running:", self.Bridge.Status
        elif self.data[0:4]=="Stop": # quando premo STOP dall'app
            self.SystemStop()
        elif self.data[0:5]=="vocIn": #stringa inviata quando il riconoscimento vocale dell'app ha riconosciuto una parola. "vocIn:parola riconosciuta"
            if self.Bridge.Control.Input == "Vocal" and self.Bridge.Status == RUNNING:
                self.Bridge.Control.jarvis_cmd = self.data.split(":")[1] #scrivo in jarvis cmd la parola riconosciuta--> verrà interpretata da Bridge Input
            if self.data.split(":")[1] == "vocale":
                self.Bridge.Control.Input = "Vocal"
                wx.CallAfter(Publisher.sendMessage, "UpdateControlInfo")
                wx.CallAfter(Publisher.sendMessage, "UpdateInputInfo")
                print 'Input: ' + self.Bridge.Control.Input
            elif self.data.split(":")[1] == "manuale":
                self.Bridge.Control.Input = "Joystick"
                wx.CallAfter(Publisher.sendMessage, "UpdateControlInfo")
                wx.CallAfter(Publisher.sendMessage, "UpdateInputInfo")
                print 'Input: ' + self.Bridge.Control.Input

    def SystemStop(self):

    
        threads_list = threading.enumerate()
        print threads_list

        try:
            for i in range(0, len(threads_list)):
                th = threads_list[i]
                if th.name != "MainThread"  and th.name != "BluetoothThread":
                    th.terminate()
        except Exception, e:
            print str(e)

        " Wait for the threads to end "
        for i in range(1,len(threads_list)):
            th = threads_list[i]
            if th.name != "MainThread"  and th.name != "BluetoothThread":
                th.join()
        " Disable Control Flag "
        self.Bridge.Status = READY
        wx.CallAfter(Publisher.sendMessage, "UpdateControlInfo")
        self.Bridge.Control.Status = IDLE

    def InitSystem(self):

        if not __debug__:

            if self.Conf.Serial.Error:
                print "Serial error"
                self.ConnectionError= True
                return
        else:
            self.Conf.Serial.Error= False

        if not self.BridgeInitialization():
            " If BridgeInitialization() fails, return with error dialog"
            print "init Failed"
            self.ConnectionError=True
            return

        if not __debug__:

            " Open Serial Ports "
            try:
                for i, J in zip(range(0, len(self.Bridge.Joints)), self.Bridge.Joints):
                    if J.OpenPort():
                        print '+ %s Connected' % J.CommPort
                        self.Conf.Serial.Connected[i] = True
                    else:
                        print '- Error: couldn\'t open %s.' % J.CommPort
                        return
            except:
                print "Error: COM init failed."
                self.ConnectionError = True
                return

            " Check if all COM are Connected "

            if all(i == True for i in self.Conf.Serial.Connected[0:self.Bridge.JointsNum]):
                self.Conf.Serial.AllConnected = True
                print "True All Connected"
            else:
                self.Conf.Serial.AllConnected = False
                print "False All Connected"
        else:
            self.Conf.Serial.AllConnected = True

        if self.Conf.Serial.AllConnected == True:

            print 'ok'
            " Get active threads "
            threads_list = threading.enumerate()
            controlThread_running = False
            inputThread_running = False

            for i in range(0, len(threads_list)):
                th = threads_list[i]
                if th.name == "ControlThread":
                    print '# Warning: ControlThread already running.'
                    controlThread_running = True

                if th.name == "InputThread":
                    print '# Warning: InputThread already running.'
                    inputThread_running = True

            " Run InputThread "
            if not inputThread_running:
                self.Bridge.InputThread.start()

            if not controlThread_running:
                self.Bridge.ControlThread.start()

            wx.CallAfter(Publisher.sendMessage, "UpdateControlInfo")
            wx.CallAfter(Publisher.sendMessage, "UpdateInputInfo")
            wx.CallAfter(Publisher.sendMessage, "StartTimer", msg = self.Conf.InputValuesRefreshTmr)

        else:

            if not __debug__:
                try:
                    " Close serial ports previously open "
                    for i, J in zip(range(0,self.Bridge.JointsNum), self.Bridge.Joints):
                        if self.Conf.Serial.Connected[i]:
                            J.ClosePort()
                            print '+ %s Disconnected' % J.CommPort
                            self.Conf.Serial.Connected[i] = False
                        else:
                            self.ConnectionError = True
                            print '- Error: couldn\'t close %s.' % J.CommPort
                except Exception, e:
                    self.ConnectionError = True
                    print 'Error  ' + str(e)
        
        if not self.ConnectionError: #se la connessione alle porte COM è andata a buon fine
            if not __debug__:
                self.Bridge.Status= INIT_SYSTEM #avvio inizializzazione se non sono in debug
                wx.CallAfter(Publisher.sendMessage, "UpdateControlInfo")
            else:
                self.Bridge.Status = READY #metto la macchina direttamente in READY se sono in DEBUG
                self.SendMessage("Init Done!") #Comunico comunque all'app che l'inizializzazione è stata fatta (comparirà comunque il dialog donning)
        else:
            self.SendMessage("Connection Error")

    def SendMessage(self, msg):

        try:
            self.Bridge.Control.BTclient_sock.send(msg)
        except IOError:
            print "send msg error"
            pass

    def BridgeInitialization (self):
        " Joints setup "

        print 'BridgeInitialization called.'

        for i in range(0, self.Bridge.JointsNum):
            self.Bridge.Joints[i]   = Joint(i+1,
                                            self.Conf.Serial.COM[i],
                                            self.Conf.Patient,
                                            self.Conf.Exo,
                                            self.Coord)
        " Copy patient to Bridge "

        self.Bridge.Patient         = self.Conf.Patient

        " Define control thread "

        self.Bridge.ControlThread = Thread_ControlClass("ControlThread", self.Bridge, self.Coord,self.Conf)
        self.Bridge.InputThread = Thread_InputClass("InputThread", self.Bridge, self.Coord, self)

        "Define Calibration"
        for i, J in zip(range(0,self.Bridge.JointsNum), self.Bridge.Joints):
            " Define joint init threads "
            self.Bridge.JointInitThreads[i]     = Thread_JointInitClass("JointInitThread" + str(i), J)
            " Define joint update threads "
            self.Bridge.JointUpdateThreads[i]   = Thread_JointUpdateClass("JointUpdateThread" + str(i), J, self.Coord, self.Bridge)

        return True

class Bluetooth_Thread(threading.Thread):

    def __init__(self, Name,Conf,Bridge,Coord,BT):

        threading.Thread.__init__(self, name= Name)
        self.Conf   = Conf
        self.Bridge = Bridge
        self.Coord  = Coord
        self.BT     = BT
        self.Running= True
        self.BTsocket=BluetoothSocket(RFCOMM)
        self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        self.k=0



    def run(self):

        self.BTsocket.bind(("",PORT_ANY)) #associo il socket a una porta seriale virtuale
        self.BTsocket.listen(1) 

        self.port = self.BTsocket.getsockname()[1]

        advertise_service(  self.BTsocket, "SampleServer",
                            service_id = self.uuid, #il socket sarà visibile con il suo uuid che sarà uguale all'uuid del client socket dell'app. In questo modo possono trovarsi e connettersi
                            service_classes = [SERIAL_PORT_CLASS ],
                            profiles = [ SERIAL_PORT_PROFILE ],)
                   
        print "Waiting for connection on RFCOMM channel %d" % self.port

        self.BTclient_sock, self.BTclient_info = self.BTsocket.accept() #accetto connessione dall'app, creo variabile BTclient_sock a lei associata
        self.Bridge.Control.BTclient_sock=self.BTclient_sock #copio i dati ottenuti nella variabile globale (in modo tale da inviare messaggi all'app anche da altri file)
        #print self.Bridge.Control.BTclient_sock
        #print self.BTclient_sock
        print "Accepted connection from ", self.BTclient_info
        self.Bridge.Control.BTenabled = True #flag globale che comunica che il PC è connesso all'app

       
        wx.CallAfter(Publisher.sendMessage, "UpdateControlInfo")

        #cerco file .ini nella cartella di lavoro
        file2="Name:"
        for file in glob.glob("*.ini"):
            file= file.replace('.ini','')

            if not file == "Conf":

                if file2 =="Name:":
                    file2 =file2+file
                else:
                    file2=file2+","+file

        print "file2: " , file2

        self.BT.SendMessage(file2) #invio i nomi dei file di configurazione all'app
        status = "BStatus:"+str(self.Bridge.Status)
        time.sleep(0.5)
        self.BT.SendMessage(status) #invio stato corrente di BRIDGE (per capire quale schermata aprire nell'app a connessione eseguita)

        try:
            while self.Running:
                self.data = self.Bridge.Control.BTclient_sock.recv(1024)
                #print("received [%s]" % self.data)
                self.BT.InputRecognition(self.data) #funzione di riconoscimento dei dati in ingresso
        except IOError:
            pass


    def terminate(self):
        self.Running=False
        self.BTsocket.close()
        try:
            self.Bridge.Control.BTclient_sock.close()
            print "Termino connessione BT"
        except Exception, e:
            print e

