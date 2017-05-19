from PIL import Image, ImageDraw, ImageFont

def draw_common_shape(draw_method, image, bounds, width=1, outline='white', antialias=4):
    # Use a single channel image (mode='L') as mask.
    # The size of the mask can be increased relative to the imput image
    # to get smoother looking results.
    mask = Image.new(
        size=[int(dim * antialias) for dim in image.size],
        mode='L', color='black')
    draw = ImageDraw.Draw(mask)

    # draw outer shape in white (color) and inner shape in black (transparent)
    for offset, fill in (width/-2.0, 'white'), (width/2.0, 'black'):
        left, top = [(value + offset) * antialias for value in bounds[:2]]
        right, bottom = [(value - offset) * antialias for value in bounds[2:]]
        getattr(draw, draw_method)([left, top, right, bottom], fill=fill)

    # downsample the mask using PIL.Image.LANCZOS
    # (a high-quality downsampling filter).
    mask = mask.resize(image.size, Image.LANCZOS)
    # paste outline color to input image through the mask
    image.paste(outline, mask=mask)

    return image

def draw_ellipse(image, bounds, width=1, outline='white', antialias=4):
    return draw_common_shape('ellipse', image, bounds, width, outline, antialias)

def draw_rectangle(image, bounds, width=1, outline='white', antialias=4):
    return draw_common_shape('rectangle', image, bounds, width, outline, antialias)
