import zipfile
import io
import os
import toml
import Utils
from typing import Dict, List, Set, Optional, TextIO, Union
from BaseClasses import Item, MultiWorld, Tutorial, Region, Entrance, Item, ItemClassification
from Options import Accessibility
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_item_rule
from kaitaistruct import KaitaiStream
from .Options import lamulana_options, starting_location_names, starting_weapon_names, is_option_enabled, get_option_value
from .WorldState import LaMulanaWorldState
from .NPCs import get_npc_checks, get_npc_entrance_room_names
from .Items import item_table, get_items_by_category, item_exclusion_order
from .Locations import get_locations_by_region
from .Regions import create_regions_and_locations
from .Rcd import Rcd
from .Dat import Dat
from pprint import pprint

client_version = 1

class LaMulanaWebWorld(WebWorld):
	tutorial_en = Tutorial(
		"Multiworld Setup Tutorial",
		"A guide for how to set up La-Mulana multiworld",
		"English",
		"setup_en.md",
		"setup/en",
		["Author's-name"]
	)
	tutorials = [tutorial_en]

class LaMulanaWorld(World):
	"""
	Challenge the ruins in the 2012 remake of La-Mulana, a puzzle platformer that focuses
	on exploration and combat as much as it does on solving the puzzles and mysteries of the ruins.
	Will you discover the secret treasure of life?
	"""
	game = "La-Mulana"
	option_definitions = lamulana_options
	web = LaMulanaWebWorld()
	required_client_version = (0, 4, 0) #Placeholder version number

	worldstate: LaMulanaWorldState

	item_name_to_id = {name: data.code for name, data in item_table.items()}
	location_name_to_id = {location.name: location.code for locations in get_locations_by_region(None, None, None).values() for location in locations}
	location_name_to_id |= {location.name: location.code for locations in get_npc_checks(None, None).values() for location in locations}
	item_name_groups = get_items_by_category()

	def __init__(self, world : MultiWorld, player: int):
		super().__init__(world, player)
		self.worldstate = LaMulanaWorldState(self.multiworld, self.player)

	@classmethod
	def stage_assert_generate(cls, multiworld: MultiWorld):
		rcd_file = Utils.user_path("script.rcd")
		if not os.path.exists(rcd_file):
			raise FileNotFoundError(rcd_file)

	def generate_early(self) -> None:
		#Do stuff that can still modify settings
		self.multiworld.local_items[self.player].value |= self.item_name_groups['ShopInventory']

		for setting_name, item_name in {('HolyGrailShuffle', 'Holy Grail'), ('MiraiShuffle', 'mirai.exe'), ('HermesBootsShuffle', 'Hermes\' Boots'), ('TextTraxShuffle', 'bunemon.exe')}:
			option = getattr(self.multiworld, setting_name)[self.player]
			if option == 'start_with':
				self.multiworld.start_inventory[self.player].value[item_name] = 1
			elif option == 'own_world':
				self.multiworld.local_items[self.player].value.add(item_name)
			elif option == 'different_world':
				self.multiworld.non_local_items[self.player].value.add(item_name)

		starting_weapon = get_option_value(self.multiworld, self.player, "StartingWeapon")
		starting_weapon_name = starting_weapon_names[starting_weapon]
		main_weapons = {'Leather Whip', 'Knife', 'Key Sword', 'Axe', 'Katana'}
		if self.is_option_enabled('SubweaponOnly'):
			#Starting subweapon incompatible with all locations reachable - switch to all items instead
			if self.multiworld.accessibility[self.player] == 'locations':
				option = getattr(self.multiworld, 'accessibility')[self.player]
				option.value = Accessibility.option_items
			#Starting with a main weapon incompatible with subweapon-only setting - give a random starting subweapon instead
			if starting_weapon_name in main_weapons:
				option = getattr(self.multiworld, 'StartingWeapon')[self.player]
				subweapon_options = [weapon_id for weapon_id, name in starting_weapon_names.items() if name not in main_weapons]
				chosen_subweapon = self.multiworld.random.choice(subweapon_options)
				option.value = chosen_subweapon
				starting_weapon_name = starting_weapon_names[chosen_subweapon]
			# Subweapon-only is incompatible with vanilla mother ankh
			if not self.is_option_enabled('AlternateMotherAnkh'):
				option = getattr(self.multiworld, 'AlternateMotherAnkh')[self.player]
				option.value = 1

		self.multiworld.start_inventory[self.player].value[starting_weapon_name] = 1

		starting_location = get_option_value(self.multiworld, self.player, "StartingLocation")
		if starting_location_names[starting_location] == 'extinction':
			# Extinction start without entrance randomizer or glitch logic is blocked off on all sides
			if not self.is_option_enabled('RandomizeTransitions') and not self.is_option_enabled('RandomizeBacksideDoors') and not self.is_option_enabled('RaindropsInLogic') and not self.is_option_enabled('LampGlitchInLogic'):
				option = getattr(self.multiworld, 'StartingLocation')[self.player]
				option.value = lamulana_options['StartingLocation'].option_surface
			elif self.is_option_enabled("RequireFlareGun") and starting_weapon_names[starting_weapon] != 'Flare Gun':
				self.multiworld.start_inventory[self.player].value['Flare Gun'] = 1
		if starting_location_names[starting_location] == 'twin (front)':
			self.multiworld.start_inventory[self.player].value['Twin Statue'] = 1
		elif starting_location_names[starting_location] == 'goddess':
			self.multiworld.start_inventory[self.player].value['Plane Model'] = 1
		elif starting_location_names[starting_location] in {'illusion', 'ruin'}:
			self.multiworld.start_inventory[self.player].value['Holy Grail'] = 1


	def create_regions(self) -> None:
		create_regions_and_locations(self.multiworld, self.player, self.worldstate)

	def create_items(self) -> None:
		success = False
		self.assign_event_items()
		shop_items = self.create_shop_items()
		self.multiworld.itempool += shop_items
		self.multiworld.itempool += self.generate_item_pool(len(shop_items))
		print('Currently', len(self.multiworld.get_unfilled_locations()), 'unfilled locations in the pool, with', len(self.multiworld.itempool), 'items in the pool')

	def set_rules(self) -> None:
		self.multiworld.completion_condition[self.player] = lambda state: state.has_all({'Mother Defeated', 'NPC: Mulbruk'}, self.player)

		option = getattr(self.multiworld, 'RandomizeCoinChests')[self.player]
		if option.value == lamulana_options['RandomizeCoinChests'].option_include_escape_chest:
			#local progression would be a problem for the escape coin chest - if it involves another player and loops back to us, that's fine
			escape_location = self.multiworld.get_location('Twin Labyrinths Escape Coin Chest', self.player)
			add_item_rule(escape_location, lambda item: item.player != self.player or item.classification != ItemClassification.progression)

	def extend_hint_information(self, hint_data: Dict[int, Dict[int,str]]):
		hint_info = {}
		transition_display_names = self.worldstate.get_transition_spoiler_names()

		def get_transition_spoiler_name(transition_name):
			target = self.worldstate.transition_map[transition_name]
			pipe = False
			if target in {'Pipe L1', 'Pipe R1'}:
				target = self.worldstate.transition_map['Pipe R1' if target == 'Pipe L1' else 'Pipe R1']
				pipe = True
			return transition_display_names[target] + (' (Pipe)' if pipe else '')

		if self.worldstate.npc_rando and self.worldstate.npc_mapping:
			room_names = get_npc_entrance_room_names()
			npc_checks = get_npc_checks(self.multiworld, self.player)
			reverse_map = {y: x for x, y in self.worldstate.npc_mapping.items()}
			npc_transition_info = {
				'Priest Hidlyda': 'Spring D1',
				'Philosopher Giltoriyo': 'Spring D1',
				'Mr. Fishman (Original)': 'Spring D1',
				'Mr. Fishman (Alt)': 'Spring D1',
				'Mudman Qubert': 'Birth D1',
				'Priest Ashgine': 'Birth D1',
				'8-bit Elder': 'Retrosurface R1'
			}
			for npc_name, locationdata_list in npc_checks.items():
				if npc_name in reverse_map:
					door_name = reverse_map[npc_name]
					print(npc_name, '-', room_names[door_name])
					for locationdata in locationdata_list:
						if not locationdata.is_event:
							target_transition = ''
							if self.worldstate.transition_rando and door_name in npc_transition_info:
								target_transition = f' past {get_transition_spoiler_name(npc_transition_info[door_name])}'
							hint_info[locationdata.code] = room_names[door_name] + target_transition

		if self.worldstate.transition_rando:
			check_transition_info = {
				'Sacred Orb (Spring in the Sky) Chest': 'Spring D1',
				'Map (Spring in the Sky) Chest': 'Spring D1',
				'Caltrops Location': 'Spring D1',
				'Glove Chest': 'Spring D1',
				'Origin Seal Chest': 'Spring D1',
				'Scalesphere Chest': 'Spring D1',
				'Map (Chamber of Extinction) Chest': 'Extinction L2',
				'Death Seal Chest': 'Shrine D2',
				'Map (Shrine of the Mother) Chest': 'Shrine D3',
				'Sacred Orb (Shrine of the Mother) Chest': 'Shrine U1',
				'Crystal Skull Chest': 'Shrine U1',
				'Diary Chest': 'Shrine U1',
				'bounce.exe Chest': 'Shrine U1',
				'Cog of the Soul Chest': 'Illusion R1',
				'Map (Tower of Ruin) Chest': 'Ruin L1',
				'Map (Chamber of Birth) Chest': 'Birth D1',
				'Pochette Key Chest': 'Birth D1',
				'Dimensional Key Chest': 'Birth D1',
				'lamulana.exe Chest': 'Retrosurface R1'
			}
			if self.get_option_value('RandomizeCoinChests'):
				check_transition_info.update({
					'Spring in the Sky Coin Chest': 'Spring D1',
					'Shrine of the Mother Coin Chest': 'Shrine U1',
					'Chamber of Birth Dance of Life Coin Chest': 'Birth D1'
				})
			for check_name, transition_name in check_transition_info.items():
				hint_info[self.multiworld.get_location(check_name, self.player).address] = get_transition_spoiler_name(transition_name)

		if self.worldstate.door_rando:
			check_door_info = {
				'yagostr.exe Chest': 'Guidance Door',
				'Djed Pillar Chest': 'Ruin Top Door',
				'Talisman Location': 'Inferno Viy Door'
			}
			for check_name, door_name in check_door_info.items():
				target, req = self.worldstate.door_map[door_name]
				hint_info[self.multiworld.get_location(check_name, self.player).address] = f'{target} ({req})'

		if self.worldstate.cursed_chests:
			for cursed_chest_name in self.worldstate.cursed_chests:
				location = self.multiworld.get_location(cursed_chest_name, self.player)
				hint_info[location.address] = hint_info[location.address] + ' (Cursed)' if location.address in hint_info else 'Cursed'

		hint_data[self.player] = hint_info

	def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
		spoiler_handle.write(f'Cursed Chests ({len(self.worldstate.cursed_chests)}):\n')
		spoiler_handle.write(f'    - {self.worldstate.cursed_chests if len(self.worldstate.cursed_chests) else "None"}\n')

		def space_count(name):
			return ' ' * (25 - len(name))

		if self.worldstate.npc_rando and self.worldstate.npc_mapping:
			spoiler_handle.write('NPC Randomizer:\n')
			room_names = get_npc_entrance_room_names()
			reverse_map = {y: x for x, y in self.worldstate.npc_mapping.items()}
			for npc_name in self.worldstate.get_npc_hint_order():
				if npc_name in reverse_map:
					npc_door = reverse_map[npc_name]
					spoiler_handle.write(f'    - {npc_name}:{space_count(npc_name)}{room_names[npc_door]}\n')

		if self.is_option_enabled('RandomizeSeals'):
			seal_spoilers = {value: [seal_name for seal_name, seal_val in self.worldstate.seal_map.items() if seal_val == value] for value in {1, 2, 3, 4}}
			seal_order = self.worldstate.get_seal_spoiler_order()
			for seal_val, seal_name in [(1, 'Origin Seal'), (2, 'Birth Seal'), (3, 'Life Seal'), (4, 'Death Seal')]:
				spoiler_handle.write(f'{seal_name}:\n')
				for seal_location in seal_order:
					if self.worldstate.seal_map[seal_location] == seal_val:
						spoiler_handle.write(f'    - {seal_location}\n')

		def arrows(source, dest, base_length, inner_text=None, display_names=None) -> str:
			oneways = {'Endless L1'}
			oneway_dests = {'Inferno W1', 'Goddess W1', 'Moonlight L1', 'Ruin L1', 'Endless One-way Exit', 'Guidance Door', 'Ruin Top Door'}
			if not self.is_option_enabled('RaindropsInLogic'):
				oneway_dests |= {'Extinction L2', 'Dimensional D1', 'Illusion R1'}
			if not self.is_option_enabled('LampGlitchInLogic'):
				oneway_dests.add('Inferno Viy Door')
			arrow_len = base_length - len(display_names[source]) if display_names and source in display_names else base_length - len(source)
			if inner_text:
				arrow_len -= 2 + len(inner_text)
				mid_str = ('=' * int((arrow_len / 2) + (arrow_len % 2))) + f'({inner_text})' + ('=' * int(arrow_len / 2))
			else:
				mid_str = '=' * arrow_len
			if source in oneways or dest in oneway_dests:
				return ' =' + mid_str + '> '
			if source in oneway_dests or dest in oneways:
				return ' <' + mid_str + '= '
			return ' <' + mid_str + '> '

		if self.worldstate.transition_rando:
			transition_display_names = self.worldstate.get_transition_spoiler_names()
			spoiler_handle.write('Transition Randomizer\n')
			for source in self.worldstate.get_transition_spoiler_order():
				if source not in self.worldstate.transition_map or source in {'Pipe L1', 'Pipe R1'}:
					continue
				dest = self.worldstate.transition_map[source]
				pipe = None
				if dest in {'Pipe L1', 'Pipe R1'}:
					pipe = 'pipe'
					dest = self.worldstate.transition_map['Pipe L1' if dest == 'Pipe R1' else 'Pipe R1']
				spoiler_handle.write(f'    - {transition_display_names[source]}{arrows(source,dest,59,pipe,transition_display_names)}{transition_display_names[dest]}\n')

		if self.worldstate.door_rando:
			doors_included = set()
			spoiler_handle.write('Door Randomizer\n')
			for source, (dest, requirement) in self.worldstate.door_map.items():
				if dest not in doors_included:
					doors_included.add(source)
					spoiler_handle.write(f'    - {source}{arrows(source,dest,40,requirement)}{dest}\n')

	def fill_slot_data(self) -> Dict[str, object]:
		slot_data : Dict[str, object] = {}
		for option_name in lamulana_options:
			slot_data[option_name] = self.get_option_value(option_name)
		slot_data['cursed_chests'] = self.worldstate.cursed_chests
		if self.worldstate.npc_rando:
			slot_data['npc_locations'] = self.worldstate.npc_mapping
		if self.is_option_enabled('RandomizeSeals'):
			slot_data['seal_data'] = self.worldstate.seal_map
		if self.worldstate.transition_rando:
			slot_data['transition_data'] = self.worldstate.transition_map
		if self.worldstate.door_rando:
			slot_data['door_data'] = self.worldstate.door_map
		return slot_data

	def assign_event_items(self):
		for location in self.multiworld.get_locations(self.player):
			if location.address is None:
				item_name = location.name
				if '—' in location.name:
					item_name = item_name[:item_name.find('—')].strip()
				item = Item(item_name, ItemClassification.progression, None, self.player)
				location.place_locked_item(item)

	# Place specific shop items that must be present at an early shop (weights, subweapon ammo) and weights in Little Brother's shop
	# Determine which shop slots will contain local ShopInventory items and add rules to all locations to enforce that
	# Create these ShopInventory items, returning a list with them
	def create_shop_items(self):
		item_list: List[Item] = []

		starting_weapon = starting_weapon_names[self.get_option_value('StartingWeapon')]
		starting_location = starting_location_names[self.get_option_value('StartingLocation')]

		if starting_weapon in {'Shuriken', 'Rolling Shuriken', 'Flare Gun', 'Earth Spear', 'Bomb', 'Chakram', 'Caltrops', 'Pistol'}:
			required_subweapon_ammo = starting_weapon + ' Ammo'
		else:
			required_subweapon_ammo = None

		if starting_location == 'extinction' and self.is_option_enabled('RequireFlareGun') and starting_weapon != 'Flare Gun':
			required_subweapon_ammo_2 = 'Flare Gun Ammo'
		else:
			required_subweapon_ammo_2 = None

		shop_locations: Set[str] = self.worldstate.get_shop_location_names()

		#Little Brother needs weights
		lil_bro_slot = self.multiworld.random.choice(['Yiegah Kungfu Shop Item 1', 'Yiegah Kungfu Shop Item 2', 'Yiegah Kungfu Shop Item 3'])
		self.place_locked_item(lil_bro_slot, '5 Weights')
		shop_locations.remove(lil_bro_slot)

		if self.worldstate.is_surface_start:
			if self.worldstate.npc_rando:
				surface_shop_slots = []
				npc_checks = get_npc_checks(self.multiworld, self.player)
				if self.worldstate.npc_mapping['Former Mekuri Master'] == 'Elder Xelpud':
					if starting_weapon in {'Shuriken', 'Chakram', 'Pistol', 'Earth Spear'}:
						#Case: Xelpud is at Former Mekuri Master and starting subweapon that can break the wall - WorldState made sure a shop was at Xelpud
						possible_shop_npcs = {'Elder Xelpud'}
					else:
						#Case: main weapon that breaks mekuri wall, since WorldState makes sure other subweapons don't get Xelpud there
						possible_shop_npcs = {'Elder Xelpud', 'Nebur', 'Sidro', 'Modro', 'Moger', 'Hiner'}
				else:
					#Case: Xelpud is vanilla
					possible_shop_npcs = {'Nebur', 'Sidro', 'Modro', 'Moger', 'Hiner'}
				for surface_npc_door in possible_shop_npcs:
					npc_name = self.worldstate.npc_mapping[surface_npc_door]
					if npc_name in npc_checks:
						for location in npc_checks[npc_name]:
							if location.name in shop_locations:
								surface_shop_slots.append(location.name)
			else:
				surface_shop_slots = ['Nebur Shop Item 1', 'Nebur Shop Item 2', 'Nebur Shop Item 3', 'Sidro Shop Item 1', 'Sidro Shop Item 2', 'Sidro Shop Item 3', 'Modro Shop Item 1', 'Modro Shop Item 2', 'Modro Shop Item 3']
			if len(surface_shop_slots) > 0:
				weight_slot = self.multiworld.random.choice(surface_shop_slots)
				self.place_locked_item(weight_slot, '5 Weights')
				shop_locations.remove(weight_slot)
				if required_subweapon_ammo and len(surface_shop_slots) > 1:
					surface_shop_slots.remove(weight_slot)
					ammo_slot = self.multiworld.random.choice(surface_shop_slots)
					self.place_locked_item(ammo_slot, required_subweapon_ammo)
					shop_locations.remove(ammo_slot)
		else:
			self.place_locked_item('Starting Shop Item 1', '5 Weights')
			shop_locations.remove('Starting Shop Item 1')
			if required_subweapon_ammo:
				self.place_locked_item('Starting Shop Item 2', required_subweapon_ammo)
				shop_locations.remove('Starting Shop Item 2')
			if required_subweapon_ammo_2:
				self.place_locked_item('Starting Shop Item 3', required_subweapon_ammo_2)
				shop_locations.remove('Starting Shop Item 3')

		slot_amount = len(shop_locations) - self.get_option_value('ShopDensity')

		#Guaranteed minimum amounts per ammo type and weights
		shop_items: List[str] = ['5 Weights', '5 Weights']
		ammo_types = ['Shuriken Ammo', 'Rolling Shuriken Ammo', 'Earth Spear Ammo', 'Flare Gun Ammo', 'Bomb Ammo', 'Chakram Ammo', 'Caltrops Ammo', 'Pistol Ammo']
		for ammo_name in ammo_types:
			shop_items.extend([ammo_name, ammo_name])
		if slot_amount >= 19:
			shop_items.extend(self.multiworld.random.choices(ammo_types + ['5 Weights'], k=slot_amount - len(shop_items)))

		local_shop_inventory_list = self.multiworld.random.sample(list(shop_locations), slot_amount)

		shop_inventory_ids = {item_table[item_name].code for item_name in self.item_name_groups['ShopInventory']}
		for location in self.multiworld.get_unfilled_locations(self.player):
			if location.name in local_shop_inventory_list:
				add_item_rule(location, lambda item: item.player == self.player and item.code in shop_inventory_ids)
			else:
				add_item_rule(location, lambda item: item.code not in shop_inventory_ids)

		already_created = set()
		for item_name in shop_items:
			item_list.append(self.create_item(item_name, already_created))
			already_created.add(item_name)

		return item_list

	def get_excluded_items(self) -> Set[str]:
		#101 base locations (chests + NPC checks) + 24 coin chests + escape chest + 4 trap items + number of randomized items in shops + 1 Hell Temple check
		coin_chest_option = self.get_option_value('RandomizeCoinChests')
		location_pool_size = 101 + (24 if coin_chest_option else 0) + (1 if coin_chest_option == 2 else 0) + (4 if self.is_option_enabled('RandomizeTrapItems') else 0) + self.get_option_value('ShopDensity') + (1 if self.is_option_enabled('HellTempleReward') else 0)

		item_pool_size = 125
		if self.is_option_enabled('AlternateMotherAnkh'):
			item_pool_size += 1

		if self.is_option_enabled('SubweaponOnly'):
			item_pool_size -= 6

		if not self.is_option_enabled('HellTempleReward'):
			item_exclusion_order.append('guild.exe')

		for item_name, amt in self.multiworld.start_inventory[self.player].value.items():
			if item_name == 'Ankh Jewel':
				if not self.is_option_enabled('GuardianSpecificAnkhJewels'):
					item_pool_size -= min(amt, 9 if self.is_option_enabled('AlternateMotherAnkh') else 8)
			elif item_name == 'Ankh Jewel (Mother)':
				if self.is_option_enabled('GuardianSpecificAnkhJewels') and self.is_option_enabled('AlternateMotherAnkh'):
					item_pool_size -= 1
			elif item_name in {'Ankh Jewel (Amphisbaena)', 'Ankh Jewel (Sakit)', 'Ankh Jewel (Ellmac)', 'Ankh Jewel (Bahamut)', 'Ankh Jewel (Viy)', 'Ankh Jewel (Palenque)', 'Ankh Jewel (Baphomet)', 'Ankh Jewel (Tiamat)'}:
				if self.is_option_enabled("GuardianSpecificAnkhJewels"):
					item_pool_size -= 1
			else:
				item_pool_size -= min(amt, item_table[item_name].count)
			if item_name in item_exclusion_order:
				item_exclusion_order.remove(item_name)

		pool_diff = item_pool_size - location_pool_size
		if pool_diff <= 0:
			return None

		return set(item_exclusion_order[:pool_diff])

	def generate_item_pool(self, shop_item_amt: int) -> List[Item]:
		item_pool: List[Item] = []
		excluded_items = self.get_excluded_items()

		for name, data in item_table.items():
			if excluded_items and name in excluded_items:
				continue
			if data.category == 'MainWeapon' and self.is_option_enabled('SubweaponOnly'):
				continue
			for _ in range(data.count - (self.multiworld.start_inventory[self.player].value[name] if name in self.multiworld.start_inventory[self.player].value else 0)):
				item = self.create_item(name)
				item_pool.append(item)

		if self.is_option_enabled('GuardianSpecificAnkhJewels'):
			guardians = {'Amphisbaena', 'Sakit', 'Ellmac', 'Bahamut', 'Viy', 'Palenque', 'Baphomet', 'Tiamat'}
			if self.is_option_enabled('AlternateMotherAnkh'):
				guardians.add('Mother')
			for guardian in guardians:
				jewel_name = f'Ankh Jewel ({guardian})'
				if jewel_name not in self.multiworld.start_inventory[self.player].value:
					item_pool.append(self.create_item(jewel_name))
		else:
			ankh_jewel_amt = 9 if self.is_option_enabled('AlternateMotherAnkh') else 8
			if 'Ankh Jewel' in self.multiworld.start_inventory[self.player].value:
				ankh_jewel_amt -= self.multiworld.start_inventory[self.player].value['Ankh Jewel']
			for _ in range(ankh_jewel_amt):
				item_pool.append(self.create_item('Ankh Jewel'))

		filler_pool_size = len(self.multiworld.get_unfilled_locations(self.player)) - shop_item_amt - len(item_pool)

		for i in range(filler_pool_size):
			item_pool.append(self.create_item(self.get_filler_item(i)))

		return item_pool

	def create_item(self, name: str, exclude_shop_progression:Set[str]=None) -> Item:
		data = item_table[name]

		if data.category == 'ShopInventory' and data.progression:
			if exclude_shop_progression and name in exclude_shop_progression:
				classification = ItemClassification.filler
			else:
				classification = ItemClassification.progression_skip_balancing
		elif data.progression:
			classification = ItemClassification.progression
		elif data.useful:
			classification = ItemClassification.useful
		elif data.trap:
			classification = ItemClassification.trap
		else:
			classification = ItemClassification.filler

		item = Item(name, classification, data.code, self.player)

		if not item.advancement:
			return item

		if name == 'guild.exe' and not self.is_option_enabled('HellTempleReward'):
			item.classification = ItemClassification.filler
		elif name == 'miracle.exe' and not self.is_option_enabled('RandomizeNPCs') and not self.is_option_enabled('RequireKeyFairyCombo'):
			item.classification = ItemClassification.useful
		elif name == 'mekuri.exe' and not self.is_option_enabled('RequireKeyFairyCombo'):
			item.classification = ItemClassification.useful
		elif name == 'Mulana Talisman' and len(self.worldstate.cursed_chests) == 0:
			item.classification = ItemClassification.filler

		return item

	def get_filler_item(self, k: Optional[int]):
		if k == 0:
			return '200 coins'
		elif k and k <= 2:
			return '100 coins'
		return self.multiworld.random.choices(['50 coins', '30 coins', '10 coins', '1 Weight'], weights=[1, 4, 6, 2], k=1)[0]

	def place_locked_item(self, location_name: str, item_name: str):
		self.multiworld.get_location(location_name, self.player).place_locked_item(self.create_item(item_name))

	def is_option_enabled(self, option: str) -> bool:
		return is_option_enabled(self.multiworld, self.player, option)

	def get_option_value(self, option: str) -> Union[int, Dict, List]:
		return get_option_value(self.multiworld, self.player, option)

	def generate_output(self, output_directory: str) -> None:
		rcd_path = Utils.user_path("script.rcd")
		rcd_size = os.path.getsize(rcd_path)

		rcd_io = KaitaiStream(open(rcd_path, 'rb'))
		rcd_file = Rcd(rcd_io)
		rcd_file._read()

		dat_path = Utils.user_path("script_code.dat")
		dat_size = os.path.getsize(dat_path)

		dat_io = KaitaiStream(open(dat_path, 'rb'))
		dat_file = Dat(dat_io)
		dat_file._read()

		configurations = {
			"server_url": "<get_from_host>",
			"password": "<get_from_host_or_leave_as_empty_quotes>",
			"log_file_name": "lamulanamw.txt",
			"local_player_id": self.player,
			"players": [{"id": player_id, "name": self.multiworld.player_name[player_id]} for player_id in self.multiworld.player_ids]
		}
		locations = self.multiworld.get_locations(self.player)

		item_mapping = []

		for location in locations:
			item = item_table.get(location.item.name)
			if (item is None and location.item.player == self.player) or location.address is None:
				continue
			item_mapping.append(
				{
					"flag": location.obtain_flag,
					"location_id": location.address,
					"player_id": location.item.player,
					"obtain_value": location.obtain_value
				}
			)
			item_id = item.game_code if item is not None and location.item.player == self.player else 83
			if location.file_type == 'rcd':
				for zone in location.zones:
					screen = rcd_file.zones[zone].rooms[location.room].screens[location.screen]
					skip = False

					objects = screen.objects_with_position
					param_index = 0
					iterations = 1
					item_mod = 0
					location_ids = [location.item_id]

					if location.object_type == 0x2c:
						param_len = 7
						item_mod = 11
						# Endless Corridor Twin Statue Chest Exists Twice
						if location.zones[0] == 8 and location.room == 3 and location.screen == 0 and location.item_id == 59:
							iterations = 2
					elif location.object_type == 0x2f:
						param_index = 1
						param_len = 4
						# Endless Corridor Keysword Exists Twice, Once as Regular and Once as Empowered
						if location.zones[0] == 8 and location.room == 2 and location.screen == 1 and location.item_id == 4:
							location_ids.append(7)
					elif location.object_type == 0xb5:
						param_len = 5
					elif location.object_type == 0xc3:
						iterations = 2
						param_index = 3
						param_len = 5
						objects = screen.objects_without_position
					else:
						skip = True

					if not skip:
						original_obtain_flag = location.original_obtain_flag if location.original_obtain_flag is not None else location.obtain_flag
						obtain_flag = item.obtain_flag if item.obtain_flag is not None else location.obtain_flag
						obtain_value = item.obtain_value if item.obtain_value is not None else location.obtain_value
						for location_id in location_ids:
							rcd_size = self.place_item(objects=objects, object_type=location.object_type, param_index=param_index, param_len=param_len, location_id=location_id, item_id=item_id, item_mod=item_mod, iterations=iterations, rcd_size=rcd_size, original_obtain_flag=original_obtain_flag, new_obtain_flag=obtain_flag, obtain_value=obtain_value)

			elif location.file_type == 'dat':
				for card_index in location.cards:
					card = dat_file.cards[card_index]
					entries = card.contents.entries
					if location.slot is None:
						e = enumerate(entries)
						entry_index = next((i for i,v in e if v.header == 0x0042 and v.contents.value == location.item_id), None)
						entries[entry_index].contents.value = item_id

						original_obtain_flag = location.original_obtain_flag if location.original_obtain_flag is not None else location.obtain_flag
						obtain_flag = item.obtain_flag if item.obtain_flag is not None else location.obtain_flag
						obtain_value = item.obtain_value if item.obtain_value is not None else location.obtain_value

						e = enumerate(entries)
						entry_index = next((i for i,v in e if v.header == 0x0040 and v.contents.address == original_obtain_flag), None)
						entries[entry_index].contents.address = obtain_flag
						entries[entry_index].contents.value = obtain_value
					else:
						e = enumerate(entries)
						data_indices = [i for i,v in e if v.header == 0x004e]
						entries[data_indices[0]].contents.values[location.slot] = item_id
						if item.cost is not None:
							entries[data_indices[1]].contents.values[location.slot] = item.cost
						entries[data_indices[2]].contents.values[location.slot] = item.quantity
						entries[data_indices[3]].contents.values[location.slot] = location.obtain_flag
						if location.obtain_value > 1:
							entries[data_indices[6]].contents.values[location.slot] = location.obtain_flag

		for item_name, _ in self.multiworld.start_inventory[self.player].value.items():
			item_id = item_table[item_name].game_code
			item_giver = Rcd.ObjectWithPosition()
			item_giver.id = 0xb5
			item_giver.test_operations_length = 0
			item_giver.write_operations_length = 0
			item_giver.parameters_length = 4
			item_giver.x_pos = 0
			item_giver.y_pos = 0
			item_giver.test_operations = []
			item_giver.write_operations = []
			item_giver.parameters = [item_id,160,120,39]
			starting_room = rcd_file.zones[1].rooms[2].screens[1]
			starting_room.objects_with_position.append(item_giver)
			starting_room.objects_length += 1
			rcd_size += 16

		# Xelpud flag checks
		dat_size = self.rewrite_xelpud_flag_checks(dat_file, dat_size)

		rcd_write_io = KaitaiStream(io.BytesIO(bytearray(rcd_size)))
		rcd_file._write(rcd_write_io)

		dat_write_io = KaitaiStream(io.BytesIO(bytearray(dat_size)))
		dat_file._write(dat_write_io)

		configurations["item_mapping"] = item_mapping

		output_path = os.path.join(output_directory, f"AP-{self.multiworld.seed_name}-P{self.player}-{self.multiworld.get_file_safe_player_name(self.player)}_{Utils.__version__}.zip")
		with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED, True, 9) as output_zip:
			output_zip.writestr("script.rcd", rcd_write_io.to_byte_array())
			output_zip.writestr("script_code.dat", dat_write_io.to_byte_array())
			output_zip.writestr("lamulana-config.toml", toml.dumps(configurations))

	def rewrite_xelpud_flag_checks(self, dat_file, dat_size):
		card = dat_file.cards[480]
		dat_size -= self.remove_data_entry_by_value(card, 1049)
		dat_size -= self.remove_data_entry_by_value(card, 371)
		dat_size -= self.remove_data_entry_by_value(card, 370)
		dat_size -= self.remove_data_entry_by_value(card, 364)

		talisman_item_values = [0xaed, 1, 371, 0]
		dat_size += self.add_data_entry(dat_file, card, talisman_item_values)

		xelpud_pillar_conversation = [0xaec, 2, 370, 0]
		dat_size += self.add_data_entry(dat_file, card, xelpud_pillar_conversation)

		xelpud_talisman_conversation_values = [0xaec, 1, 369, 0]
		dat_size += self.add_data_entry(dat_file, card, xelpud_talisman_conversation_values)

		xmailer_item_values = [0xad0, 0, 364, 0]
		dat_size += self.add_data_entry(dat_file, card, xmailer_item_values)
		return dat_size

	def place_item(self, objects, object_type, param_index, param_len, location_id, item_id, original_obtain_flag, new_obtain_flag, obtain_value, rcd_size, item_mod, iterations):
		o = enumerate(objects)
		for _ in range(iterations):
			o_index = next((i for i,v in o if v.id == object_type and v.parameters[param_index] == location_id+item_mod and len(v.parameters) < param_len), None)
			location = objects[o_index]

			for test_op in location.test_operations:
				if test_op.flag == original_obtain_flag:
					test_op.flag = new_obtain_flag
			for write_op in location.write_operations:
				if write_op.flag == original_obtain_flag:
					write_op.flag = new_obtain_flag
					if object_type == 0x2c:
						location.write_operations[3].op_value = obtain_value
					elif object_type == 0x2f or 0xb5 or 0xc3:
						write_op.value = obtain_value

			location.parameters[param_index] = item_id+item_mod
			location.parameters.append(1)
			location.parameters_length += 1
			rcd_size += 2
		return rcd_size

	def remove_data_entry_by_value(self, card, value):
		entries = card.contents.entries

		e = enumerate(entries)
		entry_index = next((i for i,v in e if v.header == 0x004e and v.contents.values[2] == value), None)
		next_index_to_delete = entry_index + 2

		# entry.header + entry.header.data.num_values + break + entry.header.data.values
		size = 6 + (entries[entry_index].contents.num_values * 2)
		if entry_index == len(entries):
			# Possible to not have the break after the entry
			size -= 2
			# Inclusive means that this only deletes one element?
			next_index_to_delete = 1


		del entries[entry_index:next_index_to_delete]
		return size

	def add_data_entry(self, dat_file, card, values):
		entry = Dat.Entry(None, card, dat_file)
		entry.header = 0x000a
		entry.contents = Dat.Noop(None, entry, dat_file)

		entry = Dat.Entry(None, card, dat_file)
		entry.header = 0x004e

		data = Dat.Data(None, entry, dat_file)
		data.num_values = len(values)
		data.values = values

		entry.contents = data
		card.contents.entries.append()

		return 6 + (data.num_values * 2)
