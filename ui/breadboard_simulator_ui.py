import tkinter as tk
import random
from tkinter import ttk
from logic.breadboard_logic import Breadboard
from components.resistor import Resistor
from components.voltage_source import VoltageSource
from components.thermistor import Thermistor

class BreadboardSimulator:
    def __init__(self):
        self.breadboard = Breadboard()
        self.root = tk.Tk()
        self.root.title("Breadboard Circuit Simulator")
        self.root.geometry("900x600")
        self.selected_component = None
        self.resistor_value = tk.StringVar()
        self.thermistor_value = tk.StringVar()
        self.voltage_value = tk.StringVar(value="5")
        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self.root)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        button_frame = tk.Frame(frame)
        button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        tk.Label(button_frame, text="Resistor (Ω):").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(button_frame, textvariable=self.resistor_value).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Add Resistor", command=self.add_resistor).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(button_frame, text="Thermistor (Ω):").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(button_frame, textvariable=self.thermistor_value).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Add Thermistor", command=self.add_thermistor).grid(row=1, column=2, padx=5, pady=5)

        tk.Label(button_frame, text="Voltage (V):").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(button_frame, textvariable=self.voltage_value).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Add Power Source", command=self.add_power_source).grid(row=2, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="Remove Power Source", command=self.remove_power_source).grid(row=3, column=2, padx=5, pady=5)

        tk.Button(button_frame, text="Reset Simulator", command=self.reset_simulator).grid(row=4, column=2, padx=5, pady=5)

        self.canvas = tk.Canvas(self.root, width=800, height=400, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.canvas.bind("<ButtonPress-1>", self.select_component)
        self.canvas.bind("<B1-Motion>", self.drag_component)
        self.canvas.bind("<ButtonRelease-1>", self.release_component)

        self.draw_breadboard()

    def draw_breadboard(self):
        self.canvas.delete("all")
        self.canvas.create_line(50, 100, 750, 100, fill="red", width=3)
        self.canvas.create_line(50, 120, 750, 120, fill="blue", width=3)
        for col, row in self.breadboard.holes.keys():
            color = "black"
            if self.breadboard.voltage_source and row == 100:
                color = "green"
            self.canvas.create_oval(col - 2, row - 2, col + 2, row + 2, fill=color)
        for comp in self.breadboard.components:
            color = "blue" if isinstance(comp, Resistor) else "green"
            self.canvas.create_rectangle(comp.x - 20, comp.y - 20, comp.x + 20, comp.y + 20, fill=color)
            resistance_text = f"{comp.resistance} Ω"
            self.canvas.create_text(comp.x, comp.y, text=resistance_text, fill="white", font=("Arial", 14, "bold"), anchor="center")

    def add_resistor(self):
        resistance = float(self.resistor_value.get())
        component = Resistor(resistance, x=random.choice(range(100, 700, 20)), y=random.choice(range(140, 360, 20)))
        self.breadboard.add_component(component)
        self.draw_breadboard()

    def add_thermistor(self):
        resistance = float(self.thermistor_value.get())
        component = Thermistor(resistance, x=random.choice(range(100, 700, 20)), y=random.choice(range(140, 360, 20)))
        self.breadboard.add_component(component)
        self.draw_breadboard()

    def add_power_source(self):
        voltage = float(self.voltage_value.get())
        if not self.breadboard.voltage_source:
            self.breadboard.voltage_source = VoltageSource(voltage, x=50, y=100)
            self.breadboard.add_component(self.breadboard.voltage_source)
        self.draw_breadboard()

    def remove_power_source(self):
        self.breadboard.remove_voltage_source()
        self.draw_breadboard()

    def select_component(self, event):
        for comp in self.breadboard.components:
            if comp.x - 20 <= event.x <= comp.x + 20 and comp.y - 20 <= event.y <= comp.y + 20:
                self.selected_component = comp
                break

    def drag_component(self, event):
        if self.selected_component:
            self.selected_component.x = event.x
            self.selected_component.y = event.y
            self.draw_breadboard()

    def release_component(self, event):
        if self.selected_component:
            closest_hole = min(self.breadboard.holes.keys(), key=lambda hole: (hole[0] - event.x) ** 2 + (hole[1] - event.y) ** 2)
            self.selected_component.x, self.selected_component.y = closest_hole
            self.selected_component = None
            self.draw_breadboard()

    def reset_simulator(self):
        self.breadboard.reset()
        self.draw_breadboard()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    simulator = BreadboardSimulator()
    simulator.run()
