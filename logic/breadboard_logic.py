from components.voltage_source import VoltageSource
from components.resistor import Resistor

class Breadboard:
    def __init__(self):
        self.components = []
        self.voltage_source = None
        self.holes = {(col, row): None for col in range(50, 750, 20) for row in range(180, 360, 20)}

    def add_component(self, component):
        self.components.append(component)

    def remove_component(self, index):
        if 0 <= index < len(self.components):
            self.components.pop(index)

    def add_voltage_source(self, voltage):
        if self.voltage_source is None:
            self.voltage_source = VoltageSource(voltage, x=50, y=180)
        else:
            self.voltage_source.voltage = voltage

    def remove_voltage_source(self):
        self.voltage_source = None

    def reset(self):
        self.components.clear()
        self.voltage_source = None
