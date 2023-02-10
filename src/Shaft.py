import numpy as np
"""
 user will pass a list of shaft sensor/item locations 
  [[kse, 1000], [kne, 25000], [phs, 5000]]
 end result will have:
 [0, 1, 2, 3, .....25000]
 [ ,  ,  , kseu, .....25000]

 or 

 [BOT, 0, 0, kseu, ..... TOP]
 and using index as mm amount

"""

class Shaft:
    def __init__(self, height, floorTable, sensorTable):
        self.floor_table = self.populateTable(height, floorTable)
        self.sensor_table = sensorTable

    def populateTable(self, height, floorTable):
        height = 1000 * height # height is initially in m, want mm
        fT = np.zeros(height)
        for entry in floorTable:
            fT[entry[1]] = entry[0] # entry[0] = kseu, entry[1] =  5000
        return fT

    
