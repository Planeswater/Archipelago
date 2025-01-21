from typing import TYPE_CHECKING, Callable, NamedTuple
from BaseClasses import CollectionState
from .Options import StartingLocation
from .Locations import LocationData
from .LogicShortcuts import LaMulanaLogicShortcuts

if TYPE_CHECKING:
	from . import LaMulanaWorld


class LaMulanaNPCDoor(NamedTuple):
	checks: list[LocationData] = []
	logic: Callable[[CollectionState], bool] | None = None


def get_npc_checks(world: "LaMulanaWorld | None") -> dict[str, list[LocationData]]:
	if world:
		player = world.player
		s = LaMulanaLogicShortcuts(world)
	include_dracuet = not world or world.options.RandomizeDracuetsShop
	return {
		# 'Starting Shop': [
		# 	LocationData('Starting Shop Item 1', 2359200, is_shop=True),
		# 	LocationData('Starting Shop Item 2', 2359201, is_shop=True),
		# 	LocationData('Starting Shop Item 3', 2359202, is_shop=True)
		# ],
		'Elder Xelpud': [
			LocationData('Xelpud xmailer.exe Gift', 2359203, file_type='dat', cards=[364], item_id=86, obtain_flag=0xe3, obtain_value=1),
			LocationData('Xelpud Mulana Talisman Gift', 2359204, lambda state: state.has('Diary', player), file_type='dat', cards=[371], item_id=73, obtain_flag=0x105, obtain_value=1),
			LocationData('NPC: Xelpud', None, lambda state: True, True),
		],
		'Nebur': [
			LocationData('Nebur Shop Item 1', 2359205, is_shop=True, file_type='dat', cards=[34], slot=0, item_id=105, obtain_flag=0x808, obtain_value=2),
			LocationData('Nebur Shop Item 2', 2359206, is_shop=True, file_type='dat', cards=[34, 490], slot=1, item_id=85, obtain_flag=0xe2, obtain_value=2),
			LocationData('Nebur Shop Item 3', 2359207, is_shop=True, file_type='dat', cards=[34, 490], slot=2, item_id=87, obtain_flag=0xe4, obtain_value=2),
			# Must be an item, so doesn't get marked as shop
			LocationData('Nebur Shop Item - 4 Guardians', 2359208, lambda state: s.guardian_count(state) >= 4, file_type='dat', cards=[490], slot=0, item_id=76, obtain_flag=0x2e6, obtain_value=2)
		],
		'Sidro': [
			LocationData('Sidro Shop Item 1', 2359209, is_shop=True, file_type='dat', cards=[35], slot=0, item_id=16, obtain_flag=0x809, obtain_value=2),
			LocationData('Sidro Shop Item 2', 2359210, is_shop=True, file_type='dat', cards=[35], slot=1, item_id=36, obtain_flag=0xa5, obtain_value=2),
			LocationData('Sidro Shop Item 3', 2359211, is_shop=True, file_type='dat', cards=[35], slot=2, item_id=15, obtain_flag=0x8a, obtain_value=2)
		],
		'Modro': [
			LocationData('Modro Shop Item 1', 2359212, is_shop=True, file_type='dat', cards=[36], slot=0, item_id=20, obtain_flag=0x96, obtain_value=2),
			LocationData('Modro Shop Item 2', 2359213, is_shop=True, file_type='dat', cards=[36], slot=1, item_id=114, obtain_flag=0x80a, obtain_value=2),
			LocationData('Modro Shop Item 3', 2359214, is_shop=True, file_type='dat', cards=[36], slot=2, item_id=107, obtain_flag=0x80b, obtain_value=2)
		],
		'Former Mekuri Master': [
			LocationData('Former Mekuri Master mekuri.exe Gift', 2359215, file_type='dat', cards=[37], item_id=100, obtain_flag=0xf1, obtain_value=2)
		],
		'Penadvent of Ghost': [
			LocationData('Penadvent of Ghost Shop Item 1', 2359216, is_shop=True, file_type='dat', cards=[39], slot=0, item_id=107, obtain_flag=0x80c, obtain_value=2),
			LocationData('Penadvent of Ghost Shop Item 2', 2359217, is_shop=True, file_type='dat', cards=[39], slot=1, item_id=92, obtain_flag=0xe9, obtain_value=2),
			LocationData('Penadvent of Ghost Shop Item 3', 2359218, is_shop=True, file_type='dat', cards=[39], slot=2, item_id=105, obtain_flag=0x80d, obtain_value=2)
		],
		'Greedy Charlie': [
			LocationData('Greedy Charlie Shop Item 1', 2359219, is_shop=True, file_type='dat', cards=[74], slot=0, item_id=57, obtain_flag=0xba, obtain_value=2),
			LocationData('Greedy Charlie Shop Item 2', 2359220, is_shop=True, file_type='dat', cards=[74], slot=1, item_id=108, obtain_flag=0x80e, obtain_value=2),
			LocationData('Greedy Charlie Shop Item 3', 2359221, is_shop=True, file_type='dat', cards=[74], slot=2, item_id=105, obtain_flag=0x80f, obtain_value=2)
		],
		'Mulbruk': [
			LocationData('Mulbruk Book of the Dead Gift', 2359222, lambda state: state.can_reach_region('Temple of Moonlight [Southeast]', player), file_type='dat', cards=[397], item_id=54, obtain_flag=0x32a, obtain_value=2),
			LocationData('NPC: Mulbruk', None, lambda state: True, True),
		],
		'Shalom III': [
			LocationData('Shalom III Shop Item 1', 2359223, is_shop=True, file_type='dat', cards=[100], slot=0, item_id=108, obtain_flag=0x810, obtain_value=2),
			LocationData('Shalom III Shop Item 2', 2359224, is_shop=True, file_type='dat', cards=[100], slot=1, item_id=109, obtain_flag=0x811, obtain_value=2),
			LocationData('Shalom III Shop Item 3', 2359225, is_shop=True, file_type='dat', cards=[100], slot=2, item_id=89, obtain_flag=0xe6, obtain_value=2)
		],
		'Usas VI': [
			LocationData('Usas VI Shop Item 1', 2359226, is_shop=True, file_type='dat', cards=[102], slot=0, item_id=37, obtain_flag=0xa6, obtain_value=2),
			LocationData('Usas VI Shop Item 2', 2359227, is_shop=True, file_type='dat', cards=[102], slot=1, item_id=110, obtain_flag=0x812, obtain_value=2),
			LocationData('Usas VI Shop Item 3', 2359228, is_shop=True, file_type='dat', cards=[102], slot=2, item_id=105, obtain_flag=0x813, obtain_value=2)
		],
		'Kingvalley I': [
			LocationData('Kingvalley I Shop Item 1', 2359229, is_shop=True, file_type='dat', cards=[103], slot=0, item_id=114, obtain_flag=0x814, obtain_value=2),
			LocationData('Kingvalley I Shop Item 2', 2359230, is_shop=True, file_type='dat', cards=[103], slot=1, item_id=111, obtain_flag=0x815, obtain_value=2),
			LocationData('Kingvalley I Shop Item 3', 2359231, is_shop=True, file_type='dat', cards=[103], slot=2, item_id=107, obtain_flag=0x816, obtain_value=2)
		],
		'Philosopher Giltoriyo': [
			LocationData('NPC: Philosopher Giltoriyo', None, lambda state: state.has("Philosopher's Ocarina", player), True)
		],
		'Mr. Fishman (Original)': [
			LocationData('Mr. Fishman (Original) Shop Item 1', 2359232, is_shop=True, file_type='dat', cards=[132], slot=0, item_id=105, obtain_flag=0x817, obtain_value=2),
			LocationData('Mr. Fishman (Original) Shop Item 2', 2359233, is_shop=True, file_type='dat', cards=[132], slot=1, item_id=107, obtain_flag=0x818, obtain_value=2),
			LocationData('Mr. Fishman (Original) Shop Item 3', 2359234, is_shop=True, file_type='dat', cards=[132], slot=2, item_id=113, obtain_flag=0x819, obtain_value=2)
		],
		'Mr. Fishman (Alt)': [
			LocationData('Mr. Fishman (Alt) Shop Item 1', 2359235, is_shop=True, file_type='dat', cards=[133], slot=0, item_id=38, obtain_flag=0x84e, obtain_value=2),
			LocationData('Mr. Fishman (Alt) Shop Item 2', 2359236, is_shop=True, file_type='dat', cards=[133], slot=1, item_id=92, obtain_flag=0xe9, obtain_value=2),
			LocationData('Mr. Fishman (Alt) Shop Item 3', 2359237, is_shop=True, file_type='dat', cards=[133], slot=2, item_id=97, obtain_flag=0xee, obtain_value=2)
		],
		'Hot-blooded Nemesistwo': [
			LocationData('Hot-blooded Nemesistwo Shop Item 1', 2359238, is_shop=True, file_type='dat', cards=[470], slot=0, item_id=98, obtain_flag=0xef, obtain_value=2),
			LocationData('Hot-blooded Nemesistwo Shop Item 2', 2359239, is_shop=True, file_type='dat', cards=[470], slot=1, item_id=109, obtain_flag=0x81b, obtain_value=2),
			LocationData('Hot-blooded Nemesistwo Shop Item 3', 2359240, is_shop=True, file_type='dat', cards=[470], slot=2, item_id=105, obtain_flag=0x81c, obtain_value=2)
		],
		'Operator Combaker': [
			LocationData('Operator Combaker Shop Item 1', 2359241, is_shop=True, file_type='dat', cards=[167], slot=0, item_id=109, obtain_flag=0x81d, obtain_value=2),
			LocationData('Operator Combaker Shop Item 2', 2359242, is_shop=True, file_type='dat', cards=[167], slot=1, item_id=110, obtain_flag=0x81e, obtain_value=2),
			LocationData('Operator Combaker Shop Item 3', 2359243, is_shop=True, file_type='dat', cards=[167], slot=2, item_id=112, obtain_flag=0x81f, obtain_value=2)
		],
		'Yiegah Kungfu': [
			LocationData('Yiegah Kungfu Shop Item 1', 2359244, is_shop=True, file_type='dat', cards=[185], slot=0, item_id=43, obtain_flag=0xac, obtain_value=1),
			LocationData('Yiegah Kungfu Shop Item 2', 2359245, is_shop=True, file_type='dat', cards=[185], slot=1, item_id=113, obtain_flag=0x822, obtain_value=1),
			LocationData('Yiegah Kungfu Shop Item 3', 2359246, is_shop=True, file_type='dat', cards=[185], slot=2, item_id=105, obtain_flag=0x823, obtain_value=1),
			LocationData('NPC: Yiegah Kungfu', None, lambda state: True, True)
		],
		'Yiear Kungfu': [
			LocationData('Yiear Kungfu Shop Item 1', 2359247, is_shop=True, file_type='dat', cards=[205], slot=0, item_id=27, obtain_flag=0x9d, obtain_value=2),
			LocationData('Yiear Kungfu Shop Item 2', 2359248, is_shop=True, file_type='dat', cards=[205], slot=1, item_id=109, obtain_flag=0x820, obtain_value=2),
			LocationData('Yiear Kungfu Shop Item 3', 2359249, is_shop=True, file_type='dat', cards=[205], slot=2, item_id=110, obtain_flag=0x821, obtain_value=2)
		],
		'Arrogant Sturdy Snake': [
			LocationData('Arrogant Sturdy Snake Shop Item 1', 2359250, is_shop=True, file_type='dat', cards=[204], slot=0, item_id=60, obtain_flag=0xbd, obtain_value=2),
			LocationData('Arrogant Sturdy Snake Shop Item 2', 2359251, is_shop=True, file_type='dat', cards=[204], slot=1, item_id=111, obtain_flag=0x824, obtain_value=2),
			LocationData('Arrogant Sturdy Snake Shop Item 3', 2359252, is_shop=True, file_type='dat', cards=[204], slot=2, item_id=113, obtain_flag=0x825, obtain_value=2)
		],
		'Arrogant Metagear': [
			LocationData('Arrogant Metagear Shop Item 1', 2359253, is_shop=True, file_type='dat', cards=[187], slot=0, item_id=25, obtain_flag=0x9b, obtain_value=2),
			LocationData('Arrogant Metagear Shop Item 2', 2359254, is_shop=True, file_type='dat', cards=[187], slot=1, item_id=107, obtain_flag=0x826, obtain_value=2),
			LocationData('Arrogant Metagear Shop Item 3', 2359255, is_shop=True, file_type='dat', cards=[187], slot=2, item_id=112, obtain_flag=0x827, obtain_value=2)
		],
		'Fairy Queen': [
			LocationData('Fairies Unlocked', None, lambda state: state.has("Isis' Pendant", player), True)
		],
		'Affected Knimare': [
			LocationData('Affected Knimare Shop Item 1', 2359256, is_shop=True, file_type='dat', cards=[220], slot=0, item_id=111, obtain_flag=0x828, obtain_value=2),
			LocationData('Affected Knimare Shop Item 2', 2359257, is_shop=True, file_type='dat', cards=[220], slot=1, item_id=113, obtain_flag=0x829, obtain_value=2),
			LocationData('Affected Knimare Shop Item 3', 2359258, is_shop=True, file_type='dat', cards=[220], slot=2, item_id=105, obtain_flag=0x82a, obtain_value=2)
		],
		'Mr. Slushfund': [
			LocationData('Mr. Slushfund Pepper Gift', 2359259, file_type='dat', cards=[245], item_id=30, obtain_flag=0x228, obtain_value=1),
			LocationData('Mr. Slushfund Anchor Gift', 2359260, lambda state: state.has('Treasures', player), file_type='dat', cards=[247], item_id=50, obtain_flag=0x228, obtain_value=2)
		],
		'Priest Alest': [
			LocationData('Priest Alest Mini Doll Gift', 2359261, file_type='dat', cards=[249], item_id=22, obtain_flag=0x98, obtain_value=2)
		],
		'Mover Athleland': [
			LocationData('Mover Athleland Shop Item 1', 2359262, is_shop=True, file_type='dat', cards=[244], slot=0, item_id=99, obtain_flag=0xf0, obtain_value=2),
			LocationData('Mover Athleland Shop Item 2', 2359263, is_shop=True, file_type='dat', cards=[244], slot=1, item_id=111, obtain_flag=0x82b, obtain_value=2),
			LocationData('Mover Athleland Shop Item 3', 2359264, is_shop=True, file_type='dat', cards=[244], slot=2, item_id=105, obtain_flag=0x82c, obtain_value=2)
		],
		'Giant Mopiran': [
			LocationData('Giant Mopiran Shop Item 1', 2359265, is_shop=True, file_type='dat', cards=[272], slot=0, item_id=109, obtain_flag=0x82d, obtain_value=2),
			LocationData('Giant Mopiran Shop Item 2', 2359266, is_shop=True, file_type='dat', cards=[272], slot=1, item_id=75, obtain_flag=0x82e, obtain_value=2),
			LocationData('Giant Mopiran Shop Item 3', 2359267, is_shop=True, file_type='dat', cards=[272], slot=2, item_id=105, obtain_flag=0x82f, obtain_value=2)
		],
		'Philosopher Alsedana': [
			LocationData('NPC: Philosopher Alsedana', None, lambda state: state.has("Philosopher's Ocarina", player), True)
		],
		'Kingvalley II': [
			LocationData('Kingvalley II Shop Item 1', 2359268, is_shop=True, file_type='dat', cards=[290], slot=0, item_id=56, obtain_flag=0xb9, obtain_value=2),
			LocationData('Kingvalley II Shop Item 2', 2359269, is_shop=True, file_type='dat', cards=[290], slot=1, item_id=107, obtain_flag=0x830, obtain_value=2),
			LocationData('Kingvalley II Shop Item 3', 2359270, is_shop=True, file_type='dat', cards=[290], slot=2, item_id=114, obtain_flag=0x831, obtain_value=2)
		],
		'Philosopher Samaranta': [
			LocationData('NPC: Philosopher Samaranta', None, lambda state: state.has("Philosopher's Ocarina", player), True)
		],
		'Energetic Belmont': [
			LocationData('Energetic Belmont Shop Item 1', 2359271, is_shop=True, file_type='dat', cards=[303], slot=0, item_id=102, obtain_flag=0xf3, obtain_value=2),
			LocationData('Energetic Belmont Shop Item 2', 2359272, is_shop=True, file_type='dat', cards=[303], slot=1, item_id=113, obtain_flag=0x832, obtain_value=2),
			LocationData('Energetic Belmont Shop Item 3', 2359273, is_shop=True, file_type='dat', cards=[303], slot=2, item_id=105, obtain_flag=0x833, obtain_value=2)
		],
		'Mechanical Efspi': [
			LocationData('Mechanical Efspi Shop Item 1', 2359274, is_shop=True, file_type='dat', cards=[321], slot=0, item_id=91, obtain_flag=0xe8, obtain_value=2),
			LocationData('Mechanical Efspi Shop Item 2', 2359275, is_shop=True, file_type='dat', cards=[321], slot=1, item_id=111, obtain_flag=0x834, obtain_value=2),
			LocationData('Mechanical Efspi Shop Item 3', 2359276, is_shop=True, file_type='dat', cards=[321], slot=2, item_id=110, obtain_flag=0x835, obtain_value=2)
		],
		'Mudman Qubert': [
			LocationData('Mudman Qubert Shop Item 1', 2359277, is_shop=True, file_type='dat', cards=[337], slot=0, item_id=114, obtain_flag=0x836, obtain_value=2),
			LocationData('Mudman Qubert Shop Item 2', 2359278, is_shop=True, file_type='dat', cards=[337], slot=1, item_id=19, obtain_flag=0x93, obtain_value=2),
			LocationData('Mudman Qubert Shop Item 3', 2359279, is_shop=True, file_type='dat', cards=[337], slot=2, item_id=105, obtain_flag=0x837, obtain_value=2)
		],
		'Philosopher Fobos': [
			LocationData('NPC: Philosopher Fobos', None, lambda state: state.has("Philosopher's Ocarina", player), True)
		],
		'Tailor Dracuet': [
			LocationData('Tailor Dracuet Shop Item 1', 2359280, is_shop=True, file_type='dat', cards=[1008], slot=0, item_id=110, obtain_flag=0x838, obtain_value=2),
			LocationData('Tailor Dracuet Shop Item 2', 2359281, is_shop=True, file_type='dat', cards=[1008], slot=1, item_id=111, obtain_flag=0x839, obtain_value=2),
			LocationData('Tailor Dracuet Shop Item 3', 2359282, is_shop=True, file_type='dat', cards=[1008], slot=2, item_id=114, obtain_flag=0x83a, obtain_value=2)
		] if include_dracuet else []
	}


def get_npc_entrances(world: 'LaMulanaWorld', s: LaMulanaLogicShortcuts) -> dict[str, list[LaMulanaNPCDoor]]:
	player = world.player
	worldstate = world.worldstate
	npc_checks = get_npc_checks(world)
	if worldstate.npc_rando and worldstate.npc_mapping:
		get_entrance_checks = lambda door: npc_checks[worldstate.npc_mapping[door]] if door in worldstate.npc_mapping and worldstate.npc_mapping[door] in npc_checks else []
	else:
		get_entrance_checks = lambda door: npc_checks[door] if door in npc_checks else []

	is_surface_start = world.options.StartingLocation == StartingLocation.option_surface

	npc_doors = {
		'Menu': [
			# Starting shop exists only in non-surface starts, and isn't affected by NPC rando
			LaMulanaNPCDoor(npc_checks['Starting Shop'])
		] if not is_surface_start else [],
		'Surface [Main]': [
			LaMulanaNPCDoor(get_entrance_checks('Elder Xelpud')),
			LaMulanaNPCDoor(get_entrance_checks('Nebur'), lambda state: state.has('NPC: Xelpud', player)),
			LaMulanaNPCDoor(get_entrance_checks('Sidro'), lambda state: state.has('NPC: Xelpud', player)),
			LaMulanaNPCDoor(get_entrance_checks('Modro'), lambda state: state.has('NPC: Xelpud', player)),
			LaMulanaNPCDoor(get_entrance_checks('Moger'), lambda state: state.has("NPC: Xelpud", player)),
			LaMulanaNPCDoor(get_entrance_checks('Hiner'), lambda state: state.has("NPC: Xelpud", player)),
			LaMulanaNPCDoor(get_entrance_checks('Former Mekuri Master'), lambda state: s.attack_far(state) or s.attack_s_straight(state) or s.attack_earth_spear(state) or state.has("Katana", player)),
		],
		'Gate of Guidance [Main]': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Zarnac')),
			LaMulanaNPCDoor(get_entrance_checks('Penadvent of Ghost')),
		],
		'Mausoleum of the Giants': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Xanado')),
			LaMulanaNPCDoor(get_entrance_checks('Greedy Charlie'), lambda state: s.attack_chest_any(state)),
		],
		'Temple of the Sun [Main]': [
			LaMulanaNPCDoor(get_entrance_checks('Mulbruk'), lambda state: s.guardian_count(state) >= 1 and state.has(worldstate.get_seal_name('Mulbruk\'s Seal'), player)),
			LaMulanaNPCDoor(get_entrance_checks('Shalom III'), lambda state: s.attack_shuriken(state) or s.attack_bomb(state) or s.glitch_catpause(state) or (state.has('Feather', player) and (s.attack_forward(state) or s.attack_chakram(state)))),
			LaMulanaNPCDoor(get_entrance_checks('Usas VI')),
			LaMulanaNPCDoor(get_entrance_checks('Kingvalley I'), lambda state: state.has_all(('Feather', worldstate.get_seal_name('Sun Discount Shop')), player)),
		],
		'Temple of the Sun [Sphinx]': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Madomo')),
		],
		'Spring in the Sky [Main]': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Hidlyda'), lambda state: s.spring_npc(state)),
			LaMulanaNPCDoor(get_entrance_checks('Philosopher Giltoriyo')),
		],
		'Spring in the Sky [Upper]': [
			LaMulanaNPCDoor(get_entrance_checks('Mr. Fishman (Original)'), lambda state: state.has_all(('Helmet', worldstate.get_seal_name('Mr. Fishman\'s Shop')), player)),
			LaMulanaNPCDoor(get_entrance_checks('Mr. Fishman (Alt)'), lambda state: state.has_all(('Helmet', worldstate.get_seal_name('Mr. Fishman\'s Shop')), player) and s.state_key_fairy_access(state, False)),
		],
		'Inferno Cavern [Main]': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Gailious')),
			LaMulanaNPCDoor(get_entrance_checks('Hot-blooded Nemesistwo'), lambda state: s.attack_chest_any(state)),
		],
		'Inferno Cavern [Pazuzu]': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Romancis')),
		],
		'Chamber of Extinction [Main]': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Aramo'), lambda state: s.attack_chest_any(state)),
		],
		'Chamber of Extinction [Ankh Lower]': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Triton'), lambda state: state.has('Feather', player)),
			LaMulanaNPCDoor(get_entrance_checks('Operator Combaker'), lambda state: s.attack_chest_any(state)),
		],
		'Twin Labyrinths [Loop]': [
			LaMulanaNPCDoor(get_entrance_checks('Yiegah Kungfu')),
			LaMulanaNPCDoor(get_entrance_checks('Yiear Kungfu'), lambda state: state.has('NPC: Yiegah Kungfu', player)),
		],
		'Twin Labyrinths [Lower]': [
			LaMulanaNPCDoor(get_entrance_checks('Arrogant Sturdy Snake'), lambda state: state.has('Feather', player)),
			LaMulanaNPCDoor(get_entrance_checks('Arrogant Metagear'), lambda state: (state.has('Feather', player) and s.attack_bomb(state)) or (state.has('Zu Defeated', player) and s.glitch_raindrop(state))),
		],
		'Twin Labyrinths [Poseidon]': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Jaguarfiv')),
		],
		'Endless Corridor [1F]': [
			LaMulanaNPCDoor(get_entrance_checks('Fairy Queen')),
			LaMulanaNPCDoor(get_entrance_checks('Affected Knimare'), lambda state: state.has(worldstate.get_seal_name('Endless Shop Seal'), player)),
		],
		'Gate of Illusion [Grail]': [
			LaMulanaNPCDoor(get_entrance_checks('duplex'), lambda state: state.has('Chi You Defeated', player) and s.attack_forward(state) and s.combo_dev_npcs(state)),
		],
		'Gate of Illusion [Dracuet]': [
			LaMulanaNPCDoor(get_entrance_checks('Mr. Slushfund'), lambda state: s.attack_chest(state)),
			LaMulanaNPCDoor(get_entrance_checks('Priest Alest'), lambda state: s.attack_chest(state) and state.has('Anchor', player)),
		],
		'Gate of Illusion [Middle]': [
			LaMulanaNPCDoor(get_entrance_checks('Mover Athleland')),
		],
		'Graveyard of the Giants [West]': [
			LaMulanaNPCDoor(get_entrance_checks('Giant Mopiran')),
		],
		'Graveyard of the Giants [East]': [
			LaMulanaNPCDoor(get_entrance_checks('Giant Thexde'), lambda state: state.has('Feather', player)),
		],
		'Temple of Moonlight [Pyramid]': [
			LaMulanaNPCDoor(get_entrance_checks('Philosopher Alsedana')),
		],
		'Temple of Moonlight [Upper]': [
			LaMulanaNPCDoor(get_entrance_checks('Samieru'), lambda state: s.combo_dev_npcs(state) and ((s.state_mobility(state) and s.attack_forward(state)) or (state.has('Grapple Claw', player) and (s.attack_shuriken(state) or s.attack_rolling_shuriken(state)))) and (s.attack_below(state) or s.attack_bomb(state) or s.attack_earth_spear(state) or s.attack_rolling_shuriken(state)))
		],
		'Temple of Moonlight [Southeast]': [
			LaMulanaNPCDoor(get_entrance_checks('Kingvalley II'), lambda state: s.attack_bomb(state) or (s.glitch_catpause(state) and s.attack_forward(state))),
		],
		'Tower of the Goddess [Lower]': [
			LaMulanaNPCDoor(get_entrance_checks('Philosopher Samaranta'), lambda state: state.has('Flooded Tower of the Goddess', player)),
			LaMulanaNPCDoor(get_entrance_checks('Naramura'), lambda state: s.combo_dev_npcs(state)),
			LaMulanaNPCDoor(get_entrance_checks('Energetic Belmont'), lambda state: ((state.has('Flooded Tower of the Goddess', player) and s.state_lamp(state)) or (s.glitch_raindrop(state) and state.has('Feather', player))) and state.has_any(('Anchor', 'Holy Grail'), player)),
		],
		'Tower of Ruin [Southwest]': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Laydoc')),
		],
		'Tower of Ruin [Grail]': [
			LaMulanaNPCDoor(get_entrance_checks('Mechanical Efspi'), lambda state: state.has_any(('Feather', 'Grapple Claw'), player) and (s.attack_below(state) or s.attack_earth_spear(state) or s.attack_bomb(state) or s.attack_rolling_shuriken(state) or s.attack_caltrops(state))),
		],
		'Chamber of Birth [West]': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Ashgine')),
			LaMulanaNPCDoor(get_entrance_checks('Mudman Qubert'), lambda state: state.has('Mudmen Awakened', player)),
		],
		'Dimensional Corridor [Grail]': [
			LaMulanaNPCDoor(get_entrance_checks('Philosopher Fobos'), lambda state: state.has('Left Side Children Defeated', player)),
		],
		'Gate of Time [Surface]': [
			LaMulanaNPCDoor(get_entrance_checks('8-bit Elder'))
		]
	}

	if world.options.RandomizeDracuetsShop:
		npc_doors['Hell Temple [Shop]'] = [
			LaMulanaNPCDoor(get_entrance_checks('Tailor Dracuet'))
		]

	return npc_doors


def get_npc_entrance_room_names() -> dict[str, str]:
	return {
		'Elder Xelpud': 'Surface - Village of Departure (Xelpud)',
		'Nebur': 'Surface - Village of Departure (Nebur)',
		'Sidro': 'Surface - Village of Departure (Sidro)',
		'Modro': 'Surface - Village of Departure (Modro)',
		'Moger': 'Surface - Village of Departure (Moger)',
		'Hiner': 'Surface - Altar Hill',
		'Former Mekuri Master': 'Surface - Bahrun\'s Waterfall',
		'Priest Zarnac': 'Gate of Guidance - Pit of the Holy Grail',
		'Penadvent of Ghost': 'Gate of Guidance - Monument of Time',
		'Priest Xanado': 'Mausoleum of the Giants - Room of Redemption',
		'Greedy Charlie': 'Mausoleum of the Giants - Monument to Hermes',
		'Mulbruk': 'Temple of the Sun - Thoth\'s Room',
		'Shalom III': 'Temple of the Sun - Altar of War',
		'Usas VI': 'Temple of the Sun - Sanctuary',
		'Kingvalley I': 'Temple of the Sun - Horus\' Room of Pillars',
		'Priest Madomo': 'Temple of the Sun - Great Colonnade, Right-side room',
		'Priest Hidlyda': 'Spring in the Sky - Mirror Waterfall',
		'Philosopher Giltoriyo': 'Spring in the Sky - Mural of Oannes',
		'Mr. Fishman (Original)': 'Spring in the Sky - Waterfall Approach',
		'Mr. Fishman (Alt)': 'Spring in the Sky - Waterfall Approach (Key Fairy)',
		'Priest Gailious': 'Inferno Cavern - Pit of Fire',
		'Hot-blooded Nemesistwo': 'Inferno Cavern - Anterior Chamber',
		'Priest Romancis': 'Inferno Cavern - Pazuzu\'s Room',
		'Priest Aramo': 'Chamber of Extinction - Mural of Light',
		'Priest Triton': 'Chamber of Extinction - Palenque\'s Coffin',
		'Operator Combaker': 'Chamber of Extinction - Shiva\'s Crucifix',
		'Yiegah Kungfu': 'Twin Labyrinths - Twin\'s Surrounding Wall (Little Brother)',
		'Yiear Kungfu': 'Twin Labyrinths - Twin\'s Surrounding Wall (Big Brother)',
		'Arrogant Sturdy Snake': 'Twin Labyrinths - Treasury (Right)',
		'Arrogant Metagear': 'Twin Labyrinths - Treasury (Left)',
		'Priest Jaguarfiv': 'Twin Labyrinths - Sanctuary',
		'Fairy Queen': 'Endless Corridor - First Endless Corridor (Fairy Queen)',
		'Affected Knimare': 'Endless Corridor - First Endless Corridor (Seal)',
		'duplex': 'Gate of Illusion - Chi You\'s Room',
		'Mr. Slushfund': 'Gate of Illusion - Sacred Lake of the Sky (Mr. Slushfund)',
		'Priest Alest': 'Gate of Illusion - Sacred Lake of the Sky (Mini Doll)',
		'Mover Athleland': 'Gate of Illusion - Lizard\'s Room',
		'Giant Mopiran': 'Graveyard of the Giants - First Tomb',
		'Giant Thexde': 'Graveyard of the Giants - Anterior Chamber',
		'Philosopher Alsedana': 'Temple of Moonlight - Moon Watchtower',
		'Samieru': 'Temple of Moonlight - Serdab of Power',
		'Kingvalley II': 'Temple of Moonlight - Serdab of Treasure',
		'Philosopher Samaranta': 'Tower of the Goddess - Scales of the Heart',
		'Naramura': 'Tower of the Goddess - Skuld\'s Tower',
		'Energetic Belmont': 'Tower of the Goddess - Verdandi\'s Tower',
		'Priest Laydoc': 'Tower of Ruin - Fountain of Heat',
		'Mechanical Efspi': 'Tower of Ruin - One Who Reads Tablets',
		'Priest Ashgine': 'Chamber of Birth - Brahma\'s Room',
		'Mudman Qubert': 'Chamber of Birth - Brahma\'s Room (Mudman Qubert)',
		'Philosopher Fobos': 'Dimensional Corridor - Kuusarikku\'s Room',
		'8-bit Elder': 'Gate of Time - 8-bit Surface',
		'Tailor Dracuet': 'Hell Temple - Room 14'
	}
