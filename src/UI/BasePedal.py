from uuid import uuid4
from customtkinter import CTkCanvas


class BasePedal:
    """
    a base class to represent an effects pedal UI
    """

    def __init__(self, canvas : CTkCanvas, tags, aspect):
        """
        initializes the pedal and its fields

        :param canvas: the pedalboard canvas to draw onto
        :param tags: tags to use when drawing the canvas objects so parent class can control behavior
        :param aspect: the aspect ratio of the pedal
        """

        # set fields
        self.canvas = canvas
        self.id = str(uuid4())
        self._aspect = aspect
        self._bbox = (0, 0, 0, 0)

        # ensure tag is tuple
        if isinstance(tags, tuple):
            self._tags = tags + (self.id,)
        elif isinstance(tags, str):
            self._tags = (tags, self.id)
        else:
            self._tags = (self.id,)

    def rel_pos(self, relx=None, rely=None):
        """
        calculates the position of a point given a bbox and relative coordinates
            ** note: this method is unreliable when called outside the draw method
             as bbox on parent canvas is subject to change **

        :param relx: relative position between x1 (value of 0) and x2 (value of 1)
        :param rely: relative position between y1 (value of 0) and y2 (value of 1)

        :return: the actual position
        """

        # calculates positon
        x = y = None
        if relx is not None:
            x = self._bbox[0] + (self._bbox[2] - self._bbox[0]) * relx
        if rely is not None:
            y = self._bbox[1] + (self._bbox[3] - self._bbox[1]) * rely

        # returns only the given relative positions
        if (x is not None) and (y is not None):
            return x, y
        if x is not None:
            return x
        else:
            return y

    def draw(self, x, y1, y2, **kwargs):
        """
        draws the pedal to the canvas with the given bbox

        :param x: x coordinate of the top left of the rectangle
        :param y1: y coordinate of the top left of the rectangle
        :param y2: y coordinate of the bottom of the rectangle
        :param kwargs: the keyword arguments to draw the background

        :return: the width of the pedal
        """

        # base class functionality - draw outline
        width = (y2 - y1) * self._aspect
        self._bbox = (x, y1, x + width, y2)
        self.canvas.delete(self.id)
        self.canvas.create_rounded_rectangle(self._bbox, 20, tags=self._tags, padx=kwargs.get("width", 0) / 2, **kwargs)

        # functionality only for this class - draw selection buttons
        if type(self) == BasePedal:
            pos = self.rel_pos(relx=.5, rely=.07)
            self.canvas.create_text(pos, text="Add Pedal", font=("Comic Sans MS", 20), tags=self._tags)

            # calculates button positions
            buttons = ["Chorus", "Distortion", "Phaser"]
            x1 = self.rel_pos(.1)
            x2 = self.rel_pos(.9)
            for y, name in enumerate(buttons):
                y = self.rel_pos(rely=(y + 1) / (len(buttons) + 1))
                bbox = x1, y, x2, y + 50
                text_pos = bbox[0] + (bbox[2] - bbox[0]) / 2, bbox[1] + (bbox[3] - bbox[1]) / 2

                # draws buttons and text
                button = self.canvas.create_rounded_rectangle(bbox, 10, fill="light blue", tags=self._tags)
                self.canvas.create_text(text_pos, text=name, font=("Comic Sans MS", 20, "italic"), tags=self._tags + (button,))
                self.canvas.add_button_binding(button, lambda e, n=name: self.canvas.add_pedal(n))

        return width

    def delete(self):
        """
        unbinds all button bindings and deletes the canvas objects for the pedal
        """

        self.canvas.delete(self.id)
