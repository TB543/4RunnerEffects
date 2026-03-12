from pedalboard import NoiseGate
from UI.Pedals.BasePedal import BasePedal
from UI.Widgets import *


class NoiseGatePedal(BasePedal):
    """
    a class to represent a NoiseGate Pedal
    """

    DRAW_KWARGS = {"fill": "#f2f2f2", "radius": 20, "padx": 1, "aspect": 2 / 3}
    MIN_MAX_VALUES = {"threshold_db": (-100, 0)}
    EFFECT = NoiseGate

    def draw(self, x, y1, y2):
        """
        draws the pedal to the canvas with the given bbox

        :param x: x coordinate of the top left of the rectangle
        :param y1: y coordinate of the top left of the rectangle
        :param y2: y coordinate of the bottom of the rectangle

        :return: the width of the pedal
        """

        width = super().draw(x, y1, y2)
        self.canvas.create_text(self.rel_pos(.5, .6), text="NoiseGate", fill="black", font=("Comic Sans MS", 30, "italic bold"), tags=self.tags)
        Knob(self.canvas, self.rel_pos(.5, .3), 50, lambda v: self.modify("threshold_db", v), self.tags, self.norm("threshold_db"))
        return width
