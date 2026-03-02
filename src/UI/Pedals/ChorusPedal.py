from pedalboard import Chorus
from UI.Pedals.BasePedal import BasePedal
from UI.Widgets import *


class ChorusPedal(BasePedal, Chorus):
    """
    a class to represent a Chorus Pedal
    """

    DRAW_KWARGS = {"fill": "blue", "radius": 20, "padx": 1, "aspect": 2 / 3}

    def draw(self, x, y1, y2):
        """
        draws the pedal to the canvas with the given bbox todo make pretty and add sound mods

        :param x: x coordinate of the top left of the rectangle
        :param y1: y coordinate of the top left of the rectangle
        :param y2: y coordinate of the bottom of the rectangle

        :return: the width of the pedal
        """

        width = super().draw(x, y1, y2)
        Knob(self.canvas, self.rel_pos(.5, .5), 50, lambda v: print("implement audio effect modification"), self.tags)
        return width
