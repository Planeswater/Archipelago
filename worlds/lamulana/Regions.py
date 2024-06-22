from typing import List, Set, Dict, Tuple, Optional, Callable
from BaseClasses import MultiWorld, CollectionState, Region, Entrance, Location
from .Options import is_option_enabled, get_option_value, starting_location_names
from .LogicShortcuts import LaMulanaLogicShortcuts
from .CombatLogic import LaMulanaCombatLogic
from .Locations import LocationData, get_locations_by_region
from .NPCs import LaMulanaNPCDoor, get_npc_entrances
from .WorldState import LaMulanaWorldState, LaMulanaTransition

def get_starting_region(starting_location: int):
	initial_regions = {
		'surface': 'Surface [Main]',
		'guidance': 'Gate of Guidance [Main]',
		'mausoleum': 'Mausoleum of the Giants',
		'sun': 'Temple of the Sun [Grail]',
		'spring': 'Spring in the Sky [Main]',
		'inferno': 'Inferno Cavern [Main]',
		'extinction': 'Chamber of Extinction [Main]',
		'twin (front)': 'Twin Labyrinths [Poison 2]',
		'endless': 'Endless Corridor [1F]',
		'illusion': 'Gate of Illusion [Grail]',
		'graveyard': 'Graveyard of the Giants [Grail]',
		'moonlight': 'Temple of Moonlight [Grail]',
		'goddess': 'Tower of the Goddess [Grail]',
		'ruin': 'Tower of Ruin [Grail]',
		'birth': 'Chamber of Birth [West Entrance]',
		'twin (back)': 'Twin Labyrinths [Lower]',
		'gate of time (surface)': 'Gate of Time [Surface]'
	}
	start = starting_location_names[starting_location]
	return initial_regions[start]


def create_regions_and_locations(world: MultiWorld, player: int, worldstate: LaMulanaWorldState):
	s = LaMulanaLogicShortcuts(world, player)

	locations = get_locations_by_region(world, player, worldstate)
	npcs = get_npc_entrances(world, player, worldstate, s)
	cursed_chests = worldstate.cursed_chests

	regions = [
		create_region(world, player, "Menu", locations, npcs, cursed_chests),
		create_region(world, player, "Surface [Main]", locations, npcs, cursed_chests),
		create_region(world, player, "Surface [Ruin Path Upper]", locations, npcs, cursed_chests),
		create_region(world, player, "Surface [Ruin Path Lower]", locations, npcs, cursed_chests),
		create_region(world, player, "Gate of Guidance [Main]", locations, npcs, cursed_chests),
		create_region(world, player, "Gate of Guidance [Door]", locations, npcs, cursed_chests),
		create_region(world, player, "Gate of Illusion [Eden]", locations, npcs, cursed_chests),
		create_region(world, player, "Gate of Illusion [Lower]", locations, npcs, cursed_chests),
		create_region(world, player, "Gate of Illusion [Middle]", locations, npcs, cursed_chests),
		create_region(world, player, "Gate of Illusion [Dracuet]", locations, npcs, cursed_chests),
		create_region(world, player, "Gate of Illusion [Grail]", locations, npcs, cursed_chests),
		create_region(world, player, "Gate of Illusion [Ruin]", locations, npcs, cursed_chests),
		create_region(world, player, "Gate of Illusion [Upper]", locations, npcs, cursed_chests),
		create_region(world, player, "Gate of Illusion [Pot Room]", locations, npcs, cursed_chests),
		create_region(world, player, "Mausoleum of the Giants", locations, npcs, cursed_chests),
		create_region(world, player, "Graveyard of the Giants [West]", locations, npcs, cursed_chests),
		create_region(world, player, "Graveyard of the Giants [Grail]", locations, npcs, cursed_chests),
		create_region(world, player, "Graveyard of the Giants [East]", locations, npcs, cursed_chests),
		create_region(world, player, "Temple of the Sun [Top Entrance]", locations, npcs, cursed_chests),
		create_region(world, player, "Temple of the Sun [Grail]", locations, npcs, cursed_chests),
		create_region(world, player, "Temple of the Sun [Main]", locations, npcs, cursed_chests),
		create_region(world, player, "Temple of the Sun [West]", locations, npcs, cursed_chests),
		create_region(world, player, "Temple of the Sun [East]", locations, npcs, cursed_chests),
		create_region(world, player, "Temple of the Sun [Sphinx]", locations, npcs, cursed_chests),
		create_region(world, player, "Temple of Moonlight [Pyramid]", locations, npcs, cursed_chests),
		create_region(world, player, "Temple of Moonlight [Upper]", locations, npcs, cursed_chests),
		create_region(world, player, "Temple of Moonlight [Lower]", locations, npcs, cursed_chests),
		create_region(world, player, "Temple of Moonlight [Eden]", locations, npcs, cursed_chests),
		create_region(world, player, "Temple of Moonlight [Grail]", locations, npcs, cursed_chests),
		create_region(world, player, "Temple of Moonlight [Grapple]", locations, npcs, cursed_chests),
		create_region(world, player, "Temple of Moonlight [Map]", locations, npcs, cursed_chests),
		create_region(world, player, "Temple of Moonlight [Southeast]", locations, npcs, cursed_chests),
		create_region(world, player, "Spring in the Sky [Main]", locations, npcs, cursed_chests),
		create_region(world, player, "Spring in the Sky [Upper]", locations, npcs, cursed_chests),
		create_region(world, player, "Tower of the Goddess [Lower]", locations, npcs, cursed_chests),
		create_region(world, player, "Tower of the Goddess [Lamp]", locations, npcs, cursed_chests),
		create_region(world, player, "Tower of the Goddess [Grail]", locations, npcs, cursed_chests),
		create_region(world, player, "Tower of the Goddess [Spaulder]", locations, npcs, cursed_chests),
		create_region(world, player, "Tower of the Goddess [Pipe]", locations, npcs, cursed_chests),		
		#create_region(world, player, "Tower of the Goddess [Shield Statue]", locations, npcs, cursed_chests),
		create_region(world, player, "Inferno Cavern [Main]", locations, npcs, cursed_chests),
		create_region(world, player, "Inferno Cavern [Pazuzu]", locations, npcs, cursed_chests),
		create_region(world, player, "Inferno Cavern [Viy]", locations, npcs, cursed_chests),
		create_region(world, player, "Inferno Cavern [Lava]", locations, npcs, cursed_chests),
		create_region(world, player, "Inferno Cavern [Spikes]", locations, npcs, cursed_chests),
		create_region(world, player, "Tower of Ruin [Southeast]", locations, npcs, cursed_chests),
		create_region(world, player, "Tower of Ruin [Southwest]", locations, npcs, cursed_chests),
		create_region(world, player, "Tower of Ruin [Southwest Door]", locations, npcs, cursed_chests),
		create_region(world, player, "Tower of Ruin [La-Mulanese]", locations, npcs, cursed_chests),
		create_region(world, player, "Tower of Ruin [Illusion]", locations, npcs, cursed_chests),
		create_region(world, player, "Tower of Ruin [Grail]", locations, npcs, cursed_chests),
		create_region(world, player, "Tower of Ruin [Spirits]", locations, npcs, cursed_chests),
		create_region(world, player, "Tower of Ruin [Medicine]", locations, npcs, cursed_chests),
		create_region(world, player, "Tower of Ruin [Top]", locations, npcs, cursed_chests),
		create_region(world, player, "Chamber of Extinction [Map]", locations, npcs, cursed_chests),
		create_region(world, player, "Chamber of Extinction [Main]", locations, npcs, cursed_chests),
		create_region(world, player, "Chamber of Extinction [Left Main]", locations, npcs, cursed_chests),
		create_region(world, player, "Chamber of Extinction [Teleport]", locations, npcs, cursed_chests),
		create_region(world, player, "Chamber of Extinction [Magatama Left]", locations, npcs, cursed_chests),
		create_region(world, player, "Chamber of Extinction [Magatama Right]", locations, npcs, cursed_chests),
		create_region(world, player, "Chamber of Extinction [Magatama]", locations, npcs, cursed_chests),
		create_region(world, player, "Chamber of Extinction [Ankh Upper]", locations, npcs, cursed_chests),
		create_region(world, player, "Chamber of Extinction [Ankh Lower]", locations, npcs, cursed_chests),
		create_region(world, player, "Chamber of Birth [West Entrance]", locations, npcs, cursed_chests),
		create_region(world, player, "Chamber of Birth [West]", locations, npcs, cursed_chests),
		create_region(world, player, "Chamber of Birth [Grail]", locations, npcs, cursed_chests),
		create_region(world, player, "Chamber of Birth [Skanda]", locations, npcs, cursed_chests),
		create_region(world, player, "Chamber of Birth [Dance]", locations, npcs, cursed_chests),
		create_region(world, player, "Chamber of Birth [Northeast]", locations, npcs, cursed_chests),
		create_region(world, player, "Chamber of Birth [Southeast]", locations, npcs, cursed_chests),
		create_region(world, player, "Twin Labyrinths [Loop]", locations, npcs, cursed_chests),
		create_region(world, player, "Twin Labyrinths [Lower]", locations, npcs, cursed_chests),
		create_region(world, player, "Twin Labyrinths [Poison 1]", locations, npcs, cursed_chests),
		create_region(world, player, "Twin Labyrinths [Poison 2]", locations, npcs, cursed_chests),
		create_region(world, player, "Twin Labyrinths [Upper Grail]", locations, npcs, cursed_chests),
		create_region(world, player, "Twin Labyrinths [Jewel]", locations, npcs, cursed_chests),
		create_region(world, player, "Twin Labyrinths [Katana]", locations, npcs, cursed_chests),
		create_region(world, player, "Twin Labyrinths [Poseidon]", locations, npcs, cursed_chests),
		create_region(world, player, "Twin Labyrinths [Upper Left]", locations, npcs, cursed_chests),
		create_region(world, player, "Endless Corridor [1F]", locations, npcs, cursed_chests),
		create_region(world, player, "Endless Corridor [2F]", locations, npcs, cursed_chests),
		create_region(world, player, "Endless Corridor [3F Upper]", locations, npcs, cursed_chests),
		create_region(world, player, "Endless Corridor [3F Lower]", locations, npcs, cursed_chests),
		create_region(world, player, "Endless Corridor [4F]", locations, npcs, cursed_chests),
		create_region(world, player, "Endless Corridor [5F]", locations, npcs, cursed_chests),
		create_region(world, player, "Dimensional Corridor [Lower]", locations, npcs, cursed_chests),
		create_region(world, player, "Dimensional Corridor [Grail]", locations, npcs, cursed_chests),
		create_region(world, player, "Dimensional Corridor [Upper]", locations, npcs, cursed_chests),
		create_region(world, player, "Shrine of the Mother [Main]", locations, npcs, cursed_chests),
		create_region(world, player, "Shrine of the Mother [Lower]", locations, npcs, cursed_chests),
		create_region(world, player, "Shrine of the Mother [Seal]", locations, npcs, cursed_chests),
		create_region(world, player, "Shrine of the Mother [Map]", locations, npcs, cursed_chests),
		create_region(world, player, "True Shrine of the Mother", locations, npcs, cursed_chests),
		create_region(world, player, "Gate of Time [Mausoleum Lower]", locations, npcs, cursed_chests),
		create_region(world, player, "Gate of Time [Mausoleum Upper]", locations, npcs, cursed_chests),
		create_region(world, player, "Gate of Time [Guidance]", locations, npcs, cursed_chests),
		create_region(world, player, "Gate of Time [Surface]", locations, npcs, cursed_chests),
	]

	if is_option_enabled(world, player, "HellTempleReward") or is_option_enabled(world, player, "RandomizeDracuetsShop"):
		regions.extend([
			create_region(world, player, "Hell Temple [Entrance]", locations, npcs, cursed_chests),
			create_region(world, player, "Hell Temple [Shop]", locations, npcs, cursed_chests),
		])
	
	if is_option_enabled(world, player, "HellTempleReward"):
		regions.extend([
			create_region(world, player, "Hell Temple [Dracuet]", locations, npcs, cursed_chests)
		])


	world.regions += regions

	#Connect Menu (the starting node) to our starting location's region
	starting_region = get_starting_region(get_option_value(world, player, "StartingLocation"))
	connect(world, player, 'Menu', starting_region)

	#Internal connections within fields that don't change with ER
	connect(world, player, 'Surface [Main]', 'Surface [Ruin Path Lower]', lambda state: s.glitch_raindrop(state))
	connect(world, player, 'Surface [Ruin Path Upper]', 'Surface [Ruin Path Lower]', lambda state: state.has_any({'Feather', 'Holy Grail'}, player))
	connect(world, player, 'Surface [Ruin Path Lower]', 'Surface [Ruin Path Upper]', lambda state: state.has('Feather', player))

	connect(world, player, 'Gate of Guidance [Door]', 'Gate of Guidance [Main]')

	connect(world, player, 'Gate of Illusion [Grail]', 'Gate of Illusion [Eden]', lambda state: state.has('Holy Grail', player))
	connect(world, player, 'Gate of Illusion [Eden]', 'Gate of Illusion [Lower]', lambda state: state.has('Illusion Unlocked', player))
	connect(world, player, 'Gate of Illusion [Dracuet]', 'Gate of Illusion [Lower]', lambda state: state.has_any({'Hand Scanner', 'Holy Grail'}, player) or s.glitch_raindrop(state))
	connect(world, player, 'Gate of Illusion [Lower]', 'Gate of Illusion [Dracuet]', lambda state: state.has('Hand Scanner', player) or s.glitch_raindrop(state))
	connect(world, player, 'Gate of Illusion [Grail]', 'Gate of Illusion [Middle]', lambda state: s.glitch_lamp(state))
	connect(world, player, 'Gate of Illusion [Dracuet]', 'Gate of Illusion [Middle]', lambda state: (s.attack_far(state) or s.attack_bomb(state)) and state.has_all({'Illusion Unlocked', 'Anchor'}, player))
	connect(world, player, 'Gate of Illusion [Middle]', 'Gate of Illusion [Dracuet]', lambda state: state.has('Holy Grail', player) or (state.has_all({'Illusion Unlocked', 'Anchor'}, player) and s.attack_chest(state))) #Puzzle solves itself when you go backwards, so backtracking doesn't require attack-far
	connect(world, player, 'Gate of Illusion [Middle]', 'Gate of Illusion [Grail]')
	connect(world, player, 'Gate of Illusion [Upper]', 'Gate of Illusion [Grail]', lambda state: state.has('Holy Grail', player))
	connect(world, player, 'Gate of Illusion [Ruin]', 'Gate of Illusion [Grail]', lambda state: state.has(worldstate.get_seal_name('Chi You Seal'), player))
	connect(world, player, 'Gate of Illusion [Grail]', 'Gate of Illusion [Ruin]', lambda state: state.has_any({'Holy Grail', worldstate.get_seal_name('Chi You Seal')}, player))
	connect(world, player, 'Gate of Illusion [Grail]', 'Gate of Illusion [Pot Room]', lambda state: s.glitch_raindrop(state))
	connect(world, player, 'Gate of Illusion [Pot Room]', 'Gate of Illusion [Upper]', lambda state: state.has('Feather', player))

	connect(world, player, 'Graveyard of the Giants [West]', 'Graveyard of the Giants [Grail]', lambda state: state.has('Feather', player))
	connect(world, player, 'Graveyard of the Giants [Grail]', 'Graveyard of the Giants [West]', lambda state: state.has_any({'Holy Grail', 'Feather'}, player))
	connect(world, player, 'Graveyard of the Giants [West]', 'Graveyard of the Giants [East]', lambda state: (s.attack_bomb(state) and state.has('Ring', player)) or (state.has_all({'Bomb', 'Ring'}, player) and s.fairy_point_reachable(state, True, False) and state.can_reach('Graveyard of the Giants [Grail]', 'Region', player)))
	connect(world, player, 'Graveyard of the Giants [East]', 'Graveyard of the Giants [West]', lambda state: s.attack_bomb(state))

	connect(world, player, 'Temple of the Sun [Grail]', 'Temple of the Sun [Top Entrance]', lambda state: state.has("Hermes' Boots", player) or s.sun_watchtower(state))
	connect(world, player, 'Temple of the Sun [Top Entrance]', 'Temple of the Sun [Grail]', lambda state: state.has_any({'Holy Grail', "Hermes' Boots"}, player) or s.sun_watchtower(state))
	connect(world, player, 'Temple of the Sun [Top Entrance]', 'Temple of the Sun [West]', lambda state: s.sun_watchtower(state) and (s.attack_main(state) or state.has_any({'Grapple Claw', 'Feather'}, player)))
	connect(world, player, 'Temple of the Sun [Top Entrance]', 'Temple of the Sun [Main]', lambda state: state.has('Holy Grail', player) or s.sun_watchtower(state))
	connect(world, player, 'Temple of the Sun [West]', 'Temple of the Sun [Top Entrance]', lambda state: state.has('Buer Defeated', player) and s.sun_watchtower(state))
	connect(world, player, 'Temple of the Sun [Main]', 'Temple of the Sun [Top Entrance]', lambda state: s.sun_watchtower(state))
	connect(world, player, 'Temple of the Sun [Main]', 'Temple of the Sun [East]', lambda state: state.has("Hermes' Boots", player))
	connect(world, player, 'Temple of the Sun [Main]', 'Temple of the Sun [Sphinx]', lambda state: state.has_all({"Hermes' Boots", 'Feather'}, player))
	connect(world, player, 'Temple of the Sun [Sphinx]', 'Temple of the Sun [East]', lambda state: state.has('Holy Grail', player) or s.sun_watchtower(state))
	connect(world, player, 'Temple of the Sun [East]', 'Temple of the Sun [Main]', lambda state: state.has_any({'Holy Grail', "Hermes' Boots"}, player))
	connect(world, player, 'Temple of the Sun [Main]', 'Temple of Moonlight [Pyramid]', lambda state: state.has('Holy Grail', player) and (s.attack_above(state) or s.attack_s_above(state)))

	connect(world, player, 'Temple of Moonlight [Pyramid]', 'Temple of Moonlight [Upper]')
	connect(world, player, 'Temple of Moonlight [Pyramid]', 'Temple of Moonlight [Lower]', lambda state: s.glitch_raindrop(state))
	connect(world, player, 'Temple of Moonlight [Upper]', 'Temple of Moonlight [Pyramid]', lambda state: s.glitch_raindrop(state))
	connect(world, player, 'Temple of Moonlight [Lower]', 'Temple of Moonlight [Upper]', lambda state: s.moonlight_face(state))
	connect(world, player, 'Temple of Moonlight [Upper]', 'Temple of Moonlight [Eden]', lambda state: (s.attack_forward(state) or s.attack_flare_gun(state)) and (state.has('Holy Grail', player) or s.attack_chest(state)))
	connect(world, player, 'Temple of Moonlight [Eden]', 'Temple of Moonlight [Upper]', lambda state: s.attack_chest(state))
	connect(world, player, 'Temple of Moonlight [Eden]', 'Temple of Moonlight [Grail]', lambda state: s.attack_chest(state) and (state.has('Holy Grail', player) or s.attack_flare_gun(state)))
	connect(world, player, 'Temple of Moonlight [Eden]', 'Temple of Moonlight [Grapple]', lambda state: state.has_any({'Holy Grail', 'Feather'}, player) or s.attack_chest(state))
	connect(world, player, 'Temple of Moonlight [Grapple]', 'Temple of Moonlight [Map]')
	connect(world, player, 'Temple of Moonlight [Lower]', 'Temple of Moonlight [Southeast]', lambda state: (state.has(worldstate.get_seal_name('Path to Anubis'), player) or s.glitch_raindrop(state)) and (s.attack_forward(state) or s.attack_flare_gun(state)))
	connect(world, player, 'Temple of Moonlight [Grail]', 'Temple of Moonlight [Eden]', lambda state: s.attack_forward(state) or s.attack_vertical(state) or (s.attack_earth_spear(state) and state.has('Holy Grail', player)))

	connect(world, player, 'Spring in the Sky [Main]', 'Spring in the Sky [Upper]', lambda state: state.has('Helmet', player))
	connect(world, player, 'Spring in the Sky [Upper]', 'Surface [Main]', lambda state: state.has('Holy Grail', player) and (state.has('Bahamut Defeated', player) or s.glitch_lamp(state)))
	connect(world, player, 'Spring in the Sky [Main]', 'Temple of the Sun [Sphinx]', lambda state: state.has_all({'Flooded Temple of the Sun', 'Holy Grail'}, player))

	connect(world, player, 'Tower of the Goddess [Grail]', 'Tower of the Goddess [Lower]', lambda state: state.has_any({'Holy Grail', 'Feather'}, player))
	connect(world, player, 'Tower of the Goddess [Lamp]', 'Tower of the Goddess [Lower]', lambda state: s.attack_forward(state) or state.has_all({'Feather', 'Holy Grail'}, player))
	connect(world, player, 'Tower of the Goddess [Lower]', 'Tower of the Goddess [Lamp]', lambda state: state.has('Flooded Tower of the Goddess', player) and state.has_any({'Holy Grail', 'Anchor'}, player))
	connect(world, player, 'Tower of the Goddess [Lower]', 'Tower of the Goddess [Grail]', lambda state: state.has('Feather', player))
	connect(world, player, 'Tower of the Goddess [Grail]', 'Tower of the Goddess [Spaulder]', lambda state: s.attack_forward(state))
	connect(world, player, 'Tower of the Goddess [Spaulder]', 'Tower of the Goddess [Grail]', lambda state: state.has('Holy Grail', player) or s.attack_forward(state))

	connect(world, player, 'Inferno Cavern [Viy]', 'Inferno Cavern [Main]', lambda state: s.state_lava_swim(state, 3) and (s.attack_forward(state) or s.glitch_catpause(state)))
	connect(world, player, 'Inferno Cavern [Main]', 'Inferno Cavern [Pazuzu]', lambda state: state.has(worldstate.get_seal_name('Pazuzu Seal'), player) and (state.has_any({'Feather', 'Grapple Claw'}, player) or s.state_lamp(state))),
	connect(world, player, 'Inferno Cavern [Main]', 'Inferno Cavern [Viy]', lambda state: s.glitch_lamp(state) and s.attack_forward(state) and (state.has('Holy Grail', player) or s.state_lava_swim(state, 3)))
	connect(world, player, 'Inferno Cavern [Lava]', 'Inferno Cavern [Main]', lambda state: s.state_lava_swim(state, 2))
	connect(world, player, 'Inferno Cavern [Viy]', 'Chamber of Extinction [Ankh Upper]', lambda state: state.has_all({'Viy Defeated', 'Holy Grail'}, player))

	connect(world, player, 'Tower of Ruin [Southeast]', 'Tower of Ruin [Southwest]', lambda state: s.state_mobility(state) or s.state_lava_swim(state, 1))
	connect(world, player, 'Tower of Ruin [Southwest]', 'Tower of Ruin [Southeast]', lambda state: s.state_mobility(state) or s.state_lava_swim(state, 1))
	connect(world, player, 'Tower of Ruin [Grail]', 'Tower of Ruin [Southwest]', lambda state: state.has('Holy Grail', player))
	connect(world, player, 'Tower of Ruin [Southwest]', 'Tower of Ruin [Southwest Door]', lambda state: s.attack_earth_spear(state) or s.glitch_raindrop(state) or (state.has('Earth Spear', player) and s.fairy_point_reachable(state, True, False)))
	connect(world, player, 'Tower of Ruin [Southwest Door]', 'Tower of Ruin [Southwest]', lambda state: state.has('Holy Grail', player) or s.attack_earth_spear(state) or s.glitch_raindrop(state))
	connect(world, player, 'Tower of Ruin [Southwest]', 'Tower of Ruin [La-Mulanese]', lambda state: state.has_all({'Thunderbird Defeated', 'Feather'}, player))
	connect(world, player, 'Tower of Ruin [Southwest]', 'Tower of Ruin [Grail]', lambda state: state.has_all({'Thunderbird Defeated', 'Feather'}, player) and s.attack_forward(state))
	connect(world, player, 'Tower of Ruin [Illusion]', 'Tower of Ruin [Grail]', lambda state: s.attack_forward(state))
	connect(world, player, 'Tower of Ruin [Spirits]', 'Tower of Ruin [Grail]', lambda state: state.has('Holy Grail', player))
	connect(world, player, 'Tower of Ruin [Medicine]', 'Tower of Ruin [Spirits]', lambda state: s.state_lava_swim(state, 3) and (state.has('Holy Grail', player) or s.state_lava_swim(state, 5)))
	connect(world, player, 'Tower of Ruin [Top]', 'Tower of Ruin [Medicine]', lambda state: state.has('Holy Grail', player))
	connect(world, player, 'Tower of Ruin [Top]', 'Tower of Ruin [Spirits]', lambda state: s.nuwa_access(state, worldstate))

	connect(world, player, 'Chamber of Extinction [Left Main]', 'Chamber of Extinction [Map]', lambda state: s.state_extinction_light(state) and s.glitch_raindrop(state))
	connect(world, player, 'Chamber of Extinction [Map]', 'Chamber of Extinction [Main]', lambda state: s.state_extinction_light(state) and state.has('Holy Grail', player))
	connect(world, player, 'Chamber of Extinction [Left Main]', 'Chamber of Extinction [Main]', lambda state: s.state_extinction_light(state) and state.has('Feather', player))
	connect(world, player, 'Chamber of Extinction [Main]', 'Chamber of Extinction [Left Main]', lambda state: s.state_extinction_light(state) and state.has_any({'Holy Grail', 'Feather'}, player))
	connect(world, player, 'Chamber of Extinction [Magatama Left]', 'Chamber of Extinction [Left Main]', lambda state: s.glitch_raindrop(state) and s.state_extinction_light(state))
	connect(world, player, 'Chamber of Extinction [Ankh Upper]', 'Chamber of Extinction [Teleport]', lambda state: s.glitch_raindrop(state))
	connect(world, player, 'Chamber of Birth [Southeast]', 'Chamber of Extinction [Teleport]', lambda state: s.attack_forward(state) and state.has('Feather', player))
	connect(world, player, 'Chamber of Birth [Northeast]', 'Chamber of Extinction [Teleport]', lambda state: s.glitch_raindrop(state) and s.attack_forward(state))
	connect(world, player, 'Chamber of Extinction [Teleport]', 'Chamber of Birth [Northeast]', lambda state: state.has('Feather', player))
	connect(world, player, 'Chamber of Extinction [Magatama Left]', 'Chamber of Extinction [Magatama]', lambda state: state.has_any({'Holy Grail', 'Feather'}, player) or s.attack_forward(state))
	connect(world, player, 'Chamber of Extinction [Magatama]', 'Chamber of Extinction [Magatama Left]', lambda state: state.has('Ox-head & Horse-face Defeated', player))
	connect(world, player, 'Chamber of Extinction [Magatama]', 'Chamber of Extinction [Magatama Right]', lambda state: state.has('Ox-head & Horse-face Defeated', player))
	connect(world, player, 'Chamber of Extinction [Magatama Right]', 'Chamber of Extinction [Magatama]', lambda state: state.has('Holy Grail', player) or (s.attack_chest(state) and state.has('Feather', player)))
	connect(world, player, 'Chamber of Extinction [Ankh Upper]', 'Chamber of Extinction [Ankh Lower]', lambda state: state.has_any({'Holy Grail', 'Feather'}, player))
	connect(world, player, 'Chamber of Extinction [Ankh Lower]', 'Chamber of Extinction [Ankh Upper]', lambda state: state.has('Feather', player))
	connect(world, player, 'Chamber of Extinction [Teleport]', 'Chamber of Extinction [Ankh Lower]', lambda state: s.glitch_raindrop(state))

	connect(world, player, 'Chamber of Birth [West Entrance]', 'Chamber of Birth [West]', lambda state: state.has('Holy Grail', player))
	connect(world, player, 'Chamber of Birth [West]', 'Chamber of Birth [Grail]', lambda state: (s.glitch_catpause(state) and state.has('Feather', player)) or (state.has_all({'Serpent Staff', 'Crystal Skull'}, player) and s.attack_chakram(state) and s.state_mobility(state)))
	connect(world, player, 'Chamber of Birth [West]', 'Chamber of Birth [Skanda]', lambda state: s.glitch_raindrop(state) and s.attack_forward(state))
	connect(world, player, 'Chamber of Birth [Grail]', 'Chamber of Birth [Skanda]', lambda state: state.has_all({'Serpent Staff', 'Cog of the Soul'}, player) and s.attack_chakram(state))
	connect(world, player, 'Chamber of Birth [West]', 'Chamber of Birth [Dance]', lambda state: s.glitch_raindrop(state) or (state.has_all({'Serpent Staff', 'Holy Grail'}, player) and s.attack_chakram(state)))
	connect(world, player, 'Chamber of Birth [Southeast]', 'Chamber of Birth [Northeast]', lambda state: state.has('Feather', player))
	connect(world, player, 'Chamber of Birth [Northeast]', 'Chamber of Birth [Southeast]', lambda state: state.has_any({'Holy Grail', 'Feather'}, player))

	connect(world, player, 'Temple of the Sun [Main]', 'Twin Labyrinths [Poison 1]', lambda state: state.has('Ellmac Defeated', player))
	connect(world, player, 'Temple of the Sun [Main]', 'Twin Labyrinths [Upper Grail]', lambda state: state.has('Ellmac Defeated', player) and s.glitch_raindrop(state))
	connect(world, player, 'Twin Labyrinths [Poison 1]', 'Twin Labyrinths [Poison 2]', lambda state: state.has('Twin Statue', player))
	connect(world, player, 'Twin Labyrinths [Poison 2]', 'Twin Labyrinths [Poison 1]', lambda state: state.has_any({'Twin Statue', 'Twin Poison Cleared'}, player))
	connect(world, player, 'Twin Labyrinths [Poison 1]', 'Twin Labyrinths [Upper Grail]', lambda state: state.has('Twin Poison Cleared', player))
	connect(world, player, 'Twin Labyrinths [Upper Grail]', 'Twin Labyrinths [Jewel]', lambda state: s.glitch_raindrop(state))
	connect(world, player, 'Twin Labyrinths [Poison 2]', 'Twin Labyrinths [Jewel]', lambda state: s.attack_forward(state) and state.has('Twin Poison Cleared', player))
	connect(world, player, 'Twin Labyrinths [Jewel]', 'Twin Labyrinths [Katana]', lambda state: s.attack_forward(state))
	connect(world, player, 'Twin Labyrinths [Poseidon]', 'Twin Labyrinths [Katana]', lambda state: s.glitch_raindrop(state) and s.attack_forward(state))
	connect(world, player, 'Twin Labyrinths [Poison 2]', 'Twin Labyrinths [Poseidon]', lambda state: state.has('Twin Poison Cleared', player) or (s.glitch_raindrop(state) and s.state_frontside_warp(state)))
	connect(world, player, 'Twin Labyrinths [Katana]', 'Twin Labyrinths [Loop]', lambda state: state.has('Holy Grail', player))
	connect(world, player, 'Twin Labyrinths [Lower]', 'Twin Labyrinths [Loop]', lambda state: state.has('Twin Poison Cleared', player))
	connect(world, player, 'Twin Labyrinths [Loop]', 'Twin Labyrinths [Upper Left]', lambda state: s.glitch_raindrop(state))
	connect(world, player, 'Twin Labyrinths [Poison 1]', 'Twin Labyrinths [Upper Left]', lambda state: state.has('Twin Poison Cleared', player))
	connect(world, player, 'Twin Labyrinths [Upper Left]', 'Twin Labyrinths [Loop]', lambda state: state.has('Twin Poison Cleared', player))
	connect(world, player, 'Twin Labyrinths [Upper Left]', 'Twin Labyrinths [Lower]', lambda state: state.has('Twin Poison Cleared', player))
	connect(world, player, 'Twin Labyrinths [Loop]', 'Twin Labyrinths [Lower]', lambda state: state.has('Twin Poison Cleared', player))

	connect(world, player, 'Endless Corridor [1F]', 'Endless Corridor [2F]', lambda state: state.has('Key of Eternity', player) and s.attack_chest(state))
	connect(world, player, 'Endless Corridor [2F]', 'Endless Corridor [1F]', lambda state: state.has('Holy Grail', player) or (state.has('Key of Eternity', player) and s.attack_chest(state)))
	connect(world, player, 'Endless Corridor [2F]', 'Endless Corridor [3F Upper]', lambda state: state.has('Key of Eternity', player) or (s.glitch_raindrop(state) and s.attack_forward(state)))
	connect(world, player, 'Endless Corridor [3F Upper]', 'Endless Corridor [3F Lower]', lambda state: state.has('Holy Grail', player) or s.attack_forward(state) or (s.attack_earth_spear(state) and state.has('Feather', player)))
	connect(world, player, 'Endless Corridor [3F Lower]', 'Endless Corridor [4F]', lambda state: s.glitch_raindrop(state) or (state.has('Key of Eternity', player) and (state.has('Holy Grail', player) or s.attack_forward(state) or (s.attack_earth_spear(state) and state.has('Feather', player)))))
	connect(world, player, 'Endless Corridor [4F]', 'Endless Corridor [5F]', lambda state: state.has('Key of Eternity', player))
	connect(world, player, 'Endless Corridor [5F]', 'Endless Corridor [1F]', lambda state: s.glitch_raindrop(state))

	connect(world, player, 'Dimensional Corridor [Lower]', 'Dimensional Corridor [Grail]', lambda state: state.has('Feather', player))
	connect(world, player, 'Dimensional Corridor [Grail]', 'Dimensional Corridor [Lower]', lambda state: state.has('Feather', player))
	connect(world, player, 'Dimensional Corridor [Grail]', 'Dimensional Corridor [Upper]', lambda state: state.has('Feather', player) or (state.has_all({'Dimensional Key', 'Left Side Children Defeated'}, player)))

	connect(world, player, 'Shrine of the Mother [Main]', 'Shrine of the Mother [Lower]', lambda state: state.has('Feather', player) and (s.attack_forward(state) or s.attack_flare_gun(state)) and state.has_any({'Holy Grail', 'Removed Shrine Skulls'}, player))
	connect(world, player, 'Shrine of the Mother [Main]', 'True Shrine of the Mother', lambda state: s.guardian_count(state) == 8)

	connect(world, player, 'Gate of Time [Mausoleum Lower]', 'Gate of Time [Mausoleum Upper]', lambda state: state.has('Feather', player))
	connect(world, player, 'Gate of Time [Mausoleum Upper]', 'Gate of Time [Mausoleum Lower]', lambda state: state.has_any({'Holy Grail', 'Feather'}, player))

	if is_option_enabled(world, player, "HellTempleReward") or is_option_enabled(world, player, "RandomizeDracuetsShop"):
		connect(world, player, 'Gate of Guidance [Main]', 'Hell Temple [Entrance]', lambda state: state.has_all({'Hell Temple Unlocked', 'Feather', worldstate.get_seal_name('Crucifix Chest/3 Lights')}, player))
		connect(world, player, 'Hell Temple [Entrance]', 'Hell Temple [Shop]', lambda state: s.attack_bomb(state) and state.has('Ring', player) and (state.has("Hermes' Boots", player) or s.state_lamp(state)))
	
	if is_option_enabled(world, player, "HellTempleReward"):
		combat = LaMulanaCombatLogic(world, player, s)
		connect(world, player, 'Hell Temple [Shop]', 'Hell Temple [Dracuet]', lambda state: s.state_literacy(state) and s.state_key_fairy_access(state, False) and state.has_all({"Hermes' Boots", 'Grapple Claw', 'guild.exe'}, player) and combat.hell_temple_bosses(state) and (s.attack_chakram(state) or s.attack_pistol(state)))

	if not worldstate.door_rando:
		get_and_connect_doors(world, player, worldstate, s)

	if worldstate.transition_rando:
		success = False
		simulated_state = worldstate.build_simulated_state()

		base_exits = set()
		for region in world.get_regions(player):
			base_exits.update(set(region.exits))

		total_attempt_count = 100
		for attempt in range(total_attempt_count):
			worldstate.randomize_transitions(s)
			get_and_connect_transitions(world, player, worldstate, s)

			if worldstate.door_rando:
				worldstate.randomize_doors(s)
				get_and_connect_doors(world, player, worldstate, s)

			success = worldstate.layout_fulfills_accessibility(simulated_state)
			if success:
				print(f'Player {player}: La-Mulana entrance randomizer success on attempt {attempt}')
				break
			else:
				remove_entrances(world, player, base_exits)
		if not success:
			raise Exception(f'Could not find valid La-Mulana entrance layout in {total_attempt_count} attempts for player {player}')

	else:
		if worldstate.door_rando:
			worldstate.randomize_doors(s)
			get_and_connect_doors(world, player, worldstate, s)
		get_and_connect_transitions(world, player, worldstate, s)


def remove_entrances(world: MultiWorld, player: int, exits_to_keep: Set[Entrance]):
	for region in world.get_regions(player):
		for entrance in reversed(region.exits):
			if entrance not in exits_to_keep:
				region.exits.remove(entrance)


def get_and_connect_transitions(world: MultiWorld, player: int, worldstate: LaMulanaWorldState, s: LaMulanaLogicShortcuts):
	transitions = worldstate.get_transitions(s)
	for transition_name, transition_data in transitions['left'].items():
		if transition_data.is_oneway:
			if worldstate.include_oneways:
				target_name = worldstate.transition_map[transition_name]
				target = transitions['right'][target_name]
				if transition_name == 'Endless L1':
					# Endless L1 special case: if connected to Surface R1
					# (logic is false but does send you to its connection), instead direct to Surface R1's connection
					if target_name == 'Surface R1':
						target_name = worldstate.transition_map['Surface R1']
						target = transitions['left'][target_name]
					# Since this is Endless L1, do not connect backward
					connect_transitions(world, player, transition_data, target, False)
				else:
					connect_transitions(world, player, transition_data, target)
			else:
				target_name = transition_data.vanilla_destination
				target = transitions['right'][target_name]
				connect_transitions(world, player, transition_data, target)
		else:
			if worldstate.transition_rando:
				target_name = worldstate.transition_map[transition_name]
			else:
				target_name = transition_data.vanilla_destination
			target = transitions['right'][target_name]
			connect_transitions(world, player, transition_data, target)

	for transition_name, transition_data in transitions['up'].items():
		if transition_data.is_oneway:
			target_name = worldstate.transition_map[transition_name] if worldstate.include_oneways else transition_data.vanilla_destination
		else:
			target_name = worldstate.transition_map[transition_name] if worldstate.transition_rando else transition_data.vanilla_destination
		target = transitions['down'][target_name]
		connect_transitions(world, player, transition_data, target)

def connect_transitions(world: MultiWorld, player: int, source: LaMulanaTransition, destination: LaMulanaTransition, both_ways=True):
	# Accounts for Endless L1 leading to the same region
	if source.region == destination.region:
		return
	if source.in_logic and destination.out_logic:
		transition_logic = lambda state: source.in_logic(state) and destination.out_logic(state)
	elif source.in_logic:
		transition_logic = source.in_logic
	else:
		transition_logic = destination.out_logic
	
	exit_name = f'{source.region} -> {source.vanilla_destination}'
	connect(world, player, source.region, destination.region, transition_logic, exit_name)

	if both_ways:
		connect_transitions(world, player, destination, source, False)

def get_and_connect_doors(world: MultiWorld, player: int, worldstate: LaMulanaWorldState, s: LaMulanaLogicShortcuts):
	doors = worldstate.get_doors()
	door_logic = worldstate.door_requirement_logic(s)
	for door_name, door_data in doors.items():
		if not door_data.is_oneway:
			if not worldstate.door_rando or (door_data.is_nonboss and not worldstate.include_nonboss):
				target_name = door_data.vanilla_destination
				logic_type = door_data.vanilla_requirement
			else:
				target_name, logic_type = worldstate.door_map[door_name]
			target = doors[target_name]
			connection_logic = door_logic[logic_type]
			if worldstate.include_nonboss and logic_type == 'Key':
				#Doors without a warp within region - hopefully, fairy timer shouldn't be an issue if you can warp anywhere and have boots
				if door_name in {'Inferno Spikes Door', 'Extinction Magatama Door', 'Birth Door', 'Retromausoleum Door'}:
					connection_logic = lambda state: state.has('Hermes\'s Boots', player) and s.state_key_fairy_access(state, False) and s.state_frontside_warp(state) and s.state_backside_warp(state)
				elif door_name in {'Surface Door', 'Mausoleum Door', 'Sun Door', 'Inferno Viy Door'}:
					connection_logic = lambda state: s.state_key_fairy_access(state, True, True)
				elif door_name in {'Graveyard Door', 'Ruin Lower Door'}:
					connection_logic = lambda state: s.state_key_fairy_access(state, True, False)
				elif door_name == 'Illusion Door':
					connection_logic = lambda state: s.state_key_fairy_access(state, False) and (state.can_reach('Gate of Illusion [Middle]', 'Region', player) or s.state_backside_warp(state))

			exit_name = f'{door_name} -> {target_name}'

			if target_name == 'Endless One-way Exit':
				connect(world, player, door_data.region, target.region, lambda state: connection_logic(state) and state.has('Holy Grail', player) if callable(connection_logic) else lambda state: state.has('Holy Grail', player), exit_name)
			else:
				connect(world, player, door_data.region, target.region, connection_logic, exit_name)


def connect(world: MultiWorld, player: int, source: str, target: str, logic: Optional[Callable[CollectionState,bool]] = None, exit_name=None):
	source_region = world.get_region(source, player)
	target_region = world.get_region(target, player)

	exit_data = {target: exit_name} if exit_name else [target]

	source_region.add_exits(exit_data, {target: logic} if logic else None)


def create_location(player: int, location_data: LocationData, region: Region, additional_logic: Optional[Callable]=None):
	location = Location(player, location_data.name, location_data.code, region)
	if additional_logic:
		location.access_rule = lambda state: additional_logic(state) and location_data.logic(state)
	else:
		location.access_rule = location_data.logic
	return location

def create_region(world: MultiWorld, player: int, region_name: str, locations_per_region: Dict[str, List[LocationData]], npcs_per_region: Dict[str,LaMulanaNPCDoor], cursed_chests: Optional[Set[str]] = {}):
	region = Region(region_name, player, world)
	if region_name in locations_per_region:
		for location_data in locations_per_region[region_name]:
			cursed_logic = (lambda state: state.has('Mulana Talisman', player)) if cursed_chests and location_data.name in cursed_chests else None
			location = create_location(player, location_data, region, cursed_logic)
			region.locations.append(location)
	if region_name in npcs_per_region:
		for npc_door in npcs_per_region[region_name]:
			for location_data in npc_door.checks:
				location = create_location(player, location_data, region, npc_door.logic)
				region.locations.append(location)
	return region

