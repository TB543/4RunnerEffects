from pedalboard import MP3Compressor
from UI.Pedals.BasePedal import BasePedal
from UI.Widgets import *


class MP3CompressorPedal(BasePedal):
    """
    a class to represent a MP3Compressor Pedal
    """

    DRAW_KWARGS = {"fill": "#f2f2f2", "radius": 20, "padx": 1, "aspect": 2 / 3}
    MIN_MAX_VALUES = {"vbr_quality": (0, 9)}
    EFFECT = MP3Compressor

    def draw(self, x, y1, y2):
        """
        draws the pedal to the canvas with the given bbox

        :param x: x coordinate of the top left of the rectangle
        :param y1: y coordinate of the top left of the rectangle
        :param y2: y coordinate of the bottom of the rectangle

        :return: the width of the pedal
        """

        width = super().draw(x, y1, y2)
        self.canvas.create_text(self.rel_pos(.5, .6), text="MP3Compressor", fill="black", font=("Comic Sans MS", 28, "italic bold"), tags=self.tags)
        Knob(self.canvas, self.rel_pos(.5, .3), 50, lambda v: self.modify("vbr_quality", v), self.tags, self.norm("vbr_quality"))
        return width
