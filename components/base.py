class Component:
    def __init__(self, name, x=0, y=0):
        self.name = name
        self.x = x
        self.y = y
        self.connected_to = []

    def connect(self, component):
        if component not in self.connected_to:
            self.connected_to.append(component)
            component.connected_to.append(self)

    def disconnect(self, component):
        if component in self.connected_to:
            self.connected_to.remove(component)
            component.connected_to.remove(self)

    def __repr__(self):
        return f"{self.name} at ({self.x}, {self.y})"
