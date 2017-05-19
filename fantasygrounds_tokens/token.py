from fantasygrounds_tokens import draw_ellipse, draw_rectangle
from PIL import Image, ImageDraw, ImageFont
from cStringIO import StringIO
import os

class Token(object):
    letter_prefix = None
    max_tokens = None
    color = None

    shape = None

    background = None
    width = 280
    height = 280

    half_width = None
    half_height = None

    offset = 15
    output_dir = './'

    def __init__(self, letter_prefix, max_tokens, color):
        self.set_prefix_letter(letter_prefix)
        self.set_max_tokens(max_tokens)

        assert isinstance(color, tuple), "Color must be a tuple of (r, g, b) OR (r, g, b, a)"
        self.set_color(*color)

    def set_color(self, r, g, b, a=None):
        assert r >= 0 and r <= 255, "Red channel must be 0-255"
        assert g >= 0 and g <= 255, "Green channel must be 0-255"
        assert b >= 0 and b <= 255, "Blue channel must be 0-255"

        if a is not None:
            assert a >= 0 and a <= 255, "Alpha must be 0-255"
            self.color = (r, g, b, a)
        else:
            self.color = (r, g, b)

    def set_prefix_letter(self, a_letter):
        assert len(a_letter) == 1, "Prefix Letter can only be ONE character"

        self.letter_prefix = a_letter

    def set_max_tokens(self, a_number):
        assert a_number >= 1 and a_number <= 9, "Max tokens must be 1-9"
        self.max_tokens = a_number

    def circular(self):
        self.shape = 'circle'
        return self

    def square(self):
        self.shape = 'square'
        return self

    def image_to_disk(self, index):
        image_bytes = StringIO()
        self.im.save(image_bytes, 'png')
        # display(ipython_image(data=image_bytes.getvalue()))

        image_filename = '{output_dir}/{prefix}{num}.png'.format(
            output_dir=self.output_dir,
            prefix=self.letter_prefix,
            num=index
        )
        print "--- Saving to {image_filename}".format(
            image_filename=image_filename
        )
        self.im.save(image_filename, 'png')

    def render(self, *args, **kwargs):
        if self.color is None:
            self.color = (241, 63, 63)

        if self.background is None:
            self.background = (44, 44, 44)

        self.width = int(kwargs.get('width', 280))
        self.height = int(kwargs.get('height', 280))

        self.half_width = self.width / 2
        self.half_height = self.height / 2

        self.output_dir = kwargs.get('output_dir')
        self.font_file = kwargs.get('font', os.path.expanduser('~/Library/Fonts/PragmataPro_Mono_R_0822.ttf'))


        # Text Placement
        self.text_height_pts = int(kwargs.get('font_size', 200))
        self.text_x = ((self.width - self.text_height_pts) / 2) + 5
        self.text_y = ((self.height - self.text_height_pts)/ 2) - 15

        # Offset
        self.offset = 15

        # Center fill width
        self.inner_fill_width = self.width - 15

        self.im = Image.new('RGBA', (self.width, self.height))
        self.im_font = ImageFont.truetype(self.font_file, self.text_height_pts)

        self.im_draw = ImageDraw.Draw(self.im)

        # Outer ellipse path
        self.outer_border_box = [15, 15, 265, 265]

        render_method = 'render_%s' % self.shape
        assert hasattr(self, render_method), "%s is an unknown shape..." % self.shape

        for i in range(1, self.max_tokens + 1):
            print ">>> {prefix}{token_number} with FG={fgcolor} and BG={bgcolor}".format(
                prefix=self.letter_prefix,
                token_number=i,
                fgcolor=self.color,
                bgcolor=self.background
            )
            getattr(self, render_method)(i)

    def render_circle(self, index):
        print "RENDER CIRCLE %s%s" % (self.letter_prefix, index)
        draw_ellipse(
            self.im,
            self.outer_border_box,
            width=20,
            outline=self.background
        )

        # Inner Fill
        draw_ellipse(
            self.im,
            (self.half_width, self.half_height, self.half_width, self.half_height),
            outline=self.background,
            width=self.inner_fill_width,
            antialias=8
        )

        # Border Stripe
        draw_ellipse(
            self.im,
            self.outer_border_box,
            outline=self.color,
            width=5,
            antialias=8
        )

        self.im_draw.text((self.text_x, self.text_y), "{prefix}{number}".format(prefix=self.letter_prefix, number=index), font=self.im_font, fill=self.color)

        self.image_to_disk(index)

    def render_square(self, index):
        print "RENDER SQUARE %s%s" % (self.letter_prefix, index)
        # Color under border
        draw_rectangle(self.im, self.outer_border_box, width=20, outline=self.background)

        # Inner Fill
        draw_rectangle(
            self.im,
            (self.offset, self.offset, self.width, self.height),
            outline=self.background,
            width=self.inner_fill_width,
            antialias=8
        )

        # Outer Stripe
        draw_rectangle(self.im, self.outer_border_box, outline=self.color, width=5, antialias=8)

        self.im_draw.text((self.text_x, self.text_y), "{prefix}{number}".format(prefix=self.letter_prefix, number=index), font=self.im_font, fill=self.color)

        self.image_to_disk(index)
