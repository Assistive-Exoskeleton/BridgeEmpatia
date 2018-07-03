# -*- coding: utf-8 -*-

import threading
import tables
import time
import numpy as np
from Bridge import *

class Record(tables.IsDescription):
    J_current   = tables.Float32Col(5)
    J_des       = tables.Float32Col(5)
    Jv          = tables.Float32Col(5)
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
        self.filename = self.Bridge.Patient.Name + '_' + time.strftime("%Y%m%d_%H%M.h5", time.localtime())

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
                self.record['p0']               = self.Coord.p0
                self.record['J_current']        = self.Coord.J_current
                self.record['J_des']            = self.Coord.J_des
                self.record['Jv']               = self.Coord.Jv

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
