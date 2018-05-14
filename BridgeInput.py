# -*- coding: utf-8 -*-
#!/usr/bin/env python

import threading
import time
import pygame
import math

from BridgeConf import *
import winsound     # Audio Feedback
import subprocess
#from BridgeDialog import *
from BridgeConf import *
from BridgeGUI import Dialog_Error
#from BridgeDialog import DialogError
import BridgeGUI

import wx
from wx.lib.wordwrap import wordwrap
#from wx.lib.pubsub import setuparg1 #evita problemi con py2exe
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub as Publisher

import speech_recognition as sr

" ################################ "
" # JOYSTICK UPDATE THREAD CLASS # "
" ################################ "

class Thread_InputClass(threading.Thread):
    def __init__(self, Name, Bridge, Coord, BT):

        threading.Thread.__init__(self, name=Name)
        self.Running            = False
        self.Name               = Name
        self.Bridge             = Bridge
        self.Coord              = Coord
        self.BT                 = BT

        self.AudioPath          = os.getcwd() + '\\Assets\\Audio\\'

        self.PyJoystick         = None

        self.VocalCmd           = None


        " Variabili per il riconoscimento vocale "
        self.r                          = sr.Recognizer()
        #self.r.energy_threshold         = 4000
        self.r.dynamic_energy_threshold = False


        " Variabili per il controllo dei cicli "
        self.VOCAL_IDLE                 = 0
        self.VOCAL_RUNNING_CONFERMATION = 1     # wait for running confermation
        self.VOCAL_RUNNING              = 2
        self.VOCAL_STOP_CONFERMATION    = 3     # wait for running confermation
        self.VOCAL_HELP                 = 4

        self.VocalStatus                = self.VOCAL_IDLE

        " Variabili per controllo 'step' "
        self.VocalSteps                 = self.Bridge.Control.VocalMaxSteps

        " Variabili per la memorizzazione " # TODO: SAVED POS
        self.var_mem                    = ['0', '0', '0', '0', '0']
        self.NumVarMem                  = 0
        self.vm                         = 4*[0]

        self.Step_Param                  = [1, 5, 20]
        self.Speed_Param                 = []

        " Dizionari "
        self.instr_dict    = {'fer':'fermo', 'rip':'riposo', 'mem':'memorizza', 'dor':'dormi', 'ter':'termina'}
        self.direction_dict = {'sin':[0,0.5,0,0], 'des':[0,-0.5,0,0], 'sal':[0,0,0.5,0], 'sce':[0,0,-0.5,0], 'ava':[0.5,0,0,0], 'ind':[-0.5,0,0,0]}
        self.step_dict      = {'spostamento picc': self.Step_Param[0], 'spostamento medi': self.Step_Param[1], 'spostamento gran': self.Step_Param[2]}
        self.speed_dict = {'velocità picc': self.Step_Param[0], 'velocità medi': self.Step_Param[1], 'velocità gran': self.Step_Param[2]}

    def run(self):

        print '* Input Thread Run'


        " Human-Machine Interfaces Initialization"

        for i in range(len(self.Bridge.InputList)):  # InputList is defined a priori in Conf.ini (HMIs to be used)

            if self.Bridge.InputList[i] == 'Joystick':

                try:
                    print '+ Joystick Interface'
                    " Init pygame "
                    pygame.init()

                    " Count available joysticks "
                    if pygame.joystick.get_count() == 0:
                        print '# Warning: Joystick missing'
                        wx.CallAfter(Publisher.sendMessage, "ShowDialogError", msg = "# Warning: Joystick missing")
                        return

                    " Init Joystick "
                    pygame.display.init()
                    pygame.joystick.init()
                    self.PyJoystick = pygame.joystick.Joystick(0)
                    self.PyJoystick.init()
                    " Update input info in main window "
                    wx.CallAfter(Publisher.sendMessage, "UpdateInputInfo")
                    self.Bridge.Joystick.Initialized = True

                except Exception, e:

                    print '# Error: Pygame initialization failed | ' + str(e)
                    wx.CallAfter(Publisher.sendMessage, "ShowDialogError", msg = "# Error: Pygame initialization failed")
                    self.Bridge.Joystick.Initialized = False
                    return

            elif self.Bridge.InputList[i] == 'Vocal':
                print '+ Vocal Interface'
                " Introduzione controllo vocale "

                try:
                    with sr.Microphone() as source:
                        self.r.adjust_for_ambient_noise(source)
                    # winsound.PlaySound(self.AudioPath + 'Jarvis.wav', winsound.SND_FILENAME)
                    # au_file = audio_file+'Jarvis.wav'
                    # return_code = subprocess.call(["afplay", au_file])
                    " Update input info in main window "
                    wx.CallAfter(Publisher.sendMessage, "UpdateInputInfo")

                except Exception, e:
                    print '# Error: Init Embedded Vocal failed' + str(e)
                    " Update input info in main window "
                    return False

            elif self.Bridge.InputList[i] == 'Visual':
                print '+ Visual Interface'
            else:
                print '# Error: Not implemented interface: ' + self.Bridge.InputList[i]
                wx.CallAfter(Publisher.sendMessage, "ShowDialogError", msg = "# Error: Not implemented interface")


        self.Running = True

        while self.Running:

            if self.Bridge.Control.Input == "Joystick" and self.Bridge.Joystick.Initialized:

                self.Bridge.Control.FIRST_RUN = 1
                self.VocalStatus = self.VOCAL_IDLE
                events = pygame.event.get()

                #ALE: comunico all'app qual è il piano di lavoro corrente per aggiornare l'icona dedicata
                if self.Bridge.Status== RUNNING and self.Bridge.Control.BTenabled:
                            self.BT.SendMessage("Axis-joy:"+str(self.Bridge.Joystick.Mode))

                " If a joystick event occurred "
                for event in events:
                    if event.type == pygame.QUIT:
                        self.terminate()

                    elif event.type == pygame.JOYBUTTONUP:
                        pass

                    elif event.type == pygame.JOYBUTTONDOWN:

                        if self.PyJoystick.get_button(0):

                            if self.Bridge.Joystick.Mode:
                                self.Bridge.Joystick.Mode = 0
                                print '* Change Plane Button: X-Y'
                                winsound.Beep(880, 500)

                            else:
                                self.Bridge.Joystick.Mode = 1
                                print '* Change Plane Button: Z'
                                winsound.Beep(440, 500)

                        #self.Bridge.Joystick.SavePosition         = self.PyJoystick.get_button(2)
                        #self.Bridge.Joystick.GotoSavedPosition    = self.PyJoystick.get_button(3)
                        #self.Bridge.Joystick.Alarm                = self.PyJoystick.get_button(4)

                        " Update input info in main window "
                        wx.CallAfter(Publisher.sendMessage, "UpdateInputInfo")

                    elif event.type == pygame.JOYAXISMOTION:

                        for i in range (0,2):
                            axis = ( - self.PyJoystick.get_axis(i) + self.Bridge.Joystick.AxisOffset[i])

                            " Remove Deadband"
                            if abs(axis) < 0.05:
                                axis = 0.0

                            " Calibrated Joystick Acquisition " # 0:Forward 1:Backward 2:Right 3:Left
                            if self.Bridge.Joystick.Mode: # Z axis

                                self.Coord.p0[0] = 0.0
                                self.Coord.p0[1] = 0.0

                                if i == 1:  # Z axis
                                    if axis > 0:
                                        self.Coord.p0[2] = axis/self.Bridge.Patient.JoystickCalibration[0] # Forward
                                    else:
                                        self.Coord.p0[2] = axis/self.Bridge.Patient.JoystickCalibration[1]  # Backward
                                else:       # Theta 5
                                    self.Coord.p0[3] = 0

                            else: # X-Y axis

                                if i == 1: # X axis
                                    if axis > 0:
                                        self.Coord.p0[0] = axis/self.Bridge.Patient.JoystickCalibration[0]  # Forward
                                    else:
                                        self.Coord.p0[0] = axis/self.Bridge.Patient.JoystickCalibration[1]  # Backward
                                else: # Y axis
                                    if axis > 0:
                                        self.Coord.p0[1] = -axis/self.Bridge.Patient.JoystickCalibration[2] # Left
                                    else:
                                        self.Coord.p0[1] = -axis/self.Bridge.Patient.JoystickCalibration[3]  # Right

                                self.Coord.p0[2] = 0.0
                                self.Coord.p0[3] = 0.0



                        " Update input info in main window "
                        wx.CallAfter(Publisher.sendMessage, "UpdateInputInfo")

                pygame.event.clear()

            elif self.Bridge.Control.Input == "Vocal":

                if self.Bridge.Control.FIRST_RUN:
                    # TODO: SISTEMARE VOCAL
                    " Introduzione controllo vocale "
                    winsound.PlaySound(self.AudioPath + 'Jarvis.wav', winsound.SND_FILENAME)
                    # au_file = audio_file+'Jarvis.wav'
                    # return_code = subprocess.call(["afplay", au_file])
                    self.Bip()
                    self.Bridge.Control.FIRST_RUN = False
                else:
                    " Get command "
                    #self.Bridge.Control.Listen = 1
                    if self.Bridge.Control.Listen:

                        #self.Bridge.Control.Listen = 0
                        print "Listening on Laptop... "
                        self.Bridge.Control.jarvis_cmd = self.WaitForInstructions()
                        print "Recognized ", self.Bridge.Control.jarvis_cmd

                    self.Bridge.Control.jarvis_cmd = self.Bridge.Control.jarvis_cmd.lower()


                    " ################### "
                    " VOCAL STATE MACHINE "
                    " ################### "

                    if self.Bridge.Control.jarvis_cmd[0:4] == 'aiut':
                        self.Bridge.Control.jarvis_cmd=""
                        print '*** ALLARME!'
                        self.VocalStatus = self.VOCAL_HELP

                    elif 'termina' in self.Bridge.Control.jarvis_cmd:
                        self.Bridge.Control.jarvis_cmd = ""
                        self.VocalStatus = self.VOCAL_STOP_CONFERMATION
                        winsound.PlaySound(self.AudioPath + 'ConfermaSpegnimento.wav', winsound.SND_FILENAME)
                        # au_file = audio_file+'ConfermaSpegnimento.wav'
                        # return_code = subprocess.call(["afplay", au_file])
                        self.Bip()

                    elif self.VocalStatus == self.VOCAL_IDLE:

                        if 'jarvis' in self.Bridge.Control.jarvis_cmd:

                            winsound.PlaySound(self.AudioPath + 'ConfermaAttivazione.wav', winsound.SND_FILENAME)
                            print "vero o falso?"
                            self.Bridge.Control.jarvis_cmd=""
                            # au_file = audio_file + 'ConfermaAttivazione.wav'
                            # return_code = subprocess.call(["afplay", au_file])
                            self.Bip()

                            self.VocalStatus = self.VOCAL_RUNNING_CONFERMATION

                        elif 'dormi' in self.Bridge.Control.jarvis_cmd:
                            self.Bridge.Control.jarvis_cmd = ""
                            self.VocalStatus = self.VOCAL_IDLE

                    elif self.VocalStatus == self.VOCAL_RUNNING_CONFERMATION:

                        if self.Bridge.Control.jarvis_cmd == 'vero':
                            self.Bridge.Control.jarvis_cmd = ""
                            print '*** CONTROLLO VOCALE ATTIVATO ***'
                            winsound.PlaySound(self.AudioPath + 'SonoAttivo.wav', winsound.SND_FILENAME)
                            # au_file = audio_file+'SonoAttivo.wav'
                            # return_code = subprocess.call(["afplay", au_file])
                            self.Bip()

                            self.VocalStatus = self.VOCAL_RUNNING

                        elif self.Bridge.Control.jarvis_cmd == 'falso':
                            self.Bridge.Control.jarvis_cmd = ""
                            print '*** CONTROLLO VOCALE DISATTIVATO ***'
                            winsound.PlaySound(self.AudioPath + 'Dormi2.wav', winsound.SND_FILENAME)
                            # au_file = audio_file + 'Dormi2.wav'
                            # return_code = subprocess.call(["afplay", au_file])
                            self.Bip()

                            self.VocalStatus = self.VOCAL_IDLE

                        elif not self.Bridge.Control.jarvis_cmd=="":

                            print '*** COMANDO VOCALE NON VALIDO ***'
                            self.Bridge.Control.jarvis_cmd = ""
                            winsound.PlaySound(self.AudioPath + 'IstruzioneNonValida.wav', winsound.SND_FILENAME)
                            # au_file = audio_file+'IstruzioneNonValida.wav'
                            # return_code = subprocess.call(["afplay", au_file])
                            self.Bip()
                            pass

                    elif self.VocalStatus == self.VOCAL_RUNNING:

                        " Parse command "
                        if not self.Bridge.Control.jarvis_cmd == "":
                            self.CommandRecognition(self.Bridge.Control.jarvis_cmd)
                            self.Bridge.Control.jarvis_cmd = ""

                        if self.VocalCmd == 'dormi':
                            winsound.PlaySound(self.AudioPath + 'Dormi.wav', winsound.SND_FILENAME)
                            # au_file = audio_file+'Dormi.wav'
                            # return_code = subprocess.call(["afplay", au_file])
                            self.Bip()
                            self.VocalStatus = self.VOCAL_IDLE

                        elif self.VocalCmd == 'memorizza':
                            self.Bridge.Control.jarvis_cmd = ""
                            '''
                            winsound.PlaySound('Memorizza.wav', winsound.SND_FILENAME)
                            self.Bip()
                            self.running_3 = True
    
                            print '*** Vuoi memorizzare questa posizione come nuovo comando? [Vero/Falso] ***'
                            conf_memo = self.WaitForInstructions()                          
                            print conf_memo
    
                            if conf_memo == 'falso':
                                self.running_3 = False
                                self.Bip()
    
                            elif conf_memo == 'vero':
                                self.Memorizza()
    
                            elif conf_memo[0:4] == 'aiut':
                                print '*** ALLARME!'
                                self.Coord.VocalCtrlPos = 'aiuto'
                                self.running_VocalControl = False
                                self.running_2 = False
                                self.running_3 = False
    
                            else :
                                self.running_3 = False
                                self.Bip()
                            '''

                    elif self.VocalStatus == self.VOCAL_STOP_CONFERMATION:
                        if Bridge.Control.jarvis_cmd == 'vero':
                            self.Bridge.Control.jarvis_cmd = ""
                            print '*** CONTROLLO VOCALE TERMINATO ***'
                            winsound.PlaySound(self.AudioPath + 'Spegnimento.wav', winsound.SND_FILENAME)
                            # au_file = audio_file+'Spegnimento.wav'
                            # return_code = subprocess.call(["afplay", au_file])
                            self.Bip()

                            self.VocalStatus = self.VOCAL_IDLE
                            self.terminate()

                        elif Bridge.Control.jarvis_cmd == 'falso':
                            self.Bridge.Control.jarvis_cmd = ""
                            print '*** CONTROLLO VOCALE ATTIVO ***'
                            winsound.PlaySound(self.AudioPath + 'Jarvis.wav', winsound.SND_FILENAME)
                            # au_file = audio_file+'Dormi2.wav'
                            # return_code = subprocess.call(["afplay", au_file])
                            self.Bip()
                            self.VocalStatus = self.VOCAL_IDLE
                        else:
                            if not self.Bridge.Control.jarvis_cmd == "":
                                print '*** COMANDO VOCALE NON VALIDO ***'
                                winsound.PlaySound(self.AudioPath + 'IstruzioneNonValida.wav', winsound.SND_FILENAME)
                                # au_file = audio_file+'IstruzioneNonValida.wav'
                                # return_code = subprocess.call(["afplay", au_file])
                                self.Bip()

                    elif self.VocalStatus == self.VOCAL_HELP:
                        # TODO: VOCAL HELP
                        print 'TODO: VOCAL_HELP'
                        time.sleep(1)

            time.sleep(0.1)

        print '- Input Thread Out'

    " Funzione di riconoscimento dei comandi che può essere personalizzata -> customizzazione "

    def CommandRecognition(self, instr):

        " instr_dict "
        # 'fer': 'fermo'
        # 'rip': 'riposo'
        # 'mem': 'memorizza'
        # 'dor': 'dormi'

        " direction_dict "
        # 'sin':[-1, 0, 0, 0]
        # 'des':[ 1, 0, 0, 0]
        # 'sal':[ 0, 0,-1, 0]
        # 'sce':[ 0, 0, 1, 0]
        # 'ava':[ 0,-1, 0, 0]
        # 'ind':[ 0, 1, 0, 0]

        " step_dict "
        # 'spostamento picc': self.Step_Param[0]
        # 'spostamento medi': self.Step_Param[1]
        # 'spostamento gran': self.Step_Param[2]


        self.Coord.p0                       = [0,0,0,0]
        self.Bridge.Control.VocalStepsCnt   = 0

        self.VocalCmd = None

        if instr[0:3] in self.instr_dict:
            " ############## "
            " VOCAL COMMANDS "
            " ############## "
            self.VocalCmd   = self.instr_dict[instr[0:3]]

            if self.VocalCmd == 'fermo' or self.VocalCmd == 'termina':
                self.Coord.p0 = [0,0,0,0]

        elif instr[0:3] in self.direction_dict:

            " ########## "
            " DIRECTIONS "
            " ########## "

            " Rest VocalComand "
            self.VocalCmd   = None
            " Update p0 coordinates "
            self.Coord.p0   = self.direction_dict[instr[0:3]]

        elif instr[0:16] in self.step_dict:
            " ##### "
            " STEPS "
            " ##### "
            self.Bridge.Control.VocalSteps = self.step_dict[instr[0:16]]
            print 'Numero di step selezionati: ', self.Bridge.Control.VocalSteps

        elif instr == self.var_mem[0]:
            print '*** Vado a',self.var_mem[0],'***'
            #self.Coord.VocalCtrlPos = 'memo1'

        elif instr == self.var_mem[1]:
            print '*** Vado a',self.var_mem[1],'***'
            #self.Coord.VocalCtrlPos = 'memo2'

        elif instr == self.var_mem[2]:
            print '*** Vado a',self.var_mem[2],'***'
            #self.Coord.VocalCtrlPos = 'memo3'

        elif instr == self.var_mem[3]:
            print '*** Vado a',self.var_mem[3],'***'
            #self.Coord.VocalCtrlPos = 'memo4'

        elif instr == self.var_mem[4]:
            print '*** Vado a',self.var_mem[4],'***'
            #self.Coord.VocalCtrlPos = 'memo5'
       
        elif not instr== "" :
            print '*** Istruzione non valida ***'
            self.Bridge.Control.jarvis_cmd=""
            winsound.PlaySound('IstruzioneNonValida.wav', winsound.SND_FILENAME)
            # au_file = audio_file+'IstruzioneNonValida.wav'
            # return_code = subprocess.call(["afplay", au_file])
            self.Bip()

        " Update input info in main window "
        wx.CallAfter(Publisher.sendMessage, "UpdateInputInfo")


    def WaitForInstructions(self):

        with sr.Microphone() as source:
            try:
                cmd = self.r.listen(source, phrase_time_limit = 2)
                print '+ Microphone Record called.'
                #cmd = self.r.record(source, duration=2)
                self.Bridge.Control.Status = POS_CTRL

                # TODO: evitare deadlock "
                # metto al massimo il numero di step fatti così interrompo il ciclo
                #ALE
                self.Bridge.Control.VocalStepsCnt = self.Bridge.Control.VocalSteps

                try:
                    print '+ Recognize Google called.'
                    instruction = self.r.recognize_google(cmd, language = "it-IT")
                except Exception, e:
                    instruction = 'Recognition Failed'
                    print '# ERROR: Speech Recognition Failed ' + str(e)

                return instruction

            except Exception, e:
                instruction = 'Listen Failed'
                print str(e)

    def Bip(self):
        Freq    = 700 # Set Frequency To 2500 Hertz
        Dur     = 950 # Set Duration To 1000 ms == 1 second
        winsound.Beep(Freq,Dur)

    def terminate(self):
        " Exit the thread "
        self.Running = False

" ############################## "
" # JOYSTICK CALIBRATION CLASS # "
" ############################## "

class Thread_JoystickCalibrationClass(threading.Thread):

    def __init__(self, Name, Bridge, Conf, direction):

        threading.Thread.__init__(self)
        self.Running = False
        self.Bridge = Bridge
        self.Conf   = Conf
        self.direction= direction # 0:Forward 1:Backward 2:Right 3:Left


    def run(self):

        self.Running = True

        if self.direction <= 1:
            i=1
        else:
            i=0

        self.Bridge.Patient.JoystickCalibration[self.direction] = 0

        try:

            self.PyJoystick = pygame.joystick.Joystick(0)
            self.PyJoystick.init()

            while self.Running:

                axis = ( - self.PyJoystick.get_axis(i) + self.Bridge.Joystick.AxisOffset[i])


                if abs(axis) > self.Bridge.Patient.JoystickCalibration[self.direction]:

                    self.Bridge.Patient.JoystickCalibration[self.direction] = abs(axis)
                    print axis

            print str(self.direction) + ': ' + str(self.Bridge.Patient.JoystickCalibration[self.direction])

            #self.Conf.SavePatient(self.Bridge.Patient.Filename, self.Bridge.Patient)
            wx.CallAfter(Publisher.sendMessage, "UpdateJoystickCalibrationInfo")

        except Exception, e:

            print '# ERROR: Joystick failure | ' + str(e)
            wx.CallAfter(Publisher.sendMessage, "ShowDialogError", msg="# Error: Joystick failure")
            self.Running = False
            return


    def terminate(self):

        self.Running = False
