# -*- coding: utf-8 -*-
import threading, time
import pygame
from serial import *
import math
from numpy.linalg import inv
import math
import numpy
from BridgeConf import *
import scipy.io as spio
import datetime
import winsound # per audio feedback

import wx
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub as Publisher

from BridgeConf import *
from BridgeJoint import *

global file_EndEff0
file_EndEff0 = []
global file_EndEff_des
file_EndEff_des = []
global file_Jpos
file_Jpos = []
global file_Jdes
file_Jdes = []
global file_p0
file_p0_ = []
global file_elbow
file_elbow = []

class Thread_ControlClass(threading.Thread):
    def __init__(self, Name, Bridge, Coord, Conf, CheckWs=False):

        threading.Thread.__init__(self, name=Name)
        self.Running            = False
        self.Name               = Name
        self.Coord              = Coord
        self.Bridge             = Bridge

        self.CheckWS            = CheckWs
        self.Coord.Jpos= self.Bridge.Patient.Jrest

    def run(self):

        print '* Control Thread Run'

        self.Running = True

        while self.Running:



            " ############# "
            " STATE MACHINE "
            " ############# "

            if self.Bridge.Status == IDLE:
                time.sleep(0.2)

            elif self.Bridge.Status == INIT_SYSTEM:

                " Initialize Joints "

                " Initialize joint 1 - Start init thread "
                self.Bridge.JointInitThreads[1].start()

                " Wait for the joint to get to the home position "
                while self.Bridge.Joints[1].Homed is False:
                    " Keep escape chance "
                    if not self.Running:
                        break

                    time.sleep(0.5)

                " Update graphics in main window "
                wx.CallAfter(Publisher.sendMessage, "UpdateJointsInfo", None)
                
                " Initialize all the remaining joints - Start init threads "
                
                for initThread in self.Bridge.JointInitThreads:
                    if initThread.Name != "JointInitThread1":
                        initThread.start()

                " TODO: da riscrivere in modo pitonico "
                " MARTA: da ripristinare per giunto 5 "
                " MARTA: da ripristinare per giunto 3 "
                # while self.Bridge.Joints[0].Homed == False or self.Bridge.Joints[1].Homed == False or self.Bridge.Joints[2].Homed == False or self.Bridge.Joints[3].Homed == False or self.Bridge.Joints[4].Homed == False:
                while self.Bridge.Joints[0].Homed is False or self.Bridge.Joints[1].Homed == False or self.Bridge.Joints[2].Homed == False or self.Bridge.Joints[3].Homed == False:
                # while self.Bridge.Joints[0].Homed == False or self.Bridge.Joints[1].Homed == False or self.Bridge.Joints[2].Homed == False:
                    " Keep escape chance "
                    if not self.Running:
                        break

                    " Update graphics in main window "
                    wx.CallAfter(Publisher.sendMessage, "UpdateJointsInfo", None)

                    time.sleep(0.5)

                
                " All the joints are initialized and in home position - change control status "
                self.Bridge.Status = DONNING

                time.sleep(0.1)

                " Update graphics in main window "
                wx.CallAfter(Publisher.sendMessage, "UpdateJointsInfo", None)

                " Call donning dialog "
                wx.CallAfter(Publisher.sendMessage, "UpdateControlInfo", None)
                wx.CallAfter(Publisher.sendMessage, "ShowDonningDialog", None)

            elif self.Bridge.Status == DONNING:
                time.sleep(0.5)

            elif self.Bridge.Status == REST_POSITION:

                " Status where the initialization of the system is done, but the ctrl is NOT enabled "
                
                arrigon         = []
                arrigon_thread  = []

                for i, J in zip(range(0, self.Bridge.JointsNum), self.Bridge.Joints):
                    print i
                    # arrigon.append(self.Bridge.Joints[i].RestDone)
                    arrigon_thread.append(Thread_JointRestPositionClass("JointRestPositionThread" + str(i), J))

                " Run all the threads "
                for thread in arrigon_thread:
                    thread.start()

                while 1 and self.Running:
                    ''' MARTA: da ripristinare per Giunto 3
                    " Wait for all flags to be true - molto pitonico! "
                    if all(i == True for i in arrigon):
                        break
                    '''
                    if self.Bridge.Joints[0].RestDone == True and self.Bridge.Joints[1].RestDone == True and self.Bridge.Joints[2].RestDone == True:
                        break

                    time.sleep(0.5)
                    
                self.Bridge.Status = READY
                wx.CallAfter(Publisher.sendMessage, "UpdateControlInfo", None)
                wx.CallAfter(Publisher.sendMessage, "UpdateJointsInfo", None)


            elif self.Bridge.Status == READY:
                " Status where the initialization of the system is done, but the ctrl is NOT enabled "

                time.sleep(0.1)

            elif self.Bridge.Status == RUNNING:

                t0 = time.clock()

                #TODO check self.p0_check - da valutare "
                if self.Bridge.Control.Input == 'Vocal':

                    if self.Bridge.Control.VocalStepsCnt >= self.Bridge.Control.VocalSteps:
                        self.Coord.p0 = [0]*4
                        # self.Bridge.Control.VocalStepsCnt = 0
                    else:
                        self.Bridge.Control.VocalStepsCnt = self.Bridge.Control.VocalStepsCnt+1

                # TODO: ALTRA FLAG ENABLE CONTROL: NON FARE L'IK QUANDO NON DEVE.
                if all(i == 0 for i in self.Coord.p0):
                    self.Bridge.Control.Status = POS_CTRL

                else:
                    self.Bridge.Control.Status = SPEED_CTRL


                    " 2. Run IK algorithm "
                    self.MartaCtrl()

                    " Update graphics in main window "
                    wx.CallAfter(Publisher.sendMessage, "UpdateJointsInfo", None)


                elapsed_time = time.clock() - t0
                # print elapsed_time

                if elapsed_time > self.Bridge.Control.ThreadPeriod:
                    elapsed_time = self.Bridge.Control.ThreadPeriod
                    print ' ControlThread: Overrun'
                else:
                    time.sleep(self.Bridge.Control.ThreadPeriod - elapsed_time)

        print 'Control Thread Out'

    " ##################################################################################### "


    def MartaCtrl(self):

        # print 'control'

        self.Jpos_rad           = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0])
        self.temp_EndEff0       = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0])
        self.WS_is_gay          = False
        self.dq_prev            = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0]) # inizializzazione del primo step
        " Matrice 'la' Jacobiana "
        self.Jacob              = numpy.zeros((3, self.Bridge.JointsNum))
        " Matrice pesi "
        self.Wq                 = numpy.eye(self.Bridge.JointsNum)

        self.ul                 = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0])
        self.dl                 = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0])
        #TODO: ?
        self.change_dir_count   = [0]*5
        self.p0_check           = [0]*4


        " STEP 1: FK "

        for i in range (0,self.Bridge.JointsNum):

            if not __debug__:
                self.Coord.Jpos[i] = self.Bridge.Joints[i].Position

            self.Jpos_rad[i] = self.Coord.Jpos[i]*math.pi/180

        " FK per calcolo di posizione attuale -> Elbow "

        # 3 Giunti
        # self.Coord.Elbow[0] = math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2)
        # self.Coord.Elbow[1] = -math.cos(self.Jpos_rad[1])*math.sin(self.Jpos_rad[0])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2)
        # self.Coord.Elbow[2] = math.sin(self.Jpos_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2)

        "4 Joints"
        self.Coord.Elbow[0]   = self.Bridge.Patient.RJoint3*(math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[2]) - math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[1])) + math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2)
        self.Coord.Elbow[1]   = self.Bridge.Patient.RJoint3*(math.cos(self.Jpos_rad[0])*math.sin(self.Jpos_rad[2]) + math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1])) - math.cos(self.Jpos_rad[1])*math.sin(self.Jpos_rad[0])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2)
        self.Coord.Elbow[2]   = math.sin(self.Jpos_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.RJoint3*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[2])

        " FK per calcolo di posizione attuale -> EndEff_current "
        # 3 Giunti
        # self.Coord.EndEff_current[0] = math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) - self.Bridge.Patient.RJoint3*math.cos(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1]) - self.Bridge.Patient.l3*math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[2]) + self.Bridge.Patient.l3*math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[2])
        # self.Coord.EndEff_current[1] = -math.cos(self.Jpos_rad[1])*math.sin(self.Jpos_rad[0])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.RJoint3*math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1]) - self.Bridge.Patient.l3*math.cos(self.Jpos_rad[0])*math.sin(self.Jpos_rad[2]) - self.Bridge.Patient.l3*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[0])
        # self.Coord.EndEff_current[2] = math.sin(self.Jpos_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.RJoint3*math.cos(self.Jpos_rad[1]) + self.Bridge.Patient.l3*math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[1])

        "4 Joints"
        self.Coord.EndEff_current[0] = self.Bridge.Patient.RJoint3*(math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[2]) - math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[1])) - self.Bridge.Patient.l3*math.sin(self.Jpos_rad[3])*(math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[0]) + math.cos(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1])*math.sin(self.Jpos_rad[2])) + math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.l3*math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[3])
        self.Coord.EndEff_current[1] = self.Bridge.Patient.RJoint3*(math.cos(self.Jpos_rad[0])*math.sin(self.Jpos_rad[2]) + math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1])) - self.Bridge.Patient.l3*math.sin(self.Jpos_rad[3])*(math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[2]) - math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1])*math.sin(self.Jpos_rad[2])) - math.cos(self.Jpos_rad[1])*math.sin(self.Jpos_rad[0])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) - self.Bridge.Patient.l3*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[3])*math.sin(self.Jpos_rad[0])
        self.Coord.EndEff_current[2] = math.sin(self.Jpos_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.RJoint3*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[2]) + self.Bridge.Patient.l3*math.cos(self.Jpos_rad[3])*math.sin(self.Jpos_rad[1]) + self.Bridge.Patient.l3*math.cos(self.Jpos_rad[1])*math.sin(self.Jpos_rad[2])*math.sin(self.Jpos_rad[3])

        " Calculate EndEff_des (only for step-by-step control) "
        # if not self.Coord.GoToSavedPosMainTrigger:
        self.Coord.EndEff_des[0] = self.Coord.EndEff_current[0] + self.Coord.p0[1]*self.Bridge.Control.S*self.Bridge.Control.Time # x attuale + p0*v_max*tempo loop controllo [m]
        self.Coord.EndEff_des[1] = self.Coord.EndEff_current[1] + self.Coord.p0[0]*self.Bridge.Control.S*self.Bridge.Control.Time # y attuale + p0*v_max*tempo loop controllo [m]
        self.Coord.EndEff_des[2] = self.Coord.EndEff_current[2] + self.Coord.p0[2]*self.Bridge.Control.S*self.Bridge.Control.Time # z attuale + p0*v_max*tempo loop controllo [m]
        # self.Coord.EndEff_des[3] = self.Coord.EndEff_current[3] + self.Coord.p0[3]*self.Bridge.Control.MaxDegDispl        # PS pesata per input [°]

        self.temp_EndEff_current = [0]*4
        for i in range (0,4):
            self.temp_EndEff_current[i] = self.Coord.EndEff_current[i]

        " STEP 2: Check belonging to the possible workspace di EndEff_des "
        # TODO: modificare condizioni WS
        self.WS_is_gay = True # aggiungere funzione check WS


        " STEP 3: IK: EndEff_des -> Jdes (valori di giunto che devo raggiungere [deg]) "
        # inizializzazione parametri ciclo IK
        exit         = False # controlla num massimo di iterazioni algoritmo IK
        n            = 0     # counter numero iterazioni algoritmo IK        
        self.Wq      = numpy.eye(self.Bridge.JointsNum)
        self.dq_prev = numpy.array([0.0, 0.0, 0.0, 0.0])

        # TODO: check input movimento nel thread gestione input "

        if self.WS_is_gay and (abs(self.Coord.p0[0]) > 0 or abs(self.Coord.p0[1]) > 0 or abs(self.Coord.p0[2]) > 0 or abs(self.Coord.p0[3]) > 0):
            
            dp = self.Coord.EndEff_des[0:3]-self.temp_EndEff_current[0:3]
            # print 'dp: ', dp

            while (abs(dp[0]) > 1e-7+self.Bridge.Control.Tollerance*abs(self.Coord.p0[1]) or abs(dp[1]) > 1e-7+self.Bridge.Control.Tollerance*abs(self.Coord.p0[0]) or abs(dp[2]) > 1e-7+self.Bridge.Control.Tollerance*abs(self.Coord.p0[2])) and exit == False:

                # 3 Giunti
                '''
                self.Jacob[0,0] = self.Bridge.Patient.RJoint3*math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1]) - math.cos(self.Jpos_rad[1])*math.sin(self.Jpos_rad[0])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) - self.Bridge.Patient.l3*math.cos(self.Jpos_rad[0])*math.sin(self.Jpos_rad[2]) - self.Bridge.Patient.l3*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[0])
                self.Jacob[0,1] = - math.cos(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) - self.Bridge.Patient.RJoint3*math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[1]) - self.Bridge.Patient.l3*math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[1])
                self.Jacob[0,2] = - self.Bridge.Patient.l3*math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[0]) - self.Bridge.Patient.l3*math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[1])*math.sin(self.Jpos_rad[2])
                self.Jacob[1,0] = - math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.RJoint3*math.cos(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1]) + self.Bridge.Patient.l3*math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[2]) - self.Bridge.Patient.l3*math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[2])
                self.Jacob[1,1] = math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.RJoint3*math.cos(self.Jpos_rad[1])*math.sin(self.Jpos_rad[0]) + self.Bridge.Patient.l3*math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1])
                self.Jacob[1,2] = - self.Bridge.Patient.l3*math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[2]) + self.Bridge.Patient.l3*math.cos(self.Jpos_rad[1])*math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[2])
                self.Jacob[2,0] = 0
                self.Jacob[2,1] = math.cos(self.Jpos_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) - self.Bridge.Patient.RJoint3*math.sin(self.Jpos_rad[1]) + self.Bridge.Patient.l3*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[2])
                self.Jacob[2,2] = -self.Bridge.Patient.l3*math.sin(self.Jpos_rad[1])*math.sin(self.Jpos_rad[2])              
                '''

                # 4 Giunti
                self.Jacob[0,0]= self.Bridge.Patient.RJoint3 *(math.cos(self.Jpos_rad[0]) *math.sin(self.Jpos_rad[2]) + math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1])) - self.Bridge.Patient.l3*math.sin(self.Jpos_rad[3])*(math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[2]) - math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1])*math.sin(self.Jpos_rad[2])) - math.cos(self.Jpos_rad[1])*math.sin(self.Jpos_rad[0])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) - self.Bridge.Patient.l3*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[3])*math.sin(self.Jpos_rad[0])
                self.Jacob[0,1]= - math.cos(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) -self.Bridge.Patient.RJoint3*math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[2]) -self.Bridge.Patient.l3*math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[3])*math.sin(self.Jpos_rad[1]) -self.Bridge.Patient.l3*math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[1])*math.sin(self.Jpos_rad[2])*math.sin(self.Jpos_rad[3])
                self.Jacob[0,2]= self.Bridge.Patient.RJoint3*(math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[0]) + math.cos(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1])*math.sin(self.Jpos_rad[2])) + self.Bridge.Patient.l3*math.sin(self.Jpos_rad[3])*(math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[2]) - math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[1]))
                self.Jacob[0,3]= - self.Bridge.Patient.l3*math.cos(self.Jpos_rad[3])*(math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[0]) + math.cos(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1])*math.sin(self.Jpos_rad[2])) - self.Bridge.Patient.l3*math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[1])*math.sin(self.Jpos_rad[3])
                self.Jacob[1,0]= self.Bridge.Patient.l3*math.sin(self.Jpos_rad[3])*(math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[0]) + math.cos(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1])*math.sin(self.Jpos_rad[2])) - self.Bridge.Patient.RJoint3*(math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[2]) - math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[1])) - math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) - self.Bridge.Patient.l3*math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[3])
                self.Jacob[1,1]= math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.RJoint3*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[0]) + self.Bridge.Patient.l3*math.cos(self.Jpos_rad[3])*math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1]) + self.Bridge.Patient.l3*math.cos(self.Jpos_rad[1])*math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[2])*math.sin(self.Jpos_rad[3])
                self.Jacob[1,2]= self.Bridge.Patient.RJoint3*(math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[2]) - math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1])*math.sin(self.Jpos_rad[2])) + self.Bridge.Patient.l3*math.sin(self.Jpos_rad[3])*(math.cos(self.Jpos_rad[0])*math.sin(self.Jpos_rad[2]) + math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1]))
                self.Jacob[1,3]= self.Bridge.Patient.l3*math.cos(self.Jpos_rad[1])*math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[3]) - self.Bridge.Patient.l3*math.cos(self.Jpos_rad[3])*(math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[2]) - math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1])*math.sin(self.Jpos_rad[2]))
                self.Jacob[2,0]= 0
                self.Jacob[2,1]= math.cos(self.Jpos_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) - self.Bridge.Patient.RJoint3*math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[1]) + self.Bridge.Patient.l3*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[3]) - self.Bridge.Patient.l3*math.sin(self.Jpos_rad[1])*math.sin(self.Jpos_rad[2])*math.sin(self.Jpos_rad[3]) 
                self.Jacob[2,2]= self.Bridge.Patient.l3*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[3]) - self.Bridge.Patient.RJoint3*math.cos(self.Jpos_rad[1])*math.sin(self.Jpos_rad[2])
                self.Jacob[2,3]= self.Bridge.Patient.l3*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[3])*math.sin(self.Jpos_rad[2]) - self.Bridge.Patient.l3*math.sin(self.Jpos_rad[1])*math.sin(self.Jpos_rad[3])

                # print 'Jacob ', self.Jacob
                # Jacobiano moltiplicato per i pesi -> iterazione sulla matrice Jacobiana
                JacobW = numpy.dot(self.Jacob, self.Wq)

                # SVD
                U, s, V = numpy.linalg.svd(JacobW, full_matrices=False)
                s_min = numpy.amin(s)

                if s_min < self.Bridge.Control.Eps:

                    " Peso per smorzare le velocità di giunto in singolarita' "
                    self.Wq[0,0] = self.Bridge.Control.Wq0s+(1-self.Bridge.Control.Wq0s)*s_min/self.Bridge.Control.Eps
                    self.Wq[1,1] = self.Bridge.Control.Wq0s+(1-self.Bridge.Control.Wq0s)*s_min/self.Bridge.Control.Eps
                    self.Wq[2,2] = self.Bridge.Control.Wq0s+(1-self.Bridge.Control.Wq0s)*s_min/self.Bridge.Control.Eps
                    self.Wq[3,3] = self.Bridge.Control.Wq0s+(1-self.Bridge.Control.Wq0s)*s_min/self.Bridge.Control.Eps
            
                else:
                    self.Wq[0,0] = 1
                    self.Wq[1,1] = 1
                    self.Wq[2,2] = 1
                    self.Wq[3,3] = 1

                " ################### "
                " 3.2. LIMITI dei ROM "
                " ################### "

                if not __debug__:
                    for i, J in zip(range(0, self.Bridge.JointsNum), self.Bridge.Joints):

                        if self.dq_prev[i] >= 0:
                            self.dl[i] = J.Jmax - J.Position
                        else:
                            self.dl[i] = J.Position - J.Jmin

                        if self.dl[i] < self.Bridge.Control.Dol:
                            self.ul[i] = max(self.ul[i] - self.Bridge.Control.Du, self.dl[i] / self.Bridge.Control.Dol)
                        else:
                            self.ul[i] = min(self.ul[i] + self.Bridge.Control.Du, 1)
                        self.Wq[i, i] = self.Bridge.Control.Wq0s + (1 - self.Bridge.Control.Wq0s) * self.ul[i]
                        self.Bridge.Control.Alpha = self.Bridge.Control.Alpha0 * (1 - self.ul[i] ** 2)
                else:
                    for i, Jpos, J in zip(range(0, self.Bridge.JointsNum), self.Coord.Jpos, self.Bridge.Joints):

                        if self.dq_prev[i] >= 0:
                            self.dl[i] = J.Jmax - Jpos
                        else:
                            self.dl[i] = Jpos - J.Jmin

                        if self.dl[i] < self.Bridge.Control.Dol:
                            self.ul[i] = max(self.ul[i] - self.Bridge.Control.Du, self.dl[i] / self.Bridge.Control.Dol)
                        else:
                            self.ul[i] = min(self.ul[i] + self.Bridge.Control.Du, 1)

                        self.Wq[i, i] = self.Bridge.Control.Wq0s + (1 - self.Bridge.Control.Wq0s) * self.ul[i]

                        self.Bridge.Control.Alpha = self.Bridge.Control.Alpha0 * (1 - self.ul[i] ** 2)


                " ###################################################### "
                " 3.3 Aggiornamento e calcolo della variazione di giunto "
                " ###################################################### "

                " Aggiorno il Jacobiano "
                JacobW = numpy.dot(self.Jacob, self.Wq)

                " Equazione per trovare la variazione di giunto da applicare "
                temp = inv(numpy.dot(JacobW, JacobW.transpose()) + self.Bridge.Control.Alpha*numpy.eye(3))

                dq = numpy.dot(numpy.dot(numpy.dot(self.Wq,JacobW.transpose()), temp), dp.transpose())
                self.dq_prev = dq               

                " Update dei valori di giunto che voglio raggiungere "

                self.Coord.Jdes[0:self.Bridge.JointsNum] = self.Jpos_rad[0:self.Bridge.JointsNum]*180/math.pi + dq*180/math.pi

                " ################################### "
                " 3.4. Aggiornamento valori di giunto "
                " ################################### "

                # self.Jpos_rad[0:4] = self.Coord.Jdes[0:4]*math.pi/180
                self.Jpos_rad[0] = self.Coord.Jdes[0]*math.pi/180
                self.Jpos_rad[1] = self.Coord.Jdes[1]*math.pi/180
                self.Jpos_rad[2] = self.Coord.Jdes[2]*math.pi/180
                self.Jpos_rad[3] = self.Coord.Jdes[3]*math.pi/180

                # 3 Giunti
                '''
                p_update    = numpy.array([0.0, 0.0, 0.0]) 
                p_update[0] = math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) - self.Bridge.Patient.RJoint3*math.cos(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1]) - self.Bridge.Patient.l3*math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[2]) + self.Bridge.Patient.l3*math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[2])
                p_update[1] = -math.cos(self.Jpos_rad[1])*math.sin(self.Jpos_rad[0])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.RJoint3*math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1]) - self.Bridge.Patient.l3*math.cos(self.Jpos_rad[0])*math.sin(self.Jpos_rad[2]) - self.Bridge.Patient.l3*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[0])
                p_update[2] = math.sin(self.Jpos_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.RJoint3*math.cos(self.Jpos_rad[1]) + self.Bridge.Patient.l3*math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[1])
                '''

                # 4 Giunti
                p_update    = numpy.array([0.0, 0.0, 0.0]) 
                p_update[0] = self.Bridge.Patient.RJoint3*(math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[2]) - math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[1])) - self.Bridge.Patient.l3*math.sin(self.Jpos_rad[3])*(math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[0]) + math.cos(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1])*math.sin(self.Jpos_rad[2])) + math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.l3*math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[3])
                p_update[1] = self.Bridge.Patient.RJoint3*(math.cos(self.Jpos_rad[0])*math.sin(self.Jpos_rad[2]) + math.cos(self.Jpos_rad[2])*math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1])) - self.Bridge.Patient.l3*math.sin(self.Jpos_rad[3])*(math.cos(self.Jpos_rad[0])*math.cos(self.Jpos_rad[2]) - math.sin(self.Jpos_rad[0])*math.sin(self.Jpos_rad[1])*math.sin(self.Jpos_rad[2])) - math.cos(self.Jpos_rad[1])*math.sin(self.Jpos_rad[0])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) - self.Bridge.Patient.l3*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[3])*math.sin(self.Jpos_rad[0])
                p_update[2] = self.Coord.EndEff_current[2] = math.sin(self.Jpos_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.RJoint3*math.cos(self.Jpos_rad[1])*math.cos(self.Jpos_rad[2]) + self.Bridge.Patient.l3*math.cos(self.Jpos_rad[3])*math.sin(self.Jpos_rad[1]) + self.Bridge.Patient.l3*math.cos(self.Jpos_rad[1])*math.sin(self.Jpos_rad[2])*math.sin(self.Jpos_rad[3])
                
                " Update errore che devo ridurre con le mie iterazioni (idealmente zero) "
                dp = self.Coord.EndEff_des[0:3] - p_update

                " Update del num di iterazioni ciclo while "
                n = n+1
                if n >= self.Bridge.Control.IterMax:
                    exit = True
                    for i in range(0, self.Bridge.JointsNum):

                        if not __debug__:
                            self.Coord.Jdes[i] = self.Bridge.Joints[i].Position
                            #self.Coord.p0 = [0] * 4
                            self.Bridge.Control.Status = POS_CTRL
                        else:
                            self.Coord.Jdes[i] = self.Coord.Jpos[i]
                            #self.Coord.p0 = [0] * 4
                            self.Bridge.Control.Status = POS_CTRL


                    print '  Maximum # of iterations'

            " Verifico che la soluzione trovata rispetti i limiti di giunto altrimenti li limito all'estremo più vicino --> riporto errore "

            for i, J in zip(range(0,self.Bridge.JointsNum), self.Bridge.Joints):


                if self.Coord.Jdes[i] <= (J.Jmin + self.Bridge.Control.Threshold) and (self.Coord.Jdes[i] - J.Position) <= 0:
                    winsound.Beep(440, 500)  # frequency, duration[ms
                    print '# J%d close to lower limit (%f)' % (i+1, self.Coord.Jdes[i])

                    self.Coord.Jdes[i] = J.Jmin + self.Bridge.Control.Threshold
                    print '# J%d new Jdes: %f' % (i+1, self.Coord.Jdes[i])
                    self.Coord.Jv[i]   = 0
                    self.Bridge.Control.Status = POS_CTRL

                elif self.Coord.Jdes[i] >= (J.Jmax - self.Bridge.Control.Threshold) and (self.Coord.Jdes[i] - J.Position) >= 0:
                    winsound.Beep(440, 500) # frequency, duration[ms]
                    print '# J%d close to upper limit (%f)' % (i+1, self.Coord.Jdes[i])

                    self.Coord.Jdes[i] = J.Jmax - self.Bridge.Control.Threshold
                    print '# J%d new Jdes: %f' % (i + 1, self.Coord.Jdes[i])
                    self.Coord.Jv[i]   = 0
                    self.Bridge.Control.Status = POS_CTRL
                else:
                    JCurrentPos = []
                    if not __debug__:
                        for J in self.Bridge.Joints:
                            JCurrentPos.append(J.Position)
                    else:
                        for i in range(0, self.Bridge.JointsNum):
                            JCurrentPos.append(self.Coord.Jpos[i])

                    '''
                    diff = [x - y for x, y in zip(JCurrentPos, self.Coord.Jdes)]
                    for i in diff:
                        if abs(i) > self.Bridge.Control.MaxDegDispl:
                            print 'Repentine Change'
                            self.Coord.Jdes = JCurrentPos
                            self.Bridge.Control.Status = POS_CTRL
                    '''
                    " Check no repentine change of joints value! "
                    diff = [0]*5
                    for i in range(0, self.Bridge.JointsNum):
                        diff[i] = self.Coord.Jdes[i] - JCurrentPos[i]
                        
                        if abs(diff[i]) > self.Bridge.Control.MaxDegDispl:
                            print '# Repentine Change'
                            self.Coord.Jdes = JCurrentPos
                            self.Bridge.Control.Status = POS_CTRL
                        else:
                            self.Coord.Jv[i] = ((self.Coord.Jdes[i] - JCurrentPos[i]) / self.Bridge.Control.Time)
                    # TODO: valutare cosa fare - "
                    #self.Conf.CtrlEnable =  False





            '''
            " Mappo lo spostamento di posizione in spostamento di velocità richiesto ai giunti "
            " calcolo delta in gradi che voglio muovere sui vari motori"
            for i in range(0,self.Bridge.JointsNum):
                if self.Bridge.Control.BoundedJv[i]:
                    # reset del flag
                    self.Bridge.Control.BoundedJv[i] = False
                else:
            '''

            # print 'Jv ', self.Coord.Jv
            # for i in range(0,self.Bridge.JointsNum):
            #   print
            #   print str(i) + ' ' + str(self.Coord.Jv[i])



            # TODO: vericare che con Jv = 1 passo in ctrl posizione - chi lo decide? Update dei joints?"

            for i in range(0,self.Bridge.JointsNum):
                if abs(self.Coord.Jv[i]) <= 5/360:
                    self.Bridge.Control.Status = POS_CTRL
                if __debug__:
                    self.Coord.Jpos[i] = self.Coord.Jdes[i]
                else:
                    self.Coord.Jpos[i] = self.Bridge.Joints[i].Position

            # # monitor variables
            # #file_Jpos.append(self.Coord.Jpos[0])
            # file_Jpos.append(self.Coord.Jpos[1])
            # #file_Jpos.append(self.Coord.Jpos[2])
            # #file_Jpos.append(self.Coord.Jpos[3])
            # file_p0_.append(self.Coord.p0[0])
            # file_p0_.append(self.Coord.p0[1])
            # file_p0_.append(self.Coord.p0[2])
            # file_p0_.append(self.Coord.p0[3])
            # #file_EndEff0.append(self.Coord.EndEff_current[0])
            # #file_EndEff0.append(self.Coord.EndEff_current[1])
            # file_EndEff0.append(self.Coord.EndEff_current[2])
            # #file_EndEff_des.append(self.Coord.EndEff_des[0])
            # #file_EndEff_des.append(self.Coord.EndEff_des[1])
            # file_EndEff_des.append(self.Coord.EndEff_des[2])
            # # file_Jpos.append(self.Bridge.Joints[0].Position)
            # # file_Jpos.append(self.Bridge.Joints[1].Position)
            # # file_Jpos.append(self.Bridge.Joints[2].Position)
            # # file_Jpos.append(self.Bridge.Joints[3].Position)

            # #file_Jdes.append(self.Coord.Jdes[0])
            # file_Jdes.append(self.Coord.Jdes[1])
            # #file_Jdes.append(self.Coord.Jdes[2])
            # #file_Jdes.append(self.Coord.Jdes[3])
            # file_elbow.append(self.Coord.Elbow[2])

        else:
            self.Coord.Jv = [0]*5
            self.Bridge.Control.Status = POS_CTRL


    def terminate(self):
        " Exit the thread "
        self.Running = False

        # text_file_EndEff0 = open("Output_EndEff0.txt", "w")
        # text_file_EndEff_des = open("Output_EndEff_des.txt", "w")
        # text_file_Jpos = open("Output_Jpos.txt", "w")
        # text_file_Jdes = open("Output_Jdes.txt", "w")
        # text_file_p0_ = open("Output_p0.txt", "w")

        # # scrivo variabili sui file prima di chiudere
        # text_file_EndEff0.write("\n{0}".format(file_EndEff0))
        # text_file_EndEff_des.write("\n{0}".format(file_EndEff_des))
        # text_file_Jpos.write("\n{0}".format(file_Jpos))
        # text_file_Jdes.write("\n{0}".format(file_Jdes))
        # text_file_p0_.write("\n{0}".format(file_p0_))


