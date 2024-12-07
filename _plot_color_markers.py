from dyplot import DyPlot
from PIL import Image
import numpy as np
import random
image = Image.open("image3.png")

# get image size
image_width, image_height = image.size

# if image is not portrait, rotate it
if image_width > image_height:
    image = image.rotate(90)
    image_width, image_height = image.size




# paper offsete from home 
paper_size_x = 229
paper_size_y = 305

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


virtual_pixel_size = 5.0
virtual_pixels_in_x = int(plotted_width_mm / virtual_pixel_size)
virtual_pixels_in_y = int(plotted_height_mm / virtual_pixel_size)

noise_amount = 0.2
max_circle_radius = 5.0

for px_x in range(virtual_pixels_in_x):
    dyplot.move_axis_to('z', 5.0)
    dyplot.move_to(margin + px_x * virtual_pixel_size, margin, 5.0)
    for px_y in range(virtual_pixels_in_y):
        image_px = int(px_x * mm_to_px_ratio * virtual_pixel_size)
        image_py = int(px_y * mm_to_px_ratio * virtual_pixel_size)   
        if image_px >= image_width or image_py >= image_height:
            continue

        pixel_color = image.getpixel((image_px, image_py))
        
        (yellow, red, blue) = dyplot.rgb_to_yrb(pixel_color[0], pixel_color[1], pixel_color[2])
        
        dyplot.draw_circle_mm((margin + px_x * virtual_pixel_size, margin + px_y * virtual_pixel_size), 
                              yellow * max_circle_radius, 
                              0.5,
                              "yellow",
                              multiply_blend=True)
        dyplot.draw_circle_mm((margin + px_x * virtual_pixel_size, margin + px_y * virtual_pixel_size), 
                              red * max_circle_radius, 
                              0.5,
                              "red",
                              multiply_blend=True)
        dyplot.draw_circle_mm((margin + px_x * virtual_pixel_size, margin + px_y * virtual_pixel_size), 
                              blue * max_circle_radius, 
                              0.5,
                              "blue",
                              multiply_blend=True)
        






dyplot.move_axis_to('z', 10.0)
dyplot.go_home()
dyplot.move_axis_to('z', 10.0)
dyplot.save_gcode("test.gcode")
dyplot.show_image()