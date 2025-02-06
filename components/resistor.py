from components.base import Component

class Resistor(Component):
    def __init__(self, resistance, x=0, y=0):
        super().__init__("Resistor", x, y)
        self.resistance = resistance

    def __repr__(self):
        return f"Resistor ({self.resistance} Ω) at ({self.x}, {self.y})"
