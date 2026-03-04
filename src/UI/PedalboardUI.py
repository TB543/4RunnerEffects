from tkinter import EventType, Event
from uuid import uuid4
from customtkinter import CTkCanvas
from pedalboard.io import AudioStream
from pedalboard import Pedalboard
from UI.Settings import Settings
from UI.Pedals import *


class PedalboardUI(CTkCanvas):
    """
    a class to represent a graphical Pedal Board
    """

    CONTENT_HEIGHT_RELATIVE = (.15, .9) # height ranges from 15% of screen to 90%
    CONTENT_PADDING = 10
    SCROLLBAR_PADDING = 50

    def __init__(self, parent):
        """
        creates the Pedal Board UI
        """

        # initializes fields
        super(PedalboardUI, self).__init__(parent, background="#252525")
        self.bind("<Configure>", self._resize)
        self._width = 1
        self._height = 1

        # scrollbar settings
        self._scroll_x = 0
        self._content_width = 0
        self._scroll_event = 0
        self._scrollbar_tag = "scrollbar"
        self._content_tag = "content"
        self.tag_bind(self._scrollbar_tag, "<Button-1>", self._scroll)
        self.tag_bind(self._scrollbar_tag, "<B1-Motion>", self._scroll)
        self.add_button_binding(self._scrollbar_tag)

        # creates title
        self._title_tag = "title"
        self.create_text(5, 5, text="4Runner FX", font=("Comic Sans MS", 25, "bold"), tags=self._title_tag)
        self.create_text(0, 0, text="4Runner FX", font=("Comic Sans MS", 25, "bold"), fill="white", tags=self._title_tag)

        # creates the add pedals menu
        self._audio = None
        self._pedals = []
        self._pedals_height = (0, 0)
        self._add_pedals_menu = BasePedal(self, self._content_tag)
        self._add_pedals_width = 0

        # creates settings button
        settings = Settings(self, self._audio, fg_color="#2b2b2b", bg_color="#252525", border_color="black", border_width=2, corner_radius=10)
        self._settings_tag = "settings"
        self.create_rounded_rectangle((-25, -25, 25, 25), 5, fill="#1F6AA5", width=3, tags=self._settings_tag)
        self.create_text(1, -1, text="⚙", font=("Comic Sans MS", 25, "bold"), tags=self._settings_tag)
        self.add_button_binding(self._settings_tag, lambda: settings.place(relx=.5, rely=.5, relwidth=.8, relheight=.9, anchor="center"))

    def modify_audio_stream(self, input_device, output_device):
        """
        changes the input and output device of the audio stream

        :param input_device: the input device
        :param output_device: the output device

        :return: the new audio stream if the audio stream was changed, false on failure
        """

        # closes old stream
        if self._audio:
            self._audio.close()

        # attempts to create new stream
        try:
            plugins = Pedalboard([pedal.effect for pedal in self._pedals])
            self._audio = AudioStream(input_device_name=input_device, output_device_name=output_device, plugins=plugins)
            self._audio.__enter__()
            return True

        # returns false on failure
        except ValueError:
            self._audio = None
            return False

    def add_pedal(self, name):
        """
        adds a pedal to the board

        :param name: name of the effects pedal to add
        """

        # create pedal
        pedal = None
        match name:
            case "Gain":
                pedal = GainPedal(self, self._content_tag)
            case "Chorus":
                pedal = ChorusPedal(self, self._content_tag)
            case "Distortion":
                pedal = DistortionPedal(self, self._content_tag)

        # draw pedal and add effect to audio stream
        x = self._content_width - self.CONTENT_PADDING - self._scroll_x - self._add_pedals_width
        width = pedal.draw(x, *self._pedals_height)
        self._pedals.append(pedal)
        if self._audio:
            self._audio.plugins.append(pedal.effect)

        # adjust remaining content
        self.move(self._add_pedals_menu.id, width, 0)
        self._content_width += width
        self._draw_scrollbar()
        self._set_scroll(1)

    def delete_pedal(self, pedal):
        """
        removes a pedal from the board

        :param pedal: the pedal to delete
        """

        # removes pedal
        index = self._pedals.index(pedal)
        self._pedals.remove(pedal)
        if self._audio:
            self._audio.plugins.remove(pedal.effect)

        # shifts remaining pedals over
        dx = -pedal.destroy()
        self._content_width += dx
        self._draw_scrollbar()
        self.move(self._add_pedals_menu.id, dx, 0)
        for pedal in self._pedals[index:]:
            self.move(pedal.id, dx, 0)

    def add_button_binding(self, tag_or_id, callback=None):
        """
        adds button bindings to a canvas object
            adds button animation bindings
            adds button callback if given

        :param tag_or_id: tag or id of the canvas object
        :param callback: callback function
        """

        self.tag_bind(tag_or_id, "<Button-1>", lambda e: self.move(tag_or_id, 2, 2), add="+")
        self.tag_bind(tag_or_id, "<ButtonRelease-1>", lambda e: self.move(tag_or_id, -2, -2), add="+")
        if callback:
            self.tag_bind(tag_or_id, "<ButtonRelease-1>", lambda e: callback(), add="+")

    def create_rounded_rectangle(self, bbox, radius, **kwargs):
        """
        creates a rounded rectangle on the canvas

        :param bbox: bounding box in the format (x1, y1, x2, y2):
            x1: x coordinate of the top left of the rectangle
            y1: y coordinate of the top left of the rectangle
            x2: x coordinate of the bottom right of the rectangle
            y2: y coordinate of the bottom right of the rectangle
        :param radius: radius of the corners of the rectangle
        :param kwargs: additional keyword arguments

        :return: the id of the rectangle
        """

        # configures kwargs
        x1, y1, x2, y2 = bbox
        outline = kwargs.pop("outline", None)
        width = kwargs.pop("width", 2)
        kwargs["outline"] = kwargs.get("fill")
        if padx := kwargs.pop("padx", None):
            x1 += padx
            x2 -= padx

        # sets id of rectangle
        uuid = str(uuid4())
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

    def destroy(self):
        """
        closes the audio stream on destroy
        """

        super().destroy()
        if self._audio:
            self._audio.close()

    def _set_scroll(self, relx):
        """
        sets the scroll position

        :param relx: scroll amount where 0 is all the way left and 1 is all the way right
        """

        # does nothing if scrollbar doesnt exist
        bbox = self.bbox(self._scrollbar_tag)
        if bbox is None:
            return

        # calculates positioning parameters
        self._scroll_event = bbox[0]
        scrollbar_width = bbox[2] - bbox[0]
        min_x = PedalboardUI.SCROLLBAR_PADDING / 2
        max_x = self._width - (PedalboardUI.SCROLLBAR_PADDING / 2) - scrollbar_width

        # creates simulated scroll event and triggers it
        event = Event()
        event.type = EventType.Motion
        event.x = min_x + (max_x - min_x) * relx
        self._scroll(event)

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
            min_x = PedalboardUI.SCROLLBAR_PADDING / 2
            max_x = self._width - (PedalboardUI.SCROLLBAR_PADDING / 2) - scrollbar_width
            scrollbar_dx = max(min_x - bbox[0], min(scrollbar_dx, max_x + scrollbar_width - bbox[2]))

            # calculate content scroll amount
            scroll_percent = (bbox[0] + scrollbar_dx - min_x) / (max_x - min_x)
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

        # redraw scrollbar
        self.delete(self._scrollbar_tag)
        if self._content_width > self._width:
            scroll_percent = self._scroll_x / (self._content_width - self._width)
            scrollbar_width = ((self._width / self._content_width) * self._width) - PedalboardUI.SCROLLBAR_PADDING
            scrollbar_width = max(scrollbar_width, 75)
            scrollbar_x = scroll_percent * (self._width - scrollbar_width - PedalboardUI.SCROLLBAR_PADDING) + (PedalboardUI.SCROLLBAR_PADDING / 2)
            pos = scrollbar_x, self._height - 45, scrollbar_x + scrollbar_width, self._height - 25
            self.create_rounded_rectangle(pos, 7, fill="gray", tags=self._scrollbar_tag)

            # ensure content is in correct position
            self._scroll_event = 0
            event = Event()
            event.type = EventType.Motion
            event.x = 0
            self._scroll(event)

        # ensures all content is visible when scrollbar is hidden
        else:
            self.move(self._content_tag, self._scroll_x, 0)
            self._scroll_x = 0

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
        self._scroll_x = 0
        self._content_width = 0

        # redraws pedals
        self._pedals_height = (self._height * PedalboardUI.CONTENT_HEIGHT_RELATIVE[0], self._height * PedalboardUI.CONTENT_HEIGHT_RELATIVE[1])
        x = PedalboardUI.CONTENT_PADDING
        for pedal in self._pedals:
            x += pedal.draw(x, *self._pedals_height)

        # adjust drawn object positions
        self._add_pedals_width = self._add_pedals_menu.draw(x, *self._pedals_height)
        self._content_width = x + self._add_pedals_width + PedalboardUI.CONTENT_PADDING
        self.move(self._title_tag, dx * .5, dy * .07)
        self.move(self._settings_tag, dx * .95, dy * .08)
        self._draw_scrollbar()
