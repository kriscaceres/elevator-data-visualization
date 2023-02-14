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
    def __init__(self, height, floorTable):
        self.height = height
        self.floor_table = self.populateTable(height, floorTable)
        
        
    def populateTable(self, height, floorTable):
        fT = [None] * (self.height + 1)
        for entry in floorTable:
            print(entry)
            print(entry[0])
            print(entry[1])
            fT[entry[1]] = entry[0] # entry[0] = kseu, entry[1] =  5000
        return fT

    
