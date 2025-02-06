class CircuitCalculations:
    @staticmethod
    def calculate_total_resistance(components):
        return sum(c.resistance for c in components if hasattr(c, 'resistance'))

    @staticmethod
    def calculate_current(voltage_source, total_resistance):
        return 0 if total_resistance == 0 else voltage_source.voltage / total_resistance

    @staticmethod
    def apply_kirchhoffs_law(components, voltage_source):
        total_resistance = CircuitCalculations.calculate_total_resistance(components)
        return CircuitCalculations.calculate_current(voltage_source, total_resistance)
