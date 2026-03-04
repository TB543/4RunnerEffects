from pedalboard import Distortion
from UI.Pedals.BasePedal import BasePedal
from UI.Widgets import *


class DistortionPedal(BasePedal):
    """
    a class to represent a Distortion Pedal
    """

    DRAW_KWARGS = {"fill": "#EB8A20", "radius": 20, "padx": 1, "aspect": 2 / 3}
    MIN_MAX_VALUES = {"drive_db": (0, 40)}
    EFFECT = Distortion

    def draw(self, x, y1, y2):
        """
        draws the pedal to the canvas with the given bbox

        :param x: x coordinate of the top left of the rectangle
        :param y1: y coordinate of the top left of the rectangle
        :param y2: y coordinate of the bottom of the rectangle

        :return: the width of the pedal
        """

        width = super().draw(x, y1, y2)
        self.canvas.create_text(self.rel_pos(.5, .6), text="Distortion", fill="white", font=("Comic Sans MS", 30, "italic bold"), tags=self.tags)
        Knob(self.canvas, self.rel_pos(.5, .3), 50, lambda v: self.modify("drive_db", v), self.tags, self.norm("drive_db"))
        return width

