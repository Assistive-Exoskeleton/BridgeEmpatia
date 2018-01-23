# -*- coding: utf-8 -*-

import threading
import time
import pygame
import math
from BridgeConf import *
import winsound     # Audio Feedback
import subprocess

import wx
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub as Publisher
import speech_recognition as sr


class Thread_InputClass(threading.Thread):
    def __init__(self, Name, Bridge, Coord):

        threading.Thread.__init__(self, name=Name)
        self.Running            = False
        self.Name               = Name
        self.Bridge             = Bridge
        self.Coord              = Coord

        self.AudioPath          = os.getcwd() + '\\Assets\\Audio\\'

        self.PyJoystick         = None

        " fermo, riposo, memorizza, dormi"
        self.VocalCmd           = None


        " Variabili per il riconoscimento vocale "
        self.r                          = sr.Recognizer()
        # self.r.energy_threshold         = 4000
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

        " Variabili per la memorizzazione "
        self.var_mem                    = ['', '', '', '', '']
        self.NumVarMem                  = 0
        self.vm                         = 4*[0]

        self.Step_Param                 = [1, 5, 20]

        " Dizionari "
        self.instr_dict    = {'fer':'fermo', 'rip':'riposo', 'mem':'memorizza', 'dor':'dormi', 'ter':'termina'}
        self.direction_dict = {'sin':[1,0,0,0], 'des':[-1,0,0,0], 'sal':[0,0,1,0], 'sce':[0,0,-1,0], 'ava':[0,1,0,0], 'ind':[0,-1,0,0]}
        self.step_dict      = {'spostamento picc': self.Step_Param[0], 'spostamento medi': self.Step_Param[1], 'spostamento gran': self.Step_Param[2]}

    def run(self):

        print '+ InputThread running.'

        self.Bridge.Control.Input = self.Bridge.Patient.Input

        print 'Input: ' + self.Bridge.Control.Input



        if self.Bridge.Control.Input == "Joystick":

            try:
                self.PyJoystick = pygame.joystick.Joystick(0)
                self.PyJoystick.init()
                " Update input info in main window "
                wx.CallAfter(Publisher.sendMessage, "UpdateInputInfo", None)


            except Exception, e:
                print '# ERROR: Init Joystick Failed ' + str(e)
                " Update input info in main window "
                return False

        elif self.Bridge.Control.Input == "Vocal":

            " Introduzione controllo vocale "
            try:
                # winsound.PlaySound(self.AudioPath + 'Jarvis.wav', winsound.SND_FILENAME)
                # au_file = audio_file+'Jarvis.wav'
                # return_code = subprocess.call(["afplay", au_file])
                # self.Bip()
                " Update input info in main window "
                wx.CallAfter(Publisher.sendMessage, "UpdateInputInfo", None)

            except Exception, e:
                print '# ERROR: Init Vocal failed' + str(e)
                " Update input info in main window "
                return False

        else:
            print '# ERROR: Input Init failed'

        
        self.Running = True

        while self.Running:

            if self.Bridge.Control.Input == "Joystick":
                
                events = pygame.event.get()
                self.Bridge.Joystick.Mode = self.PyJoystick.get_button(1)
                " If a joystick event occurred "
                for event in events:
                    if event.type == pygame.QUIT:
                        self.terminate()

                    elif event.type == pygame.JOYBUTTONDOWN:
                        self.Bridge.Joystick.Mode                 = self.PyJoystick.get_button(1)

                        self.Bridge.Joystick.SavePosition         = self.PyJoystick.get_button(2)
                        self.Bridge.Joystick.GotoSavedPosition    = self.PyJoystick.get_button(3)
                        self.Bridge.Joystick.Alarm                = self.PyJoystick.get_button(4)

                    elif event.type == pygame.JOYAXISMOTION:
                        self.Bridge.Joystick.Mode = self.PyJoystick.get_button(1)
                        for i in range (0,2):
                            axis = (self.PyJoystick.get_axis(i) - self.Bridge.Joystick.AxisOffset[i]) * self.Bridge.Joystick.Gain

                            # controllo la banda morta (troppo vicino al non spostamento del joystick)
                            if abs(axis) < 0.1:
                                axis = 0.0

                            if self.Bridge.Joystick.Mode == 0:
                                if i == 0:
                                    self.Coord.p0[i] = axis * 1.2
                                else:

                                    self.Coord.p0[i] = -axis * 1.2

                                self.Coord.p0[2] = 0.0
                                self.Coord.p0[3] = 0.0
                            else:
                                if i == 0:
                                    #self.Coord.p0[3] = axis * 1.2
                                    self.Coord.p0[3] = 0
                                else:
                                    self.Coord.p0[2] = -axis * 1.2
                                    

                                self.Coord.p0[0] = 0.0
                                self.Coord.p0[1] = 0.0

                        # print self.Coord.p0



                        " Update input info in main window "
                        wx.CallAfter(Publisher.sendMessage, "UpdateInputInfo", None)

                pygame.event.clear()

            elif self.Bridge.Control.Input == "Vocal":

                if self.Bridge.Control.FIRST_RUN:
                    # TODO: SISTEMARE VOCAL
                    " Introduzione controllo vocale "
                    # winsound.PlaySound(self.AudioPath + 'Jarvis.wav', winsound.SND_FILENAME)
                    # au_file = audio_file+'Jarvis.wav'
                    # return_code = subprocess.call(["afplay", au_file])
                    self.Bip()
                    self.Bridge.Control.FIRST_RUN = False
                else:
                    " Get command "
                    if self.Bridge.Control.Listen:

                        self.Bridge.Control.Listen = 0
                        print "Listening..."
                        jarvis_cmd = self.WaitForInstructions()
                        jarvis_cmd = jarvis_cmd.lower()

                        print jarvis_cmd

                        " ################### "
                        " VOCAL STATE MACHINE "
                        " ################### "

                        if jarvis_cmd[0:4] == 'aiut':
                            print '*** ALLARME!'
                            self.VocalStatus = self.VOCAL_HELP

                        elif jarvis_cmd == 'termina':
                            self.VocalStatus = self.VOCAL_STOP_CONFERMATION
                            winsound.PlaySound(self.AudioPath + 'ConfermaSpegnimento.wav', winsound.SND_FILENAME)
                            # au_file = audio_file+'ConfermaSpegnimento.wav'
                            # return_code = subprocess.call(["afplay", au_file])
                            self.Bip()

                        elif self.VocalStatus == self.VOCAL_IDLE:
                            if jarvis_cmd == 'jarvis':

                                winsound.PlaySound(self.AudioPath + 'ConfermaAttivazione.wav', winsound.SND_FILENAME)
                                # au_file = audio_file + 'ConfermaAttivazione.wav'
                                # return_code = subprocess.call(["afplay", au_file])
                                self.Bip()

                                self.VocalStatus = self.VOCAL_RUNNING_CONFERMATION

                            elif jarvis_cmd == 'dormi':
                                self.VocalStatus = self.VOCAL_IDLE

                        elif self.VocalStatus == self.VOCAL_RUNNING_CONFERMATION:

                            if jarvis_cmd == 'vero':
                                print '*** CONTROLLO VOCALE ATTIVATO ***'
                                winsound.PlaySound(self.AudioPath + 'SonoAttivo.wav', winsound.SND_FILENAME)
                                # au_file = audio_file+'SonoAttivo.wav'
                                # return_code = subprocess.call(["afplay", au_file])
                                self.Bip()

                                self.VocalStatus = self.VOCAL_RUNNING

                            elif jarvis_cmd == 'falso':
                                print '*** CONTROLLO VOCALE DISATTIVATO ***'
                                winsound.PlaySound(self.AudioPath + 'Dormi2.wav', winsound.SND_FILENAME)
                                # au_file = audio_file + 'Dormi2.wav'
                                # return_code = subprocess.call(["afplay", au_file])
                                self.Bip()

                                self.VocalStatus = self.VOCAL_IDLE

                            else:
                                print '*** COMANDO VOCALE NON VALIDO ***'
                                winsound.PlaySound(self.AudioPath + 'IstruzioneNonValida.wav', winsound.SND_FILENAME)
                                # au_file = audio_file+'IstruzioneNonValida.wav'
                                # return_code = subprocess.call(["afplay", au_file])
                                self.Bip()
                                pass

                        elif self.VocalStatus == self.VOCAL_RUNNING:

                            " Parse command "
                            self.CommandRecognition(jarvis_cmd)

                            if self.VocalCmd == 'dormi':
                                winsound.PlaySound(self.AudioPath + 'Dormi.wav', winsound.SND_FILENAME)
                                # au_file = audio_file+'Dormi.wav'
                                # return_code = subprocess.call(["afplay", au_file])
                                self.Bip()
                                self.VocalStatus = self.VOCAL_IDLE

                            elif self.VocalCmd == 'memorizza':
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
                            if jarvis_cmd == 'vero':
                                print '*** CONTROLLO VOCALE TERMINATO ***'
                                winsound.PlaySound(self.AudioPath + 'Spegnimento.wav', winsound.SND_FILENAME)
                                # au_file = audio_file+'Spegnimento.wav'
                                # return_code = subprocess.call(["afplay", au_file])
                                self.Bip()

                                self.VocalStatus = self.VOCAL_IDLE
                                self.terminate()

                            elif jarvis_cmd == 'falso':
                                print '*** CONTROLLO VOCALE ATTIVO ***'
                                winsound.PlaySound(self.AudioPath + 'Jarvis.wav', winsound.SND_FILENAME)
                                # au_file = audio_file+'Dormi2.wav'
                                # return_code = subprocess.call(["afplay", au_file])
                                self.Bip()
                                self.VocalStatus = self.VOCAL_IDLE
                            else:
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

        print 'Input Thread Out'

    " Funzione di riconoscimento dei comandi che può essere personalizzata -> custumizzazione "
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
       
        else :
            print '*** Istruzione non valida ***'
            winsound.PlaySound('IstruzioneNonValida.wav', winsound.SND_FILENAME)
            # au_file = audio_file+'IstruzioneNonValida.wav'
            # return_code = subprocess.call(["afplay", au_file])
            self.Bip()

        " Update input info in main window "
        wx.CallAfter(Publisher.sendMessage, "UpdateInputInfo", None)


    def WaitForInstructions(self):

        with sr.Microphone() as source:
            try:
                # cmd = self.r.listen(source, timeout = 2)
                print '+ Microphone Record called.'
                cmd = self.r.record(source, duration=2)
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


