from customtkinter import CTkCanvas
from tkinter import EventType
from uuid import uuid4
from math import radians, sin, cos, atan2, pi


class Knob:
    """
    a class to represent a knob widget that can be rotated to adjust its value
    """

    MIN_ANGLE = radians(230)
    MAX_ANGLE = radians(140)

    def __init__(self, canvas: CTkCanvas, pos, r, callback, tags):
        """
        creates the knob widget

        :param canvas: the canvas to draw to
        :param pos: the position of the knob
        :param r: the radius of the knob
        :param callback: the callback function to call when the knob value changes
            should have 1 parameter which is a normalized value between 0 and 1 representing knob rotation
        :param tags: the tags to draw the knob with
        """

        # sets fields
        self._id = str(uuid4())
        self.canvas = canvas
        self.r = r
        self._callback = callback
        self.tags = tags + (self._id,)
        self._mouse_angle = None

        # draws and adds functionality
        self.angle = Knob.MIN_ANGLE
        self._center_id = self.draw(pos)
        self.canvas.tag_bind(self._id, "<Button-1>", self._rotate)
        self.canvas.tag_bind(self._id, "<B1-Motion>", self._rotate)

    def draw(self, pos):
        """
        draws the knob to the screen todo make pretty

        :param pos: the current position of the knob (can be changed by canvas moves)

        :return: the id of the circle that contains the rotational center of the knob
        """

        tag = self.canvas.create_aa_circle(*pos, self.r, fill="black", tags=self.tags)
        x = pos[0] + self.r * sin(self.angle)
        y = pos[1] - self.r * cos(self.angle)
        self.canvas.create_line(*pos, x, y, fill="white", tags=self.tags)
        return tag

    def _rotate(self, event):
        """
        handles when the knob is rotated
        """

        # ignore the generated click event that ensures click is maintained across redraw
        if event.type == EventType.ButtonPress and event.state & 0x0100:
            return

        # calculates current mouse angle
        pos = super(CTkCanvas, self.canvas).coords(self._center_id)
        dx = event.x - pos[0]
        dy = event.y - pos[1]
        angle = atan2(dy, dx)

        # handles when knob is first clicked
        if event.type == EventType.ButtonPress:
            self._mouse_angle = angle
            return

        # finds the change in angle accounting for wraparound
        delta_angle = angle - self._mouse_angle
        delta_angle = max(-pi, min(pi, ((delta_angle + pi) % (2 * pi)) - pi))
        self.angle += delta_angle
        self.angle = self.angle % (2 * pi)
        self._mouse_angle = angle

        # clamps angle to min and max values
        if self.angle >= Knob.MIN_ANGLE or self.angle <= Knob.MAX_ANGLE:
            self.angle = self.angle
        elif self.angle < Knob.MIN_ANGLE and delta_angle < 0:
            self.angle = Knob.MIN_ANGLE
        else:
            self.angle = Knob.MAX_ANGLE

        # redraws the knob at the new rotation value
        self.canvas.delete(self._id)
        self._center_id = self.draw(pos)
        self.canvas.event_generate("<Button-1>", x=pos[0], y=pos[1], state=256)

        # calculates new value
        total_sweep = (Knob.MAX_ANGLE - Knob.MIN_ANGLE) % (2 * pi)
        current_position = (self.angle - Knob.MIN_ANGLE) % (2 * pi)
        self._callback((current_position / total_sweep))
