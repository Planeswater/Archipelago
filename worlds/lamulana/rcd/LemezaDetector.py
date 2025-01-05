from .ObjectWithPosition import *


class LemezaDetector(ObjectWithPosition):

    def __init__(self, x, y, width, height, delay_seconds=0, delay_frames=0, continuous=0, interation=0):
        super().__init__(x, y)
        self.rcd_object.id = RCD_OBJECTS["lemeza_detector"]
        self.rcd_object.parameters = [delay_seconds, delay_frames, continuous, interation, width, height]
