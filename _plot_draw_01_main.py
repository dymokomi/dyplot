from dyplot import DyPlot
from PIL import Image, ImageFilter
import numpy as np
import random
image = Image.open("a.jpg").convert('L')

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


virtual_pixel_size = 2.0
virtual_pixels_in_x = int(plotted_width_mm / virtual_pixel_size)
virtual_pixels_in_y = int(plotted_height_mm / virtual_pixel_size)

maximum_lines_in_pixel = 6
noise_amount = 0.5

# create a wave field based on the image
blured_image = image.filter(ImageFilter.GaussianBlur(radius=10.0))
img_array = np.array(blured_image)
grad_y, grad_x = np.gradient(img_array.astype(float))
blured_image.show()

for x in range(int(paper_size_x)):
    y = 150
    image_px = int(x * mm_to_px_ratio)
    image_py = int(y * mm_to_px_ratio) 
    if image_px >= image_width or image_py >= image_height:
        continue

    dx = grad_x[y, x]
    dy = grad_y[y, x]
    length = np.sqrt(dx**2 + dy**2)
    if length == 0:
        break
    dx /= length
    dy /= length
    
        



dyplot.move_axis_to('z', 10.0)
dyplot.go_home()
dyplot.move_axis_to('z', 10.0)
dyplot.save_gcode("test.gcode")
dyplot.show_image()