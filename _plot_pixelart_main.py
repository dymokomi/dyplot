from dyplot import DyPlot
from PIL import Image
import numpy as np
import random
image = Image.open("image.png").convert('L')

# get image size
image_width, image_height = image.size

# if image is not portrait, rotate it
if image_width > image_height:
    image = image.rotate(90)
    image_width, image_height = image.size


dyplot = DyPlot()
dyplot.go_home()
dyplot.move_axis_to('z', 10.0)

# paper offsete from home 
paper_size_x = 356.0
paper_size_y = 432.0

feedrate = 3000.0
margin = 10.0

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

maximum_lines_in_pixel = 20
noise_amount = 1.0

for px_x in range(virtual_pixels_in_x):
    dyplot.move_axis_to('z', 5.0)
    dyplot.move_to(margin + px_x * virtual_pixel_size, margin, 5.0)
    for px_y in range(virtual_pixels_in_y):
        image_px = int(px_x * mm_to_px_ratio * virtual_pixel_size)
        image_py = int(px_y * mm_to_px_ratio * virtual_pixel_size)   
        if image_px > image_width or image_py > image_height:
            continue

        dyplot.move_axis_to('z', 5.0)
        (nx, ny) = ((random.random() - 0.5) * noise_amount, (random.random() - 0.5) * noise_amount)
        dyplot.move_to(margin + px_x * virtual_pixel_size + nx, margin + px_y * virtual_pixel_size + ny, 5.0)
        dyplot.move_axis_to('z', 0.0)
        # Draw the pixel square
        (nx, ny) = ((random.random() - 0.5) * noise_amount, (random.random() - 0.5) * noise_amount)
        dyplot.move_by(virtual_pixel_size + nx, 0.0 + ny, 0.0, feedrate)
        (nx, ny) = ((random.random() - 0.5) * noise_amount, (random.random() - 0.5) * noise_amount)
        dyplot.move_by(0.0 + nx, virtual_pixel_size + ny, 0.0, feedrate)
        (nx, ny) = ((random.random() - 0.5) * noise_amount, (random.random() - 0.5) * noise_amount)
        dyplot.move_by(-virtual_pixel_size + nx, 0.0 + ny, 0.0, feedrate)
        (nx, ny) = ((random.random() - 0.5) * noise_amount, (random.random() - 0.5) * noise_amount)
        dyplot.move_by(0.0 + nx, -virtual_pixel_size + ny, 0.0, feedrate)
        dyplot.move_axis_to('z', 5.0)

        
        pixel_color = image.getpixel((image_px, image_py))
        pixel_brightness = pixel_color / 255.0 

        lines_to_draw = int(maximum_lines_in_pixel * pixel_brightness)
        for _ in range(lines_to_draw):
            top_edge = random.random() * virtual_pixel_size
            bottom_edge = random.random() * virtual_pixel_size
            (nx, ny) = ((random.random() - 0.5) * noise_amount, (random.random() - 0.5) * noise_amount)
            dyplot.move_to(margin + px_x * virtual_pixel_size + top_edge + nx,    margin + px_y * virtual_pixel_size + ny, 0.0)
            (nx, ny) = ((random.random() - 0.5) * noise_amount, (random.random() - 0.5) * noise_amount)
            dyplot.move_to(margin + px_x * virtual_pixel_size + bottom_edge + nx, margin + px_y * virtual_pixel_size + virtual_pixel_size + ny, 0.0)







dyplot.move_axis_to('z', 10.0)
dyplot.go_home()
dyplot.move_axis_to('z', 10.0)
dyplot.save_gcode("test.gcode")
