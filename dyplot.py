from PIL import Image, ImageDraw 
import math 

class DyPlot:
    
    def __init__(self, canvas_size_mm = (356.0, 432.0)):
        self.canvas_size_mm = canvas_size_mm
        self.gcode = []
        self.gcode.append("G21")
        self.gcode.append("G90")
        self.mode = 'absolute'
        self.last_code = ""
        self.x = 0.0 
        self.y = 0.0 
        self.z = 0.0 

        self.pen_width_mm = 0.3

        self.create_image_mm(canvas_size_mm[0], canvas_size_mm[1], "white")
    def show_image(self):
        self.image.show()
    def save_image(self, filename):
        self.image.save(filename)
    def mm_to_pixels(self, mm, dpi=300):
        return round(mm * dpi / 25.4)
    
    def create_image_mm(self, width_mm, height_mm, color="white", dpi=300):
        width_px = self.mm_to_pixels(width_mm, dpi)
        height_px = self.mm_to_pixels(height_mm, dpi)
        self.image = Image.new("RGB", (width_px, height_px), color)
    def draw_line_mm(self, start_point_mm, end_point_mm, thickness_mm, color="black", dpi=300):
    
        start_point_px = (self.mm_to_pixels(start_point_mm[0], dpi), 
                        self.mm_to_pixels(start_point_mm[1], dpi))
        end_point_px = (self.mm_to_pixels(end_point_mm[0], dpi), 
                        self.mm_to_pixels(end_point_mm[1], dpi))
        thickness_px = self.mm_to_pixels(thickness_mm, dpi)
        draw = ImageDraw.Draw(self.image)
        draw.line([start_point_px, end_point_px], fill=color, width=thickness_px)

    def draw_circle_mm(self, center_mm, radius_mm, thickness_mm, color="black", dpi=300, multiply_blend=False, feedrate=1000):

        start_x = center_mm[0] + radius_mm
        start_y = center_mm[1]
        self.gcode.append(f"G0 Z2.0")
        self.gcode.append(f"G0 X{start_x} Y{start_y}")
        if radius_mm > 0.0:
            self.gcode.append(f"G0 Z0.0")
            self.gcode.append(f"G2 X{start_x} Y{start_y} I{-radius_mm} J0 F{feedrate}")
        



        center_px = (self.mm_to_pixels(center_mm[0], dpi), 
                        self.mm_to_pixels(center_mm[1], dpi))
        radius_px = self.mm_to_pixels(radius_mm, dpi)
        thickness_px = self.mm_to_pixels(thickness_mm, dpi)

        draw = ImageDraw.Draw(self.image)
        draw.ellipse([center_px[0] - radius_px, center_px[1] - radius_px, center_px[0] + radius_px, center_px[1] + radius_px], outline=color, width=thickness_px)
        
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
        if self.z + z < 0.5:
            self.draw_line_mm((self.x, self.y), (self.x + x, self.y + y), self.pen_width_mm, "black")
        self.x += x
        self.y += y
        self.z += z
        if feedrate is None:
            self.gcode.append(f"G0 X{x} Y{y} Z{z}")
        else:
            self.gcode.append(f"G1 X{x} Y{y} Z{z} F{feedrate}")
    def move_to(self, x, y, z, feedrate=None):
        self.mode_absolute()
        if self.z + z < 0.5:
            self.draw_line_mm((self.x, self.y), (x, y), self.pen_width_mm, "black")
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
        self.draw_line_mm((x2, y2), (x1, y1), self.pen_width_mm, "black")

    def rgb_to_yrb(self, r, g, b):

        # Normalize RGB values to 0-1
        r = r / 255
        g = g / 255
        b = b / 255
        
        # Yellow is derived from red and green
        yellow = min(r, g)
        
        # After yellow is extracted, remaining red goes to red value
        red = max(0, r - yellow)
        
        # Blue comes directly from blue channel
        blue = b
        
        # Normalize the values so at least one is 1 (if not black)
        max_value = max(yellow, red, blue)
        if max_value > 0:
            yellow = yellow / max_value
            red = red / max_value
            blue = blue / max_value
        
        return (yellow, red, blue)