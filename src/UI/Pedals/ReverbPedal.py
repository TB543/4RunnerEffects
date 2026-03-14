from pedalboard import Reverb
from UI.Pedals.BasePedal import BasePedal
from UI.Widgets import *


class ReverbPedal(BasePedal):
    """
    a class to represent a Reverb Pedal
    """

    DRAW_KWARGS = {"fill": "#5b448a", "radius": 20, "padx": 1, "aspect": 2 / 3}
    MIN_MAX_VALUES = {"room_size": (0, 1), "damping": (0, 1)}
    EFFECT = Reverb

    def draw(self, x, y1, y2):
        """
        draws the pedal to the canvas with the given bbox

        :param x: x coordinate of the top left of the rectangle
        :param y1: y coordinate of the top left of the rectangle
        :param y2: y coordinate of the bottom of the rectangle

        :return: the width of the pedal
        """

        width = super().draw(x, y1, y2)
        self.canvas.create_text(self.rel_pos(.5, .6), text="Reverb", fill="white", font=("Comic Sans MS", 30, "italic bold"), tags=self.tags)
        Knob(self.canvas, self.rel_pos(.25, .3), 50, lambda v: self.modify("room_size", v), self.tags, self.norm("room_size"))
        Knob(self.canvas, self.rel_pos(.75, .3), 50, lambda v: self.modify("damping", v), self.tags, self.norm("damping"))
        return width
