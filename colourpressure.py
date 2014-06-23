import colorsys
import csv
import sys
import roygbiv
from colormath.color_objects import RGBColor

class ArtColour:

    hsv = ()
    rgb = ()
    ansi = ()
    ansi_rgb = ()
    ansi_hsv = ()
    _color = None
    GREY = False
    distance = None

    def __init__(self, r, g, b):

        self.rgb = (r, g, b)
        (self.red, self.blue, self.green) = (r, g, b)
        self.hsv = self.rgb_to_hsv(r, g, b)
        (self.hue, self.sat, self.val) = (self.hsv[0], self.hsv[1], self.hsv[2])
        self.ansi = self.ansi_number(r, g, b)
        self.ansi_rgb = self.rgb_reduce(r, g, b)
        self.ansi_hsv = self.rgb_to_hsv(*self.ansi_rgb)

    def rgb_to_hsv(self, r, g, b):

        fracs = [ch/255.0 for ch in (r, g, b)]
        hsv = colorsys.rgb_to_hsv(*fracs)
        return (int(round(hsv[0] * 360)),
                int(round(hsv[1] * 100)),
                int(round(hsv[2] * 100)))

    def hsv_to_rgb(self, h, s, v):

        rgb = colorsys.hsv_to_rgb(h/360.0, s/100.0, v/100.0)

        return (int(round(rgb[0] * 255)),
                int(round(rgb[1] * 255)),
                int(round(rgb[2] * 255)))

    def rgb_reduce(self, r, g, b):

        reduced_rgb = [int(6 * float(val) / 256) * (256/6) for val in (r, g, b)]
        return tuple(reduced_rgb)

    def spin(self, deg):
        return (deg + 180) % 360 - 180

    @property
    def color(self):
        if self._color is None:
            self._color = self._get_color()
        return self._color

    def _get_color(self):

        self.nearest = None
        self.shortest_distance = 100
        chosen_name = None
        for color_dict in (COLOURS, GREYSCALE):
            for name, color in color_dict.iteritems():
                desired_rgb = color[0]

                target = RGBColor(*desired_rgb)
                cdist = target.delta_e(RGBColor(*self.rgb), method="cmc")

                if self.nearest is None or cdist < self.shortest_distance:
                    self.nearest = name
                    self.shortest_distance = cdist
                    self.distance = cdist

                # print 'Checking', name
                (hue_lo, hue_hi) = color[1]

                if hue_lo > hue_hi:
                    h = self.spin(self.hue)
                    hue_lo = self.spin(hue_lo)
                    hue_hi = self.spin(hue_hi)
                else:
                    h = self.hue
                sat_range = color[2] or DEFAULT_SAT
                val_range = color[3] or DEFAUL_VAL

                if h in range(hue_lo, hue_hi + 1) and \
                    self.sat in range(sat_range[0], sat_range[1] + 1) and \
                        self.val in range(val_range[0], val_range[1] + 1):
                    # TODO set up desirable hues, sat and b per named colour
                    target = RGBColor(*desired_rgb)
                    self.distance = cdist
                    chosen_name = name
                    return chosen_name

        return None

    def ansi_number(self, r, g, b):
        '''
        Convert an RGB colour to 256 colour ANSI graphics.
        '''
        grey = False
        poss = True
        step = 2.5

        while poss:  # As long as the colour could be grey scale
            if r < step or g < step or b < step:
                grey = r < step and g < step and b < step
                poss = False

            step += 42.5

        if grey:
            colour = 232 + int(float(sum([r, g, b]) / 33.0))
        else:
            colour = sum([16] + [int((6 * float(val) / 256)) * mod
                         for val, mod in ((r, 36), (g, 6), (b, 1))])
        return colour

if __name__ == "__main__":
    VERBOSE = False
    if sys.argv[1] == "-v":
        image = sys.argv[2]
        VERBOSE = True
    else:
        image = sys.argv[1]
        
    roy_im = roygbiv.Roygbiv(image)
    p = roy_im.get_palette()
    
    line = ""
    rgbs = []
    hsvs = []
    for palette_colour in p.colors:
        c = ArtColour(*palette_colour.value)
        if VERBOSE:
            print '\x1b[48;5;%dm     \x1b[0m' % (c.ansi)
        rgbs.append(c.rgb)
        hsvs.append(c.hsv)

        
    line = "" 
    
    rgb_string = '|'.join(["(%s,%s,%s)" % (ab[0], ab[1], ab[2]) for ab in rgbs])
    hsv_string = '|'.join(["(%s,%s,%s)" % (ab[0], ab[1], ab[2]) for ab in hsvs])
    
    print '"%s","%s","%s"' % (image, rgb_string, hsv_string)
    