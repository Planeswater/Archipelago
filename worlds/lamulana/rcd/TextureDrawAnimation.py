from .ObjectWithPosition import *


class TextureDrawAnimation(ObjectWithPosition):

    def __init__(self, x, y, layer=0, image_file=0, image_x=0, image_y=0, dx=0, dy=0, animation=0, animation_frames=0, pause_frames=0, repeat=0, hit_tile=0, entry_effect=0, exit_effect=0, cycle_colors=0, alpha=0, max_alpha=0, red=0, max_red=0, green=0, max_green=0, blue=0, max_blue=0, blend=0, unknown=0):
        super().__init__(x, y)
        self.rcd_object.id = RCD_OBJECTS["texture_draw_animation"]
        self.rcd_object.parameters = [layer, image_file, image_x, image_y, dx, dy, animation, animation_frames, pause_frames, repeat, hit_tile, entry_effect, exit_effect, cycle_colors, alpha, max_alpha, red, max_red, green, max_green, blue, max_blue, blend, unknown]
