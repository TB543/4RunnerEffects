from pedalboard import Limiter
from UI.Pedals.BasePedal import BasePedal
from UI.Widgets import *


class LimiterPedal(BasePedal):
    """
    a class to represent a Limiter Pedal
    """

    DRAW_KWARGS = {"fill": "black", "radius": 20, "padx": 1, "aspect": 2 / 3}
    MIN_MAX_VALUES = {}
    EFFECT = Limiter

    def draw(self, x, y1, y2):
        """
        draws the pedal to the canvas with the given bbox

        :param x: x coordinate of the top left of the rectangle
        :param y1: y coordinate of the top left of the rectangle
        :param y2: y coordinate of the bottom of the rectangle

        :return: the width of the pedal
        """

        width = super().draw(x, y1, y2)

        return width
