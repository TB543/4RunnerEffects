from customtkinter import CTkButton, CTkEntry
from Controller.InteractableManager import InteractionManager as _InteractionManager


class Interactable:
    """
    a class to represent an interactable element on the screen
    keeps track of neighboring elements as well as functionality for it
    """

    # will be set by canvas instance for calling canvas functions
    CANVAS = None

    def __init__(self, reference, up=None, down=None, left=None, right=None, focus_after=None, select_hold_focus=False):
        """
        creates the interactable element

        :param reference: a reference to the interactable element, either a canvas tag or tkinter object reference
        :param up: a reference to an instance of the interactable object above this one
        :param down: a reference to an instance of the interactable object below this one
        :param left: a reference to an instance of the interactable object to the left of this one
        :param right: a reference to an instance of the interactable object to the right of this one
        :param focus_after: the group to focus after the element is selected
        :param select_hold_focus: determines if selecting the element should hold the focus

        ** note: if the interactable element in a given direction should be dynamically calculated pass
            the group name containing the elements to dynamically calculate as the parameter **
        """

        # metadata for neighboring elements (should be set externally)
        self.reference = reference
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.focus_after = focus_after
        self.select_hold_focus = select_hold_focus
        self.focused_pos = {}

        # sets neighboring element metadata
        if type(up) == Interactable: up.down = self
        if type(down) == Interactable: down.up = self
        if type(left) == Interactable: left.right = self
        if type(right) == Interactable: right.left = self

    def focus(self):
        """
        focuses this interactable element
        """

        # changes border to red for tkinter widgets
        if type(self.reference) != str:
            self.reference.configure(border_color="red")

        # changes border to red for custom drawn canvas elements
        else:
            for tag in Interactable.CANVAS.find_withtag(self.reference):
                if Interactable.CANVAS.type(tag) == "arc":
                    Interactable.CANVAS.itemconfigure(tag, outline="red")
                if Interactable.CANVAS.type(tag) == "line":
                    Interactable.CANVAS.itemconfigure(tag, fill="red")

    def unfocus(self):
        """
        removes the focus from this element
        """

        if type(self.reference) != str:
            try:
                self.reference.configure(border_color="black")
            except:
                pass

        # changes border to black for custom drawn canvas elements
        else:
            for tag in Interactable.CANVAS.find_withtag(self.reference):
                if Interactable.CANVAS.type(tag) == "arc":
                    Interactable.CANVAS.itemconfigure(tag, outline="black")
                if Interactable.CANVAS.type(tag) == "line":
                    Interactable.CANVAS.itemconfigure(tag, fill="white" if self.select_hold_focus else "black")

    def select(self):
        """
        selects the interactable element
        """

        # select functionality for tkinter widgets
        if type(self.reference) == CTkButton:
            self.reference.invoke()
        elif type(self.reference) == CTkEntry:
            self.reference.focus()

        # select functionality for custom drawn canvas elements
        else:
            x1, y1, x2, y2 = Interactable.CANVAS.bbox(self.reference)
            x = (x1 + x2) // 2
            y = (y1 + y2) // 2
            Interactable.CANVAS.event_generate("<ButtonRelease-1>" if self.focused_pos else "<Button-1>", x=x, y=y)
            if self.select_hold_focus:
                self.focused_pos = {} if self.focused_pos else {"x": x1, "y": y1}
                if self.focused_pos: Interactable.CANVAS.create_aa_circle(*self.focused_pos.values(), 5, fill="red", tags="pointer")
                if not self.focused_pos: Interactable.CANVAS.delete("pointer")
            else:
                Interactable.CANVAS.after(200, lambda: Interactable.CANVAS.event_generate("<ButtonRelease-1>", x=x, y=y))

        # changes focus if a new menu is opened
        if self.focus_after:
            _InteractionManager._singleton.set_active_group(self.focus_after)
