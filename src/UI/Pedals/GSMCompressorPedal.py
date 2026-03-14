from pedalboard import GSMFullRateCompressor
from UI.Pedals.BasePedal import BasePedal
from UI.Widgets import *


class GSMCompressorPedal(BasePedal):
    """
    a class to represent a GSMCompressor Pedal
    """

    DRAW_KWARGS = {"fill": "#EB8A20", "radius": 20, "padx": 1, "aspect": 2 / 3}
    MIN_MAX_VALUES = {}
    EFFECT = GSMFullRateCompressor

    def draw(self, x, y1, y2):
        """
        draws the pedal to the canvas with the given bbox

        :param x: x coordinate of the top left of the rectangle
        :param y1: y coordinate of the top left of the rectangle
        :param y2: y coordinate of the bottom of the rectangle

        :return: the width of the pedal
        """

        width = super().draw(x, y1, y2)
        self.canvas.create_text(self.rel_pos(.5, .6), text="GSMCompressor", fill="black", font=("Comic Sans MS", 28, "italic bold"), tags=self.tags)
        self.canvas.create_text(self.rel_pos(.5, .3), text="Status: On", fill="black", font=("Comic Sans MS", 28, "italic bold"), tags=self.tags)
        return width
