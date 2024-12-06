
class DyPlot:
    
    def __init__(self):
        self.gcode = []
        self.gcode.append("G21")
        self.gcode.append("G90")
        self.mode = 'absolute'
        self.last_code = ""
        self.x = 0.0 
        self.y = 0.0 
        self.z = 0.0 
        
    def save_gcode(self, filename):
        with open(filename, 'w') as f:
            for line in self.gcode:
                f.write(line + '\n')

    def mode_absolute(self):
        if self.mode != 'absolute':
            self.gcode.append("G90")
            self.mode = 'absolute'

    def mode_relative(self):
        if self.mode != 'relative':
            self.gcode.append("G91")
            self.mode = 'relative'

    def mode_units_mm(self):
        self.gcode.append("G21")

    def move_axis_by(self, axis, distance, feedrate=None):
        self.mode_relative()
        if axis == 'x':
            self.x += distance
            if feedrate is None:
                self.gcode.append(f"G0 X{distance}")
            else:
                self.gcode.append(f"G1 X{distance} F{feedrate}")
        elif axis == 'y':
            self.y += distance
            if feedrate is None:
                self.gcode.append(f"G0 Y{distance}")
            else:
                self.gcode.append(f"G1 Y{distance} F{feedrate}")
        elif axis == 'z':
            self.z += distance
            if feedrate is None:
                self.gcode.append(f"G0 Z{distance}")
            else:
                self.gcode.append(f"G1 Z{distance} F{feedrate}")
    def move_axis_to(self, axis, position, feedrate=None):
        self.mode_absolute()
        if axis == 'x':
            self.x = position
            if feedrate is None:
                self.gcode.append(f"G0 X{self.x}")
            else:
                self.gcode.append(f"G1 X{self.x} F{feedrate}")
        elif axis == 'y':
            self.y = position
            if feedrate is None:
                self.gcode.append(f"G0 Y{self.y}")
            else:
                self.gcode.append(f"G1 Y{self.y} F{feedrate}")
        elif axis == 'z':
            self.z = position
            if feedrate is None:
                self.gcode.append(f"G0 Z{self.z}")
            else:
                self.gcode.append(f"G1 Z{self.z} F{feedrate}")
    def move_by(self, x, y, z, feedrate=None):
        self.mode_relative()
        self.x += x
        self.y += y
        self.z += z
        if feedrate is None:
            self.gcode.append(f"G0 X{x} Y{y} Z{z}")
        else:
            self.gcode.append(f"G1 X{x} Y{y} Z{z} F{feedrate}")
    def move_to(self, x, y, z, feedrate=None):
        self.mode_absolute()
        self.x = x
        self.y = y
        self.z = z
        if feedrate is None:
            self.gcode.append(f"G0 X{self.x} Y{self.y} Z{self.z}")
        else:
            self.gcode.append(f"G1 X{self.x} Y{self.y} Z{self.z} F{feedrate}")
    def go_home(self):
        if self.z <= 1.0:
            self.move_axis_to('z', 5.0)
        self.mode_absolute()   
        self.move_axis_to('x', 0.0)
        self.move_axis_to('y', 0.0)     
        self.move_axis_to('z', 0.0)

    def line(self, x1, y1, x2, y2, z_offset=0.0, feedrate=None):
        self.gcode.append("")
        self.gcode.append(";draw line")
        self.mode_absolute()
        self.move_axis_to('z', 5.0)
        self.move_to(x1, y1, 5.0)

        # Lower pen
        self.move_axis_to('z', z_offset)

        # Draw line
        self.move_to(x2, y2, z_offset, feedrate)
        self.move_axis_to('z', 5.0)

