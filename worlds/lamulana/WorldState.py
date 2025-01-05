from typing import TYPE_CHECKING, Callable, NamedTuple
from BaseClasses import MultiWorld, CollectionState, Location, LocationProgressType, Item, ItemClassification
from .Options import RandomizeTransitions, RandomizeBacksideDoors, StartingLocation, starting_weapon_names
from .Locations import get_locations_by_region
from .LogicShortcuts import LaMulanaLogicShortcuts
from .Items import item_table

if TYPE_CHECKING:
	from . import LaMulanaWorld


class LaMulanaTransition(NamedTuple):
	region: str
	vanilla_destination: str
	in_logic: Callable[[CollectionState], bool] | None = None
	out_logic: Callable[[CollectionState], bool] | None = None
	is_oneway: bool = False


class LaMulanaDoor(NamedTuple):
	region: str
	vanilla_destination: str
	vanilla_requirement: str
	is_oneway: bool = False
	is_nonboss: bool = False


class LaMulanaWorldState:
	world: "LaMulanaWorld"
	multiworld: MultiWorld
	player: int
	transition_rando: bool
	include_oneways: bool
	door_rando: bool
	include_nonboss: bool
	transition_map: dict[str, str] = {}
	door_map: dict[str, tuple[str, str]]= {}
	npc_rando: bool
	include_dracuet: bool
	npc_mapping: dict[str, str]
	cursed_chests: set[str]
	seal_map: dict[str, int]
	is_surface_start: bool

	def __init__(self, world: 'LaMulanaWorld'):
		self.world = world
		self.multiworld = world.multiworld
		self.player = world.player
		self.transition_rando = bool(world.options.RandomizeTransitions)
		self.include_oneways = world.options.RandomizeTransitions == RandomizeTransitions.option_full
		self.door_rando = bool(world.options.RandomizeBacksideDoors)
		self.include_nonboss = world.options.RandomizeBacksideDoors == RandomizeBacksideDoors.option_full
		self.npc_rando = bool(world.options.RandomizeNPCs)
		self.include_dracuet = bool(world.options.RandomizeDracuetsShop)
		self.randomize_cursed_chests = world.options.RandomizeCursedChests
		self.is_surface_start = world.options.StartingLocation == StartingLocation.option_surface

		self.set_cursed_chests()
		self.set_seal_values()
		if self.npc_rando:
			self.build_npc_mapping()

	# Called in Regions.py after "internal" regions (within the same field, or fixed exits) have been connected
	# and immediately before using worldstate to connect transitions and doors
	def randomize_doors(self, s: LaMulanaLogicShortcuts):
		if self.door_rando:
			door_list = list(self.get_doors().keys())
			requirements_list = list(self.door_requirement_logic(s).keys())
			if not self.include_nonboss:
				requirements_list.remove('Open')
				requirements_list.remove('Key')
				for doorname in {'Dimensional Door', 'Endless One-way Exit', 'Extinction Key Door', 'Retromausoleum Door'}:
					door_list.remove(doorname)
			success = False
			while not success:
				success = self.build_door_layout(door_list, requirements_list, s)

	def build_door_layout(self, door_list: list[str], requirements_list: list[str], s: LaMulanaLogicShortcuts):
		self.door_map = {}
		door_data = self.get_doors()

		# Remove and re-append Dimensional Door/Open after shuffling so they're always paired together
		if self.include_nonboss:
			door_list.remove('Dimensional Door')
			requirements_list.remove('Open')

		self.world.random.shuffle(door_list)
		self.world.random.shuffle(requirements_list)

		if self.include_nonboss:
			door_list.append('Dimensional Door')
			requirements_list.append('Open')

		for ndx in range(len(requirements_list)):
			req = requirements_list[ndx]
			door1 = door_list[2 * ndx]
			door2 = door_list[2 * ndx + 1]
			# 2/3 of one-ways (Guidance, Ruin Top, Endless) have checks, so return False if connected to each other
			if door_data[door1].is_oneway and door_data[door2].is_oneway:
				return False
			if 'Retromausoleum Door' in {door1, door2} and req not in {'Open', 'Key'}:
				req = 'Open'
			if not s.flag_lamp_glitch:
				if 'Inferno Viy Door' in {door1, door2}:
					if req == 'Viy':
						return False
					if req == 'Palenque' and not self.include_oneways and not s.flag_raindrop:
						return False
					if door_data[door1].is_oneway or door_data[door2].is_oneway:
						return False
			self.door_map[door1] = (door2, req)
			self.door_map[door2] = (door1, req)
		return True

	# Copies self.multiworld.state and gives it all progression items, to simulate full movement ability
	def build_simulated_state(self, give_ammo=True) -> CollectionState:
		simulated_state = self.multiworld.state.copy()
		flag_alt_mother_ankh = self.world.options.AlternateMotherAnkh
		flag_specific_ankh_jewels = self.world.options.GuardianSpecificAnkhJewels

		for item_name, item_data in item_table.items():
			if item_data.progression:
				item_count = item_data.number
				if item_count == 0:
					if give_ammo and item_data.category == 'ShopInventory':
						item_count = 1
					if item_name == 'Ankh Jewel' and not flag_specific_ankh_jewels:
						item_count = 9 if flag_alt_mother_ankh else 8
					if item_name == 'Ankh Jewel (Mother)':
						if flag_specific_ankh_jewels and flag_alt_mother_ankh:
							item_count = 1
					elif item_name.startswith('Ankh Jewel (') and flag_specific_ankh_jewels:
						item_count = 1
				for _ in range(item_count):
					item = Item(item_name, ItemClassification.progression, item_data.code, self.player)
					simulated_state.collect(item)
		simulated_state.stale[self.player] = True
		return simulated_state

	# Called in Regions.py
	def randomize_transitions(self, s: LaMulanaLogicShortcuts):
		transitions = self.get_transitions(s)
		if not self.include_oneways:
			for direction in transitions.keys():
				transitions[direction] = {name: data for name, data in transitions[direction].items() if not data.is_oneway}
		self.build_transition_layout(transitions)

	def build_transition_layout(self, transitions: dict[str, dict[str, LaMulanaTransition]]):
		self.transition_map = {}
		if self.include_oneways:
			self.transition_map['Endless L1'] = self.world.random.choice(list(transitions['right'].keys()))

		left_transition_list = [name for name in transitions['left'].keys() if name != 'Endless L1']
		up_transition_list = list(transitions['up'].keys())
		right_transition_list = list(transitions['right'].keys())
		down_transition_list = list(transitions['down'].keys())

		self.world.random.shuffle(left_transition_list)
		self.world.random.shuffle(up_transition_list)

		for ndx, left_transition in enumerate(left_transition_list):
			right_transition = right_transition_list[ndx]
			self.transition_map[left_transition] = right_transition
			self.transition_map[right_transition] = left_transition
		for ndx, up_transition in enumerate(up_transition_list):
			down_transition = down_transition_list[ndx]
			self.transition_map[up_transition] = down_transition
			self.transition_map[down_transition] = up_transition

	def layout_fulfills_accessibility(self, state: CollectionState):
		state = state.copy()
		accessibility = self.world.options.accessibility.value

		beatable_fulfilled = False

		def location_relevant(location: Location) -> bool:
			if location.progress_type != LocationProgressType.EXCLUDED and (accessibility == 'locations' or location.is_event or location.progress_type == LocationProgressType.PRIORITY):
				return True
			return False

		def all_done() -> bool:
			if not beatable_fulfilled:
				return False
			if accessibility != 'minimal' and len(locations) > 0:
				return False
			# Make sure shops aren't made inaccessible due to the transition map, since we will place progression (ammo) on them
			# Reaching Fobos, Mulbruk, and Fairy Queen is already covered by the seed being beatable
			if not state.can_reach_region('Gate of Time [Surface]', self.player):
				if self.shop_npc_found({'8-bit Elder'}) or self.npc_mapping['8-bit Elder'] == 'Elder Xelpud':
					return False
			return True

		def victory(state: CollectionState) -> bool:
			return state.has_all(('Mother Defeated', 'NPC: Mulbruk'), self.player)

		locations = [location for location in self.multiworld.get_locations(self.player) if location_relevant(location)]
		while locations:
			state.update_reachable_regions(self.player)
			sphere: list[Location] = []

			for n in range(len(locations) - 1, -1, -1):
				if locations[n].can_reach(state):
					sphere.append(locations.pop(n))
			if not sphere:
				return False

			for location in sphere:
				if location.is_event:
					item_name = location.item.name if location.item is not None else location.name
					# Special case for Lamp Recharge events, since item and location names don't match
					if 'Lamp Recharge' in item_name:
						item_name = 'Lamp Recharge'
					event_item = Item(item_name, ItemClassification.progression, None, self.player)
					state.collect(event_item)
					state.stale[self.player] = True

			if victory(state):
				beatable_fulfilled = True

			if all_done():
				return True

		return False

	def randomize_npcs(self, npc_list: list[str]) -> dict[str, str]:
		randomized_list = npc_list.copy()
		self.world.random.shuffle(randomized_list)
		return {npc_list[i]: randomized_list[i] for i in range(len(npc_list))}

	def get_shop_names(self) -> set[str]:
		shop_npcs = {'Nebur', 'Sidro', 'Modro', 'Penadvent of Ghost', 'Greedy Charlie', 'Shalom III', 'Usas VI', 'Kingvalley I', 'Mr. Fishman (Original)', 'Mr. Fishman (Alt)', 'Hot-blooded Nemesistwo', 'Operator Combaker', 'Yiegah Kungfu', 'Yiear Kungfu', 'Arrogant Sturdy Snake', 'Arrogant Metagear', 'Affected Knimare', 'Mover Athleland', 'Giant Mopiran', 'Kingvalley II', 'Energetic Belmont', 'Mechanical Efspi', 'Mudman Qubert'}
		if self.include_dracuet:
			shop_npcs.add('Tailor Dracuet')
		if not self.is_surface_start:
			shop_npcs.add('Starting')
		return shop_npcs

	def get_shop_location_names(self) -> set[str]:
		locations: set[str] = set()
		shop_npc_names = self.get_shop_names()
		for npc_name in shop_npc_names:
			locations.add(f'{npc_name} Shop Item 1')
			locations.add(f'{npc_name} Shop Item 2')
			locations.add(f'{npc_name} Shop Item 3')
		return locations

	def shop_npc_found(self, npc_doors: set[str]) -> bool:
		shop_npc_found = False
		shop_names = self.get_shop_names()
		for door in npc_doors:
			if self.npc_mapping[door] in shop_names:
				return True
		return False

	def npc_rando_checks_passed(self) -> bool:
		if self.is_surface_start:
			# Surface start - make sure Xelpud and a shop are accessible
			starting_weapon = starting_weapon_names[self.world.options.StartingWeapon.value]
			if starting_weapon in {'Knife', 'Rolling Shuriken', 'Flare Gun', 'Bomb', 'Caltrops'}:
				# Case: starting weapon can't break Mekuri Wall - Xelpud must be vanilla, with a shop available
				if self.npc_mapping['Elder Xelpud'] != 'Elder Xelpud':
					return False
				if not self.shop_npc_found({'Nebur', 'Sidro', 'Modro', 'Moger', 'Hiner'}):
					return False
			else:
				# Xelpud must be vanilla or at former mekuri master
				if self.npc_mapping['Former Mekuri Master'] == 'Elder Xelpud':
					# Case: subweapon that can break mekuri wall, ammo needs to be at xelpud
					if starting_weapon in {'Shuriken', 'Chakram', 'Pistol', 'Earth Spear'}:
						if not self.shop_npc_found({'Elder Xelpud'}):
							return False
					else:
						# Case: main weapon that can break mekuri wall. Shop anywhere else
						if not self.shop_npc_found({'Elder Xelpud', 'Nebur', 'Sidro', 'Modro', 'Moger', 'Hiner'}):
							return False
				elif self.npc_mapping['Elder Xelpud'] != 'Elder Xelpud':
					return False
				if not self.shop_npc_found({'Nebur', 'Sidro', 'Modro', 'Moger', 'Hiner'}):
					return False
		else:
			# Non-surface start - just make Xelpud isn't locked behind himself
			for surface_npc in {'Nebur', 'Sidro', 'Modro', 'Moger', 'Hiner'}:
				if self.npc_mapping[surface_npc] == 'Elder Xelpud':
					return False
				if self.npc_mapping[surface_npc] == 'Yiegah Kungfu' and self.npc_mapping['Yiear Kungfu'] == 'Elder Xelpud':
					return False
				if self.npc_mapping[surface_npc] == 'Fairy Queen' and self.npc_mapping['Mr. Fishman (Alt)'] == 'Elder Xelpud':
					return False
		# Unless fixed, the door to the Moonlight shop area (Kingvalley II) does not open during escape
		if self.npc_mapping['Kingvalley II'] == 'Mulbruk':
			return False
		if self.npc_mapping['Yiear Kungfu'] == 'Yiegah Kungfu':
			return False
		if self.npc_mapping['Mr. Fishman (Alt)'] == 'Fairy Queen':
			return False
		if self.npc_mapping['Mr. Fishman (Alt)'] == 'Yiegah Kungfu' and self.npc_mapping['Yiear Kungfu'] == 'Fairy Queen':
			return False
		if not self.transition_rando and not self.include_nonboss:
			if self.npc_mapping['8-bit Elder'] == 'Fairy Queen':
				return False
			if self.npc_mapping['8-bit Elder'] == 'Yiegah Kungfu' and self.npc_mapping['Yiear Kungfu'] == 'Fairy Queen':
				return False
		if 'Tailor Dracuet' in self.npc_mapping:
			if self.npc_mapping['Tailor Dracuet'] in {'Mulbruk', 'Fairy Queen', 'Elder Xelpud'}:
				return False
			if self.npc_mapping['Tailor Dracuet'] == 'Yiegah Kungfu' and self.npc_mapping['Yiear Kungfu'] in {'Mulbruk', 'Fairy Queen', 'Elder Xelpud'}:
				return False
		return True

	def get_npc_names(self):
		npcs = self.get_npc_hint_order()
		npcs.extend(['Hiner', 'Moger', 'Priest Zarnac', 'Priest Xanado', 'Priest Madomo', 'Priest Hidlyda', 'Priest Gailious', 'Priest Romancis', 'Priest Aramo', 'Priest Triton', 'Priest Jaguarfiv', 'duplex', 'Giant Thexde', 'Samieru', 'Naramura', 'Priest Laydoc', 'Priest Ashgine', '8-bit Elder'])
		return npcs

	def build_npc_mapping(self):
		npc_names = self.get_npc_names()
		self.npc_mapping = self.randomize_npcs(npc_names)
		while not self.npc_rando_checks_passed():
			self.npc_mapping = self.randomize_npcs(npc_names)

	def set_cursed_chests(self):
		if self.randomize_cursed_chests:
			possible_cursed_chests = []
			locations_by_region = get_locations_by_region(self.world)
			for locationlist in locations_by_region.values():
				for location in locationlist:
					if location.code and location.is_cursable:
						possible_cursed_chests.append(location.name)
			curse_count = min(len(possible_cursed_chests), self.world.options.CursedChestCount.value)
			self.cursed_chests = set(self.world.random.sample(possible_cursed_chests, curse_count))
		else:
			# 4 vanilla cursed chests
			self.cursed_chests = {'Shrine of the Mother - Crystal Skull Chest', 'Chamber of Birth - Dimensional Key Chest', 'Tower of Ruin - Djed Pillar Chest', 'Dimensional Corridor - Magatama Jewel Chest'}

	def get_npc_hint_order(self):
		npcs = ['Elder Xelpud', 'Mulbruk', 'Fairy Queen', 'Philosopher Fobos', 'Philosopher Alsedana', 'Philosopher Giltoriyo', 'Philosopher Samaranta', 'Former Mekuri Master', 'Mr. Slushfund', 'Priest Alest', 'Nebur', 'Sidro', 'Modro', 'Penadvent of Ghost', 'Greedy Charlie', 'Shalom III', 'Usas VI', 'Kingvalley I', 'Mr. Fishman (Original)', 'Mr. Fishman (Alt)', 'Hot-blooded Nemesistwo', 'Operator Combaker', 'Yiegah Kungfu', 'Yiear Kungfu', 'Arrogant Sturdy Snake', 'Arrogant Metagear', 'Affected Knimare', 'Mover Athleland', 'Giant Mopiran', 'Kingvalley II', 'Energetic Belmont', 'Mechanical Efspi', 'Mudman Qubert']
		if self.include_dracuet:
			npcs.append('Tailor Dracuet')
		return npcs

	def get_seal_spoiler_order(self):
		return ['Birth Seal Chest', 'Surface Coin Chest Seal', 'Crucifix Chest/3 Lights', 'Mulbruk\'s Seal', 'Sun Right Exits', 'Sun Discount Shop',
		'Spring Sacred Orb Chest', 'Mr. Fishman\'s Shop', 'Bahamut\'s Room', 'Pazuzu Seal', 'Life Seal Chest', 'Endless Shop Seal',
		'Chi You Seal', 'Gauntlet Chest', 'Path to Anubis', 'Nuwa', 'Dimensional Sacred Orb Chest',
		'Extinction Perma-light (Extinction)', 'Extinction Perma-light (Birth)', 'Shrine Laptop Room',
		'Crystal Skull Chest',
		'Shrine 4 Seals (Origin)', 'Shrine 4 Seals (Birth)', 'Shrine 4 Seals (Life)', 'Shrine 4 Seals (Death)',
		'Mother (Origin)', 'Mother (Birth)', 'Mother (Life)', 'Mother (Death)']

	def get_seal_name(self, name):
		if not self.seal_map:
			return None
		seal_value = self.seal_map[name]
		return {1: 'Origin Seal', 2: 'Birth Seal', 3: 'Life Seal', 4: 'Death Seal'}[seal_value]

	def set_seal_values(self):
		self.seal_map = {}
		seal_rando = self.world.options.RandomizeSeals
		for seal_name in {'Birth Seal Chest', 'Mulbruk\'s Seal', 'Sun Right Exits', 'Mr. Fishman\'s Shop', 'Bahamut\'s Room', 'Endless Shop Seal', 'Shrine 4 Seals (Origin)', 'Mother (Origin)'}:
			self.seal_map[seal_name] = self.world.random.choice([1, 2, 3, 4]) if seal_rando else 1
		for seal_name in {'Spring Sacred Orb Chest', 'Pazuzu Seal', 'Life Seal Chest', 'Chi You Seal', 'Path to Anubis', 'Shrine 4 Seals (Birth)', 'Mother (Birth)'}:
			self.seal_map[seal_name] = self.world.random.choice([1, 2, 3, 4]) if seal_rando else 2
		for seal_name in {'Crucifix Chest/3 Lights', 'Surface Coin Chest Seal', 'Gauntlet Chest', 'Extinction Perma-light (Extinction)', 'Extinction Perma-light (Birth)', 'Crystal Skull Chest', 'Shrine 4 Seals (Life)', 'Mother (Life)'}:
			self.seal_map[seal_name] = self.world.random.choice([1, 2, 3, 4]) if seal_rando else 3
		for seal_name in {'Sun Discount Shop', 'Nuwa', 'Dimensional Sacred Orb Chest', 'Shrine Laptop Room', 'Shrine 4 Seals (Death)', 'Mother (Death)'}:
			self.seal_map[seal_name] = self.world.random.choice([1, 2, 3, 4]) if seal_rando else 4

	def get_transitions(self, s: LaMulanaLogicShortcuts):
		transitions = {
			'left': {
				'Guidance L1': 		 LaMulanaTransition('Gate of Guidance [Main]', 'Surface R1'),
				'Mausoleum L1': 	 LaMulanaTransition('Mausoleum of the Giants', 'Endless R1'),
				'Sun L1': 			 LaMulanaTransition('Temple of the Sun [West]', 'Inferno R1', in_logic = lambda state: state.has('Buer Defeated', self.player)),
				'Graveyard L1': 	 LaMulanaTransition('Graveyard of the Giants [West]', 'Ruin R2'),
				'Moonlight L1': 	 LaMulanaTransition('Temple of Moonlight [Lower]', 'Pipe R1', in_logic = lambda state: False, out_logic = lambda state: state.has('Holy Grail', self.player) or (s.moonlight_face(state) and s.attack_below(state))),
				'Goddess L1':		 LaMulanaTransition('Tower of the Goddess [Spaulder]', 'Illusion R1', in_logic = lambda state: state.has('Plane Model', self.player) and s.state_mobility(state), out_logic = lambda state: state.has('Holy Grail', self.player) or (state.has('Plane Model', self.player) and s.state_mobility(state))),
				'Goddess L2':		 LaMulanaTransition('Tower of the Goddess [Lower]', 'Ruin R1', in_logic = lambda state: state.has('Plane Model', self.player)),
				'Ruin L1':			 LaMulanaTransition('Tower of Ruin [Illusion]', 'Illusion R2', in_logic = lambda state: False),
				'Extinction L1':	 LaMulanaTransition('Chamber of Extinction [Left Main]', 'Sun R1', in_logic = lambda state: s.state_extinction_light(state), out_logic = lambda state: s.state_extinction_light(state)),
				'Extinction L2':	 LaMulanaTransition('Chamber of Extinction [Map]', 'Sun R2', in_logic = lambda state: s.state_extinction_light(state), out_logic = lambda state: s.state_extinction_light(state)),
				'Birth L1':			 LaMulanaTransition('Chamber of Birth [Southeast]', 'Birth R1'),
				'Endless L1':		 LaMulanaTransition('Endless Corridor [1F]', 'Endless R1', in_logic = lambda state: state.has('Holy Grail', self.player), is_oneway=True),
				'Retroguidance L1':	 LaMulanaTransition('Gate of Time [Guidance]', 'Retrosurface R1'),
				'Pipe L1':			 LaMulanaTransition('Tower of the Goddess [Pipe]', 'Graveyard R1')
			},
			'right': {
				'Surface R1':		 LaMulanaTransition('Surface [Main]', 'Guidance L1', in_logic = lambda state: state.has('NPC: Xelpud', self.player) or s.glitch_raindrop(state), out_logic = lambda state: False),
				'Illusion R1':		 LaMulanaTransition('Gate of Illusion [Pot Room]', 'Goddess L1', out_logic = lambda state: state.has('Illusion Unlocked', self.player)),
				'Illusion R2':		 LaMulanaTransition('Gate of Illusion [Ruin]', 'Ruin L1', in_logic = lambda state: state.has('Illusion Unlocked', self.player) or s.glitch_raindrop(state), out_logic = lambda state: state.has('Illusion Unlocked', self.player)),
				'Graveyard R1':		 LaMulanaTransition('Graveyard of the Giants [Grail]', 'Pipe L1'),
				'Sun R1':			 LaMulanaTransition('Temple of the Sun [East]', 'Extinction L1', in_logic = lambda state: state.has_all(('Flooded Temple of the Sun', self.get_seal_name('Sun Right Exits')), self.player) and s.state_mobility(state), out_logic = lambda state: s.glitch_raindrop(state) or (s.glitch_lamp(state) and state.has('Holy Grail', self.player))),
				'Sun R2':			 LaMulanaTransition('Temple of the Sun [East]', 'Extinction L2', in_logic = lambda state: state.has_all(('Flooded Temple of the Sun', self.get_seal_name('Sun Right Exits')), self.player) or (s.glitch_lamp(state) and state.has('Holy Grail', self.player)), out_logic = lambda state: s.glitch_raindrop(state) or (s.glitch_lamp(state) and state.has('Holy Grail', self.player))),
				'Inferno R1':		 LaMulanaTransition('Inferno Cavern [Main]', 'Sun L1'),
				'Ruin R1':			 LaMulanaTransition('Tower of Ruin [Medicine]', 'Goddess L2'),
				'Ruin R2':			 LaMulanaTransition('Tower of Ruin [Southeast]', 'Graveyard L1'),
				'Birth R1':			 LaMulanaTransition('Chamber of Birth [Skanda]', 'Birth L1', in_logic = lambda state: state.has('Skanda Defeated', self.player) or s.glitch_raindrop(state), out_logic = lambda state: state.has('Skanda Defeated', self.player)),
				'Endless R1':		 LaMulanaTransition('Endless Corridor [1F]', 'Mausoleum L1'),
				'Retrosurface R1':	 LaMulanaTransition('Gate of Time [Surface]', 'Retroguidance L1'),
				'Pipe R1':			 LaMulanaTransition('Tower of the Goddess [Pipe]', 'Moonlight L1')
			},
			'up': {
				'Guidance U1':		 LaMulanaTransition('Gate of Guidance [Main]', 'Spring D1'),
				'Mausoleum U1':		 LaMulanaTransition('Mausoleum of the Giants', 'Guidance D1'),
				'Graveyard U1':		 LaMulanaTransition('Graveyard of the Giants [West]', 'Illusion D1', in_logic = lambda state: s.attack_chest(state), out_logic = lambda state: state.has('Holy Grail', self.player) or s.attack_chest(state)),
				'Graveyard U2':		 LaMulanaTransition('Graveyard of the Giants [East]', 'Goddess D1'),
				'Sun U1':			 LaMulanaTransition('Temple of the Sun [Top Entrance]', 'Guidance D2'),
				'Moonlight U1':		 LaMulanaTransition('Temple of Moonlight [Eden]', 'Illusion D2'),
				'Moonlight U2':		 LaMulanaTransition('Temple of Moonlight [Upper]', 'Twin D2', out_logic = lambda state: s.glitch_raindrop(state)),
				'Goddess U1':		 LaMulanaTransition('Tower of the Goddess [Lamp]', 'Birth D1', in_logic = lambda state: state.has('Plane Model', self.player), out_logic = lambda state: state.has('Plane Model', self.player)),
				'Goddess W1':		 LaMulanaTransition('Tower of the Goddess [Lamp]', 'Retromausoleum D1', in_logic = lambda state: False, out_logic = lambda state: state.has('Holy Grail', self.player), is_oneway=True),
				'Inferno U1':		 LaMulanaTransition('Inferno Cavern [Main]', 'Twin D1'),
				'Inferno U2':		 LaMulanaTransition('Inferno Cavern [Spikes]', 'Surface D1'),
				'Extinction U1':	 LaMulanaTransition('Chamber of Extinction [Main]', 'Shrine D1', in_logic = lambda state: s.state_extinction_light(state), out_logic = lambda state: s.state_extinction_light(state)),
				'Extinction U2':	 LaMulanaTransition('Chamber of Extinction [Magatama Right]', 'Surface D2', in_logic = lambda state: s.attack_chest(state) and state.has('Feather', self.player), out_logic = lambda state: state.has('Holy Grail', self.player) or (s.attack_chest(state) and state.has('Feather', self.player))),
				'Extinction U3':	 LaMulanaTransition('Chamber of Extinction [Ankh Upper]', 'Inferno W1', is_oneway=True),
				'Birth U1':			 LaMulanaTransition('Chamber of Birth [Northeast]', 'Graveyard D1'),
				'Twin U1':			 LaMulanaTransition('Twin Labyrinths [Loop]', 'Mausoleum D1'),
				'Twin U2':			 LaMulanaTransition('Twin Labyrinths [Poison 2]', 'Shrine D3', in_logic = lambda state: state.has('Twin Poison Cleared', self.player), out_logic = lambda state: state.has_any(('Holy Grail' 'Twin Statue'), self.player)),
				'Twin U3':			 LaMulanaTransition('Twin Labyrinths [Poseidon]', 'Dimensional D1', in_logic = lambda state: state.has_all(('Crystal Skull', 'Feather'), self.player), out_logic = lambda state: state.has('Holy Grail', self.player) or state.has_all(('Crystal Skull', 'Feather'), self.player), is_oneway=True),
				'Endless U1':		 LaMulanaTransition('Endless Corridor [2F]', 'Shrine D2', in_logic = lambda state: state.has('NPC: Philosopher Giltoriyo', self.player), out_logic = lambda state: state.has_any(('Holy Grail', 'NPC: Philosopher Giltoriyo'), self.player)),
				'Shrine U1':		 LaMulanaTransition('Shrine of the Mother [Main]', 'Endless D1'),
				'Retromausoleum U1': LaMulanaTransition('Gate of Time [Mausoleum Upper]', 'Retroguidance D1')
			},
			'down': {
				'Surface D1':		 LaMulanaTransition('Surface [Ruin Path Lower]', 'Inferno U2'),
				'Surface D2':		 LaMulanaTransition('Surface [Ruin Path Upper]', 'Extinction U2'),
				'Guidance D1':		 LaMulanaTransition('Gate of Guidance [Main]', 'Mausoleum U1'),
				'Guidance D2':		 LaMulanaTransition('Gate of Guidance [Main]', 'Sun U1'),
				'Illusion D1':		 LaMulanaTransition('Gate of Illusion [Lower]', 'Graveyard U1', in_logic = lambda state: state.has('Illusion Unlocked', self.player), out_logic = lambda state: state.has('Illusion Unlocked', self.player)),
				'Illusion D2':		 LaMulanaTransition('Gate of Illusion [Eden]', 'Moonlight U1'),
				'Mausoleum D1':		 LaMulanaTransition('Mausoleum of the Giants', 'Twin U1'),
				'Graveyard D1':		 LaMulanaTransition('Graveyard of the Giants [East]', 'Birth U1'),
				'Spring D1':		 LaMulanaTransition('Spring in the Sky [Main]', 'Guidance U1'),
				'Goddess D1':		 LaMulanaTransition('Tower of the Goddess [Grail]', 'Graveyard U2', in_logic = lambda state: state.has('Plane Model', self.player) or s.glitch_raindrop(state), out_logic = lambda state: False),
				'Inferno W1':		 LaMulanaTransition('Inferno Cavern [Lava]', 'Extinction U3', in_logic = lambda state: False, out_logic = lambda state: state.has('Holy Grail', self.player), is_oneway=True),
				'Birth D1':			 LaMulanaTransition('Chamber of Birth [West Entrance]', 'Goddess U1'),
				'Twin D1':			 LaMulanaTransition('Twin Labyrinths [Lower]', 'Inferno U1'),
				'Twin D2':			 LaMulanaTransition('Twin Labyrinths [Lower]', 'Moonlight U2'),
				'Endless D1':		 LaMulanaTransition('Endless Corridor [5F]', 'Shrine U1', in_logic = lambda state: state.has('Backbeard & Tai Sui Defeated', self.player), out_logic = lambda state: state.has('Holy Grail', self.player) or s.glitch_raindrop(state)),
				'Dimensional D1':	 LaMulanaTransition('Dimensional Corridor [Lower]', 'Twin U3', in_logic = lambda state: s.glitch_raindrop(state), out_logic = lambda state: state.has_all(('Feather', 'Holy Grail'), self.player) or s.glitch_raindrop(state), is_oneway=True),
				'Shrine D1':		 LaMulanaTransition('Shrine of the Mother [Lower]', 'Extinction U1', out_logic = lambda state: False),
				'Shrine D2':		 LaMulanaTransition('Shrine of the Mother [Seal]', 'Endless U1'),
				'Shrine D3':		 LaMulanaTransition('Shrine of the Mother [Map]', 'Twin U2'),
				'Retromausoleum D1': LaMulanaTransition('Gate of Time [Mausoleum Lower]', 'Goddess W1', in_logic = lambda state: s.attack_below(state) or s.attack_bomb(state) or s.attack_earth_spear(state) or s.attack_rolling_shuriken(state) or s.glitch_raindrop(state), out_logic = lambda state: state.has('Holy Grail', self.player) or s.attack_below(state) or s.attack_bomb(state) or s.attack_earth_spear(state) or s.attack_rolling_shuriken(state) or s.glitch_raindrop(state), is_oneway=True),
				'Retroguidance D1':	 LaMulanaTransition('Gate of Time [Guidance]', 'Retromausoleum U1')
			}
		}
		return transitions

	def get_transition_spoiler_order(self) -> list[str]:
		return [
			'Surface R1', 'Surface D1', 'Surface D2',
			'Guidance L1', 'Guidance U1', 'Guidance D1', 'Guidance D2',
			'Mausoleum L1', 'Mausoleum U1', 'Mausoleum D1',
			'Sun L1', 'Sun R1', 'Sun R2', 'Sun U1',
			'Spring D1',
			'Inferno R1', 'Inferno U1', 'Inferno U2',
			'Extinction L1', 'Extinction L2', 'Extinction U1', 'Extinction U2', 'Extinction U3',
			'Twin U1', 'Twin U2', 'Twin U3', 'Twin D1', 'Twin D2',
			'Endless L1', 'Endless R1', 'Endless U1', 'Endless D1',
			'Shrine U1', 'Shrine D1', 'Shrine D2', 'Shrine D3',
			'Illusion R1', 'Illusion R2', 'Illusion D1', 'Illusion D2',
			'Graveyard L1', 'Graveyard R1', 'Graveyard U1', 'Graveyard U2', 'Graveyard D1',
			'Moonlight L1', 'Moonlight U1', 'Moonlight U2',
			'Goddess L1', 'Goddess L2', 'Goddess U1', 'Goddess D1',
			'Ruin L1', 'Ruin R1', 'Ruin R2',
			'Birth L1', 'Birth R1', 'Birth U1', 'Birth D1',
			'Dimensional D1',
			'Retrosurface R1', 'Retroguidance L1', 'Retroguidance D1', 'Retromausoleum U1', 'Retromausoleum D1'
		]

	def get_transition_spoiler_names(self) -> dict[str, str]:
		return {
			'Surface R1': 'Surface (Entrance to La-Mulana Ruins)',
			'Surface D1': 'Surface (Sound Canyon)',
			'Surface D2': 'Surface (Underground Passage)',
			'Guidance L1': 'Gate of Guidance (Pillars Gate)',
			'Guidance U1': 'Gate of Guidance (Room of Courage)',
			'Guidance D1': 'Gate of Guidance (Monument of Time)',
			'Guidance D2': 'Gate of Guidance (Cliff of Radiance)',
			'Mausoleum L1': 'Mausoleum of the Giants (Moon Palace of the Giants)',
			'Mausoleum U1': 'Mausoleum of the Giants (Last Shrine)',
			'Mausoleum D1': 'Mausoleum of the Giants (Star Palace of the Giants)',
			'Sun L1': 'Temple of the Sun (Isis\'s Anterior Chamber)',
			'Sun R1': 'Temple of the Sun (Altar of Mirrors) (Upper)',
			'Sun R2': 'Temple of the Sun (Altar of Mirrors) (Lower)',
			'Sun U1': 'Temple of the Sun (Watchtower)',
			'Spring D1': 'Spring in the Sky (Mural of Oannes)',
			'Inferno R1': 'Inferno Cavern (Statue of the Giant)',
			'Inferno U1': 'Inferno Cavern (Twin\'s Footstool)',
			'Inferno U2': 'Inferno Cavern (Echinda\'s Chamber)',
			'Inferno W1': 'Inferno Cavern (Anterior Chamber)',
			'Extinction L1': 'Chamber of Extinction (Mural of Invocation) (Upper)',
			'Extinction L2': 'Chamber of Extinction (Mural of Invocation) (Lower)',
			'Extinction U1': 'Chamber of Extinction (Lake of Life)',
			'Extinction U2': 'Chamber of Extinction (Gate of Ox-Head and Horse-Face)',
			'Extinction U3': 'Chamber of Extinction (Shiva\'s Crucifix)',
			'Twin U1': 'Twin Labyrinths (Twin\'s Surrounding Wall)',
			'Twin U2': 'Twin Labyrinths (Hero\'s Approach)',
			'Twin U3': 'Twin Labyrinths (Sanctuary)',
			'Twin D1': 'Twin Labyrinths (Idigna\'s Room)',
			'Twin D2': 'Twin Labyrinths (Poseidon\'s Room)',
			'Endless L1': 'Endless Corridor (First Endless Corridor) (Left Exit)',
			'Endless R1': 'Endless Corridor (First Endless Corridor)',
			'Endless U1': 'Endless Corridor (Second Endless Corridor)',
			'Endless D1': 'Endless Corridor (Fifth Endless Corridor)',
			'Shrine U1': 'Shrine of the Mother (Amphisbaena\'s Room)',
			'Shrine D1': 'Shrine of the Mother (Bahamut\'s Room)',
			'Shrine D2': 'Shrine of the Mother (Treasury) (Death Seal)',
			'Shrine D3': 'Shrine of the Mother (Treasury) (Map)',
			'Illusion R1': 'Gate of Illusion (Children\'s Room)',
			'Illusion R2': 'Gate of Illusion (Sacrificial Abyss)',
			'Illusion D1': 'Gate of Illusion (Fool\'s Confusion Corridor)',
			'Illusion D2': 'Gate of Illusion (Entrance of Illusion)',
			'Graveyard L1': 'Graveyard of the Giants (Third Tomb)',
			'Graveyard R1': 'Graveyard of the Giants (Second Tomb)',
			'Graveyard U1': 'Graveyard of the Giants (First Tomb)',
			'Graveyard U2': 'Graveyard of the Giants (Altar of Knowledge)',
			'Graveyard D1': 'Graveyard of the Giants (Anterior Corridor)',
			'Moonlight L1': 'Temple of Moonlight (Sealed Approach)',
			'Moonlight U1': 'Temple of Moonlight (Stairway of Eden)',
			'Moonlight U2': 'Temple of Moonlight (Neptune\'s Feet)',
			'Goddess L1': 'Tower of the Goddess (Path to Life)',
			'Goddess L2': 'Tower of the Goddess (Urd\'s Tower)',
			'Goddess U1': 'Tower of the Goddess (Verdandi\'s Tower)',
			'Goddess D1': 'Tower of the Goddess (Path to Power)',
			'Goddess W1': 'Tower of the Goddess (Gate of Time exit)',
			'Ruin L1': 'Tower of Ruin (Approach of the Philosophers)',
			'Ruin R1': 'Tower of Ruin (Burial Chamber of Life)',
			'Ruin R2': 'Tower of Ruin (Fountain of Heat)',
			'Birth L1': 'Chamber of Birth (Vishnu\'s Room)',
			'Birth R1': 'Chamber of Birth (Skanda\'s Room)',
			'Birth U1': 'Chamber of Birth (Saraswati\'s Room)',
			'Birth D1': 'Chamber of Birth (Deva\'s Room)',
			'Dimensional D1': 'Dimensional Corridor (Kishar\'s Room)',
			'Retrosurface R1': 'Gate of Time (Surface to Guidance)',
			'Retroguidance L1': 'Gate of Time (Guidance to Surface)',
			'Retroguidance D1': 'Gate of Time (Guidance to Mausoleum)',
			'Retromausoleum U1': 'Gate of Time (Mausoleum to Guidance)',
			'Retromausoleum D1': 'Gate of Time (Mausoleum to Tower of the Goddess)',
			'Pipe R1': 'Tower of the Goddess (Pipe)',
			'Pipe L1': 'Tower of the Goddess (Pipe)'
		}

	def door_requirement_logic(self, s: LaMulanaLogicShortcuts) -> dict[str, Callable[[CollectionState], bool] | None]:
		door_requirements = {
			'Amphisbaena': lambda state: state.has_all(('Bronze Mirror', 'Amphisbaena Defeated'), self.player),
			'Sakit': lambda state: state.has_all(('Bronze Mirror', 'Sakit Defeated'), self.player),
			'Ellmac': lambda state: state.has_all(('Bronze Mirror', 'Ellmac Defeated'), self.player),
			'Bahamut': lambda state: state.has_all(('Bronze Mirror', 'Bahamut Defeated'), self.player),
			'Viy': lambda state: state.has_all(('Bronze Mirror', 'Viy Defeated'), self.player),
			'Palenque': lambda state: state.has_all(('Bronze Mirror', 'Palenque Defeated'), self.player),
			'Baphomet': lambda state: state.has_all(('Bronze Mirror', 'Baphomet Defeated'), self.player),
			'Open': None,
			'Key': lambda state: s.state_key_fairy_access(state, False)
		}
		return door_requirements

	def get_doors(self):
		doors = {
			'Guidance Door':			LaMulanaDoor('Gate of Guidance [Door]', 'Illusion Door', 'Amphisbaena', is_oneway=True),
			'Mausoleum Door':			LaMulanaDoor('Mausoleum of the Giants', 'Graveyard Door', 'Sakit'),
			'Sun Door':					LaMulanaDoor('Temple of the Sun [Main]', 'Moonlight Door', 'Ellmac'),
			'Inferno Viy Door':			LaMulanaDoor('Inferno Cavern [Viy]', 'Ruin Lower Door', 'Bahamut'),
			'Surface Door':				LaMulanaDoor('Surface [Main]', 'Goddess Door', 'Viy'),
			'Extinction Magatama Door':	LaMulanaDoor('Chamber of Extinction [Magatama Left]', 'Birth Door', 'Palenque'),
			'Inferno Spikes Door':		LaMulanaDoor('Inferno Cavern [Spikes]', 'Ruin Top Door', 'Baphomet'),
			'Illusion Door':			LaMulanaDoor('Gate of Illusion [Grail]', 'Guidance Door', 'Amphisbaena'),
			'Graveyard Door':			LaMulanaDoor('Graveyard of the Giants [West]', 'Mausoleum Door', 'Sakit'),
			'Moonlight Door':			LaMulanaDoor('Temple of Moonlight [Lower]', 'Sun Door', 'Ellmac'),
			'Ruin Lower Door':			LaMulanaDoor('Tower of Ruin [Southwest Door]', 'Inferno Viy Door', 'Bahamut'),
			'Goddess Door':				LaMulanaDoor('Tower of the Goddess [Lower]', 'Surface Door', 'Viy'),
			'Birth Door':				LaMulanaDoor('Chamber of Birth [Northeast]', 'Extinction Magatama Door', 'Palenque'),
			'Ruin Top Door':			LaMulanaDoor('Tower of Ruin [Top]', 'Inferno Spikes Door', 'Baphomet', is_oneway=True),
			'Dimensional Door':			LaMulanaDoor('Dimensional Corridor [Grail]', 'Endless One-way Exit', 'Open', is_nonboss=True),
			'Endless One-way Exit':		LaMulanaDoor('Endless Corridor [1F]', 'Dimensional Door', 'Open', is_oneway=True, is_nonboss=True),
			'Extinction Key Door':		LaMulanaDoor('Chamber of Extinction [Main]', 'Retromausoleum Door', 'Key', is_nonboss=True),
			'Retromausoleum Door':		LaMulanaDoor('Gate of Time [Mausoleum Lower]', 'Extinction Key Door', 'Key', is_nonboss=True)
		}
		return doors
