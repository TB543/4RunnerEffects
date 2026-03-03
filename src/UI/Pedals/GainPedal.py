from pedalboard import Gain
from UI.Pedals.BasePedal import BasePedal
from UI.Widgets import *


class GainPedal(BasePedal):
    """
    a class to represent a Gain Pedal
    """

    DRAW_KWARGS = {"fill": "blue", "radius": 20, "padx": 1, "aspect": 2 / 3}
    MIN_MAX_VALUES = {"gain_db": (0, 20)}
    EFFECT = Gain

    def draw(self, x, y1, y2):
        """
        draws the pedal to the canvas with the given bbox todo make pretty

        :param x: x coordinate of the top left of the rectangle
        :param y1: y coordinate of the top left of the rectangle
        :param y2: y coordinate of the bottom of the rectangle

        :return: the width of the pedal
        """

        width = super().draw(x, y1, y2)
        Knob(self.canvas, self.rel_pos(.5, .5), 50, lambda v: self.modify("gain_db", v), self.tags, self.norm("gain_db"))
        return width
