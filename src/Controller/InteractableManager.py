from flask import Flask, request
from threading import Thread
from math import hypot


class InteractionManager:
    """
    a class to keep track of where all interactable elements are on screen and how to switch focus between them
    """

    _singleton = None
    _server = Flask("4RunnerEffects")
    CANVAS = None

    @staticmethod
    @_server.route("/", methods=["POST"])
    def _process_input():
        """
        processes a given input to the program
        """

        data = request.get_json()
        if data["input"] == "select":
            InteractionManager.CANVAS.after(0, InteractionManager._singleton._focus.select)
        else:
            InteractionManager.CANVAS.after(0, lambda: InteractionManager._singleton.change_focus(data["input"]))

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

        # gets the next element to focus
        if self._focus is not None and (elem := getattr(self._focus, direction)):
            self._focus.unfocus()
            elem = self._dynamic_focus(elem) if type(elem) == str else elem

            # skips element if it is hidden
            while type(elem.reference) == str and InteractionManager.CANVAS.itemcget(elem.reference, "state") == "hidden":
                elem = getattr(elem, direction)
            self._focus = elem
            self._focus.focus()

    def _dynamic_focus(self, group):
        """
        dynamically calculates the next focused element in a group given a direction

        :param group: the group of elements that is attempted to be focused

        :return: the next interactable element to focus
        """

        # gets position of currently focused element
        x1, y1, x2, y2 = InteractionManager.CANVAS.bbox(self._focus.reference)
        focus_x, focus_y = (x1 + x2) // 2, (y1 + y2) // 2

        # gets every node within the quad tree of interactable elements
        nodes = {}
        stack = [self._groups[group]]
        while stack:
            node = stack.pop()
            if node is None or node in nodes or type(node) == str: continue

            # calculates the distance to the currently focused element
            x1, y1, x2, y2 = InteractionManager.CANVAS.bbox(node.reference)
            x, y = (x1 + x2) // 2, (y1 + y2) // 2
            nodes[node] = hypot(x - focus_x, y - focus_y)
            stack.extend([node.up, node.down, node.left, node.right])

        return min(nodes, key=nodes.get)
