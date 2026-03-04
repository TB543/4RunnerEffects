from uuid import uuid4
from customtkinter import CTkCanvas


class BasePedal:
    """
    a base class to represent an effects pedal UI
    """

    DRAW_KWARGS = {"fill": "gray", "width": 4, "radius": 20, "padx": 1, "aspect": 2 / 3}
    MIN_MAX_VALUES = {}  # {effect: (min, max)}
    EFFECT = None

    def __init__(self, canvas: CTkCanvas, tags):
        """
        initializes the pedal and its fields

        :param canvas: the pedalboard canvas to draw onto
        :param tags: tags to use when drawing the canvas objects so parent class can control behavior
        """

        # set fields
        super().__init__()
        self.canvas = canvas
        self.id = str(uuid4())
        self._bbox = (0, 0, 0, 0)
        if self.EFFECT is not None:
            self.effect = self.EFFECT()

        # ensure tag is tuple
        if isinstance(tags, tuple):
            self.tags = tags + (self.id,)
        elif isinstance(tags, str):
            self.tags = (tags, self.id)
        else:
            self.tags = (self.id,)

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

    def norm(self, attr):
        """
        normalizes the value of a given attribute

        :param attr: the attribute to normalize
        """

        return (getattr(self.effect, attr) - self.MIN_MAX_VALUES[attr][0]) / (self.MIN_MAX_VALUES[attr][1] - self.MIN_MAX_VALUES[attr][0])

    def modify(self, attr, value):
        """
        modified the audio effect

        :param attr: the attribute to modify
        :param value: the new value for the attribute
        """

        value = self.MIN_MAX_VALUES[attr][0] + value * (self.MIN_MAX_VALUES[attr][1] - self.MIN_MAX_VALUES[attr][0])
        setattr(self.effect, attr, value)

    def draw(self, x, y1, y2):
        """
        draws the pedal to the canvas with the given bbox

        :param x: x coordinate of the top left of the rectangle
        :param y1: y coordinate of the top left of the rectangle
        :param y2: y coordinate of the bottom of the rectangle

        :return: the width of the pedal
        """

        # extract params
        kwargs = self.DRAW_KWARGS.copy()
        r = kwargs.pop("radius", 0)
        padx = (kwargs.get("width", 2) / 2) + kwargs.pop("padx", 0)
        width = (y2 - y1) * kwargs.pop("aspect", 2 / 3)

        # delete and re-draw outline
        self._bbox = (x, y1, x + width, y2)
        self.destroy()
        self.canvas.create_rounded_rectangle(self._bbox, r, tags=self.tags, padx=padx, **kwargs)

        # draw delete button - every pedal but base pedal
        if type(self) != BasePedal:
            delete_pos = self.rel_pos(.5, .9)
            delete_bbox = (delete_pos[0] - 25, delete_pos[1] - 25, delete_pos[0] + 25, delete_pos[1] + 25)
            tag = self.canvas.create_rounded_rectangle(delete_bbox, 5, fill="#1F6AA5", width=3, tags=self.tags)
            self.canvas.create_text(delete_pos, text="🗑", font=("Comic Sans MS", 20), tags=self.tags + (tag,))
            self.canvas.add_button_binding(tag, lambda: self.canvas.delete_pedal(self))
            return width

        # functionality only for this class - draw selection buttons
        pos = self.rel_pos(relx=.5, rely=.07)
        self.canvas.create_text(pos, text="Add Pedal", font=("Comic Sans MS", 20), tags=self.tags)

        # calculates button positions
        buttons = ["Gain", "Chorus", "Distortion"]
        x1 = self.rel_pos(.1)
        x2 = self.rel_pos(.9)
        for y, name in enumerate(buttons):
            y = self.rel_pos(rely=(y + 1) / (len(buttons) + 1))
            bbox = x1, y, x2, y + 50
            text_pos = bbox[0] + (bbox[2] - bbox[0]) / 2, bbox[1] + (bbox[3] - bbox[1]) / 2

            # draws buttons and text
            button = self.canvas.create_rounded_rectangle(bbox, 10, fill="light blue", tags=self.tags)
            self.canvas.create_text(text_pos, text=name, font=("Comic Sans MS", 20, "italic"), tags=self.tags + (button,))
            self.canvas.add_button_binding(button, lambda n=name: self.canvas.add_pedal(n))

        return width

    def destroy(self):
        """
        unbinds all bindings and deletes the canvas objects for the pedal

        :return: the width of the pedal
        """

        for elem in self.canvas.find_withtag(self.id):
            for tag in self.canvas.gettags(elem):
                for event in ["<Button-1>", "<ButtonRelease-1>", "<B1-Motion>"]:
                    self.canvas.tag_unbind(tag, event)
        self.canvas.delete(self.id)
        return self._bbox[2] - self._bbox[0]
