from flask import Flask, request
from threading import Thread
from customtkinter import CTk


class InteractionManager:
    """
    a class to keep track of where all interactable elements are on screen and how to switch focus between them
    """

    _singleton = None
    _server = Flask("4RunnerEffects")
    root = CTk()

    @staticmethod
    @_server.route("/", methods=["POST"])
    def _process_input():
        """
        processes a given input to the program
        """

        data = request.get_json()
        if data["input"] == "select":
            InteractionManager.root.after(0, InteractionManager._singleton._focus.select)
        else:
            InteractionManager.root.after(0, lambda: InteractionManager._singleton.change_focus(data["input"]))

        return "OK"

    def __init__(self):
        """
        creates the interaction manager
        """

        # ensures 1 manager
        if InteractionManager._singleton:
            raise RuntimeError("Only 1 interaction manager allowed")

        # starts server and sets fields
        InteractionManager._singleton = self
        self._groups = {}
        self._focus = None
        Thread(target=InteractionManager._server.run, daemon=True).start()

    def add_group(self, name, default):
        """
        adds a group of interactable elements

        :param name: the name of the group
        :param default: the interactable object that should be focused by default when group is active
        """

        self._groups[name] = default

    def set_active_group(self, group):
        """
        changes the currently active group

        :param group: the group to activate
        """

        if self._focus:
            self._focus.unfocus()
        self._focus = self._groups[group]
        self._focus.focus()

    def change_focus(self, direction):
        """
        changes the currently focused element

        :param direction: the direction to shift focus to
        """

        if self._focus is not None and (elem := getattr(self._focus, direction)):
            self._focus.unfocus()
            self._focus = elem
            self._focus.focus()
