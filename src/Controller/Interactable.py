from customtkinter import CTkButton, CTkEntry
from Controller.InteractableManager import InteractionManager as _InteractionManager


class Interactable:
    """
    a class to represent an interactable element on the screen
    keeps track of neighboring elements as well as functionality for it
    """

    def __init__(self, reference, up=None, down=None, left=None, right=None, focus_after=None):
        """
        creates the interactable element

        :param reference: a reference to the interactable element, either a canvas tag or tkinter object reference
        :param up: a reference to an instance of the interactable object above this one
        :param down: a reference to an instance of the interactable object below this one
        :param left: a reference to an instance of the interactable object to the left of this one
        :param right: a reference to an instance of the interactable object to the right of this one
        :param focus_after: the group to focus after the element is selected

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

        # sets neighboring element metadata
        if type(up) == Interactable: up.down = self
        if type(down) == Interactable: down.up = self
        if type(left) == Interactable: left.right = self
        if type(right) == Interactable: right.left = self

    def focus(self):
        """
        focuses this interactable element
        """

        if type(self.reference) != str:
            self.reference.configure(border_color="red")

    def unfocus(self):
        """
        removes the focus from this element
        """

        if type(self.reference) != str:
            try:
                self.reference.configure(border_color="black")
            except:
                pass

    def select(self):
        """
        selects the interactable element
        """

        if type(self.reference) == CTkButton:
            self.reference.invoke()
        elif type(self.reference) == CTkEntry:
            self.reference.focus()
        if self.focus_after:
            _InteractionManager._singleton.set_active_group(self.focus_after)
