from pedalboard import LowShelfFilter
from UI.Pedals.BasePedal import BasePedal
from UI.Widgets import *


class LowShelfFilterPedal(BasePedal):
    """
    a class to represent a LowShelfFilter Pedal
    """

    DRAW_KWARGS = {"fill": "#18BD60", "radius": 20, "padx": 1, "aspect": 2 / 3}
    MIN_MAX_VALUES = {"cutoff_frequency_hz": (20, 20000), "gain_db": (-15, 15)}
    EFFECT = LowShelfFilter

    def draw(self, x, y1, y2):
        """
        draws the pedal to the canvas with the given bbox

        :param x: x coordinate of the top left of the rectangle
        :param y1: y coordinate of the top left of the rectangle
        :param y2: y coordinate of the bottom of the rectangle

        :return: the width of the pedal
        """

        width = super().draw(x, y1, y2)
        self.canvas.create_text(self.rel_pos(.5, .6), text="LowShelfFilter", fill="white", font=("Comic Sans MS", 30, "italic bold"), tags=self.tags)
        Knob(self.canvas, self.rel_pos(.25, .3), 50, lambda v: self.modify("cutoff_frequency_hz", v), self.tags, self.norm("cutoff_frequency_hz"))
        Knob(self.canvas, self.rel_pos(.75, .3), 50, lambda v: self.modify("gain_db", v), self.tags, self.norm("gain_db"))
        return width
