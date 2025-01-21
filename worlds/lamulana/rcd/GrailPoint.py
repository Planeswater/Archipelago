from .ObjectWithPosition import *


class GrailPoint(ObjectWithPosition):

    def __init__(self, x, y, card, unknown1=0, unknown2=0, unknown3=1, unknown4=1, unknown5=1, unknown6=1, unknown7=506, unknown8=280):
        super().__init__(x, y)
        self.rcd_object.id = RCD_OBJECTS["grail_point"]
        self.rcd_object.parameters = [card, unknown1, unknown2, unknown3, unknown4, unknown5, unknown6, unknown7, unknown8]
