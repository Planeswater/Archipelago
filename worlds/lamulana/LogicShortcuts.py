from BaseClasses import CollectionState
from typing import TYPE_CHECKING
from .Options import starting_location_names, StartingWeapon

if TYPE_CHECKING:
	from . import LaMulanaWorld


class LaMulanaLogicShortcuts:
	player: int

	flag_specific_ankh_jewels: bool
	flag_autoscan: bool
	flag_ancient_lamulanese: bool
	flag_ice_cape_lava: bool
	flag_flare_gun_extinction: bool
	flag_key_fairy_combo_required: bool
	flag_subweapon_only: bool
	flag_pistol_start: bool
	flag_raindrop: bool
	flag_catpause: bool
	flag_lamp_glitch: bool
	is_frontside_start: bool

	def __init__(self, world: "LaMulanaWorld"):
		self.player = world.player
		self.flag_specific_ankh_jewels = bool(world.options.GuardianSpecificAnkhJewels)
		self.flag_autoscan = bool(world.options.AutoScanGrailTablets)
		self.flag_ancient_lamulanese = bool(world.options.AncientLaMulaneseLearned)
		self.flag_ice_cape_lava = bool(world.options.RequireIceCape)
		self.flag_flare_gun_extinction = bool(world.options.RequireFlareGun)
		self.flag_key_fairy_combo_required = bool(world.options.RequireKeyFairyCombo)
		self.flag_subweapon_only = bool(world.options.SubweaponOnly)
		self.flag_pistol_start = world.options.StartingWeapon == StartingWeapon.option_pistol
		self.flag_raindrop = bool(world.options.RaindropsInLogic)
		self.flag_catpause = bool(world.options.CatPausingInLogic)
		self.flag_lamp_glitch = bool(world.options.LampGlitchInLogic)

		starting_location = starting_location_names[world.options.StartingLocation.value]
		self.is_frontside_start = starting_location in {'surface', 'guidance', 'mausoleum', 'sun', 'spring', 'inferno', 'extinction', 'twin (front)', 'endless', 'gate of time (surface)'}

	# Could add +1 if revive combo was on, but that would turn move.exe and randc.exe into progression
	def get_health_count(self, state: CollectionState) -> int:
		orb_locations = ['Surface', 'Gate of Guidance', 'Mausoleum of the Giants', 'Temple of the Sun', 'Spring in the Sky', 'Tower of Ruin', 'Chamber of Extinction', 'Twin Labyrinths', 'Dimensional Corridor', 'Shrine of the Mother']
		return len([orb for orb in orb_locations if state.has(f'Sacred Orb ({orb})', self.player)])

	def attack_whip(self, state: CollectionState) -> bool:
		return state.has_any(("Leather Whip", "Chain Whip", "Flail Whip"), self.player)

	def attack_empowered_key_sword(self, state: CollectionState) -> bool:
		return state.has_all(("Key Sword", "Recited All Mantras"), self.player)

	def attack_shuriken(self, state: CollectionState) -> bool:
		return state.has_all(("Shuriken", "Shuriken Ammo"), self.player)

	def attack_ring_shuriken(self, state: CollectionState) -> bool:
		return state.has_all(("Shuriken", "Shuriken Ammo", "Ring"), self.player)

	def attack_rolling_shuriken(self, state: CollectionState) -> bool:
		return state.has_all(("Rolling Shuriken", "Rolling Shuriken Ammo"), self.player)

	def attack_earth_spear(self, state: CollectionState) -> bool:
		return state.has_all(("Earth Spear", "Earth Spear Ammo"), self.player)

	def attack_flare_gun(self, state: CollectionState) -> bool:
		return state.has_all(("Flare Gun", "Flare Gun Ammo"), self.player)

	def attack_ring_flare_gun(self, state: CollectionState) -> bool:
		return state.has_all(("Flare Gun", "Flare Gun Ammo", "Ring"), self.player)

	def attack_bomb(self, state: CollectionState) -> bool:
		return state.has_all(("Bomb", "Bomb Ammo"), self.player)

	def attack_ring_bomb(self, state: CollectionState) -> bool:
		return state.has_all(("Bomb", "Bomb Ammo", "Ring"), self.player)

	def attack_chakram(self, state: CollectionState) -> bool:
		return state.has_all(("Chakram", "Chakram Ammo"), self.player)

	def attack_ring_chakram(self, state: CollectionState) -> bool:
		return state.has_all(("Chakram", "Chakram Ammo", "Ring"), self.player)

	def attack_caltrops(self, state: CollectionState) -> bool:
		return state.has_all(("Caltrops", "Caltrops Ammo"), self.player)

	# Pistol ammo is expensive - unless it's free (pistol start or subweapon only flag), logically expect fairy access for item fairy grinding
	def attack_pistol(self, state: CollectionState) -> bool:
		return state.has_all(("Pistol", "Pistol Ammo"), self.player) and (self.flag_subweapon_only or self.flag_pistol_start or state.has('Fairies Unlocked', self.player))

	def attack_main(self, state: CollectionState) -> bool:
		return self.attack_whip(state) or state.has_any(("Knife", "Katana", "Axe", "Key Sword"), self.player)

	def attack_above(self, state: CollectionState) -> bool:
		return self.attack_whip(state) or state.has("Axe", self.player)

	def attack_below(self, state: CollectionState) -> bool:
		return state.has_any(("Axe", "Knife", "Katana"), self.player)

	def attack_far(self, state: CollectionState) -> bool:
		return self.attack_whip(state) or state.has_any(("Key Sword", "Axe"), self.player)

	def attack_vertical(self, state: CollectionState) -> bool:
		return state.has_all(("Flare Gun", "Flare Gun Ammo", "Earth Spear", "Earth Spear Ammo"), self.player)

	def attack_4(self, state: CollectionState) -> bool:
		return self.attack_5(state) or state.has("Chain Whip", self.player)

	def attack_5(self, state: CollectionState) -> bool:
		return state.has_any(("Flail Whip", "Katana", "Axe"), self.player) or self.attack_empowered_key_sword(state)

	def attack_dps(self, state: CollectionState) -> bool:
		return state.has_any(("Chain Whip", "Flail Whip", "Axe", "Katana"), self.player) or self.attack_empowered_key_sword(state)

	def attack_forward(self, state: CollectionState) -> bool:
		return self.attack_main(state) or self.attack_s_straight(state) or self.attack_rolling_shuriken(state) or self.attack_bomb(state) or self.attack_caltrops(state)

	def attack_s_straight(self, state: CollectionState) -> bool:
		return self.attack_shuriken(state) or self.attack_chakram(state) or self.attack_pistol(state)

	def attack_s_above(self, state: CollectionState) -> bool:
		return self.attack_flare_gun(state) or self.attack_caltrops(state)

	def attack_chest(self, state: CollectionState) -> bool:
		return self.attack_forward(state) or self.attack_earth_spear(state)

	def attack_chest_any(self, state: CollectionState) -> bool:
		return self.attack_chest(state) or self.attack_flare_gun(state)

	def attack_subweapon(self, state: CollectionState) -> bool:
		return self.attack_shuriken(state) or self.attack_rolling_shuriken(state) or self.attack_earth_spear(state) or self.attack_flare_gun(state) or self.attack_bomb(state) or self.attack_chakram(state) or self.attack_caltrops(state) or self.attack_pistol(state)

	def state_literacy(self, state: CollectionState) -> bool:
		return state.has_all(("Hand Scanner", "reader.exe"), self.player)

	def state_mobility(self, state: CollectionState) -> bool:
		return state.has_any(("Hermes' Boots", "Feather"), self.player)

	def state_lamp(self, state: CollectionState) -> bool:
		return state.has_all(("Lamp of Time", "Lamp Recharge"), self.player)

	def state_extinction_light(self, state: CollectionState) -> bool:
		return not self.flag_flare_gun_extinction or self.attack_flare_gun(state)

	def state_water_swim(self, state: CollectionState, amount: int) -> bool:
		if state.has('Scalesphere', self.player):
			return True
		return self.get_health_count(state) >= amount

	def state_lava_swim(self, state: CollectionState, amount: int) -> bool:
		if self.flag_ice_cape_lava:
			return state.has("Ice Cape", self.player)
		return state.has("Ice Cape", self.player) or self.get_health_count(state) >= amount

	def state_shield(self, state: CollectionState) -> bool:
		return state.has_any(("Silver Shield", "Angel Shield"), self.player)

	def fairy_point_reachable(self, state: CollectionState, warp_required=True, frontside=True) -> bool:
		if not state.has('Fairies Unlocked', self.player):
			return False
		if warp_required and not (self.state_frontside_warp(state) if frontside else self.state_backside_warp(state)):
			return False
		for region in {'Spring in the Sky [Main]', 'Chamber of Extinction [Main]', 'Twin Labyrinths [Lower]', 'Endless Corridor [3F Upper]', 'Gate of Illusion [Middle]', 'Temple of Moonlight [Lower]', 'Tower of the Goddess [Lower]', 'Shrine of the Mother [Main]'}:
			if state.can_reach_region(region, self.player):
				return True
		return False

	def state_key_fairy_access(self, state: CollectionState, warp_required=True, frontside=True) -> bool:
		return self.fairy_point_reachable(state, warp_required, frontside) and (state.has_all(("miracle.exe", "mekuri.exe"), self.player) or not self.flag_key_fairy_combo_required)

	def state_read_grail(self, state: CollectionState) -> bool:
		return self.flag_autoscan or self.state_literacy(state)

	def state_ancient_lamulanese(self, state: CollectionState) -> bool:
		if self.flag_ancient_lamulanese:
			return True
		for region in {'Tower of Ruin [La-Mulanese]', 'Chamber of Birth [Northeast]', 'Shrine of the Mother [Seal]'}:
			if not state.can_reach_region(region, self.player):
				return False
		move_past_shrine_skulls = state.has('Removed Shrine Skulls', self.player) or self.guardian_count(state) >= 8 or self.glitch_raindrop(state)
		return move_past_shrine_skulls and self.state_literacy(state)

	def state_frontside_warp(self, state: CollectionState) -> bool:
		return state.has("Holy Grail", self.player) and self.state_read_grail(state) and (state.has("mirai.exe", self.player) or self.is_frontside_start)

	def state_backside_warp(self, state: CollectionState) -> bool:
		return state.has("Holy Grail", self.player) and self.state_read_grail(state) and (state.has("mirai.exe", self.player) or not self.is_frontside_start)

	# Only relevant if NPC rando is on
	def combo_dev_npcs(self, state: CollectionState) -> bool:
		return state.has_all(("miracle.exe", "mirai.exe"), self.player)

	def glitch_raindrop(self, state: CollectionState) -> bool:
		return self.flag_raindrop and state.has_all(("Hermes' Boots", "Grapple Claw"), self.player)

	def glitch_catpause(self, state: CollectionState) -> bool:
		return self.flag_catpause

	def glitch_lamp(self, state: CollectionState) -> bool:
		return self.flag_lamp_glitch and self.state_lamp(state)

	def guardian_count(self, state: CollectionState) -> int:
		counter = 0
		for boss in {'Amphisbaena Defeated', 'Sakit Defeated', 'Ellmac Defeated', 'Bahamut Defeated', 'Viy Defeated', 'Palenque Defeated', 'Baphomet Defeated', 'Tiamat Defeated'}:
			if state.has(boss, self.player):
				counter += 1
		return counter

	def has_ankh_jewel(self, state: CollectionState, guardian: str) -> bool:
		if self.flag_specific_ankh_jewels:
			return state.has(f'Ankh Jewel ({guardian})', self.player)
		return state.has('Ankh Jewel', self.player, 9 if guardian == 'Mother' else 8)

	def sun_watchtower(self, state: CollectionState) -> bool:
		return self.attack_forward(state) or self.attack_flare_gun(state)

	def bronze_mirror_chest_logic(self, state: CollectionState) -> bool:
		if self.glitch_raindrop(state) and (self.attack_rolling_shuriken(state) or self.attack_earth_spear(state) or self.attack_bomb(state)):
			return True
		reach_extinction_map = state.can_reach_region('Chamber of Extinction [Map]', self.player)
		if self.glitch_lamp(state) and (reach_extinction_map or state.has('Holy Grail', self.player)) and (self.attack_forward(state) or self.attack_flare_gun(state)):
			return True
		if self.glitch_catpause(state) and reach_extinction_map and state.has('Feather', self.player) and self.attack_chest(state):
			return True
		return reach_extinction_map and state.has('Flooded Temple of the Sun', self.player) and (self.attack_forward(state) or self.attack_flare_gun(state))

	def spring_npc(self, state: CollectionState) -> bool:
		can_escape = state.has_any(('Leather Whip', 'Chain Whip', 'Flail Whip', 'Axe', 'Holy Grail'), self.player) or self.state_shield(state) or self.attack_shuriken(state) or self.attack_flare_gun(state) or self.attack_caltrops(state) or (self.state_water_swim(state, 1) and self.attack_chest(state))
		if not can_escape:
			return False
		if self.attack_earth_spear(state) or self.attack_bomb(state) or self.attack_caltrops(state) or self.attack_flare_gun(state) or state.has_any(('Knife', 'Axe', 'Katana'), self.player):
			return True
		return (state.has('Helmet', self.player) or self.state_water_swim(state, 1)) and state.has_any(('Leather Whip', 'Chain Whip', 'Flail Whip', 'Key Sword'), self.player)

	def endless_oneway_open(self, state: CollectionState, worldstate) -> bool:
		if worldstate and worldstate.include_oneways:
			if worldstate.transition_map['Endless L1'] == 'Birth R1':
				return state.has_all(('Skanda Defeated', 'Holy Grail'), self.player)
			if worldstate.transition_map['Endless L1'] in ['Illusion R1', 'Illusion R2']:
				return state.has_all(('Illusion Unlocked', 'Holy Grail'), self.player)
			return state.has('Holy Grail', self.player)
		return True

	def moonlight_face(self, state: CollectionState) -> bool:
		return self.attack_caltrops(state) or self.attack_shuriken(state) or self.attack_rolling_shuriken(state) or self.attack_chakram(state) or self.attack_bomb(state) or self.attack_pistol(state)

	def nuwa_access(self, state: CollectionState, worldstate) -> bool:
		return state.has_all(('NPC: Philosopher Alsedana', 'Feather', worldstate.get_seal_name('Nuwa')), self.player)

	def all_mantras(self, state: CollectionState) -> bool:
		# All the regions where you need to learn + chant mantras - excluding Illusion since that's where the event is placed
		for region in {'Gate of Guidance [Main]', 'Graveyard of the Giants [East]', 'Graveyard of the Giants [West]', 'Temple of the Sun [Sphinx]', 'Temple of Moonlight [Southeast]', 'Tower of the Goddess [Lower]', 'Tower of Ruin [Spirits]', 'Inferno Cavern [Spikes]', 'Inferno Cavern [Main]'}:
			if not state.can_reach_region(region, self.player):
				return False
		if not self.glitch_lamp(state):
			# Lamp glitch lets you skip first 3 mantras
			for region in {'Twin Labyrinths [Lower]', 'Chamber of Extinction [Magatama Left]', 'Chamber of Birth [Northeast]', 'Endless Corridor [1F]'}:
				if not state.can_reach_region(region, self.player):
					return False
		# Reach, read + chant mantras, ancient la-mulanese, viy -> sun sphinx destroyed, lamp glitch or samaranta for BAHRUN
		return state.has_all(('Hand Scanner', 'reader.exe', 'Djed Pillar', 'mantra.exe', 'Feather', 'Viy Defeated'), self.player) and self.state_ancient_lamulanese(state) and (self.glitch_lamp(state) or state.has('NPC: Philosopher Samaranta', self.player))

	def hell_temple_requirements(self, state: CollectionState) -> bool:
		for region in {'Surface [Main]', 'Gate of Guidance [Main]', 'Gate of Illusion [Dracuet]', 'Gate of Time [Guidance]'}:
			if not state.can_reach_region(region, self.player):
				return False
		warpless_fairy_reachable = state.can_reach_region('Gate of Illusion [Middle]', self.player)
		if not warpless_fairy_reachable and not state.can_reach_region('Gate of Illusion [Grail]', self.player):
			return False
		return state.has_all(('NPC: Mulbruk', 'Feather', 'Ice Cape', 'Holy Grail'), self.player) and self.state_key_fairy_access(state, not warpless_fairy_reachable, False) and (self.glitch_raindrop(state) or state.has('NPC: Xelpud', self.player)) and self.get_health_count(state) >= 2 and self.attack_forward(state)
