from customtkinter import CTkCanvas
from tkinter import EventType
from uuid import uuid4


class PedalBoard(CTkCanvas):
    """
    a class to represent a graphical Pedal Board
    """

    def __init__(self, parent):
        """
        creates the Pedal Board UI
        """

        # initializes fields
        super(PedalBoard, self).__init__(parent, background="#252525")
        self.bind("<Configure>", self._resize)
        self._width = 1
        self._height = 1

        # scrollbar settings
        self._scroll_x = 0
        self._content_width = 0
        self._scrollbar_padding = 50
        self._scroll_event = 0
        self._scrollbar_tag = "scrollbar"
        self._content_tag = "content"

        # creates title
        self._title_tag = "title"
        self.create_text(5, 5, text="4Runner FX", font=("Comic Sans MS", 25, "bold"), tags=self._title_tag)
        self.create_text(0, 0, text="4Runner FX", font=("Comic Sans MS", 25, "bold"), fill="white", tags=self._title_tag)

        # creates settings button
        self._settings_tag = "settings"
        self.create_rounded_rectangle(-25, -25, 25, 25, 5, fill="#1F6AA5", width=3, tags=self._settings_tag)
        self.create_text(1, -1, text="⚙", font=("Comic Sans MS", 25, "bold"), tags=self._settings_tag)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        """
        creates a rounded rectangle on the canvas

        :param x1: x coordinate of the top left of the rectangle
        :param y1: y coordinate of the top left of the rectangle
        :param x2: x coordinate of the bottom right of the rectangle
        :param y2: y coordinate of the bottom right of the rectangle
        :param radius: radius of the corners of the rectangle
        :param kwargs: additional keyword arguments

        :return: the id of the rectangle
        """

        # configures kwargs
        outline = kwargs.pop("outline", None)
        width = kwargs.pop("width", 2)
        kwargs["outline"] = kwargs.get("fill")

        # sets id of rectangle
        uuid = uuid4()
        if isinstance(kwargs.get("tags"), tuple):
            kwargs["tags"] = kwargs["tags"] + (uuid,)
        elif isinstance(kwargs.get("tags"), str):
            kwargs["tags"] = (kwargs["tags"], uuid)
        else:
            kwargs["tags"] = uuid

        # draws the rounded corners
        self.create_oval(x1, y1, x1 + radius * 2, y1 + radius * 2, **kwargs)
        self.create_oval(x2 - radius * 2, y1, x2, y1 + radius * 2, **kwargs)
        self.create_oval(x1, y2 - radius * 2, x1 + radius * 2, y2, **kwargs)
        self.create_oval(x2 - radius * 2, y2 - radius * 2, x2, y2, **kwargs)

        # draws the remainder of the rounded rectangle
        self.create_rectangle(x1 + radius, y1, x2 - radius, y2, **kwargs)
        self.create_rectangle(x1, y1 + radius, x1 + radius * 2, y2 - radius, **kwargs)
        self.create_rectangle(x2 - radius * 2, y1 + radius, x2, y2 - radius, **kwargs)

        # draws rounded borders
        if width > 0:
            kwargs = {"width": width, "fill": outline, "tags": kwargs.pop("tags")}
            self.create_arc(x1, y1, x1 + radius * 2, y1 + radius * 2, start=90, style="arc", outline=outline, **kwargs)
            self.create_arc(x2 - radius * 2, y1, x2, y1 + radius * 2, start=0, style="arc", outline=outline, **kwargs)
            self.create_arc(x1, y2 - radius * 2, x1 + radius * 2, y2, start=180, style="arc", outline=outline, **kwargs)
            self.create_arc(x2 - radius * 2, y2 - radius * 2, x2, y2, start=270, style="arc", outline=outline, **kwargs)

            # draws straight borders
            self.create_line(x1 + radius, y1, x2 - radius, y1, **kwargs)
            self.create_line(x1 + radius, y2, x2 - radius, y2, **kwargs)
            self.create_line(x1, y1 + radius, x1, y2 - radius, **kwargs)
            self.create_line(x2, y1 + radius, x2, y2 - radius, **kwargs)
        return uuid

    def _scroll(self, event):
        """
        processes scroll events on the scrollbar

        :param event: the scroll event
        """

        # press event
        if event.type == EventType.ButtonPress:
            self._scroll_event = event.x

        # motion event
        else:
            scrollbar_dx = event.x - self._scroll_event
            bbox = self.bbox(self._scrollbar_tag)
            scrollbar_width = bbox[2] - bbox[0]
            min_x = self._scrollbar_padding / 2
            max_x = self._width - (self._scrollbar_padding / 2) - scrollbar_width

            # clamp so scrollbar cant go too far left/right
            if bbox[0] + scrollbar_dx < min_x:
                scrollbar_dx = min_x - bbox[0]
            elif bbox[2] + scrollbar_dx > max_x + scrollbar_width:
                scrollbar_dx = max_x + scrollbar_width - bbox[2]

            # calculate scroll amount
            scroll_percent = (bbox[0] - min_x) / (max_x - min_x)
            content_x = scroll_percent * (self._content_width - self._width)
            content_dx = self._scroll_x - content_x

            # moves canvas objects
            self.move(self._scrollbar_tag, scrollbar_dx, 0)
            self.move(self._content_tag, content_dx, 0)
            self._scroll_event = event.x
            self._scroll_x = content_x

    def _draw_scrollbar(self):
        """
        draws a horizontal scrollbar on the canvas
        """

        # calculate scrollbar bbox
        self.delete(self._scrollbar_tag)
        if self._content_width > self._width:
            scroll_percent = self._scroll_x / (self._content_width - self._width)
            scrollbar_width = ((self._width / self._content_width) * self._width) - self._scrollbar_padding
            scrollbar_x = scroll_percent * (self._width - scrollbar_width - self._scrollbar_padding) + (self._scrollbar_padding / 2)

            # create scrollbar and bind function
            pos = scrollbar_x, self._height - 45, scrollbar_x + scrollbar_width, self._height - 25
            self.create_rounded_rectangle(*pos, 7, fill="gray", tags=self._scrollbar_tag)
            self.tag_bind(self._scrollbar_tag, "<Button-1>", self._scroll)
            self.tag_bind(self._scrollbar_tag, "<B1-Motion>", self._scroll)

    def _resize(self, event):
        """
        handles when the canvas is resized

        :param event: the resize event
        """

        # update canvas fields
        dx = event.width - self._width
        dy = event.height - self._height
        self._width = event.width
        self._height = event.height

        # adjust drawn object positions
        self.move(self._title_tag, dx * .5, dy * .07)
        self.move(self._settings_tag, dx * .95, dy * .08)
        self._draw_scrollbar()
