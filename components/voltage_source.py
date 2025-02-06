from components.base import Component

class VoltageSource(Component):
    def __init__(self, voltage, x=0, y=0):
        super().__init__("Voltage Source", x, y)
        self.voltage = voltage

    def __repr__(self):
        return f"Voltage Source ({self.voltage}V) at ({self.x}, {self.y})"
