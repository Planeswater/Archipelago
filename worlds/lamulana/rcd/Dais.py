from .ObjectWithPosition import *


class Dais(ObjectWithPosition):

    def __init__(self, x, y, dust=0, fall_time=60, rise_behavior=-1, image=2, unknown1=0, image_x=860, image_y=60, width=1, unknown2=10, rise_speed=60):
        super().__init__(x, y)
        self.rcd_object.id = RCD_OBJECTS["trigger_dais"]
        self.rcd_object.parameters = [dust, fall_time, rise_behavior, image, unknown1, image_x, image_y, width, unknown2, rise_speed]
