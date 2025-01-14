from .ObjectWithPosition import *


class Ladder(ObjectWithPosition):

    def __init__(self, x, y, extend_direction, height, graphic, image_x, image_y, ladder_type, collision):
        super().__init__(x, y)
        self.rcd_object.id = RCD_OBJECTS["ladder"]
        self.rcd_object.parameters = [extend_direction, height, graphic, 0, image_x, image_y, ladder_type, collision]
