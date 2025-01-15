from .FileMod import FileMod
from .Items import item_table
from .Rcd import Rcd
from .LmFlags import GLOBAL_FLAGS, RCD_OBJECTS, TEST_OPERATIONS, WRITE_OPERATIONS, grail_flag_by_zone
from .rcd.FlagTimer import FlagTimer
from .rcd.InstantItem import InstantItem
from .rcd.Operation import Operation
from .rcd.TextureDrawAnimation import TextureDrawAnimation
from .rcd.LemezaDetector import LemezaDetector
from .rcd.GrailPoint import GrailPoint
from .rcd.Ladder import Ladder
from .rcd.WarpDoor import WarpDoor
from .rcd.Dais import Dais


class RcdMod(FileMod):

    DEFAULT_PARAMS = {
        "param_index": 0,
        "iterations": 1,
        "item_mod": 0
    }

    RCD_OBJECT_PARAMS = dict([
            (RCD_OBJECTS["chest"], {
                    "param_len": 7,
                    "item_mod": 11
                },
            ),
            (RCD_OBJECTS["naked_item"], {
                    "param_len": 4,
                    "param_index": 1
                },
            ),
            (RCD_OBJECTS["instant_item"], {
                    "param_len": 5
                },
            ),
            (RCD_OBJECTS["scan"], {
                    "param_len": 5,
                    "param_index": 3,
                    "iterations": 2
                },
            )
        ]
    )

    def __init__(self, filename, local_config, options, start_inventory, cursed_chests):
        super().__init__(Rcd, filename, local_config, options, GLOBAL_FLAGS["rcd_filler_items"])
        self.start_inventory = start_inventory
        self.cursed_chests = cursed_chests

    def place_item_in_location(self, item, item_id, location) -> None:
        object_type_params = self.RCD_OBJECT_PARAMS.get(location.object_type)
        if object_type_params is None:
            return

        params = self.DEFAULT_PARAMS | object_type_params
        params["object_type"] = location.object_type
        params["item_id"] = item_id
        params["location"] = location
        params["item"] = item
        super().set_params(params)

        location_ids = [location.item_id]

        for zone in location.zones:
            screen = self.file_contents.zones[zone].rooms[location.room].screens[location.screen]
            params["objects"] = screen.objects_with_position

            if params["object_type"] == RCD_OBJECTS["chest"]:
                # Endless Corridor Twin Statue Chest Exists Twice
                if location.zones[0] == 8 and location.room == 3 and location.screen == 0 and location.item_id == item_table["Twin Statue"].game_code:
                    params["iterations"] = 2
            elif params["object_type"] == RCD_OBJECTS["naked_item"]:
                # Endless Corridor Keysword Exists Twice, Once as Regular and Once as Empowered
                if location.zones[0] == 8 and location.room == 2 and location.screen == 1 and location.item_id == item_table["Key Sword"].game_code:
                    location_ids.append(7)
            elif params["object_type"] == RCD_OBJECTS["scan"]:
                params["objects"] = screen.objects_without_position

            for location_id in location_ids:
                params["location_id"] = location_id
                self.__place_item(**params)

    def apply_mods(self, dat_mod):
        self.__give_starting_items(self.start_inventory)

        # Xelpud/Diary Interactions
        self.__rewrite_diary_chest()
        self.__add_diary_chest_timer()
        self.__remove_xelpud_door()

        self.__rewrite_mulbruk_doors()

        self.__rewrite_slushfund_conversation_conditions()
        self.__rewrite_four_guardian_shop_conditions(dat_mod)
        self.__rewrite_cog_chest()
        self.__rewrite_fishman_alt_shop()

        self.__add_dimensional_orb_ladder()
        self.__add_true_shrine_doors()
        self.__add_moonlight_to_twin_lockout_fix()
        self.__add_chain_whip_lockout_fix()
        self.__add_flail_whip_lockout_fix()
        self.__add_angel_shield_lockout_fix()
        self.__add_hardmode_toggle()
        self.__add_sacred_orb_timers()

        self.__clean_up_operations()

        if self.options.AutoScanGrailTablets:
            self.__create_grail_autoscans()

        if self.options.BossCheckpoints:
            self.__create_boss_checkpoints()

        if self.options.AncientLaMulaneseLearned:
            self.__create_ancient_lamulanese_timer()

        if self.options.AlternateMotherAnkh:
            self.__create_alternate_mother_ankh()

    # RCD Mod Methods

    def __place_item(self, objects, object_type, param_index, param_len, location, location_id, item_id, original_obtain_flag, new_obtain_flag, obtain_value, item_mod, iterations, item):
        for _ in range(iterations):
            item_location = next((o for _, o in enumerate(objects) if o.id == object_type and o.parameters[param_index] == location_id+item_mod and len(o.parameters) < param_len), None)

            if object_type == RCD_OBJECTS["chest"]:
                if location.name in self.cursed_chests:
                    item_location.parameters[3] = 1
                    item_location.parameters[4] = 1
                    item_location.parameters[5] = 50
                else:
                    item_location.parameters[3] = 0

            for test_op in item_location.test_operations:
                if test_op.flag == original_obtain_flag:
                    test_op.flag = new_obtain_flag
            for write_op in item_location.write_operations:
                if write_op.flag == original_obtain_flag:
                    write_op.flag = new_obtain_flag
                    if object_type in (RCD_OBJECTS["naked_item"], RCD_OBJECTS["instant_item"], RCD_OBJECTS["scan"]):
                        write_op.op_value = obtain_value

            # Destructible Cover customization
            for operation in ["test", "write"]:
                self.__update_operation(operation, objects, [RCD_OBJECTS["hitbox_generator"], RCD_OBJECTS["room_spawner"]], original_obtain_flag, new_obtain_flag)

            # Surface Map customization
            if original_obtain_flag == GLOBAL_FLAGS["surface_map"]:
                self.__fix_surface_map_scan(objects, item_location, original_obtain_flag)
            
            # Shrine of the Mother Map Crusher customization
            if original_obtain_flag == GLOBAL_FLAGS["shrine_map"]:
                self.__update_operation("write", objects, [RCD_OBJECTS["crusher"]], original_obtain_flag, new_obtain_flag, new_op_value=obtain_value)

            # Mausoleum Ankh Jewel Trap customization
            if original_obtain_flag == GLOBAL_FLAGS["ankh_jewel_mausoleum"]:
                self.__update_operation("write", objects, [RCD_OBJECTS["moving_texture"]], original_obtain_flag, new_obtain_flag, new_op_value=obtain_value)

            # Yagostr Dais customization
            if original_obtain_flag == GLOBAL_FLAGS["yagostr_found"]:
                self.__update_operation("test", objects, [RCD_OBJECTS["trigger_dais"]], original_obtain_flag, new_obtain_flag)

            # Vimana customization
            if original_obtain_flag == GLOBAL_FLAGS["plane_found"]:
                vimana_objects = self.file_contents.zones[13].rooms[6].screens[1].objects_with_position
                self.__update_operation("test", vimana_objects, [RCD_OBJECTS["vimana"]], original_obtain_flag, new_obtain_flag)

            # Mekuri Master customization
            if original_obtain_flag == GLOBAL_FLAGS["mekuri"]:
                self.__update_operation("test", objects, [RCD_OBJECTS["language_conversation"], RCD_OBJECTS["texture_draw_animation"]], original_obtain_flag, new_obtain_flag)

            item_location.parameters[param_index] = item_id+item_mod
            item_location.parameters.append(1)
            item_location.parameters_length += 1
            self.file_size += 2

    def __fix_surface_map_scan(self, objects, location, obtain_flag):
        scan = next(o for _, o in enumerate(objects) if o.id == RCD_OBJECTS["scannable"] and len([t for t in o.test_operations if t.flag == obtain_flag]) > 0)

        surface_scan_flag = GLOBAL_FLAGS["replacement_surface_map_scan"]
        scan.test_operations[0].flag = surface_scan_flag
        scan.write_operations[0].flag = surface_scan_flag
        location.test_operations[0].flag = surface_scan_flag

        self.__add_operation_to_object("write", location, surface_scan_flag, WRITE_OPERATIONS["add"], 1)

    def __give_starting_items(self, items) -> None:
        flag_counter = 0
        starting_room = self.file_contents.zones[1].rooms[2].screens[1]

        for item_name in items:
            item = item_table[item_name]

            item_giver = InstantItem(x=0, y=0, item=item.game_code, width=160, height=120, sound=39)
            test_ops = [Operation.create(GLOBAL_FLAGS["starting_items"], TEST_OPERATIONS["eq"], flag_counter)]
            write_ops = [
                Operation.create(GLOBAL_FLAGS["starting_items"], WRITE_OPERATIONS["add"], 1),
                Operation.create(item.obtain_flag, WRITE_OPERATIONS["add"], item.obtain_value)
            ]
            item_giver.add_ops(test_ops, write_ops)
            item_giver.add_to_screen(self, starting_room)

            flag_counter += 1

    def __remove_xelpud_door(self) -> None:
        screen = self.file_contents.zones[1].rooms[2].screens[1]
        self.__remove_objects_by_operation(screen, "test", screen.objects_with_position, [RCD_OBJECTS["language_conversation"]], GLOBAL_FLAGS["shrine_diary_chest"], TEST_OPERATIONS["eq"], 2)

    def __rewrite_diary_chest(self) -> None:
        objects = self.file_contents.zones[9].rooms[2].screens[1].objects_with_position
        diary_chest = self.__find_objects_by_operation("write", objects, [RCD_OBJECTS["chest"]], GLOBAL_FLAGS["diary_chest_puzzle"])[0]

        self.__update_operation("test", objects, [RCD_OBJECTS["chest"]], GLOBAL_FLAGS["shrine_shawn"], GLOBAL_FLAGS["shrine_dragon_bone"])
        self.__add_operation_to_object("test", diary_chest, GLOBAL_FLAGS["talisman_found"], TEST_OPERATIONS["eq"], 2)

    def __add_diary_chest_timer(self) -> None:
        screen = self.file_contents.zones[9].rooms[2].screens[0]

        flag_timer = FlagTimer()
        test_ops = [
            Operation.create(GLOBAL_FLAGS["talisman_found"], TEST_OPERATIONS["gteq"], 3),
            Operation.create(GLOBAL_FLAGS["shrine_dragon_bone"], TEST_OPERATIONS["gteq"], 1)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["shrine_diary_chest"], WRITE_OPERATIONS["assign"], 2)]
        flag_timer.add_ops(test_ops, write_ops)
        flag_timer.add_to_screen(self, screen)

    def __rewrite_mulbruk_doors(self) -> None:
        screen = self.file_contents.zones[3].rooms[3].screens[0]
        self.__remove_objects_by_parameter(screen, screen.objects_with_position, [RCD_OBJECTS["language_conversation"]], 4, 926)
        self.__remove_objects_by_parameter(screen, screen.objects_with_position, [RCD_OBJECTS["language_conversation"]], 4, 1014)
        self.__remove_objects_by_operation(screen, "test", screen.objects_with_position, [RCD_OBJECTS["language_conversation"]], GLOBAL_FLAGS["score"], TEST_OPERATIONS["lteq"], 55)

        swimsuit_reaction_door = self.__find_objects_by_operation("test", screen.objects_with_position, [RCD_OBJECTS["language_conversation"]], GLOBAL_FLAGS["swimsuit_found"])[0]
        self.__add_operation_to_object("test", swimsuit_reaction_door, GLOBAL_FLAGS["mulbruk_father"], TEST_OPERATIONS["neq"], 9)

    def __rewrite_four_guardian_shop_conditions(self, dat_mod):
        msx2_replacement_flag = dat_mod.find_shop_flag("nebur_guardian", 0)
        objects = self.file_contents.zones[1].rooms[2].screens[0].objects_with_position
        self.__update_operation("test", objects, [RCD_OBJECTS["language_conversation"]], GLOBAL_FLAGS["xelpud_msx2"], GLOBAL_FLAGS["guardians_killed"], old_op_value=0, new_op_value=3, new_operation=TEST_OPERATIONS["lteq"])
        self.__update_operation("test", objects, [RCD_OBJECTS["language_conversation"]], GLOBAL_FLAGS["xelpud_msx2"], GLOBAL_FLAGS["guardians_killed"], old_op_value=1, new_op_value=4)
        self.__update_operation("test", objects, [RCD_OBJECTS["language_conversation"]], GLOBAL_FLAGS["msx2_found"], msx2_replacement_flag)

    def __rewrite_slushfund_conversation_conditions(self):
        objects = self.file_contents.zones[10].rooms[8].screens[0].objects_with_position
        self.__update_operation("test", objects, [RCD_OBJECTS["language_conversation"]], GLOBAL_FLAGS["slushfund_conversation"], GLOBAL_FLAGS["replacement_slushfund_conversation"])

    def __rewrite_cog_chest(self):
        objects = self.file_contents.zones[10].rooms[0].screens[1].objects_with_position
        self.__update_operation("write", objects, [RCD_OBJECTS["chest"]], GLOBAL_FLAGS["cog_puzzle"], GLOBAL_FLAGS["replacement_cog_puzzle"])

        stray_fairy_door = self.__find_objects_by_operation("write", objects, [RCD_OBJECTS["language_conversation"]], GLOBAL_FLAGS["cog_puzzle"], operation=WRITE_OPERATIONS["assign"], op_value=3)[0]
        self.__add_operation_to_object("write", stray_fairy_door, GLOBAL_FLAGS["replacement_cog_puzzle"], WRITE_OPERATIONS["assign"], 3)

    def __rewrite_fishman_alt_shop(self):
        screen = self.file_contents.zones[4].rooms[3].screens[3]
        objects = screen.objects_with_position
        
        # Persist Main Shop after Alt is Opened
        self.__update_operation("test", objects, [RCD_OBJECTS["language_conversation"]], GLOBAL_FLAGS["fishman_shop_puzzle"], GLOBAL_FLAGS["fishman_shop_puzzle"], old_op_value=2, new_operation=TEST_OPERATIONS["gteq"])

        # Relocate Alt Shop
        self.__update_position("test", objects, [RCD_OBJECTS["language_conversation"]], GLOBAL_FLAGS["fishman_shop_puzzle"], 9, 76, op_value=3)

        # Relocate Fairy Keyspot trigger
        self.__update_position("test", objects, [RCD_OBJECTS["fairy_keyspot"]], GLOBAL_FLAGS["fishman_shop_puzzle"], 9, 74)

        # Relocate Alt Shop Explosion
        self.__update_position("test", objects, [RCD_OBJECTS["explosion"]], GLOBAL_FLAGS["screen_flag_0d"], 7, 76)

        # Add Alt Shop Door Graphic
        fishman_alt_door = TextureDrawAnimation(x=9, y=76, layer=-1, image_x=260, image_y=0, dx=40, dy=40, animation_frames=1, max_alpha=255)
        test_ops = [
            Operation.create(GLOBAL_FLAGS["mother_state"], TEST_OPERATIONS["neq"], 3),
            Operation.create(GLOBAL_FLAGS["fishman_shop_puzzle"], TEST_OPERATIONS["eq"], 3)
        ]
        fishman_alt_door.add_ops(test_ops, [])
        fishman_alt_door.add_to_screen(self, screen)

    def __add_chain_whip_lockout_fix(self):
        objects = self.file_contents.zones[5].rooms[3].screens[0].objects_with_position

        # Swap permanent puzzle flags to screen flags so puzzle resets on lockout
        self.__update_operation("test", objects, [RCD_OBJECTS["trigger_dais"]], GLOBAL_FLAGS["chain_whip_dais_left"], GLOBAL_FLAGS["screen_flag_2e"])
        self.__update_operation("write", objects, [RCD_OBJECTS["trigger_dais"]], GLOBAL_FLAGS["chain_whip_dais_left"], GLOBAL_FLAGS["screen_flag_2e"])

        self.__update_operation("test", objects, [RCD_OBJECTS["trigger_dais"]], GLOBAL_FLAGS["chain_whip_dais_right"], GLOBAL_FLAGS["screen_flag_2f"])
        self.__update_operation("write", objects, [RCD_OBJECTS["trigger_dais"]], GLOBAL_FLAGS["chain_whip_dais_right"], GLOBAL_FLAGS["screen_flag_2f"])

    def __add_angel_shield_lockout_fix(self):
        screen = self.file_contents.zones[17].rooms[8].screens[0]

        left_dais_flag_timer = FlagTimer(delay_frames=30)
        left_dais_test_ops = [
            Operation.create(GLOBAL_FLAGS["dimensional_angel_shield_dais_left"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["dimensional_children_dead"], TEST_OPERATIONS["gteq"], 11)
        ]
        left_dais_write_ops = [Operation.create(GLOBAL_FLAGS["screen_flag_00"], WRITE_OPERATIONS["assign"], 1)]
        left_dais_flag_timer.add_ops(left_dais_test_ops, left_dais_write_ops)
        left_dais_flag_timer.add_to_screen(self, screen)

        right_dais_flag_timer = FlagTimer(delay_frames=30)
        right_dais_test_ops = [
            Operation.create(GLOBAL_FLAGS["dimensional_angel_shield_dais_right"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["dimensional_children_dead"], TEST_OPERATIONS["gteq"], 11)
        ]
        right_dais_write_ops = [Operation.create(GLOBAL_FLAGS["screen_flag_01"], WRITE_OPERATIONS["assign"], 1)]
        right_dais_flag_timer.add_ops(right_dais_test_ops, right_dais_write_ops)
        right_dais_flag_timer.add_to_screen(self, screen)

    def __add_dimensional_orb_ladder(self) -> None:
        screen = self.file_contents.zones[17].rooms[10].screens[0]

        ladder = Ladder(28, 31, 0, 8, 2, 660, 0, 0, 1)
        test_ops = [Operation.create(GLOBAL_FLAGS["ushumgallu_state"], TEST_OPERATIONS["eq"], 2)]
        write_ops = []

        ladder.add_ops(test_ops, write_ops)
        ladder.add_to_screen(self, screen)

    def __add_true_shrine_doors(self):
        doors = [
            {"room": 0, "screen": 0, "x": 17, "y": 4, "dest_x": 340, "dest_y": 92}, # Upper Entrance
            {"room": 8, "screen": 1, "x": 13, "y": 40, "dest_x": 300, "dest_y": 320}, # Lower Entrance 
            {"room": 7, "screen": 0, "x": 25, "y": 4, "dest_x": 500, "dest_y": 80}, # Grail Point
            {"room": 9, "screen": 0, "x": 25, "y": 20, "dest_x": 300, "dest_y": 332} # Treasury
        ]

        for door in doors:
            screen = self.file_contents.zones[18].rooms[door["room"]].screens[door["screen"]]
            warp_door = WarpDoor(door["x"], door["y"], 0, 9, door["room"], door["screen"], door["dest_x"], door["dest_y"])
            warp_door.add_ops([], [])
            warp_door.add_to_screen(self, screen)

            door_graphic = TextureDrawAnimation(x=door["x"]-1, y=door["y"]-2, image_file=-1, layer=-1, image_x=0, image_y=512, dx=80, dy=80, pause_frames=1, max_alpha=255)
            door_graphic.add_to_screen(self, screen)

    def __add_moonlight_to_twin_lockout_fix(self):
        screen = self.file_contents.zones[12].rooms[2].screens[0]

        timer = FlagTimer()
        test_ops = [Operation.create(GLOBAL_FLAGS["moonlight_to_twin_breakable_floor"], TEST_OPERATIONS["eq"], 1)]
        write_ops = [Operation.create(GLOBAL_FLAGS["moonlight_to_twin_breakable_floor"], WRITE_OPERATIONS["assign"], 0)]
        timer.add_ops(test_ops, write_ops)
        timer.add_to_screen(self, screen)

    def __add_flail_whip_lockout_fix(self):
        locations = [{"room": 5, "screen": 1}, {"room": 6, "screen": 2}]
        for location in locations:
            screen = self.file_contents.zones[13].rooms[location["room"]].screens[location["screen"]]

            timer = FlagTimer()
            test_ops = [Operation.create(GLOBAL_FLAGS["flail_whip_puzzle"], TEST_OPERATIONS["eq"], 1)]
            write_ops = [Operation.create(GLOBAL_FLAGS["flail_whip_puzzle"], WRITE_OPERATIONS["assign"], 0)]
            timer.add_ops(test_ops, write_ops)
            timer.add_to_screen(self, screen)

    def __add_hardmode_toggle(self):
        screen = self.file_contents.zones[2].rooms[2].screens[0]

        ops = [
            {"test_op": "eq", "write_val": 0},
            {"test_op": "lt", "write_val": 2}
        ]
        for op in ops:
            dais = Dais(28, 5)
            test_ops = [Operation.create(GLOBAL_FLAGS["hardmode"], TEST_OPERATIONS[op["test_op"]], 2)]
            write_ops = [Operation.create(GLOBAL_FLAGS["hardmode"], WRITE_OPERATIONS["assign"], op["write_val"])]
            dais.add_ops(test_ops, write_ops)
            dais.add_to_screen(self, screen)

    def __add_sacred_orb_timers(self):
        screen = self.file_contents.zones[1].rooms[1].screens[1]

        for i in range(10):
            timer = FlagTimer()
            test_ops = [
                Operation.create(GLOBAL_FLAGS["orb_count_incremented_guidance"]+i, TEST_OPERATIONS["eq"], 0),
                Operation.create(GLOBAL_FLAGS["guidance_orb_found"]+i, TEST_OPERATIONS["eq"], 2)
            ]
            write_ops = [
                Operation.create(GLOBAL_FLAGS["orb_count_incremented_guidance"]+i, WRITE_OPERATIONS["assign"], 1),
                Operation.create(GLOBAL_FLAGS["guidance_orb_found"]+i, WRITE_OPERATIONS["add"], 1)
            ]
            timer.add_ops(test_ops, write_ops)
            timer.add_to_screen(self, screen)

    def __clean_up_operations(self):
        # Remove Fairy Conversation Requirement from Buer Room Ladder
        buer_objects = self.file_contents.zones[3].rooms[2].screens[1].objects_with_position
        self.__remove_operation("test", buer_objects, [RCD_OBJECTS["hitbox_generator"]], GLOBAL_FLAGS["endless_fairyqueen"])

        # Remove Slushfund Conversation Requirement from Pepper Puzzle
        pepper_puzzle_objects = self.file_contents.zones[0].rooms[0].screens[0].objects_with_position
        self.__remove_operation("test", pepper_puzzle_objects, [RCD_OBJECTS["use_item"]], GLOBAL_FLAGS["slushfund_conversation"])

        # Remove Crucifix Check from Crucifix Puzzle Torches
        crucifix_puzzle_objects = self.file_contents.zones[0].rooms[1].screens[1].objects_with_position
        self.__remove_operation("test", crucifix_puzzle_objects, [RCD_OBJECTS["texture_draw_animation"]], GLOBAL_FLAGS["crucifix_found"])

        # Remove Cog Puzzle Requirement from Mudmen Activation
        mudmen_activation_objects = self.file_contents.zones[10].rooms[0].screens[1].objects_with_position
        self.__remove_operation("test", mudmen_activation_objects, [RCD_OBJECTS["use_item"]], GLOBAL_FLAGS["cog_puzzle"])

        # Remove Plane Missing Requirement from Plane Puzzle
        plane_platform_left_objects = self.file_contents.zones[13].rooms[7].screens[0].objects_with_position
        self.__remove_operation("test", plane_platform_left_objects, [RCD_OBJECTS["counterweight_platform"]], GLOBAL_FLAGS["plane_found"])
        plane_platform_right_objects = self.file_contents.zones[13].rooms[7].screens[2].objects_with_position
        self.__remove_operation("test", plane_platform_right_objects, [RCD_OBJECTS["counterweight_platform"]], GLOBAL_FLAGS["plane_found"])

        # Remove Dracuet Check From Guidance Elevator Block
        guidance_elevator_hibox_objects = self.file_contents.zones[0].rooms[6].screens[0].objects_with_position
        self.__remove_operation("test", guidance_elevator_hibox_objects, [RCD_OBJECTS["hitbox_generator"]], GLOBAL_FLAGS["mulbruk_father"])

        # Remove Shrine Chest Check from Xelpud Conversations
        xelpud_conversation_objects = self.file_contents.zones[0].rooms[6].screens[0].objects_with_position
        self.__remove_operation("test", xelpud_conversation_objects, [RCD_OBJECTS["language_conversation"]], GLOBAL_FLAGS["shrine_diary_chest"])

        # Remove Unknown Test from Mulbruk Conversations
        mulbruk_conversation_objects = self.file_contents.zones[3].rooms[3].screens[0].objects_with_position
        self.__remove_operation("test", mulbruk_conversation_objects, [RCD_OBJECTS["language_conversation"]], GLOBAL_FLAGS["mulbruk_conversation_unknown"])
        self.__update_operation("test", mulbruk_conversation_objects, [RCD_OBJECTS["language_conversation"]], GLOBAL_FLAGS["score"], GLOBAL_FLAGS["score"], old_op_value=56, old_operation=TEST_OPERATIONS["gteq"], new_op_value=0)

        # Remove Book of the Dead Write Flag from Anubis Kill
        anubis_objects = self.file_contents.zones[12].rooms[10].screens[0].objects_with_position
        self.__remove_operation("write", anubis_objects, [RCD_OBJECTS["big_anubis"]], GLOBAL_FLAGS["mulbruk_book_of_the_dead"])

    def __create_grail_autoscans(self) -> None:
        for zone in self.file_contents.zones:
            for room in zone.rooms:
                for screen in room.screens:
                    for obj in screen.objects_with_position:
                        if obj.id == RCD_OBJECTS["scannable"]:
                            language_block = obj.parameters[0]
                            frontside = language_block == 41 or language_block == 75 or language_block == 104 or language_block == 136 or language_block == 149 or language_block == 170 or language_block == 188 or language_block == 221 or (language_block == 231 and zone.zone_index == 9)
                            backside = language_block == 250 or language_block == 275 or language_block == 291 or language_block == 305 or language_block == 323 or language_block == 339 or language_block == 206 or language_block == 358 or (language_block == 231 and zone.zone_index != 9)

                            if frontside or backside:
                                grail_flag = grail_flag_by_zone(zone.zone_index, frontside)

                                lemeza_detector = LemezaDetector(x=obj.x_pos, y=obj.y_pos-1, width=2, height=3)
                                test_ops = [Operation.create(grail_flag, TEST_OPERATIONS["eq"], 0)]
                                write_ops = [Operation.create(grail_flag, WRITE_OPERATIONS["assign"], 1)]
                                lemeza_detector.add_ops(test_ops, write_ops)
                                lemeza_detector.add_to_screen(self, screen)

    def __create_boss_checkpoints(self) -> None:
        # Amphisbaena
        amphisbaena_screen = self.file_contents.zones[0].rooms[8].screens[1]
        amphisbaena_grail_point = GrailPoint(x=15, y=44, card=41)
        test_ops = [
            Operation.create(GLOBAL_FLAGS["amphisbaena_ankh_puzzle"], TEST_OPERATIONS["eq"], 5),
            Operation.create(GLOBAL_FLAGS["amphisbaena_state"], TEST_OPERATIONS["lt"], 2),
            Operation.create(GLOBAL_FLAGS["screen_flag_02"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["escape"], TEST_OPERATIONS["eq"], 0)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["screen_flag_02"], WRITE_OPERATIONS["assign"], 1)]
        amphisbaena_grail_point.add_ops(test_ops, write_ops)
        amphisbaena_grail_point.add_to_screen(self, amphisbaena_screen)

        # Sakit
        sakit_screen = self.file_contents.zones[2].rooms[8].screens[1]
        sakit_grail_point = GrailPoint(x=45, y=6, card=75)
        test_ops = [
            Operation.create(GLOBAL_FLAGS["sakit_ankh_puzzle"], TEST_OPERATIONS["eq"], 1),
            Operation.create(GLOBAL_FLAGS["sakit_state"], TEST_OPERATIONS["lt"], 2),
            Operation.create(GLOBAL_FLAGS["screen_flag_02"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["escape"], TEST_OPERATIONS["eq"], 0)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["screen_flag_02"], WRITE_OPERATIONS["assign"], 1)]
        sakit_grail_point.add_ops(test_ops, write_ops)
        sakit_grail_point.add_to_screen(self, sakit_screen)

        # Ellmac
        ellmac_screen = self.file_contents.zones[3].rooms[8].screens[0]
        ellmac_grail_point = GrailPoint(x=20, y=16, card=104)
        test_ops = [
            Operation.create(GLOBAL_FLAGS["ellmac_ankh_puzzle"], TEST_OPERATIONS["eq"], 5),
            Operation.create(GLOBAL_FLAGS["ellmac_state"], TEST_OPERATIONS["lt"], 2),
            Operation.create(GLOBAL_FLAGS["screen_flag_02"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["escape"], TEST_OPERATIONS["eq"], 0)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["screen_flag_02"], WRITE_OPERATIONS["assign"], 1)]
        ellmac_grail_point.add_ops(test_ops, write_ops)
        ellmac_grail_point.add_to_screen(self, ellmac_screen)

        # Bahamut
        bahamut_screen = self.file_contents.zones[4].rooms[4].screens[0]
        bahamut_grail_point = GrailPoint(x=19, y=17, card=136)
        test_ops = [
            Operation.create(GLOBAL_FLAGS["bahamut_ankh_puzzle"], TEST_OPERATIONS["eq"], 1),
            Operation.create(GLOBAL_FLAGS["bahamut_room_flooded"], TEST_OPERATIONS["eq"], 1),
            Operation.create(GLOBAL_FLAGS["bahamut_state"], TEST_OPERATIONS["lt"], 2),
            Operation.create(GLOBAL_FLAGS["screen_flag_02"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["escape"], TEST_OPERATIONS["eq"], 0)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["screen_flag_02"], WRITE_OPERATIONS["assign"], 1)]
        bahamut_grail_point.add_ops(test_ops, write_ops)
        bahamut_grail_point.add_to_screen(self, bahamut_screen)

        # Viy
        viy_screen = self.file_contents.zones[5].rooms[8].screens[1]
        viy_grail_point = GrailPoint(x=23, y=28, card=149)
        test_ops = [
            Operation.create(GLOBAL_FLAGS["viy_ankh_puzzle"], TEST_OPERATIONS["eq"], 4),
            Operation.create(GLOBAL_FLAGS["viy_state"], TEST_OPERATIONS["lt"], 2),
            Operation.create(GLOBAL_FLAGS["screen_flag_02"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["escape"], TEST_OPERATIONS["eq"], 0)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["screen_flag_02"], WRITE_OPERATIONS["assign"], 1)]
        viy_grail_point.add_ops(test_ops, write_ops)
        viy_grail_point.add_to_screen(self, viy_screen)

        # Palenque
        palenque_screen = self.file_contents.zones[6].rooms[9].screens[1]
        palenque_grail_point = GrailPoint(x=47, y=20, card=170)
        test_ops = [
            Operation.create(GLOBAL_FLAGS["palenque_ankh_puzzle"], TEST_OPERATIONS["eq"], 3),
            Operation.create(GLOBAL_FLAGS["palenque_screen_mural"], TEST_OPERATIONS["eq"], 3),
            Operation.create(GLOBAL_FLAGS["palenque_state"], TEST_OPERATIONS["lt"], 2),
            Operation.create(GLOBAL_FLAGS["screen_flag_02"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["escape"], TEST_OPERATIONS["eq"], 0)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["screen_flag_02"], WRITE_OPERATIONS["assign"], 1)]
        palenque_grail_point.add_ops(test_ops, write_ops)
        palenque_grail_point.add_to_screen(self, palenque_screen)

        # Baphomet
        baphomet_screen = self.file_contents.zones[7].rooms[4].screens[1]
        baphomet_grail_point = GrailPoint(x=47, y=4, card=188)
        test_ops = [
            Operation.create(GLOBAL_FLAGS["baphomet_ankh_puzzle"], TEST_OPERATIONS["eq"], 2),
            Operation.create(GLOBAL_FLAGS["baphomet_state"], TEST_OPERATIONS["lt"], 2),
            Operation.create(GLOBAL_FLAGS["screen_flag_02"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["escape"], TEST_OPERATIONS["eq"], 0)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["screen_flag_02"], WRITE_OPERATIONS["assign"], 1)]
        baphomet_grail_point.add_ops(test_ops, write_ops)
        baphomet_grail_point.add_to_screen(self, baphomet_screen)

        # Tiamat
        tiamat_screen = self.file_contents.zones[17].rooms[9].screens[0]
        tiamat_grail_point = GrailPoint(x=15, y=4, card=368)
        test_ops = [
            Operation.create(GLOBAL_FLAGS["tiamat_ankh_puzzle"], TEST_OPERATIONS["eq"], 1),
            Operation.create(GLOBAL_FLAGS["tiamat_state"], TEST_OPERATIONS["lt"], 2),
            Operation.create(GLOBAL_FLAGS["screen_flag_02"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["escape"], TEST_OPERATIONS["eq"], 0)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["screen_flag_02"], WRITE_OPERATIONS["assign"], 1)]
        tiamat_grail_point.add_ops(test_ops, write_ops)
        tiamat_grail_point.add_to_screen(self, tiamat_screen)

        # Mother
        mother_screen = self.file_contents.zones[18].rooms[3].screens[1]
        mother_grail_point = GrailPoint(x=33, y=20, card=231)
        test_ops = [
            Operation.create(GLOBAL_FLAGS["mother_ankh_puzzle"], TEST_OPERATIONS["eq"], 1),
            Operation.create(GLOBAL_FLAGS["mother_state"], TEST_OPERATIONS["lteq"], 2),
            Operation.create(GLOBAL_FLAGS["screen_flag_02"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["escape"], TEST_OPERATIONS["eq"], 0)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["screen_flag_02"], WRITE_OPERATIONS["assign"], 1)]
        mother_grail_point.add_ops(test_ops, write_ops)
        mother_grail_point.add_to_screen(self, mother_screen)

    def __create_ancient_lamulanese_timer(self):
        screen = self.file_contents.zones[1].rooms[2].screens[1]

        flag_timer = FlagTimer()
        test_ops = [Operation.create(GLOBAL_FLAGS["ancient_lamulanese_learned"], TEST_OPERATIONS["eq"], 0)]
        write_ops = [
            Operation.create(GLOBAL_FLAGS["translation_tablets_read"], WRITE_OPERATIONS["assign"], 3),
            Operation.create(GLOBAL_FLAGS["ancient_lamulanese_learned"], WRITE_OPERATIONS["assign"], 1)
        ]
        flag_timer.add_ops(test_ops, write_ops)
        flag_timer.add_to_screen(self, screen)

    def __create_alternate_mother_ankh(self):
        mother_screen = self.file_contents.zones[18].rooms[3].screens[0]

        # Remove Mother Animations
        self.__remove_objects_by_id(mother_screen, mother_screen.objects_with_position, [RCD_OBJECTS["animation"]])

        # Modify Mother Ankh
        mother_ankhs = self.__find_objects_by_id(mother_screen.objects_with_position, [RCD_OBJECTS["mother_ankh"]])
        for ankh in mother_ankhs:
            ankh.id = RCD_OBJECTS["ankh"]
            ankh.parameters[0] = 8
            ankh.write_operations[0].op_value = 1
            ankh.write_operations[1].op_value = 2
            ankh.y_pos += 3

        # Return Ankh Jewel if warped out of fight
        surface_screen = self.file_contents.zones[1].rooms[11].screens[0]

        instant_item = InstantItem(5, 3, 19, 12, 16, 39)
        test_ops = [Operation.create(GLOBAL_FLAGS["mother_ankh_jewel_recovery"], TEST_OPERATIONS["eq"], 1)]
        write_ops = [
            Operation.create(GLOBAL_FLAGS["mother_ankh_jewel_recovery"], WRITE_OPERATIONS["assign"], 0),
            Operation.create(GLOBAL_FLAGS["mother_state"], WRITE_OPERATIONS["assign"], 1)
        ]
        instant_item.add_ops(test_ops, write_ops)
        instant_item.add_to_screen(self, surface_screen)

        flag_timer = FlagTimer()
        test_ops = [
            Operation.create(GLOBAL_FLAGS["mother_state"], TEST_OPERATIONS["eq"], 2),
            Operation.create(GLOBAL_FLAGS["escape"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["mother_ankh_jewel_recovery"], TEST_OPERATIONS["eq"], 0)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["mother_ankh_jewel_recovery"], WRITE_OPERATIONS["assign"], 1)]
        flag_timer.add_ops(test_ops, write_ops)
        flag_timer.add_to_screen(self, surface_screen)

    # Utility Methods

    def __op_type(self, op):
        return f"{op}_operations"

    # Search Methods

    def __find_objects_by_id(self, objects, object_ids):
        return [o for _, o in enumerate(objects) if o.id in object_ids]

    def __find_object_index_by_id(self, objects, object_ids):
        return next(i for i, o in enumerate(objects) if o.id in object_ids)

    def __find_objects_by_operation(self, op_type, objects, object_ids, flag, operation=None, op_value=None):
        return [o for _, o in enumerate(objects) if o.id in object_ids and len([op for op in getattr(o, self.__op_type(op_type)) if self.__op_matches(op, flag, operation, op_value)]) > 0]

    def __find_object_index_by_operation(self, op_type, objects, object_ids, flag, operation=None, op_value=None):
        return next(i for i, o in enumerate(objects) if o.id in object_ids and len([op for op in getattr(o, self.__op_type(op_type)) if self.__op_matches(op, flag, operation, op_value)]) > 0)

    def __find_objects_by_parameter(self, objects, object_ids, param_index, param_value):
        return [o for _, o in enumerate(objects) if o.id in object_ids and o.parameters[param_index] == param_value]

    def __find_object_index_by_parameter(self, objects, object_ids, param_index, param_value):
        return next(i for i, o in enumerate(objects) if o.id in object_ids and o.parameters[param_index] == param_value)

    def __find_operation_index(self, ops, flag, operation=None, op_value=None):
        return next(i for i, op in enumerate(ops) if self.__op_matches(op, flag, operation, op_value))

    # Conditionals

    def __op_matches(self, op, flag, operation, op_value):
        return op.flag == flag and (operation is None or op.operation == operation) and (op_value is None or op.op_value == op_value)

    # Write Methods

    def __remove_objects_by_id(self, screen, objects, object_ids):
        for _ in self.__find_objects_by_id(objects, object_ids):
            object_index = self.__find_object_index_by_id(objects, object_ids)
            self.__remove_object(screen, objects, object_index)

    def __remove_objects_by_operation(self, screen, op_type, objects, object_ids, flag, operation=None, op_value=None):
        for _ in self.__find_objects_by_operation(op_type, objects, object_ids, flag, operation, op_value):
            object_index = self.__find_object_index_by_operation(op_type, objects, object_ids, flag, operation, op_value)
            self.__remove_object(screen, objects, object_index)

    def __remove_objects_by_parameter(self, screen, objects, object_ids, param_index, param_value):
        for _ in self.__find_objects_by_parameter(objects, object_ids, param_index, param_value):
            object_index = self.__find_object_index_by_parameter(objects, object_ids, param_index, param_value)
            self.__remove_object(screen, objects, object_index)

    def __remove_object(self, screen, objects, object_index):
        obj = objects[object_index]

        screen.objects_length -= 1

        # id (2) + test_operations_length (.5) + write_operations_length (.5) + parameters_length (1) + x_pos (2) + y_pos (2)
        object_size = 8

        # test_operations (4*len) + write_operations(4*len) + parameters (2*len)
        object_size += ((obj.test_operations_length + obj.write_operations_length) * 4) + (obj.parameters_length * 2)

        del objects[object_index]
        self.file_size -= object_size

    def __update_position(self, op_type, objects, object_ids, flag, x_pos, y_pos, operation=None, op_value=None):
        objs = self.__find_objects_by_operation(op_type, objects, object_ids, flag, operation, op_value)

        for obj in objs:
            obj.x_pos = x_pos
            obj.y_pos = y_pos

    def __update_operation(self, op_type, objects, object_ids, old_flag, new_flag, old_operation=None, new_operation=None, old_op_value=None, new_op_value=None):
        objs = self.__find_objects_by_operation(op_type, objects, object_ids, old_flag, old_operation, old_op_value)

        for obj in objs:
            ops = getattr(obj, self.__op_type(op_type))
            op_index = self.__find_operation_index(ops, old_flag, old_operation, old_op_value)
            
            op = getattr(obj, self.__op_type(op_type))[op_index]
            op.flag = new_flag
            if new_operation is not None:
                op.operation = new_operation
            if new_op_value is not None:
                op.op_value = new_op_value

    def __remove_operation(self, op_type, objects, object_ids, flag):
        objs = self.__find_objects_by_operation(op_type, objects, object_ids, flag)

        for obj in objs:
            ops = getattr(obj, self.__op_type(op_type))
            op_index = self.__find_operation_index(ops, flag)
            
            del ops[op_index]
            op_type_len = self.__op_type(op_type) + "_length"
            old_len = getattr(obj, op_type_len)
            setattr(obj, op_type_len, old_len-1)
            self.file_size -= 4

    def __add_operation_to_object(self, op_type, obj, flag, operation, op_value):
        op = Rcd.Operation()
        op.flag = flag
        op.operation = operation
        op.op_value = op_value

        ops = getattr(obj, self.__op_type(op_type))
        ops.append(op)

        op_type_len = self.__op_type(op_type) + "_length"
        old_len = getattr(obj, op_type_len)
        setattr(obj, op_type_len, old_len+1)
        self.file_size += 4
