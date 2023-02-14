class Car:
    def __init__(self,type,velocity,accel, width, depth, height):
        self.type = type
        self.velocity = velocity
        self.accel = accel
        self.width = width
        self.depth = depth
        self.height = height
        
    def __str__(self):
        return "Velocity: {} | Accel {} | Dimensions)".format(self.velocity, self.accel, self.dimensions)
        