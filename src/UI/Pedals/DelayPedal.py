from pedalboard import Delay
from UI.Pedals.BasePedal import BasePedal
from UI.Widgets import *


class DelayPedal(BasePedal):
    """
    a class to represent a Delay Pedal
    """

    DRAW_KWARGS = {"fill": "#ea2131", "radius": 20, "padx": 1, "aspect": 2 / 3}
    MIN_MAX_VALUES = {"delay_seconds": (0, 2), "feedback": (0, 1)}
    EFFECT = Delay

    def draw(self, x, y1, y2):
        """
        draws the pedal to the canvas with the given bbox

        :param x: x coordinate of the top left of the rectangle
        :param y1: y coordinate of the top left of the rectangle
        :param y2: y coordinate of the bottom of the rectangle

        :return: the width of the pedal
        """

        width = super().draw(x, y1, y2)
        self.canvas.create_text(self.rel_pos(.5, .6), text="Delay", fill="white", font=("Comic Sans MS", 30, "italic bold"), tags=self.tags)
        Knob(self.canvas, self.rel_pos(.25, .3), 50, lambda v: self.modify("delay_seconds", v), self.tags, self.norm("delay_seconds"))
        Knob(self.canvas, self.rel_pos(.75, .3), 50, lambda v: self.modify("feedback", v), self.tags, self.norm("feedback"))
        return width
