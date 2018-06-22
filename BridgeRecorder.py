# -*- coding: utf-8 -*-

import threading
import tables
import time
import numpy as np
from Bridge import PatientClass


class Record(tables.IsDescription):
    name       = tables.StringCol(itemsize = 16)    # 16-character String
    timestamp  = tables.Float64Col()                 # Unsigned 64-bit integer
    #ADCcount  = tables.UInt16Col()     # Unsigned short integer
    #TDCcount  = tables.UInt8Col()      # unsigned byte
    #grid_i    = tables.Int32Col()      # 32-bit integer
    #grid_j    = tables.Int32Col()      # 32-bit integer
    #pressure  = tables.Float32Col()    # float  (single-precision)
    #energy    = tables.Float64Col()    # double (double-precision)

" ############################ "
" # SAVE RECORD THREAD CLASS # "
" ############################ "

class Thread_RecordClass(threading.Thread):

    def __init__(self, Name):

        threading.Thread.__init__(self, name = Name)

        Patient = PatientClass()
        Patient.Name = "New_Patient"

        self.Running = False
        self.filename = Patient.Name + '_' + time.strftime("%Y%m%d_%H%M.h5", time.localtime())

        print "* Creating file: " + self.filename +" ..."

        # Open a file in "w"rite mode
        self.h5file = tables.open_file(self.filename, mode="w", title="")


        #print('\r******************* group and table creation  *******************')

        # Create a new group under "/" (root)
        #group = h5file.create_group("/", 'detector', 'Detector information')
        #rint("Group '/detector' created")

        # Create one table on it
        self.table = self.h5file.create_table(self.h5file.root, 'readout', Record, "Readout Data")
        print "* Creating table '/root/readout' ..."

        #print("Creating a new group called '/columns' to hold new arrays")
        #gcolumns = h5file.create_group(h5file.root, "columns", "Pressure and Name")

        #print("Creating an array called 'pressure' under '/columns' group")
        #pressure = [x['pressure'] for x in table.iterrows()]
        #h5file.create_array(group, 'pressure', np.array(pressure),"Pressure column selection")
        #print(repr(h5file.root.detector.pressure))

        #print("Creating another array called 'name' under '/columns' group")
        #names = [x['name'] for x in table.iterrows()]
        #h5file.create_array(group, 'name', names, "Name column selection")
        #print(repr(h5file.root.columns.name))

    def run(self):

        self.Running = True
        print("HDF5 file:")
        print(self.h5file)

        while self.Running:

            t0 = time.clock()

            try:
                # Get a shortcut to the record object in table
                self.record = self.table.row

                # Fill the table with 10 particles
                self.record['name'] = 'Name'
                self.record['timestamp'] = t0
                    # self.record['TDCcount'] = i % 256
                    # self.record['ADCcount'] = (i * 256) % (1 << 16)
                    # self.record['grid_i'] = i
                    # self.record['grid_j'] = 10 - i
                    # self.record['pressure'] = float(i * i)
                    # self.record['energy'] = float(particle['pressure'] ** 4)
                    # self.record['idnumber'] = i * (2 ** 34)
                self.record.append()

                # Flush the buffers for table
                self.table.flush()
            except Exception, e:
                print "# Error Saving Record | " + str(e)
                self.terminate()

            elapsed = t0 - time.clock()
            time.sleep(0.01-elapsed)

        self.h5file.close()
        print("File '" + self.filename + "' created")

    def terminate(self):
        # Close the file
        self.Running = False


RecordThread = Thread_RecordClass("RecordThread")
time.sleep(0.5)
RecordThread.start()
time.sleep(0.5)
RecordThread.terminate()