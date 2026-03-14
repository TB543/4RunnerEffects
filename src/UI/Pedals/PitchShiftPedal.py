from pedalboard import PitchShift
from UI.Pedals.BasePedal import BasePedal
from UI.Widgets import *


class PitchShiftPedal(BasePedal):
    """
    a class to represent a PitchShift Pedal
    """

    DRAW_KWARGS = {"fill": "#0084D6", "radius": 20, "padx": 1, "aspect": 2 / 3}
    MIN_MAX_VALUES = {"semitones": (-12, 12)}
    EFFECT = PitchShift

    def draw(self, x, y1, y2):
        """
        draws the pedal to the canvas with the given bbox

        :param x: x coordinate of the top left of the rectangle
        :param y1: y coordinate of the top left of the rectangle
        :param y2: y coordinate of the bottom of the rectangle

        :return: the width of the pedal
        """

        width = super().draw(x, y1, y2)
        self.canvas.create_text(self.rel_pos(.5, .6), text="PitchShift", fill="white", font=("Comic Sans MS", 30, "italic bold"), tags=self.tags)
        Knob(self.canvas, self.rel_pos(.5, .3), 50, lambda v: self.modify("semitones", v), self.tags, self.norm("semitones"))
        return width
