class Car:
    def __init__(self,type,velocity,accel,installation, dimensions):
        self.type = type
        self.velocity = velocity
        self.accel = accel
        self.installation = installation
        self.dimensions = dimensions
    def __str__(self):
        return f"Elevator Product {self.type} (Installation: {self.installation})"
        