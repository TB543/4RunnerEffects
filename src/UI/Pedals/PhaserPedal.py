from pedalboard import Phaser
from UI.Pedals.BasePedal import BasePedal
from UI.Widgets import *


class PhaserPedal(BasePedal):
    """
    a class to represent a Phaser Pedal
    """

    DRAW_KWARGS = {"fill": "#18BD60", "radius": 20, "padx": 1, "aspect": 2 / 3}
    MIN_MAX_VALUES = {"rate_hz": (0, 1), "depth": (0, .9)}
    EFFECT = Phaser

    def draw(self, x, y1, y2):
        """
        draws the pedal to the canvas with the given bbox

        :param x: x coordinate of the top left of the rectangle
        :param y1: y coordinate of the top left of the rectangle
        :param y2: y coordinate of the bottom of the rectangle

        :return: the width of the pedal
        """

        width = super().draw(x, y1, y2)
        self.canvas.create_text(self.rel_pos(.5, .6), text="Phaser", fill="white", font=("Comic Sans MS", 30, "italic bold"), tags=self.tags)
        Knob(self.canvas, self.rel_pos(.25, .3), 50, lambda v: self.modify("rate_hz", v), self.tags, self.norm("rate_hz"))
        Knob(self.canvas, self.rel_pos(.75, .3), 50, lambda v: self.modify("depth", v), self.tags, self.norm("depth"))
        return width
