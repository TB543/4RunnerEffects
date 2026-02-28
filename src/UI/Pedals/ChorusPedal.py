from UI.Pedals.BasePedal import BasePedal


class ChorusPedal(BasePedal):
    """
    a class to represent a Chorus Pedal
    """

    def __init__(self, canvas, tags):
        """
        initializes the pedal and its fields

        :param canvas: the pedalboard canvas to draw onto
        :param tags: tags to use when drawing the canvas objects so parent class can control behavior
        """

        super().__init__(canvas, tags, 2 / 3)

    def draw(self, x, y1, y2):
        """
        draws the pedal to the canvas with the given bbox

        :param x: x coordinate of the top left of the rectangle
        :param y1: y coordinate of the top left of the rectangle
        :param y2: y coordinate of the bottom of the rectangle

        :return: the width of the pedal
        """

        return super().draw(x, y1, y2, fill="blue")
