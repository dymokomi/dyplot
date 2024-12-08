from dyplot import DyPlot
from PIL import Image, ImageFilter
import numpy as np
import random
from vector_field import VectorField

image = Image.open("c.jpg").convert('L')

# get image size
image_width, image_height = image.size

# if image is not portrait, rotate it
if image_width > image_height:
    image = image.rotate(90)
    image_width, image_height = image.size


# paper offsete from home 

# small paper size
paper_size_x = 229
paper_size_y = 305

paper_size_x = 356.0
paper_size_y = 432.0

paper_size_x = 129.0
paper_size_y = 210.0

dyplot = DyPlot(canvas_size_mm=(paper_size_x, paper_size_y))
dyplot.go_home()
dyplot.move_axis_to('z', 10.0)

feedrate = 3000.0
margin = 15.0

plotted_width_mm = paper_size_x - margin*2
plotted_height_mm = paper_size_y - margin*2

# crop and resize image to fit on paper using difference in aspect ration of paper and image 
image_aspect_ratio = image_width / image_height
paper_aspect_ratio = paper_size_x / paper_size_y    

image = image.crop((0, 0, image_width, image_width / paper_aspect_ratio))
image_width, image_height = image.size
mm_to_px_ratio = image_width / plotted_width_mm


virtual_pixel_size = 2.0
virtual_pixels_in_x = int(plotted_width_mm / virtual_pixel_size)
virtual_pixels_in_y = int(plotted_height_mm / virtual_pixel_size)

maximum_lines_in_pixel = 6
noise_amount = 0.5

field = VectorField(
    scale=0.01,        # Controls the "zoom level" of the noise
    octaves=5,        # More octaves = more detail
    persistence=0.5,  # How much each octave contributes
    blur_radius=1.0   # Amount of smoothing
)

brightness_levels =  6 
brightness_multiplier = 1.0
minimum_brightness = 0.25
line_density = 20
section_length = 1
dx_multiplier = 1.5
dy_multiplier = dx_multiplier

squarness = 20 
squarness_multiplier = 1.1

starting_coordingates = []
the_index = 0
for x in range(int(paper_size_x*line_density)):

    current_x = x/line_density
    current_y = 0 
    starting_coordingates.append((the_index, (current_x, current_y)))
    the_index += 1

starting_coordingates.reverse()
for y in range(int(paper_size_y*line_density)):

    current_x = 0 
    current_y = y/line_density
    starting_coordingates.append((the_index, (current_x, current_y)))
    the_index += 1

# shuffle the list
random.shuffle(starting_coordingates)

random_points_to_add = 10000
for _ in range(random_points_to_add):
    starting_coordingates.append((the_index, (random.uniform(0, paper_size_x), random.uniform(0, paper_size_y))))
    the_index += 1

lines_to_draw = []
line_buffer = []
for (the_index, (current_x, current_y)) in starting_coordingates:
    image_copy = dyplot.get_image_copy()

    need_lift = True
    while True:
      

        image_px = int(current_x * mm_to_px_ratio)
        image_py = int(current_y * mm_to_px_ratio) 
        if image_px >= image_width or image_py >= image_height:
            break

        dx, dy = field.get_vector(image_px, image_py)
        
        x_factoor = 1.0
        y_factoor = 1.0
        if (current_x / squarness) % 2 == 0:
            x_factoor = squarness_multiplier    
        if (current_y / squarness) % 2 == 0:
            y_factoor = squarness_multiplier    
        target_x = current_x + section_length + dx * dx_multiplier * x_factoor * x_factoor
        target_y = current_y + section_length + dy * dy_multiplier * y_factoor * y_factoor
        image_brightness = image.getpixel((image_px, image_py)) / 255.0
   
        if dyplot.check_radius((current_x + margin, current_y + margin), minimum_brightness + image_brightness * brightness_multiplier, image=image_copy):
            dyplot.line(current_x + margin, current_y + margin, target_x + margin, target_y + margin, need_lift=need_lift)  
            if need_lift:
                lines_to_draw.append(line_buffer)
                line_buffer = [the_index]
                line_buffer.append((current_x + margin, current_y + margin, target_x + margin, target_y + margin))
            else:
                line_buffer.append((current_x + margin, current_y + margin, target_x + margin, target_y + margin))
            need_lift = False
            
        else:
            need_lift = True
            lines_to_draw.append(line_buffer)
            line_buffer = [the_index]

        current_x = target_x
        current_y = target_y

# remove all empty buffers from lines_to_draw
lines_to_draw = [line_buffer for line_buffer in lines_to_draw if len(line_buffer) > 1]

# sort all lines to draw by first point x
lines_to_draw.sort(key=lambda x: x[0])

# redo gcode
dyplot = DyPlot(canvas_size_mm=(paper_size_x, paper_size_y))
dyplot.go_home()
dyplot.move_axis_to('z', 10.0)
for line in lines_to_draw:
    need_lift = True
    for (x1, y1, x2, y2) in line[1:]:
        
        dyplot.line(x1, y1, x2, y2, need_lift=need_lift)
        need_lift = False
    


dyplot.move_axis_to('z', 10.0)
dyplot.go_home()
dyplot.move_axis_to('z', 10.0)
dyplot.save_gcode("draw_01.gcode")
dyplot.show_image()
