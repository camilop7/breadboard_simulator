from components.resistor import Resistor

class Thermistor(Resistor):
    def __init__(self, resistance, x=0, y=0):
        super().__init__(resistance, x, y)
        self.name = "Thermistor"

    def adjust_resistance(self, temperature):
        """Simulates the thermistor changing resistance with temperature."""
        # Simple model: resistance decreases as temperature increases
        self.resistance = max(10, self.resistance * (1 - 0.02 * (temperature - 25)))
