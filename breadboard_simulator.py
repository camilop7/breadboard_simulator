import numpy as np
import sympy as sp
from tkinter import Tk, Canvas, Frame, Button, Label, Entry, StringVar, OptionMenu, Toplevel

# --- Circuit Components ---
class Component:
    def __init__(self, name, x=0, y=0):
        self.name = name
        self.x = x
        self.y = y
        self.connected_to = []  # List of components it is connected to

class Resistor(Component):
    def __init__(self, resistance, x=0, y=0):
        super().__init__("Resistor", x, y)
        self.resistance = resistance  # in ohms (\u03a9)

class Thermistor(Component):
    def __init__(self, resistance, x=0, y=0):
        super().__init__("Thermistor", x, y)
        self.resistance = resistance  # in ohms (\u03a9)

class VoltageSource(Component):
    def __init__(self, voltage, x=0, y=0):
        super().__init__("Voltage Source", x, y)
        self.voltage = voltage  # in volts (V)

class Breadboard:
    def __init__(self):
        self.components = []
        self.voltage_source = VoltageSource(5, x=50, y=50)  # Default 5V source

    def add_component(self, component):
        """Add a component to the breadboard."""
        self.components.append(component)

    def remove_component(self, index):
        """Remove a component by index."""
        if 0 <= index < len(self.components):
            self.components.pop(index)

    def reset(self):
        """Reset the breadboard by clearing all components."""
        self.components.clear()

# --- GUI for Breadboard Simulator ---
class BreadboardSimulator:
    def __init__(self):
        self.breadboard = Breadboard()
        self.root = Tk()
        self.root.title("Breadboard Circuit Simulator")

        self.selected_component = None

        # Input fields
        self.resistor_value = StringVar()
        self.voltage_value = StringVar(value=str(self.breadboard.voltage_source.voltage))
        self.component_type = StringVar(value="Resistor")

        self.setup_ui()

    def setup_ui(self):
        """Setup the GUI layout."""
        frame = Frame(self.root)
        frame.pack(padx=10, pady=10)

        # Component selector
        Label(frame, text="Component Type:").grid(row=0, column=0, padx=5, pady=5)
        OptionMenu(frame, self.component_type, "Resistor", "Thermistor").grid(row=0, column=1, padx=5, pady=5)

        # Resistor value input
        Label(frame, text="Resistance (Ω):").grid(row=1, column=0, padx=5, pady=5)
        Entry(frame, textvariable=self.resistor_value).grid(row=1, column=1, padx=5, pady=5)

        # Add component
        Button(frame, text="Add Component", command=self.add_component).grid(row=1, column=2, padx=5, pady=5)

        # Edit voltage source
        Button(frame, text="Edit Voltage", command=self.edit_voltage).grid(row=2, column=0, padx=5, pady=5)

        # Buttons for edit and reset
        Button(frame, text="Delete Component", command=self.delete_component).grid(row=2, column=1, padx=5, pady=5)
        Button(frame, text="Reset Simulator", command=self.reset_simulator).grid(row=2, column=2, padx=5, pady=5)

        # Visual representation canvas
        self.canvas = Canvas(self.root, width=800, height=400, bg="white")
        self.canvas.pack(pady=10)

        # Summary area
        self.summary_label = Label(self.root, text="Circuit Summary", justify="left")
        self.summary_label.pack(pady=10)

        self.canvas.bind("<Button-1>", self.select_component)
        self.canvas.bind("<B1-Motion>", self.drag_component)
        self.canvas.bind("<ButtonRelease-1>", self.release_component)

        self.draw_breadboard()

    def draw_breadboard(self):
        """Draw the breadboard layout."""
        self.canvas.delete("all")

        # Draw power rails
        for y, color in [(50, "red"), (80, "blue")]:
            self.canvas.create_line(50, y, 750, y, fill=color, width=2)

        # Draw grid
        for col in range(50, 750, 20):
            for row in range(150, 350, 20):
                self.canvas.create_oval(col - 2, row - 2, col + 2, row + 2, fill="black")

        # Draw voltage source
        vs = self.breadboard.voltage_source
        self.canvas.create_line(vs.x - 20, vs.y, vs.x - 10, vs.y, width=2)
        self.canvas.create_line(vs.x + 10, vs.y, vs.x + 20, vs.y, width=2)
        self.canvas.create_line(vs.x - 5, vs.y - 10, vs.x - 5, vs.y + 10, width=2)
        self.canvas.create_text(vs.x, vs.y + 15, text=f"{vs.voltage}V", fill="black")

        # Draw components
        for comp in self.breadboard.components:
            if isinstance(comp, Resistor):
                self.canvas.create_rectangle(comp.x - 20, comp.y - 10, comp.x + 20, comp.y + 10, fill="blue")
                self.canvas.create_text(comp.x, comp.y, text=f"{comp.name}\n{comp.resistance}", fill="white")
            elif isinstance(comp, Thermistor):
                self.canvas.create_rectangle(comp.x - 20, comp.y - 10, comp.x + 20, comp.y + 10, fill="green")
                self.canvas.create_line(comp.x - 15, comp.y - 10, comp.x + 15, comp.y + 10, fill="black")
                self.canvas.create_text(comp.x, comp.y, text=f"{comp.resistance}", fill="white")

        # Draw current flow if applicable
        self.draw_current_flow()

    def draw_current_flow(self):
        """Simulate and display current flow in the circuit."""
        for comp in self.breadboard.components:
            if isinstance(comp, Resistor):
                self.canvas.create_line(
                    comp.x - 20, comp.y, comp.x + 20, comp.y,
                    fill="green", dash=(4, 2), width=2
                )

    def add_component(self):
        try:
            if self.component_type.get() == "Resistor":
                resistance = float(self.resistor_value.get())
                component = Resistor(resistance, x=100, y=200)
            elif self.component_type.get() == "Thermistor":
                resistance = float(self.resistor_value.get())
                component = Thermistor(resistance, x=100, y=200)

            self.breadboard.add_component(component)
            self.resistor_value.set("")
            self.update_summary()
            self.update_visual()
        except ValueError:
            self.update_status("Invalid value.")

    def delete_component(self):
        try:
            if self.breadboard.components:
                self.breadboard.remove_component(len(self.breadboard.components) - 1)
                self.update_summary()
                self.update_visual()
            else:
                self.update_status("No components to delete.")
        except Exception as e:
            self.update_status(f"Error: {e}")

    def reset_simulator(self):
        self.breadboard.reset()
        self.update_summary()
        self.update_visual()

    def edit_voltage(self):
        """Edit the voltage of the power source."""
        edit_window = Toplevel(self.root)
        edit_window.title("Edit Voltage Source")

        Label(edit_window, text="Voltage (V):").pack(pady=5)
        voltage_entry = Entry(edit_window, textvariable=self.voltage_value)
        voltage_entry.pack(pady=5)

        def save_voltage():
            try:
                voltage = float(self.voltage_value.get())
                self.breadboard.voltage_source.voltage = voltage
                self.update_visual()
                edit_window.destroy()
            except ValueError:
                self.update_status("Invalid voltage value.")

        Button(edit_window, text="Save", command=save_voltage).pack(pady=5)

    def update_visual(self):
        self.draw_breadboard()

    def update_summary(self):
        """Update the summary of components on the breadboard."""
        summary = [
            f"Voltage Source: {self.breadboard.voltage_source.voltage}V"
        ]
        for comp in self.breadboard.components:
            if isinstance(comp, Resistor):
                summary.append(f"Resistor: {comp.resistance}Ω")
            elif isinstance(comp, Thermistor):
                summary.append(f"Thermistor: {comp.resistance}Ω")

        self.summary_label.config(text="\n".join(summary))

    def select_component(self, event):
        for i, comp in enumerate(self.breadboard.components):
            if comp.x - 20 < event.x < comp.x + 20 and comp.y - 10 < event.y < comp.y + 10:
                self.selected_component = (i, comp)
                break

    def drag_component(self, event):
        if self.selected_component:
            _, comp = self.selected_component
            comp.x, comp.y = event.x, event.y
            self.snap_to_power_rails(comp)
            self.update_visual()

    def release_component(self, event):
        self.selected_component = None

    def snap_to_power_rails(self, comp):
        """Snap components to the nearest power rail or grid point."""
        if 40 <= comp.y <= 60:  # Red power rail
            comp.y = 50
        elif 70 <= comp.y <= 90:  # Blue power rail
            comp.y = 80
        else:
            comp.x = round(comp.x / 20) * 20
            comp.y = round(comp.y / 20) * 20

    def update_status(self, message):
        print(message)

    def run(self):
        self.root.mainloop()

# Run the simulator
if __name__ == "__main__":
    simulator = BreadboardSimulator()
    simulator.run()
