# -*- coding: utf-8 -*-

import threading
import tables
import time
import os
#from Bridge import PatientClass

class Record(tables.IsDescription):
    J_current   = tables.Float32Col(4)
    J_des       = tables.Float32Col(4)
    Jv          = tables.Float32Col(4)
    p0          = tables.Float32Col(4)
    timestamp   = tables.Float64Col(1)


" ############################ "
" # SAVE RECORD THREAD CLASS # "
" ############################ "

class Thread_RecordClass(threading.Thread):

    def __init__(self, Name, Bridge, Coord):

        threading.Thread.__init__(self, name = Name)

        self.Bridge = Bridge
        self.Coord  = Coord

        directory = os.getcwd() + '\\Records\\' + self.Bridge.Patient.Name
        try:
            os.stat(directory)
        except:
            os.mkdir(directory)

        self.filename =  directory + '\\' + time.strftime("%Y%m%d_%H%M.h5", time.localtime())


        self.Running = False


        print "* Creating file: " + self.filename +" ..."

        " Open a file in 'w'rite mode "
        self.h5file = tables.open_file(self.filename, mode="w", title="")

        #print("* Creating group '/J' to hold new arrays")
        #self.readout = self.h5file.create_group(self.h5file.root, "J", "Joint Angles")

        # Create one table on it
        self.table = self.h5file.create_table(self.h5file.root, "Record", Record, "Readout Data")
        print "* Creating table '/J/readout' ..."





    def run(self):

        self.Running = True
        print(self.h5file)
        self.record = self.table.row

        while self.Running:

            t0 = time.clock()

            try:
                # Get a shortcut to the record object in table

                self.record['timestamp']        = t0
                self.record['p0']               = [self.Coord.p0[0], self.Coord.p0[1], self.Coord.p0[2], self.Coord.p0[3]]
                self.record['J_current']        = [self.Bridge.Joints[0].Position, self.Bridge.Joints[1].Position,self.Bridge.Joints[2].Position,self.Bridge.Joints[3].Position]
                self.record['J_des']            = [self.Coord.J_des[0], self.Coord.J_des[1], self.Coord.J_des[2], self.Coord.J_des[3]]
                self.record['Jv']               = [self.Coord.Jv[0],self.Coord.Jv[1],self.Coord.Jv[2],self.Coord.Jv[3]]

                self.record.append()

                # Flush the buffers for table
                self.table.flush()
            except Exception, e:
                print "# Error Saving Record | " + str(e)
                self.terminate()

            elapsed = t0 - time.clock()
            time.sleep(0.05 - elapsed)

        self.h5file.close()
        print("+ File '" + self.filename + "' closed")

    def terminate(self):
        # Close the file
        self.Running = False
