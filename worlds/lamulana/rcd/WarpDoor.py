from .ObjectWithPosition import *


class WarpDoor(ObjectWithPosition):

    def __init__(self, x, y, interaction, destination_zone, destination_room, destination_screen, destination_x, destination_y):
        super().__init__(x, y)
        self.rcd_object.id = RCD_OBJECTS["warp_door"]
        self.rcd_object.parameters = [interaction, destination_zone, destination_room, destination_screen, destination_x, destination_y]
