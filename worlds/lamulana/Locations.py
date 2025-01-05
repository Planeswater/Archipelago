from typing import TYPE_CHECKING, Callable, NamedTuple
from BaseClasses import CollectionState
from .Options import RandomizeCoinChests
from .LogicShortcuts import LaMulanaLogicShortcuts
from .CombatLogic import LaMulanaCombatLogic

if TYPE_CHECKING:
	from . import LaMulanaWorld


class LocationData(NamedTuple):
	name: str
	code: int | None
	logic: Callable[[CollectionState], bool] = lambda state: True
	is_event: bool = False
	is_cursable: bool = False
	is_shop: bool = False
	file_type: str | None = None
	zones: list[int] | None = None
	room: int | None = None
	screen: int | None = None
	object_type: int | None = None
	item_id: int | None = None
	cards: list[int] | None = None
	slot: int | None = None
	original_obtain_flag: int | None = None
	obtain_flag: int | None = None
	obtain_value: int | None = None


def get_locations_by_region(world: "LaMulanaWorld | None") -> dict[str, list[LocationData]]:
	if world:
		player = world.player
		worldstate = world.worldstate
		s = LaMulanaLogicShortcuts(world)
		combat = LaMulanaCombatLogic(world, s)

	# Output all locations when "world" is not supplied - this is done when initializing so AP can get a list of all checks
	include_coin_chests = not world or world.options.RandomizeCoinChests
	include_escape_chest = not world or world.options.RandomizeCoinChests == RandomizeCoinChests.option_include_escape_chest
	include_trap_items = not world or world.options.RandomizeTrapItems
	include_hell_temple_reward = not world or world.options.HellTempleReward
	alt_mother_ankh = not world or world.options.AlternateMotherAnkh

	locations = {
		"Surface [Main]": [
			LocationData("Surface - Birth Seal Chest", 2359000, lambda state: s.attack_chest(state) and state.has_all({worldstate.get_seal_name('Birth Seal Chest'), "Helmet"}, player) and state.has_any({"Hermes' Boots", "Feather", "Bahamut Defeated"}, player), is_cursable=True, file_type='rcd', zones=[1, 22], room=7, screen=1, object_type=0x2c, item_id=66, obtain_flag=0xc3, obtain_value=2),
			LocationData("Surface - deathv.exe Breakable Wall", 2359001, lambda state: s.attack_forward(state) and (state.has("NPC: Xelpud", player) or s.glitch_raindrop(state)), file_type='rcd', zones=[1, 22], room=4, screen=2, object_type=0x2f, item_id=96, obtain_flag=0x14f, obtain_value=2),
			LocationData("Surface - Feather Chest", 2359002, lambda state: s.attack_chest(state) and state.has('Serpent Staff', player) and combat.argus(state), is_cursable=True, file_type='rcd', zones=[1, 22], room=0, screen=0, object_type=0x2c, item_id=53, obtain_flag=0xb6, obtain_value=2),
			LocationData("Surface - Skeleton Map Scan", 2359003, lambda state: state.has("Hand Scanner", player), file_type='rcd', zones=[1], room=4, screen=2, object_type=0xb5, item_id=70, original_obtain_flag=0xd1, obtain_flag=0x83b, obtain_value=2),
			LocationData("Surface - Sacred Orb Chest", 2359004, lambda state: state.has("Helmet", player) and state.has_any({"Hermes' Boots", "Bahamut Defeated"}, player) and (s.attack_above(state) or s.attack_shuriken(state) or s.attack_chakram(state) or s.attack_bomb(state) or s.attack_pistol(state) or (s.attack_s_above(state) and s.attack_chest(state)) or (s.attack_rolling_shuriken(state) and state.has("Bahamut Defeated", player))), is_cursable=True, file_type='rcd', zones=[1, 22], room=8, screen=1, object_type=0x2c, item_id=69, obtain_flag=0xc8, obtain_value=2),
			LocationData("Surface - Shell Horn Chest", 2359005, lambda state: s.attack_chest_any(state), is_cursable=True, file_type='rcd', zones=[1, 22], room=4, screen=1, object_type=0x2c, item_id=38, obtain_flag=0xa7, obtain_value=2),
			LocationData("Surface Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Gate of Guidance [Main]": [
			LocationData("Gate of Guidance - Ankh Jewel Chest", 2359006, lambda state: s.attack_main(state) or s.attack_shuriken(state) or s.attack_rolling_shuriken(state) or s.attack_chakram(state) or s.attack_caltrops(state) or s.attack_pistol(state), is_cursable=True, file_type='rcd', zones=[0], room=7, screen=1, object_type=0x2c, item_id=19, obtain_flag=0x8e, obtain_value=2),
			LocationData("Gate of Guidance - Crucifix Chest", 2359007, lambda state: (s.attack_flare_gun(state) or (state.has('Flare Gun', player) and s.fairy_point_reachable(state))) and s.attack_chest(state) and state.has(worldstate.get_seal_name('Crucifix Chest/3 Lights'), player), is_cursable=True, file_type='rcd', zones=[0], room=1, screen=1, object_type=0x2c, item_id=42, obtain_flag=0xab, obtain_value=2),
			LocationData("Gate of Guidance - Holy Grail Chest", 2359008, lambda state: s.attack_chest(state), is_cursable=True, file_type='rcd', zones=[0], room=4, screen=1, object_type=0x2c, item_id=40, obtain_flag=0xa9, obtain_value=2),
			LocationData("Gate of Guidance - Map Chest", 2359009, lambda state: s.attack_chest(state), is_cursable=True, file_type='rcd', zones=[0], room=3, screen=0, object_type=0x2c, item_id=70, original_obtain_flag=0xd2, obtain_flag=0x83c, obtain_value=2),
			LocationData("Gate of Guidance - Sacred Orb Chest", 2359010, lambda state: s.attack_chest_any(state), is_cursable=True, file_type='rcd', zones=[0], room=0, screen=1, object_type=0x2c, item_id=69, obtain_flag=0xc7, obtain_value=2),
			LocationData("Gate of Guidance - Shuriken Puzzle Reward", 2359011, lambda state: s.attack_chest_any(state), file_type='rcd', zones=[0], room=2, screen=0, object_type=0x2f, item_id=8, obtain_flag=0x83, obtain_value=1),
			LocationData("Gate of Guidance - Treasures Chest", 2359012, lambda state: s.attack_chest_any(state) and state.has("Pepper", player), is_cursable=True, file_type='rcd', zones=[0], room=0, screen=0, object_type=0x2c, item_id=71, obtain_flag=0x103, obtain_value=2),
			LocationData("Gate of Guidance Grail Tablet", None, lambda state: s.state_read_grail(state), True),
			LocationData('Amphisbaena Defeated', None, lambda state: s.attack_chest(state) and combat.amphisbaena(state) and s.has_ankh_jewel(state, 'Amphisbaena'), True)
		],
		"Gate of Guidance [Door]": [
			LocationData("Gate of Guidance - yagostr.exe Chest", 2359013, lambda state: s.attack_chest(state), is_cursable=True, file_type='rcd', zones=[0], room=5, screen=0, object_type=0x2c, item_id=88, obtain_flag=0xe5, obtain_value=2)
		],
		"Mausoleum of the Giants": [
			LocationData("Mausoleum of the Giants - Ankh Jewel Chest", 2359014, lambda state: s.attack_chest(state), is_cursable=True, file_type='rcd', zones=[2], room=6, screen=1, object_type=0x2c, item_id=19, obtain_flag=0x8f, obtain_value=2),
			LocationData("Mausoleum of the Giants - Map Chest", 2359015, lambda state: s.attack_chest_any(state), is_cursable=True, file_type='rcd', zones=[2], room=1, screen=1, object_type=0x2c, item_id=70, original_obtain_flag=0xd3, obtain_flag=0x83d, obtain_value=2),
			LocationData("Mausoleum of the Giants - Rolling Shuriken Reward", 2359016, lambda state: s.attack_chest_any(state), file_type='rcd', zones=[2], room=3, screen=0, object_type=0x2f, item_id=9, obtain_flag=0x84, obtain_value=1),
			LocationData("Mausoleum of the Giants - Sacred Orb Chest", 2359017, lambda state: s.attack_chest_any(state), is_cursable=True, file_type='rcd', zones=[2], room=7, screen=0, object_type=0x2c, item_id=69, obtain_flag=0xc9, obtain_value=2),
			LocationData("Mausoleum of the Giants Grail Tablet", None, lambda state: s.state_read_grail(state), True),
			LocationData('Sakit Defeated', None, lambda state: combat.sakit(state) and s.has_ankh_jewel(state, 'Sakit'), True)
		],
		"Temple of the Sun [Main]": [
			LocationData("Temple of the Sun - Ankh Jewel Chest", 2359018, lambda state: s.attack_chest(state), is_cursable=True, file_type='rcd', zones=[3], room=7, screen=0, object_type=0x2c, item_id=19, obtain_flag=0x90, obtain_value=2),
			LocationData("Temple of the Sun - Knife Puzzle Reward", 2359019, lambda state: s.attack_shuriken(state) or (s.attack_chakram(state) and state.has_any({"Feather", "Grapple Claw"}, player)) or s.attack_bomb(state) or (s.attack_flare_gun(state) and s.attack_forward(state) and state.has("Feather", player)) or s.glitch_catpause(state), file_type='rcd', zones=[3], room=1, screen=2, object_type=0x2f, item_id=3, obtain_flag=0x7f, obtain_value=1),
			LocationData("Temple of the Sun - Sacred Orb Chest", 2359020, lambda state: s.attack_chest_any(state), is_cursable=True, file_type='rcd', zones=[3], room=4, screen=3, object_type=0x2c, item_id=69, obtain_flag=0xca, obtain_value=2),
			LocationData('Maternity Statue', None, lambda state: state.has('Woman Statue', player), True),
			LocationData('Ellmac Defeated', None, lambda state: state.has('Holy Grail', player) and combat.ellmac(state) and s.has_ankh_jewel(state, 'Ellmac'), True)
		],
		"Temple of the Sun [Top Entrance]": [
			LocationData("Temple of the Sun - Map Chest", 2359021, lambda state: s.attack_chest(state) and s.sun_watchtower(state), is_cursable=True, file_type='rcd', zones=[3], room=0, screen=1, object_type=0x2c, item_id=70, original_obtain_flag=0xd4, obtain_flag=0x83e, obtain_value=2),
		],
		"Temple of the Sun [Grail]": [
			LocationData("Temple of the Sun Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Temple of the Sun [West]": [
			LocationData("Temple of the Sun - Isis' Pendant Chest", 2359022, lambda state: state.has("Buer Defeated", player) and s.state_literacy(state) and s.state_mobility(state) and (s.attack_above(state) or s.attack_s_above(state)), is_cursable=True, file_type='rcd', zones=[3], room=2, screen=0, object_type=0x2c, item_id=41, obtain_flag=0xaa, obtain_value=2),
			LocationData("Buer Defeated", None, lambda state: combat.buer(state), True)
		],
		"Temple of the Sun [East]": [
			LocationData("Temple of the Sun - Bronze Mirror Chest", 2359023, lambda state: s.bronze_mirror_chest_logic(state), is_cursable=True, file_type='rcd', zones=[3], room=5, screen=0, object_type=0x2c, item_id=45, obtain_flag=0xae, obtain_value=2),
			LocationData("Temple of the Sun - Talisman Location", 2359024, lambda state: state.has("Viy Defeated", player), file_type='rcd', zones=[3], room=4, screen=2, object_type=0x2f, item_id=34, obtain_flag=0xa4, obtain_value=2)
		],
		"Spring in the Sky [Main]": [
			LocationData("Spring in the Sky - Caltrops Puzzle Reward", 2359025, file_type='rcd', zones=[4], room=1, screen=0, object_type=0x2f, item_id=14, obtain_flag=0x89, obtain_value=1),
			LocationData("Spring in the Sky - Map Chest", 2359026, lambda state: s.attack_chest_any(state), is_cursable=True, file_type='rcd', zones=[4], room=2, screen=1, object_type=0x2c, item_id=70, original_obtain_flag=0xd5, obtain_flag=0x83f, obtain_value=2),
			LocationData("Spring in the Sky - Sacred Orb Chest", 2359027, lambda state: s.attack_chest_any(state) and state.has(worldstate.get_seal_name('Spring Sacred Orb Chest'), player), is_cursable=True, file_type='rcd', zones=[4], room=0, screen=0, object_type=0x2c, item_id=69, obtain_flag=0xcb, obtain_value=2),
			LocationData("Spring in the Sky - Ankh Jewel Chest", 2359123, lambda state: s.attack_chest(state) and (s.attack_earth_spear(state) or state.has('Scalesphere', player) or s.get_health_count(state) >= 1), is_cursable=True, file_type='rcd', zones=[4], room=7, screen=0, object_type=0x2c, item_id=19, obtain_flag=0x91, obtain_value=2),
			LocationData("Flooded Temple of the Sun", None, lambda state: (s.attack_forward(state) and (s.state_water_swim(state, 3) or state.has('Holy Grail', player))) or (s.attack_vertical(state) and s.state_water_swim(state, 3)), True),
			LocationData("Spring in the Sky Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Spring in the Sky [Upper]": [
			LocationData("Spring in the Sky - Glove Chest", 2359028, lambda state: state.has("Flooded Spring in the Sky", player) and s.attack_chest_any(state), is_cursable=True, file_type='rcd', zones=[4], room=2, screen=0, object_type=0x2c, item_id=39, obtain_flag=0xa8, obtain_value=2),
			LocationData("Spring in the Sky - Origin Seal Chest", 2359029, lambda state: state.has_all({'Helmet'}, player) and combat.nuckelavee(state) and (s.attack_forward(state) or (state.has("Feather", player) and s.attack_earth_spear(state))), is_cursable=True, file_type='rcd', zones=[4], room=5, screen=0, object_type=0x2c, item_id=65, obtain_flag=0xc2, obtain_value=2),
			LocationData("Spring in the Sky - Scalesphere Chest", 2359030, lambda state: s.attack_chest(state) and state.has("Helmet", player), is_cursable=True, file_type='rcd', zones=[4], room=3, screen=0, object_type=0x2c, item_id=48, obtain_flag=0xb1, obtain_value=2),
			LocationData("Flooded Spring in the Sky", None, lambda state: state.has_all({"Helmet", worldstate.get_seal_name('Bahamut\'s Room')}, player), True),
			LocationData('Bahamut Defeated', None, lambda state: state.has_all({'Helmet', worldstate.get_seal_name('Bahamut\'s Room')}, player) and combat.bahamut(state) and s.has_ankh_jewel(state, 'Bahamut'), True)
		],
		"Inferno Cavern [Main]": [
			LocationData("Inferno Cavern - bunplus.com Breakable Wall", 2359031, lambda state: s.attack_forward(state), file_type='rcd', zones=[5], room=7, screen=0, object_type=0x2f, item_id=90, obtain_flag=0xe7, obtain_value=1),
			LocationData("Inferno Cavern - Flare Gun Puzzle Reward", 2359032, lambda state: s.attack_forward(state), file_type='rcd', zones=[5], room=4, screen=0, object_type=0x2f, item_id=11, obtain_flag=0x86, obtain_value=1),
			LocationData("Inferno Cavern - Ice Cape Chest", 2359033, lambda state: s.attack_chest(state), is_cursable=True, file_type='rcd', zones=[5], room=7, screen=1, object_type=0x2c, item_id=64, obtain_flag=0xc1, obtain_value=2),
			LocationData("Inferno Cavern - Map Chest", 2359034, lambda state: s.attack_chest_any(state), is_cursable=True, file_type='rcd', zones=[5], room=1, screen=0, object_type=0x2c, item_id=70, original_obtain_flag=0xd6, obtain_flag=0x840, obtain_value=2),
			LocationData("Inferno Cavern Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Inferno Cavern [Pazuzu]": [
			LocationData("Inferno Cavern - Chain Whip Puzzle Reward", 2359035, lambda state: combat.pazuzu(state), file_type='rcd', zones=[5], room=3, screen=0, object_type=0x2f, item_id=1, obtain_flag=0x7d, obtain_value=1)
		],
		"Inferno Cavern [Viy]": [
			LocationData('Viy Defeated', None, lambda state: state.has('Holy Grail', player) and s.state_lava_swim(state, 5) and combat.viy(state) and s.has_ankh_jewel(state, 'Viy'), True)
		],
		"Chamber of Extinction [Main]": [
			LocationData("Chamber of Extinction - Chakram Reward", 2359036, lambda state: s.state_extinction_light(state) and (combat.centimani(state) or s.glitch_catpause(state)), file_type='rcd', zones=[6], room=4, screen=0, object_type=0x2f, item_id=13, obtain_flag=0x88, obtain_value=1),
			LocationData("Chamber of Extinction - Life Seal Chest", 2359037, lambda state: s.state_extinction_light(state) and s.attack_chest(state) and state.has(worldstate.get_seal_name('Life Seal Chest'), player), is_cursable=True, file_type='rcd', zones=[6], room=6, screen=0, object_type=0x2c, item_id=67, obtain_flag=0xc4, obtain_value=2),
			LocationData("Chamber of Extinction - mantra.exe Scan", 2359038, lambda state: s.attack_flare_gun(state) and state.has_all({"Magatama Jewel", "torude.exe", "Ox-head & Horse-face Defeated"}, player), file_type='rcd', zones=[6], room=4, screen=1, object_type=0xc3, item_id=93, obtain_flag=0xea, obtain_value=2),
			LocationData("Chamber of Extinction - Sacred Orb Chest", 2359039, lambda state: s.state_extinction_light(state) and (s.attack_chest(state) or (s.attack_flare_gun(state) and state.has("Feather", player))), is_cursable=True, file_type='rcd', zones=[6], room=3, screen=1, object_type=0x2c, item_id=69, obtain_flag=0xcc, obtain_value=2),
			LocationData("Chamber of Extinction Grail Tablet", None, lambda state: s.state_extinction_light(state) and s.state_read_grail(state), True)
		],
		"Chamber of Extinction [Map]": [
			LocationData("Chamber of Extinction - Map Chest", 2359040, lambda state: s.state_extinction_light(state) and s.attack_chest_any(state), is_cursable=True, file_type='rcd', zones=[6], room=3, screen=0, object_type=0x2c, item_id=70, original_obtain_flag=0xd7, obtain_flag=0x841, obtain_value=2)
		],
		"Chamber of Extinction [Left Main]": [
			LocationData("Lamp Recharge — Chamber of Extinction", None, lambda state: True, True)
		],
		"Chamber of Extinction [Magatama]": [
			LocationData("Ox-head & Horse-face Defeated", None, lambda state: combat.oxhead_horseface(state), True)
		],
		"Chamber of Extinction [Ankh Lower]": [
			# LocationData('Chamber of Extinction Backup Ankh Jewel Chest', None, lambda state: state.has('Palenque Defeated', player), zone=[6], room=9, screen=0, object_type=0x2c, item_id=19, obtain_value=2),
			LocationData('Palenque Defeated', None, lambda state: state.has('Pochette Key', player) and state.can_reach_region('Chamber of Extinction [Teleport]', player) and state.can_reach_region('Chamber of Extinction [Left Main]', player) and combat.palenque(state) and s.has_ankh_jewel(state, 'Palenque'), True),
			LocationData("Hell Temple Unlocked", None, lambda state: s.hell_temple_requirements(state), True)
		],
		"Twin Labyrinths [Loop]": [
			LocationData("Twin Labyrinths - Ring Puzzle Reward", 2359041, lambda state: s.glitch_raindrop(state) or state.can_reach_region('Twin Labyrinths [Upper Left]', player), file_type='rcd', zones=[7], room=2, screen=0, object_type=0x2f, item_id=47, obtain_flag=0xb0, obtain_value=1)
		],
		"Twin Labyrinths [Jewel]": [
			LocationData("Twin Labyrinths - Ankh Jewel Chest", 2359042, lambda state: state.can_reach_region("Twin Labyrinths [Lower]", player) and state.can_reach_region("Twin Labyrinths [Upper Left]", player) and s.attack_flare_gun(state) and s.attack_chest(state), is_cursable=True, file_type='rcd', zones=[7], room=11, screen=0, object_type=0x2c, item_id=19, obtain_flag=0x94, obtain_value=2)
		],
		"Twin Labyrinths [Katana]": [
			LocationData("Twin Labyrinths - Katana Puzzle Reward", 2359043, lambda state: state.has_all({"Peryton Defeated", "Twin Statue"}, player) or s.glitch_catpause(state), file_type='rcd', zones=[7], room=11, screen=2, object_type=0x2f, item_id=6, obtain_flag=0x82, obtain_value=1)
		],
		"Twin Labyrinths [Poison 1]": [
			LocationData("Twin Labyrinths - Map Chest", 2359044, lambda state: state.has("Twin Poison Cleared", player) and s.attack_forward(state), is_cursable=True, file_type='rcd', zones=[7], room=2, screen=2, object_type=0x2c, item_id=70, original_obtain_flag=0xd8, obtain_flag=0x842, obtain_value=2),
			LocationData("Twin Poison Cleared", None, lambda state: state.has("Twin Statue", player) or (state.can_reach_region("Twin Labyrinths [Poison 2]", player), True) and state.has('Holy Grail', player), True)
		],
		"Twin Labyrinths [Upper Grail]": [
			LocationData("Twin Labyrinths (Front) Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Twin Labyrinths [Lower]": [
			LocationData("Twin Labyrinths - Sacred Orb Chest", 2359045, lambda state: s.attack_chest(state) and (state.has("Zu Defeated", player) or s.glitch_raindrop(state) or (s.glitch_lamp(state) and state.has("Holy Grail", player))), is_cursable=True, file_type='rcd', zones=[7], room=4, screen=0, object_type=0x2c, item_id=69, obtain_flag=0xcd, obtain_value=2),
			LocationData("Zu Defeated", None, lambda state: combat.zu(state), True),
			LocationData("Peryton Defeated", None, lambda state: combat.peryton(state), True),
			LocationData("Twin Labyrinths (Back) Grail Tablet", None, lambda state: s.state_read_grail(state), True),
			LocationData("Lamp Recharge — Twin Labyrinths", None, lambda state: True, True),
			LocationData('Baphomet Defeated', None, lambda state: state.has_all({'Zu Defeated', 'Peryton Defeated'}, player) and combat.baphomet(state) and s.has_ankh_jewel(state, 'Baphomet'), True)
		],
		"Endless Corridor [1F]": [
			LocationData("Endless Corridor - Map Chest", 2359046, lambda state: s.endless_oneway_open(state, worldstate) and s.attack_chest_any(state), is_cursable=True, file_type='rcd', zones=[8], room=1, screen=0, object_type=0x2c, item_id=70, original_obtain_flag=0xd9, obtain_flag=0x843, obtain_value=2),
			LocationData("Endless Corridor Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Endless Corridor [2F]": [
			LocationData("Endless Corridor - Key Sword Puzzle Reward", 2359047, lambda state: s.attack_chest(state), file_type='rcd', zones=[8], room=2, screen=1, object_type=0x2f, item_id=4, obtain_flag=0x80, obtain_value=1)
		],
		"Endless Corridor [3F Upper]": [
			LocationData("Endless Corridor - Twin Statue Chest", 2359048, lambda state: s.attack_chest_any(state) and (state.has("Holy Grail", player) or s.glitch_raindrop(state) or (state.has("Key of Eternity", player) and (s.attack_forward(state) or (state.has("Feather", player) and (s.attack_flare_gun(state) or s.attack_earth_spear(state)))))), is_cursable=True, file_type='rcd', zones=[8], room=3, screen=0, object_type=0x2c, item_id=59, obtain_flag=0xbc, obtain_value=2)
		],
		"Endless Corridor [5F]": [
			LocationData("Backbeard & Tai Sui Defeated", None, lambda state: s.state_literacy(state) and combat.backbeard_tai_sui(state), True),
			LocationData("Lamp Recharge — Endless Corridor", None, lambda state: True, True)
		],
		"Shrine of the Mother [Main]": [
			LocationData("Shrine of the Mother - bounce.exe Chest", 2359049, lambda state: s.attack_shuriken(state) or s.attack_rolling_shuriken(state) or s.attack_earth_spear(state) or s.attack_bomb(state) or s.attack_chakram(state) or s.attack_caltrops(state) or s.attack_pistol(state) or (s.attack_flare_gun(state) and state.has("Removed Shrine Skulls", player)), is_cursable=True, file_type='rcd', zones=[9], room=5, screen=1, object_type=0x2c, item_id=101, obtain_flag=0xf2, obtain_value=2),
			LocationData("Shrine of the Mother - Crystal Skull Chest", 2359050, lambda state: s.attack_chest(state) and state.has_all({worldstate.get_seal_name('Crystal Skull Chest'), "Removed Shrine Skulls"}, player), is_cursable=True, file_type='rcd', zones=[9], room=1, screen=0, object_type=0x2c, item_id=28, obtain_flag=0x9e, obtain_value=2),
			LocationData("Shrine of the Mother - Diary Chest", 2359051, lambda state: s.attack_chest(state) and state.has_all({"Removed Shrine Skulls", "Talisman", "NPC: Xelpud"}, player), is_cursable=True, file_type='rcd', zones=[9], room=2, screen=1, object_type=0x2c, item_id=72, obtain_flag=0x104, obtain_value=2),
			LocationData("Shrine of the Mother - Sacred Orb Chest", 2359052, lambda state: s.attack_chest(state) and state.has_all({worldstate.get_seal_name('Shrine 4 Seals (Origin)'), worldstate.get_seal_name('Shrine 4 Seals (Birth)'), worldstate.get_seal_name('Shrine 4 Seals (Life)'), worldstate.get_seal_name('Shrine 4 Seals (Death)')}, player), is_cursable=True, file_type='rcd', zones=[9], room=1, screen=1, object_type=0x2c, item_id=69, obtain_flag=0xce, obtain_value=2),
			LocationData("Removed Shrine Skulls", None, lambda state: state.has_all({'Dragon Bone', 'yagostr.exe', 'yagomap.exe', 'Map (Shrine of the Mother)'}, player), True)
			# Normal shrine grail tablet doesn't matter, I think - only true shrine
		],
		"Shrine of the Mother [Seal]": [
			LocationData("Shrine of the Mother - Death Seal Chest", 2359053, lambda state: s.attack_chest(state) and ((state.has_all("Feather", player) and s.guardian_count(state) >= 8) or (state.has_any({"Feather", "Grapple Claw"}, player) and (s.glitch_raindrop(state) or state.has("Removed Shrine Skulls", player)))), is_cursable=True, file_type='rcd', zones=[9, 18], room=9, screen=0, object_type=0x2c, item_id=68, obtain_flag=0xc5, obtain_value=2)
		],
		"Shrine of the Mother [Map]": [
			LocationData("Shrine of the Mother - Map Chest", 2359054, lambda state: s.attack_chest_any(state), is_cursable=True, file_type='rcd', zones=[9, 18], room=9, screen=1, object_type=0x2c, item_id=70, original_obtain_flag=0xda, obtain_flag=0x844, obtain_value=2)
		],
		'Gate of Illusion [Eden]': [
			LocationData("Illusion Unlocked", None, lambda state: state.has('Fruit of Eden', player), True)
		],
		"Gate of Illusion [Upper]": [
			LocationData("Gate of Illusion - Cog of the Soul Chest", 2359055, lambda state: s.state_literacy(state) and combat.ba(state) and state.can_reach_region("Gate of Illusion [Pot Room]", player) and state.can_reach_region("Gate of Illusion [Middle]", player) and s.state_lamp(state) and state.has('Feather', player) and s.attack_forward(state), is_cursable=True, file_type='rcd', zones=[10], room=0, screen=1, object_type=0x2c, item_id=24, obtain_flag=0x9a, obtain_value=2),
			LocationData("Mudmen Awakened", None, lambda state: state.has_all({"Feather", "Cog of the Soul"}, player) and s.attack_forward(state), True),
			LocationData("Recited All Mantras", None, lambda state: s.all_mantras(state), True)
		],
		"Gate of Illusion [Middle]": [
			LocationData("Gate of Illusion - Fairy Clothes Chest", 2359056, lambda state: s.state_key_fairy_access(state, False) and s.attack_below(state), is_cursable=True, file_type='rcd', zones=[10], room=6, screen=0, object_type=0x2c, item_id=55, obtain_flag=0xb8, obtain_value=2)
		],
		"Gate of Illusion [Grail]": [
			LocationData("Gate of Illusion - Key of Eternity Chest", 2359057, lambda state: s.attack_chest(state) and state.has("Chi You Defeated", player), is_cursable=True, file_type='rcd', zones=[10], room=2, screen=2, object_type=0x2c, item_id=32, obtain_flag=0xa2, obtain_value=2),
			LocationData("Gate of Illusion Grail Tablet", None, lambda state: s.state_read_grail(state), True),
			LocationData("Chi You Defeated", None, lambda state: (s.glitch_raindrop(state) or (state.can_reach_region("Mausoleum of the Giants", player) and state.has("Mini Doll", player) and s.state_literacy(state))) and (state.has(worldstate.get_seal_name('Chi You Seal'), player) or s.glitch_lamp(state)) and combat.chi_you(state), True)
		],
		"Gate of Illusion [Dracuet]": [
			LocationData("Gate of Illusion - Map Chest", 2359058, lambda state: s.attack_forward(state), is_cursable=True, file_type='rcd', zones=[10], room=7, screen=1, object_type=0x2c, item_id=70, original_obtain_flag=0xdb, obtain_flag=0x845, obtain_value=2)
		],
		"Graveyard of the Giants [West]": [
			LocationData("Graveyard of the Giants - Gauntlet Chest", 2359059, lambda state: s.attack_chest_any(state) and state.has_all({"Feather", worldstate.get_seal_name('Gauntlet Chest')}, player), is_cursable=True, file_type='rcd', zones=[11], room=4, screen=1, object_type=0x2c, item_id=49, obtain_flag=0xb2, obtain_value=2),
			LocationData("Graveyard of the Giants - Map Chest", 2359060, lambda state: s.attack_chest_any(state), is_cursable=True, file_type='rcd', zones=[11], room=4, screen=0, object_type=0x2c, item_id=70, original_obtain_flag=0xdc, obtain_flag=0x846, obtain_value=2),
			LocationData("Graveyard of the Giants - mirai.exe Chest", 2359061, lambda state: s.attack_chest(state) and state.has("Feather", player), is_cursable=True, file_type='rcd', zones=[11], room=5, screen=0, object_type=0x2c, item_id=103, obtain_flag=0xf4, obtain_value=2),
			LocationData("Graveyard of the Giants - Silver Shield Puzzle Reward", 2359062, lambda state: s.attack_below(state), file_type='rcd', zones=[11], room=1, screen=1, object_type=0x2f, item_id=17, obtain_flag=0x8c, obtain_value=1)
		],
		"Graveyard of the Giants [Grail]": [
			LocationData("Graveyard of the Giants Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Graveyard of the Giants [East]": [
			LocationData("Graveyard of the Giants - Bomb Reward", 2359063, lambda state: state.has('Feather', player) and combat.kamaitachi(state), file_type='rcd', zones=[11], room=6, screen=0, object_type=0x2f, item_id=12, obtain_flag=0x87, obtain_value=1),
			LocationData("Graveyard of the Giants - emusic.exe Scan", 2359064, lambda state: state.has("torude.exe", player) and (s.attack_bomb(state) or (s.fairy_point_reachable(state, True, False) and state.has_all({'Bomb', 'Ring'}, player) and state.can_reach_region('Graveyard of the Giants [Grail]', player))), file_type='rcd', zones=[11], room=9, screen=0, object_type=0xc3, item_id=94, obtain_flag=0xeb, obtain_value=1),
			LocationData("Lamp Recharge — Graveyard of the Giants", None, lambda state: True, True)
		],
		"Temple of Moonlight [Upper]": [
			LocationData("Temple of Moonlight - Axe Puzzle Reward", 2359065, lambda state: (s.state_mobility(state) and s.attack_forward(state)) or (state.has('Grapple Claw', player) and (s.attack_shuriken(state) or s.attack_rolling_shuriken(state))), file_type='rcd', zones=[12], room=3, screen=0, object_type=0x2f, item_id=5, obtain_flag=0x81, obtain_value=1),
			LocationData("Temple of Moonlight - Fruit of Eden Chest", 2359066, lambda state: s.attack_chest_any(state) and state.has("Hand Scanner", player) and state.can_reach_region("Temple of Moonlight [Lower]", player) and state.can_reach_region("Temple of Moonlight [Grapple]", player) and state.can_reach_region("Temple of Moonlight [Southeast]", player), is_cursable=True, file_type='rcd', zones=[12], room=2, screen=0, object_type=0x2c, item_id=58, obtain_flag=0xbb, obtain_value=2),
			LocationData("Lamp Recharge — Temple of Moonlight", None, lambda state: True, True)
		],
		"Temple of Moonlight [Grail]": [
			LocationData("Temple of Moonlight Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Temple of Moonlight [Grapple]": [
			LocationData("Temple of Moonlight - Grapple Claw Chest", 2359067, lambda state: s.attack_chest(state), is_cursable=True, file_type='rcd', zones=[12], room=0, screen=0, object_type=0x2c, item_id=44, obtain_flag=0xad, obtain_value=2)
		],
		"Temple of Moonlight [Map]": [
			LocationData("Temple of Moonlight - Map Chest", 2359068, lambda state: s.attack_chest_any(state), is_cursable=True, file_type='rcd', zones=[12], room=1, screen=1, object_type=0x2c, item_id=70, original_obtain_flag=0xdd, obtain_flag=0x847, obtain_value=2)
		],
		"Temple of Moonlight [Pyramid]": [
			# Not cursable because it's not a real chest
			LocationData("Temple of Moonlight - Philosopher's Ocarina Chest", 2359069, lambda state: state.has("Maternity Statue", player) and (state.has("Feather", player) or s.glitch_raindrop(state)), file_type='rcd', zones=[12], room=5, screen=0, object_type=0x2f, item_id=52, obtain_flag=0xb5, obtain_value=2)
		],
		"Temple of Moonlight [Southeast]": [
			LocationData("Temple of Moonlight - Serpent Staff Chest", 2359070, lambda state: s.attack_chest(state) and state.has("Book of the Dead", player) and combat.anubis(state), is_cursable=True, file_type='rcd', zones=[12], room=10, screen=0, object_type=0x2c, item_id=33, obtain_flag=0xa3, obtain_value=2),
		],
		"Tower of the Goddess [Lower]": [
			LocationData("Tower of the Goddess - Eye of Truth Chest", 2359071, lambda state: s.attack_chest_any(state) and state.can_reach_region("Tower of the Goddess [Lamp]", player) and state.has("Flooded Tower of the Goddess", player), is_cursable=True, file_type='rcd', zones=[13], room=3, screen=1, object_type=0x2c, item_id=46, obtain_flag=0xaf, obtain_value=2),
			LocationData("Tower of the Goddess - Flail Whip Puzzle Reward", 2359072, lambda state: (s.state_literacy(state) or s.glitch_catpause(state)) and (s.glitch_lamp(state) or state.has('NPC: Philosopher Samaranta', player)), file_type='rcd', zones=[13], room=5, screen=0, object_type=0x2f, item_id=2, obtain_flag=0x7e, obtain_value=1),
			LocationData("Tower of the Goddess - Map Chest", 2359073, lambda state: s.attack_forward(state), is_cursable=True, file_type='rcd', zones=[13], room=1, screen=1, object_type=0x2c, item_id=70, original_obtain_flag=0xde, obtain_flag=0x848, obtain_value=2),
			LocationData("Flooded Tower of the Goddess", None, lambda state: state.has("Flooded Spring in the Sky", player) and s.state_literacy(state) and (s.attack_caltrops(state) or s.attack_earth_spear(state) or s.attack_bomb(state) or state.has_any({"Knife", "Katana"}, player)) and (state.has_any({"Holy Grail", "Scalesphere"}, player) or s.get_health_count(state) >= 1), True)
		],
		"Tower of the Goddess [Grail]": [
			LocationData("Tower of the Goddess - Plane Model Chest", 2359074, lambda state: state.has_all({'Eye of Truth', 'Flooded Tower of the Goddess'}, player) and combat.vimana(state) and (s.attack_chest(state) or (s.attack_flare_gun(state) and state.has("Feather", player))) and state.can_reach_region("Tower of the Goddess [Spaulder]", player) and state.can_reach_region("Tower of the Goddess [Lower]", player), is_cursable=True, file_type='rcd', zones=[13], room=6, screen=0, object_type=0x2c, item_id=51, obtain_flag=0xb4, obtain_value=2),
			LocationData("Tower of the Goddess - Spaulder Chest", 2359075, lambda state: s.attack_forward(state) and s.state_key_fairy_access(state, False) and (s.state_backside_warp(state) or state.has_all({"Feather", "Hermes' Boots"}, player)), is_cursable=True, file_type='rcd', zones=[13], room=7, screen=0, object_type=0x2c, item_id=62, obtain_flag=0xbf, obtain_value=2),
			LocationData("Tower of the Goddess Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Tower of the Goddess [Lamp]": [
			LocationData("Lamp Recharge — Tower of the Goddess", None, lambda state: True, True)
		],
		"Tower of Ruin [Southeast]": [
			LocationData("Tower of Ruin - Sacred Orb Chest", 2359076, lambda state: s.attack_chest_any(state), is_cursable=True, file_type='rcd', zones=[14], room=0, screen=2, object_type=0x2c, item_id=69, obtain_flag=0xcf, obtain_value=2)
		],
		"Tower of Ruin [Southwest]": [
			LocationData("Tower of Ruin - Ankh Jewel Chest", 2359077, lambda state: (state.has("Feather", player) or state.can_reach_region("Tower of Ruin [Grail]", player)) and (s.attack_below(state) or s.attack_rolling_shuriken(state) or s.attack_bomb(state) or s.attack_caltrops(state) or (s.attack_earth_spear(state) and s.attack_forward(state)) or ((s.glitch_raindrop(state) or s.glitch_catpause(state)) and (s.attack_forward(state) or s.attack_vertical(state)))), is_cursable=True, file_type='rcd', zones=[14], room=1, screen=1, object_type=0x2c, item_id=19, obtain_flag=0x92, obtain_value=2),
			LocationData("Tower of Ruin - Earth Spear Puzzle Reward", 2359078, lambda state: state.has("Feather", player) or s.glitch_catpause(state), file_type='rcd', zones=[14], room=0, screen=0, object_type=0x2f, item_id=10, obtain_flag=0x85, obtain_value=1),
			LocationData("Thunderbird Defeated", None, lambda state: combat.thunderbird(state), True)
		],
		"Tower of Ruin [La-Mulanese]": [
			LocationData("Medicine Statue Open", None, lambda state: s.state_lamp(state) and s.attack_chest(state), True)
		],
		"Tower of Ruin [Grail]": [
			LocationData("Tower of Ruin Grail Tablet", None, lambda state: s.state_read_grail(state), True),
			LocationData("Lamp Recharge — Tower of Ruin", None, lambda state: True, True)
		],
		"Tower of Ruin [Illusion]": [
			LocationData("Tower of Ruin - Map Chest", 2359079, lambda state: s.attack_forward(state), is_cursable=True, file_type='rcd', zones=[14], room=5, screen=1, object_type=0x2c, item_id=70, original_obtain_flag=0xdf, obtain_flag=0x849, obtain_value=2)
		],
		"Tower of Ruin [Top]": [
			LocationData("Tower of Ruin - Djed Pillar Chest", 2359080, lambda state: s.nuwa_access(state, worldstate) and combat.nuwa(state) and s.attack_chest(state), is_cursable=True, file_type='rcd', zones=[14], room=8, screen=0, object_type=0x2c, item_id=21, obtain_flag=0x97, obtain_value=2)
		],
		"Tower of Ruin [Medicine]": [
			LocationData("Medicine of the Mind", None, lambda state: state.has_all({'Medicine Statue Open', 'Life and Death Mantras', 'mantra.exe', 'Djed Pillar', 'Vessel'}, player) and state.can_reach_region('Tower of Ruin [Spirits]', player), True)
		],
		"Chamber of Birth [Northeast]": [
			LocationData("Chamber of Birth - Perfume Chest", 2359081, lambda state: state.has("Mudmen Awakened", player) and s.attack_chest_any(state), is_cursable=True, file_type='rcd', zones=[15], room=2, screen=0, object_type=0x2c, item_id=61, obtain_flag=0xbe, obtain_value=2),
			LocationData("Chamber of Birth - Vessel Chest", 2359082, lambda state: state.has("Angel Shield", player) and s.attack_chest(state), is_cursable=True, file_type='rcd', zones=[15], room=1, screen=1, object_type=0x2c, item_id=29, obtain_flag=0x9f, obtain_value=2)
		],
		"Chamber of Birth [Southeast]": [
			LocationData("Chamber of Birth - Woman Statue Chest", 2359083, lambda state: s.attack_chest_any(state) and state.has_any({"Feather", "Grapple Claw"}, player), is_cursable=True, file_type='rcd', zones=[15], room=4, screen=0, object_type=0x2c, item_id=31, obtain_flag=0xa1, obtain_value=2)
		],
		"Chamber of Birth [West]": [
			LocationData("Chamber of Birth - Map Chest", 2359084, lambda state: state.has_any({"Woman Statue", "Maternity Statue"}, player) and s.attack_chest(state), is_cursable=True, file_type='rcd', zones=[16], room=1, screen=0, object_type=0x2c, item_id=70, original_obtain_flag=0xe0, obtain_flag=0x84a, obtain_value=2)
		],
		"Chamber of Birth [Grail]": [
			LocationData("Chamber of Birth - Dimensional Key Chest", 2359085, lambda state: state.has_all({"Maternity Statue", "Dragon Bone", "Key of Eternity"}, player) and s.attack_forward(state) and (state.has("Cog of the Soul", player) or s.glitch_raindrop(state)), is_cursable=True, file_type='rcd', zones=[16], room=2, screen=1, object_type=0x2c, item_id=63, obtain_flag=0xc0, obtain_value=2),
			LocationData("Chamber of Birth Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Chamber of Birth [Skanda]": [
			LocationData("Chamber of Birth - Pochette Key Chest", 2359086, lambda state: state.has("Skanda Defeated", player) and s.attack_chest_any(state), is_cursable=True, file_type='rcd', zones=[16], room=3, screen=1, object_type=0x2c, item_id=26, obtain_flag=0x9c, obtain_value=2),
			LocationData("Skanda Defeated", None, lambda state: state.can_reach_region("Chamber of Birth [Dance]", player) and state.has("Mudmen Awakened", player) and combat.skanda(state), True)
		],
		"Dimensional Corridor [Grail]": [
			LocationData("Dimensional Corridor - Map Chest", 2359087, lambda state: s.attack_chest(state) and state.has("Feather", player), is_cursable=True, file_type='rcd', zones=[17], room=0, screen=1, object_type=0x2c, item_id=70, original_obtain_flag=0xe1, obtain_flag=0x84b, obtain_value=2),
			LocationData("Dimensional Corridor Grail Tablet", None, lambda state: s.state_read_grail(state), True),
			LocationData("Life and Death Mantras", None, lambda state: state.has_all({'NPC: Philosopher Fobos', 'Left Side Children Defeated', 'Hand Scanner', 'reader.exe'}, player) and s.state_ancient_lamulanese(state), True)
		],
		"Dimensional Corridor [Upper]": [
			LocationData("Dimensional Corridor - Angel Shield Puzzle Reward", 2359088, lambda state: state.has("Angel Shield Children Defeated", player) and state.has_any({"Feather", "Left Side Children Defeated"}, player) and (state.has("Dimensional Key", player) or s.glitch_catpause(state)), file_type='rcd', zones=[17], room=8, screen=0, object_type=0x2f, item_id=18, obtain_flag=0x8d, obtain_value=2),
			LocationData("Dimensional Corridor - Sacred Orb Chest", 2359089, lambda state: state.has_all({"Feather", "Dimensional Key", worldstate.get_seal_name("Dimensional Sacred Orb Chest"), "Angel Shield Children Defeated"}, player) and s.attack_chest(state), is_cursable=True, file_type='rcd', zones=[17], room=10, screen=0, object_type=0x2c, item_id=69, obtain_flag=0xd0, obtain_value=2),
			LocationData("Dimensional Corridor - Ankh Jewel Chest", 2359090, lambda state: state.has("Mushussu Defeated", player) and s.attack_chest(state), is_cursable=True, file_type='rcd', zones=[17], room=6, screen=0, object_type=0x2c, item_id=19, obtain_flag=0x95, obtain_value=2),
			LocationData("Dimensional Corridor - Magatama Jewel Chest", 2359091, lambda state: state.has('Tiamat Defeated', player) and s.attack_chest(state), is_cursable=True, file_type='rcd', zones=[17], room=9, screen=0, object_type=0x2c, item_id=23, obtain_flag=0x99, obtain_value=2),
			LocationData("Dimensional Corridor - beolamu.exe Scan", 2359124, lambda state: state.has_all({'Angel Shield Children Defeated', 'torude.exe'}, player), file_type='rcd', zones=[17], room=8, screen=1, object_type=0xc3, item_id=95, obtain_flag=0xec, obtain_value=1),
			LocationData("Left Side Children Defeated", None, lambda state: combat.left_side_children(state), True),
			LocationData("Right Side Children Defeated", None, lambda state: combat.right_side_children(state), True),
			LocationData("Angel Shield Children Defeated", None, lambda state: combat.angel_shield_children(state), True),
			LocationData("Ushumgallu Defeated", None, lambda state: state.has("Dimensional Key", player) and combat.ushumgallu(state), True),
			LocationData("Mushussu Defeated", None, lambda state: state.has_all({"Dimensional Key", "Angel Shield Children Defeated"}, player) and (state.has_all({"Left Side Children Defeated", "Right Side Children Defeated"}, player) or s.glitch_raindrop(state)) and combat.mushussu(state), True),
			LocationData('Tiamat Defeated', None, lambda state: state.has_all({'Dimensional Key', 'Left Side Children Defeated', 'Right Side Children Defeated', 'Angel Shield Children Defeated', 'Ushumgallu Defeated', 'Mushussu Defeated'}, player) and combat.tiamat(state) and s.has_ankh_jewel(state, 'Tiamat'), True)
		],
		"Gate of Time [Surface]": [
			LocationData("Gate of Time (Surface) - lamulana.exe Chest", 2359092, lambda state: s.attack_forward(state) or s.attack_flare_gun(state), is_cursable=True, file_type='rcd', zones=[21], room=0, screen=1, object_type=0x2c, item_id=104, obtain_flag=0xf5, obtain_value=2)
		],
		"True Shrine of the Mother": [
			LocationData("All Grail Tablets Read", None, lambda state: state.has_all({"Surface Grail Tablet", "Gate of Guidance Grail Tablet", "Mausoleum of the Giants Grail Tablet", "Temple of the Sun Grail Tablet", "Spring in the Sky Grail Tablet", "Inferno Cavern Grail Tablet", "Chamber of Extinction Grail Tablet", "Twin Labyrinths (Front) Grail Tablet", "Endless Corridor Grail Tablet", "Gate of Illusion Grail Tablet", "Graveyard of the Giants Grail Tablet", "Temple of Moonlight Grail Tablet", "Tower of the Goddess Grail Tablet", "Tower of Ruin Grail Tablet", "Chamber of Birth Grail Tablet", "Twin Labyrinths (Back) Grail Tablet", "Dimensional Corridor Grail Tablet"}, player), True),
			LocationData("Mother Defeated", None, lambda state: state.has_all({'All Grail Tablets Read', 'Fairies Unlocked', 'NPC: Philosopher Fobos', 'Medicine of the Mind', worldstate.get_seal_name('Mother (Origin)'), worldstate.get_seal_name('Mother (Birth)'), worldstate.get_seal_name('Mother (Life)'), worldstate.get_seal_name('Mother (Death)')}, player) and ((alt_mother_ankh and s.has_ankh_jewel(state, 'Mother')) or (not alt_mother_ankh and s.attack_empowered_key_sword(state))) and combat.mother(state), True)
		]
	}

	# if include_coin_chests:
	# 	locations['Surface [Main]'].extend([
	# 		LocationData('Surface - Waterfall Coin Chest', 2359093, lambda state: s.attack_chest(state), is_cursable=True, file_type='rcd', zones=[1,22], room=6, screen=0, object_type=0x2c, item_id=-10),
	# 		LocationData('Surface - Seal Coin Chest', 2359094, lambda state: s.attack_chest(state) and state.has(worldstate.get_seal_name('Surface Coin Chest Seal'), player), is_cursable=True, file_type='rcd', zones=[1,22], room=1, screen=0, object_type=0x2c, item_id=-10)
	# 	])
	# 	locations['Surface [Ruin Path Upper]'] = [
	# 		LocationData('Surface - Underground Path Coin Chest', 2359095, lambda state: s.attack_bomb(state), is_cursable=True, file_type='rcd', zones=[1,22], room=5, screen=1, object_type=0x2c, item_id=-10)
	# 	]
	#	locations['Gate of Guidance'].extend([
	#		LocationData('Gate of Guidance - Left Coin Chest', 2359125, lambda state: s.attack_chest_any(state), is_cursable=True, file_type='rcd', zones=[0], room=2, screen=1, object_type=0x2c, item_id=-10),
	#		LocationData('Gate of Guidance - Right Coin Chest', 2359126, lambda state: s.attack_chest_any(state), is_cursable=True, file_type='rcd', zones=[0], room=2, screen=1, object_type=0x2c, item_id=-10),
	#		LocationData('Gate of Guidance - Trapdoor Coin Chest', 2359127, lambda state: s.attack_chest(state), is_cursable=True, file_type='rcd', zones=[0], room=6, screen=0, object_type=0x2c, item_id=-10)
	#	])
	# 	locations['Mausoleum of the Giants'].extend([
	# 		LocationData('Mausoleum of the Giants - Top Entrance Coin Chest', 2359096, lambda state: s.attack_shuriken(state) or s.attack_chakram(state) or s.attack_pistol(state) or (s.attack_main(state) and state.has('Feather', player)), is_cursable=True, file_type='rcd', zones=[2], room=0, screen=1, object_type=0x2c, item_id=-10)
	# 	])
	# 	locations['Temple of the Sun [Main]'].extend([
	# 		#weapon fairy logic
	# 		LocationData('Temple of the Sun - Pyramid Coin Chest', 2359097, lambda state: s.attack_bomb(state) or (state.has('Bomb', player) and s.fairy_point_reachable(state, True, True)), is_cursable=True, file_type='rcd', zones=[3], room=4, screen=4, object_type=0x2c, item_id=-10)
	# 	])
	# 	locations['Spring in the Sky [Main]'].extend([
	# 		LocationData('Spring in the Sky - Lower Path Coin Chest', 2359098, lambda state: s.attack_forward(state) or (s.attack_vertical(state) and (state.has('Holy Grail', player) or s.state_water_swim(state, 3))), is_cursable=True, file_type='rcd', zones=[4], room=8, screen=0, object_type=0x2c, item_id=-10)
	# 	])
	# 	locations['Inferno Cavern [Main]'].extend([
	# 		LocationData('Inferno Cavern - Lava Coin Chest', 2359099, lambda state: s.attack_chest(state) and (s.state_lava_swim(state, 2) if state.has('Holy Grail', player) else s.state_lava_swim(state, 4)), is_cursable=True, file_type='rcd', zones=[5], room=1, screen=1, object_type=0x2c, item_id=-10)
	# 	])
	# 	locations['Inferno Cavern [Spikes]'] = [
	# 		LocationData('Inferno Cavern - Spikes Coin Chest', 2359100, lambda state: s.attack_main(state) or s.attack_shuriken(state) or s.attack_rolling_shuriken(state) or s.attack_earth_spear(state) or s.attack_flare_gun(state) or s.attack_bomb(state) or s.attack_caltrops(state) or s.attack_chakram(state), is_cursable=True, file_type='rcd', zones=[5], room=9, screen=1, object_type=0x2c, item_id=-10)
	# 	]
	# 	locations['Chamber of Extinction [Left Main]'].extend([
	# 		LocationData('Chamber of Extinction - Upper Path Coin Chest', 2359101, lambda state: s.attack_chest(state), is_cursable=True, file_type='rcd', zones=[6], room=3, screen=0, object_type=0x2c, item_id=-10)
	# 	])
	# 	locations['Twin Labyrinths [Lower]'].extend([
	# 		LocationData('Twin Labyrinths - Witches Coin Chest', 2359102, lambda state: state.has('Peryton Defeated', player) and s.attack_forward(state), is_cursable=True, file_type='rcd', zones=[7], room=13, screen=1, object_type=0x2c, item_id=-10),
	# 		LocationData('Twin Labyrinths - Lower Coin Chest', 2359103, lambda state: s.attack_chest_any(state), is_cursable=True, file_type='rcd', zones=[7], room=5, screen=1, object_type=0x2c, item_id=-10)
	# 	])
	# 	locations['Endless Corridor [3F Upper]'].extend([
	# 		LocationData('Endless Corridor - Third Corridor Coin Chest', 2359104, lambda state: s.attack_main(state), is_cursable=True, file_type='rcd', zones=[8], room=3, screen=2, object_type=0x2c, item_id=-10)
	# 	]),
	# 	locations['Shrine of the Mother [Main]'].extend([
	# 		LocationData('Shrine of the Mother - Katana Coin Chest', 2359105, lambda state: state.has('Katana', player), is_cursable=True, file_type='rcd', zones=[9,18], room=6, screen=0, object_type=0x2c, item_id=-10)
	# 	])
	# 	locations['Gate of Illusion [Middle]'].extend([
	# 		LocationData('Gate of Illusion - Katana Coin Chest', 2359106, lambda state: state.has('Katana', player), is_cursable=True, file_type='rcd', zones=[10], room=6, screen=0, object_type=0x2c, item_id=-4)
	# 	])
	# 	locations['Gate of Illusion [Lower]'] = [
	# 		LocationData('Gate of Illusion - Spikes Coin Chest', 2359107, lambda state: s.attack_chest(state), is_cursable=True, file_type='rcd', zones=[10], room=9, screen=0, object_type=0x2c, item_id=-10)
	# 	]
	# 	locations['Graveyard of the Giants [West]'].extend([
	# 		LocationData('Graveyard of the Giants - Droppable Ice Blocks Coin Chest', 2359108, lambda state: state.has('Feather', player) and s.attack_forward(state), is_cursable=True, file_type='rcd', zones=[11], room=0, screen=2, object_type=0x2c, item_id=-10)
	# 	])
	# 	locations['Temple of Moonlight [Eden]'] = [
	# 		LocationData('Temple of Moonlight - Subweapon Coin Chest', 2359109, lambda state: s.attack_bomb(state) or (s.attack_caltrops(state) and state.has_any({'Feather', 'Ring'}, player)) or (state.has('Feather', player) and (s.attack_shuriken(state) or s.attack_rolling_shuriken(state) or s.attack_chakram(state) or s.attack_pistol(state))), is_cursable=True, file_type='rcd', zones=[12], room=1, screen=0, object_type=0x2c, item_id=-10)
	# 	]
	# 	locations['Tower of the Goddess [Grail]'].extend([
	# 		LocationData('Tower of the Goddess - Shield Statue Coin Chest', 2359110, lambda state: state.has_any({'Katana', 'Knife'}, player) or s.attack_caltrops(state) or s.attack_bomb(state) or (s.attack_forward(state) and (s.attack_earth_spear(state) or s.glitch_catpause(state))), is_cursable=True, file_type='rcd', zones=[13], room=7, screen=2, object_type=0x2c, item_id=-10)
	# 	])
	# 	locations['Tower of the Goddess [Lower]'].extend([
	# 		LocationData('Tower of the Goddess - Fairy Spot Coin Chest', 2359111, lambda state: s.attack_chest_any(state), is_cursable=True, file_type='rcd', zones=[13], room=2, screen=0, object_type=0x2c, item_id=-10)
	# 	])
	# 	locations['Tower of Ruin [Spirits]'] = [
	# 		LocationData('Tower of Ruin - Spirits Coin Chest', 2359112, lambda state: s.attack_shuriken(state) or s.attack_rolling_shuriken(state) or s.attack_chakram(state) or s.attack_bomb(state) or s.attack_chakram(state) or s.attack_pistol(state), is_cursable=True, file_type='rcd', zones=[14], room=6, screen=1, object_type=0x2c, item_id=-10)
	# 	]
	# 	locations['Chamber of Birth [Northeast]'].extend([
	# 		LocationData('Chamber of Birth - Ninja Coin Chest', 2359113, lambda state: s.attack_main(state) or s.attack_shuriken(state) or s.attack_bomb(state) or s.attack_chakram(state) or s.attack_caltrops(state) or s.attack_pistol(state) or (s.state_lamp(state) and (s.attack_earth_spear(state) or s.attack_flare_gun(state) or s.attack_rolling_shuriken(state))), is_cursable=True, file_type='rcd', zones=[15], room=1, screen=0, object_type=0x2c, item_id=-10)
	# 	])
	# 	locations['Chamber of Birth [Southeast]'].extend([
	# 		LocationData('Chamber of Birth - Spike Trap Coin Chest', 2359114, lambda state: s.attack_forward(state), is_cursable=True, file_type='rcd', zones=[15], room=3, screen=1, object_type=0x2c, item_id=-10)
	# 	])
	# 	locations['Chamber of Birth [Dance]'] = [
	# 		LocationData('Chamber of Birth - Dance of Life Coin Chest', 2359115, lambda state: s.attack_forward(state) or s.attack_flare_gun(state), is_cursable=True, file_type='rcd', zones=[16], room=4, screen=0, object_type=0x2c, item_id=-10)
	# 	]
	# 	locations['Dimensional Corridor [Grail]'].extend([
	# 		LocationData('Dimensional Corridor - Grail Tablet Coin Chest', 2359116, lambda state: s.attack_forward(state) or s.attack_flare_gun(state), is_cursable=True, file_type='rcd', zones=[17], room=0, screen=0, object_type=0x2c, item_id=-10)
	# 	])

	# 	if include_escape_chest:
	# 		locations['Twin Labyrinths [Upper Left]'] = [
	# 			LocationData('Twin Labyrinths - Escape Coin Chest', 2359117, lambda state: state.has('Mother Defeated', player) and s.attack_chest(state), is_cursable=True, file_type='rcd', zones=[7], room=2, screen=0, object_type=0x2c, item_id=-10)
	# 		]

	# if include_trap_items:
	# 	locations['Inferno Cavern [Main]'].append(
	# 		LocationData('Inferno Cavern - Fake Orb', 2359118)
	# 	)
	# 	locations['Twin Labyrinths [Loop]'].append(
	# 		LocationData('Twin Labyrinths - Fake Ankh Jewel', 2359119)
	# 	)
	# 	locations['Gate of Illusion [Dracuet]'].append(
	# 		LocationData('Gate of Illusion - Exploding Chest', 2359120, lambda state: s.attack_chest(state), is_cursable=True)
	# 	)
	# 	locations['Graveyard of the Giants [West]'].append(
	# 		LocationData('Graveyard of the Giants - Trap Chest', 2359121, lambda state: s.attack_chest(state), is_cursable=True, file_type='rcd', zones=[11], room=4, screen=3, object_type=0x2c)
	# 	)

	# if include_hell_temple_reward:
	# 	locations['Hell Temple [Dracuet]'] = [
	# 		LocationData("Hell Temple - Final Reward", 2359122, file_type='dat', cards=[1012], item_id=74)
	# 	]

	return locations
