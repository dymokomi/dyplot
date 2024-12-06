from dyplot import DyPlot
from PIL import Image
import numpy as np

image = Image.open("image.png")

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

width_slice_width = 3.0 #mm 
divergence_width = 4.0
for x in np.arange(0, plotted_width_mm, width_slice_width):
    dyplot.move_axis_to('z', 10.0)
    dyplot.move_to(x + margin, margin, 10.0)
    dyplot.move_to(x + margin, margin, 0.0)

    for y in np.arange(0,plotted_height_mm, 2.0):
        px_x = int(x * mm_to_px_ratio)
        px_y = int(y * mm_to_px_ratio)
        if px_x < 0 or px_y < 0 or px_x >= image_width or px_y >= image_height:
            continue
        pixel_color = image.getpixel((px_x, px_y))

        pixel_brightness = pixel_color[0] / 255.0

        if pixel_brightness > 0.8:
            dyplot.move_axis_to('z', 5.0)
        elif pixel_brightness < 0.2:
            dyplot.move_axis_to('z', -0.2)
        else:
            dyplot.move_axis_to('z', 0.0)

        


        dyplot.move_by(divergence_width * (1.0 - pixel_brightness), 1.0, 0.0, feedrate)
        dyplot.move_by(-divergence_width * (1.0 - pixel_brightness), 1.0, 0.0, feedrate)


dyplot.go_home()
dyplot.save_gcode("test.gcode")
