from .ObjectWithoutPosition import *


class FlagTimer(ObjectWithoutPosition):

    def __init__(self, delay_seconds=0, delay_frames=0):
        super().__init__()
        self.rcd_object.id = RCD_OBJECTS["flag_timer"]
        self.rcd_object.parameters = [delay_seconds, delay_frames]
