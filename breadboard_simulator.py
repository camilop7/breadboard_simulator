import random
import tkinter as tk
from tkinter import ttk

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
        self.resistance = resistance  # in ohms (Ω)

class VoltageSource(Component):
    def __init__(self, voltage, x=0, y=0):
        super().__init__("Voltage Source", x, y)
        self.voltage = voltage  # in volts (V)

class Breadboard:
    def __init__(self):
        self.components = []
        self.voltage_source = None
        self.holes = {(col, row): None for col in range(50, 750, 20) for row in range(180, 360, 20)}  # Grid of holes

    def add_component(self, component):
        self.components.append(component)

    def remove_component(self, index):
        if 0 <= index < len(self.components):
            self.components.pop(index)

    def add_voltage_source(self, voltage):
        if self.voltage_source is None:
            self.voltage_source = VoltageSource(voltage, x=50, y=180)  # Placing at the top rail
        else:
            self.voltage_source.voltage = voltage

    def remove_voltage_source(self):
        self.voltage_source = None

    def reset(self):
        self.components.clear()
        self.voltage_source = None

# --- GUI for Breadboard Simulator ---
class BreadboardSimulator:
    def __init__(self):
        self.breadboard = Breadboard()
        self.root = tk.Tk()
        self.root.title("Breadboard Circuit Simulator")
        self.root.geometry("900x600")  # Set initial window size

        self.selected_component = None
        self.resistor_value = tk.StringVar()
        self.voltage_value = tk.StringVar(value="5")
        self.component_type = tk.StringVar(value="Resistor")

        self.setup_ui()

    def setup_ui(self):
        # Main frame setup with a responsive grid layout for components and buttons
        frame = tk.Frame(self.root)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Organizing component selection section using grid layout
        component_frame = tk.Frame(frame)
        component_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        tk.Label(component_frame, text="Component Type:").grid(row=0, column=0, padx=5, pady=5)
        tk.OptionMenu(component_frame, self.component_type, "Resistor", "Thermistor").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(component_frame, text="Resistance (Ω):").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(component_frame, textvariable=self.resistor_value).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(component_frame, text="Add Component", command=self.add_component).grid(row=1, column=2, padx=5, pady=5)

        # Menu buttons organized vertically using grid layout
        button_frame = tk.Frame(frame)
        button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        tk.Button(button_frame, text="Edit Voltage", command=self.edit_voltage).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Add Power Source", command=self.add_power_source).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Remove Power Source", command=self.remove_power_source).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Reset Simulator", command=self.reset_simulator).grid(row=3, column=0, padx=5, pady=5)

        # Canvas for breadboard
        self.canvas = tk.Canvas(self.root, width=800, height=350, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Component list table
        self.table = ttk.Treeview(self.root, columns=("Type", "Value", "Edit"), show='headings')
        self.table.heading("Type", text="Component")
        self.table.heading("Value", text="Value")
        self.table.heading("Edit", text="Edit")
        self.table.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Set column and row configurations to make the layout responsive
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # Draw initial breadboard
        self.draw_breadboard()

        # Bind events for drag-and-drop
        self.canvas.bind("<ButtonPress-1>", self.select_component)
        self.canvas.bind("<B1-Motion>", self.drag_component)
        self.canvas.bind("<ButtonRelease-1>", self.release_component)

    def draw_breadboard(self):
        self.canvas.delete("all")

        # ** TOP RAILS: Positive and Negative Power Rails **
        self.canvas.create_line(50, 160, 750, 160, fill="red", width=3)  # Positive power rail (red) at top
        self.canvas.create_line(50, 180, 750, 180, fill="blue", width=3)  # Negative power rail (blue) at top

        # ** Breadboard Holes **
        for col, row in self.breadboard.holes.keys():
            color = "black"
            if self.breadboard.voltage_source and row == 160:  # Positive power rail row
                color = "green"  # Change to green when power is connected
            self.canvas.create_oval(col - 2, row - 2, col + 2, row + 2, fill=color)

        # ** Voltage Source (if exists) **
        if self.breadboard.voltage_source:
            self.canvas.create_text(self.breadboard.voltage_source.x, self.breadboard.voltage_source.y,
                                    text=f"{self.breadboard.voltage_source.voltage}V", fill="black")

        # ** Components on Breadboard **
        for comp in self.breadboard.components:
            self.canvas.create_rectangle(comp.x - 20, comp.y - 10, comp.x + 20, comp.y + 10, fill="blue")
            comp_value = f"{comp.resistance:.2f} Ω"
            if comp.resistance >= 1000:
                comp_value = f"{comp.resistance / 1000:.2f} kΩ" if comp.resistance < 1000000 else f"{comp.resistance / 1000000:.2f} MΩ"
            self.canvas.create_text(comp.x, comp.y, text=comp_value, fill="white", font=("Arial", 10, "bold"))

    def add_component(self):
        try:
            resistance = float(self.resistor_value.get())
            # Random position for the component within the grid limits
            x_pos = random.choice(range(50, 750, 20))
            y_pos = random.choice(range(180, 360, 20))
            component = Resistor(resistance, x=x_pos, y=y_pos)
            self.breadboard.add_component(component)
            self.update_table(component)
            self.draw_breadboard()
        except ValueError:
            print("Invalid value.")

    def add_power_source(self):
        self.breadboard.add_voltage_source(float(self.voltage_value.get()))
        self.draw_breadboard()

    def remove_power_source(self):
        self.breadboard.remove_voltage_source()
        self.draw_breadboard()

    def update_table(self, component):
        self.table.insert("", "end", values=(component.name, f"{component.resistance} Ω", "Edit"))

    def select_component(self, event):
        # Check if user clicked on a component
        for comp in self.breadboard.components:
            if comp.x - 20 <= event.x <= comp.x + 20 and comp.y - 10 <= event.y <= comp.y + 10:
                self.selected_component = comp
                break

    def drag_component(self, event):
        if self.selected_component:
            # Drag the selected component
            self.selected_component.x = event.x
            self.selected_component.y = event.y
            self.draw_breadboard()

    def release_component(self, event):
        if self.selected_component:
            # Snap the component to the closest hole
            closest_hole = min(self.breadboard.holes.keys(), key=lambda hole: (hole[0] - event.x) ** 2 + (hole[1] - event.y) ** 2)
            self.selected_component.x, self.selected_component.y = closest_hole
            self.selected_component = None
            self.draw_breadboard()

    def reset_simulator(self):
        self.breadboard.reset()
        self.draw_breadboard()

    def edit_voltage(self):
        # Dialog to edit voltage
        def set_voltage():
            try:
                voltage = float(voltage_entry.get())
                if self.breadboard.voltage_source:
                    self.breadboard.voltage_source.voltage = voltage
                    voltage_window.destroy()
                    self.draw_breadboard()
                else:
                    print("No voltage source to edit.")
            except ValueError:
                print("Invalid Voltage")

        voltage_window = tk.Toplevel(self.root)
        voltage_window.title("Edit Voltage")
        tk.Label(voltage_window, text="Enter Voltage (V):").pack(pady=5)
        voltage_entry = tk.Entry(voltage_window)
        voltage_entry.pack(pady=5)
        tk.Button(voltage_window, text="Set Voltage", command=set_voltage).pack(pady=10)
        voltage_window.mainloop()

    def run(self):
        self.root.mainloop()

# Run the simulation
simulator = BreadboardSimulator()
simulator.run()
