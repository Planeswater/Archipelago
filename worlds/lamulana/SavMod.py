from .FileMod import FileMod
from .Sav import Sav
from .LmFlags import GLOBAL_FLAGS, INVENTORY
from .Options import starting_weapon_names

class SavMod(FileMod):

    NUM_EMAILS = 46

    def __init__(self, options):
        self.file_contents = Sav()
        self.__populate_defaults()
        self.file_size = 5321

        self.options = options

    def apply_mods(self):
        self.__set_starting_weapon()

    def __set_starting_weapon(self):
        weapon = starting_weapon_names[self.options.StartingWeapon.value]

        if weapon != "Leather Whip":
            # Remove Default Leather Whip
            self.file_contents.inventory[0] = 0xff

            if weapon == "Knife":
                self.file_contents.flags[GLOBAL_FLAGS["knife_found"]] = 2
                self.file_contents.inventory[INVENTORY["knife"]] = 1
                self.file_contents.held_main_weapon = 3
                self.file_contents.held_main_weapon_slot = 1
            elif weapon == "Key Sword":
                self.file_contents.flags[GLOBAL_FLAGS["keysword_found"]] = 2
                self.file_contents.inventory[INVENTORY["keysword"]] = 1
                self.file_contents.held_main_weapon = 4
                self.file_contents.held_main_weapon_slot = 2
            elif weapon == "Axe":
                self.file_contents.flags[GLOBAL_FLAGS["axe_found"]] = 2
                self.file_contents.inventory[INVENTORY["axe"]] = 1
                self.file_contents.held_main_weapon = 5
                self.file_contents.held_main_weapon_slot = 3
            elif weapon == "Katana":
                self.file_contents.flags[GLOBAL_FLAGS["katana_found"]] = 2
                self.file_contents.inventory[INVENTORY["katana"]] = 1
                self.file_contents.held_main_weapon = 6
                self.file_contents.held_main_weapon_slot = 4
            else:
                self.file_contents.held_main_weapon = 0xff
                self.file_contents.held_main_weapon_slot = 0xff
                if weapon == "Shuriken":
                    self.file_contents.flags[GLOBAL_FLAGS["shurikens_found"]] = 2
                    self.file_contents.inventory[INVENTORY["shurikens"]] = 1
                    self.file_contents.inventory[INVENTORY["shuriken_ammo"]] = 150
                    self.file_contents.held_sub_weapon = 8
                    self.file_contents.held_sub_weapon_slot = 0
                elif weapon == "Rolling Shuriken":
                    self.file_contents.flags[GLOBAL_FLAGS["rolling_shurikens_found"]] = 2
                    self.file_contents.inventory[INVENTORY["rolling_shurikens"]] = 1
                    self.file_contents.inventory[INVENTORY["rolling_shuriken_ammo"]] = 100
                    self.file_contents.held_sub_weapon = 9
                    self.file_contents.held_sub_weapon_slot = 1
                elif weapon == "Earth Spear":
                    self.file_contents.flags[GLOBAL_FLAGS["earth_spears_found"]] = 2
                    self.file_contents.inventory[INVENTORY["earth_spears"]] = 1
                    self.file_contents.inventory[INVENTORY["earth_spear_ammo"]] = 80
                    self.file_contents.held_sub_weapon = 10
                    self.file_contents.held_sub_weapon_slot = 2
                elif weapon == "Flare Gun":
                    self.file_contents.flags[GLOBAL_FLAGS["flare_gun_found"]] = 2
                    self.file_contents.inventory[INVENTORY["flare_gun"]] = 1
                    self.file_contents.inventory[INVENTORY["flare_gun_ammo"]] = 80
                    self.file_contents.held_sub_weapon = 11
                    self.file_contents.held_sub_weapon_slot = 3
                elif weapon == "Bomb":
                    self.file_contents.flags[GLOBAL_FLAGS["bombs_found"]] = 2
                    self.file_contents.inventory[INVENTORY["bombs"]] = 1
                    self.file_contents.inventory[INVENTORY["bomb_ammo"]] = 30
                    self.file_contents.held_sub_weapon = 12
                    self.file_contents.held_sub_weapon_slot = 4
                elif weapon == "Chakram":
                    self.file_contents.flags[GLOBAL_FLAGS["chakrams_found"]] = 2
                    self.file_contents.inventory[INVENTORY["chakrams"]] = 1
                    self.file_contents.inventory[INVENTORY["chakram_ammo"]] = 10
                    self.file_contents.held_sub_weapon = 13
                    self.file_contents.held_sub_weapon_slot = 5
                elif weapon == "Caltrops":
                    self.file_contents.flags[GLOBAL_FLAGS["caltrops_found"]] = 2
                    self.file_contents.inventory[INVENTORY["caltrops"]] = 1
                    self.file_contents.inventory[INVENTORY["caltrop_ammo"]] = 80
                    self.file_contents.held_sub_weapon = 14
                    self.file_contents.held_sub_weapon_slot = 6
                elif weapon == "Pistol":
                    self.file_contents.flags[GLOBAL_FLAGS["pistol_found"]] = 2
                    self.file_contents.inventory[INVENTORY["pistol"]] = 1
                    self.file_contents.inventory[INVENTORY["pistol_clip_ammo"]] = 3
                    self.file_contents.inventory[INVENTORY["pistol_bullet_ammo"]] = 6
                    self.file_contents.held_sub_weapon = 15
                    self.file_contents.held_sub_weapon_slot = 7

    def __populate_defaults(self):
        self.file_contents.valid = 1
        self.file_contents.game_time = 0
        self.file_contents.zone = 1
        self.file_contents.room = 2
        self.file_contents.screen = 1
        self.file_contents.x_position = 940 % 640
        self.file_contents.y_position = 160 % 480
        self.file_contents.max_hp = 1
        self.file_contents.current_hp = 32
        self.file_contents.current_exp = 0
        self.file_contents.flags = self.__flag_defaults()
        self.file_contents.inventory = [0 for _ in range(255)]
        self.file_contents.held_main_weapon = 0
        self.file_contents.held_sub_weapon = 0xff
        self.file_contents.held_use_item = 0xff
        self.file_contents.held_main_weapon_slot = 0
        self.file_contents.held_sub_weapon_slot = 0
        self.file_contents.held_use_item_slot = 0
        self.file_contents.num_emails = self.NUM_EMAILS
        self.file_contents.received_emails = 0
        self.file_contents.emails = self.__default_emails()
        self.file_contents.equipped_software = [0 for _ in range(20)]
        self.file_contents.rosettas_read = [0,0,0]
        self.file_contents.bunemon_records = self.__default_bunemon_records()
        self.file_contents.mantras_learned = [0 for _ in range(10)]
        self.file_contents.maps_owned_bit_array = 0

    def __default_emails(self):
        emails = [self.__email() for _ in range(self.NUM_EMAILS)]
        return emails

    def __default_bunemon_records(self):
        records = [self.__bunemon_record() for _ in range(20)]
        return records

    def __flag_defaults(self):
        flags = [0 for _ in range(4096)]
        flags[GLOBAL_FLAGS["end_start_animation"]] = 1
        flags[GLOBAL_FLAGS["hell_dlc"]] = 1
        return flags

    def __bunemon_record(self, slot_number=0xff, field_map_card=0, field_map_record=0, location_card=0, location_record=0, text_card=0, text_record=0, is_tablet=0):
        bunemon_record = Sav.BunemonRecord()
        bunemon_record.slot_number = slot_number
        bunemon_record.field_map_card = field_map_card
        bunemon_record.field_map_record = field_map_record
        bunemon_record.location_card = location_card
        bunemon_record.location_record = location_record
        bunemon_record.text_card = text_card
        bunemon_record.text_record = text_record
        bunemon_record.is_tablet = is_tablet
        return bunemon_record

    def __email(self, screenplay_card=0, game_time_received=0, mail_number=0xffff):
        email = Sav.Email()
        email.screenplay_card = screenplay_card
        email.game_time_received = game_time_received
        email.mail_number = mail_number
        return email
