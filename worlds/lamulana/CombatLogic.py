from BaseClasses import CollectionState
from typing import TYPE_CHECKING
from .LogicShortcuts import LaMulanaLogicShortcuts

if TYPE_CHECKING:
	from . import LaMulanaWorld


class LaMulanaCombatLogic:
	player: int
	flag_hard_logic: bool
	flag_subweapon_only: bool
	s: LaMulanaLogicShortcuts

	def __init__(self, world: "LaMulanaWorld", shortcuts: LaMulanaLogicShortcuts):
		self.flag_hard_logic = bool(world.options.HardCombatLogic)
		self.flag_subweapon_only = bool(world.options.SubweaponOnly)
		self.player = world.player
		self.s = shortcuts

	def anubis(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			return self.s.attack_main(state) or self.s.attack_shuriken(state) or self.s.attack_rolling_shuriken(state) or self.s.attack_caltrops(state) or self.s.attack_chakram(state) or self.s.attack_pistol(state) or self.s.attack_earth_spear(state)
		return self.s.attack_main(state) or self.s.attack_ring_shuriken(state) or self.s.attack_rolling_shuriken(state) or self.s.attack_caltrops(state) or self.s.attack_chakram(state) or self.s.attack_pistol(state)

	def argus(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			if self.s.attack_main(state) or self.s.attack_shuriken(state) or self.s.attack_bomb(state) or self.s.attack_chakram(state) or self.s.attack_caltrops(state) or self.s.attack_pistol(state):
				return True
			if self.s.attack_flare_gun(state) and (self.s.state_lamp(state) or self.s.get_health_count(state) >= 2 or state.has('Ring', self.player)):
				return True
			return self.s.state_lamp(state) and (self.s.attack_rolling_shuriken(state) or (self.s.attack_earth_spear(state) and state.has('Feather', self.player)))
		if self.s.attack_main(state) or self.s.attack_shuriken(state) or self.s.attack_bomb(state) or self.s.attack_chakram(state) or self.s.attack_caltrops(state) or self.s.attack_pistol(state):
			return True
		if self.s.state_lamp(state):
			return self.s.attack_rolling_shuriken(state) or self.s.attack_flare_gun(state) or (self.s.attack_earth_spear(state) and state.has("Feather", self.player))
		return False

	def ba(self, state: CollectionState) -> bool:
		# Same hard logic
		return self.s.attack_forward(state) or self.s.attack_s_above(state)

	def backbeard_tai_sui(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			return self.s.attack_main(state) or self.s.attack_shuriken(state) or self.s.attack_rolling_shuriken(state) or self.s.attack_vertical(state) or self.s.attack_caltrops(state)
		health = self.s.get_health_count(state)
		if self.flag_subweapon_only:
			if not state.has("Ring", self.player):
				return False
			if health >= 6:
				if self.s.attack_shuriken(state) or (self.s.attack_vertical(state) and state.has_all(("Feather", "Hermes' Boots"), self.player)):
					return True
			if health >= 4:
				if self.s.attack_pistol(state) and (self.s.attack_shuriken(state) or self.s.attack_rolling_shuriken(state)):
					return True
			if health >= 2:
				if self.s.attack_chakram(state) and self.s.attack_caltrops(state):
					return True
				if self.s.attack_shuriken(state) and (self.s.attack_rolling_shuriken(state) or self.s.attack_earth_spear(state) or self.s.attack_flare_gun(state) or self.s.attack_bomb(state) or self.s.attack_chakram(state) or self.s.attack_caltrops(state)):
					return True
				if self.s.attack_rolling_shuriken(state) and (self.s.attack_earth_spear(state) or self.s.attack_flare_gun(state) or self.s.attack_chakram(state) or self.s.attack_caltrops(state)):
					return True
			return False
		return state.has_any(('Katana', 'Axe', 'Knife'), self.player) or (self.s.attack_main(state) and health >= 2)

	def buer(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			return self.s.attack_far(state) or state.has('Katana', self.player) or self.s.attack_subweapon(state) or (state.has('Knife', self.player) and self.s.get_health_count(state) >= 2)
		health = self.s.get_health_count(state)
		return state.has_any(("Axe", "Chain Whip", "Flail Whip"), self.player) or self.s.attack_empowered_key_sword(state) or (health >= 1 and state.has("Katana", self.player)) or (health >= 2 and state.has_any(("Knife", "Key Sword", "Leather Whip"), self.player)) or self.s.attack_subweapon(state)

	def centimani(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			return self.s.attack_main(state) or self.s.attack_shuriken(state) or self.s.attack_earth_spear(state) or self.s.attack_bomb(state) or self.s.attack_chakram(state) or self.s.attack_caltrops(state) or self.s.attack_pistol(state) or self.s.attack_ring_flare_gun(state) or (self.s.attack_rolling_shuriken(state) and self.s.attack_flare_gun(state))
		health = self.s.get_health_count(state)
		if self.s.attack_pistol(state) or self.s.attack_ring_chakram(state) or (self.s.attack_ring_flare_gun(state) and health >= 4):
			return True
		if self.flag_subweapon_only:
			if health >= 2:
				if self.s.attack_flare_gun(state) and (self.s.attack_earth_spear(state) or self.s.attack_rolling_shuriken(state) or self.s.attack_ring_shuriken(state)):
					return True
			if health >= 1:
				return self.s.attack_chakram(state) or self.s.attack_caltrops(state)
			return False
		return (self.s.attack_4(state) and health >= 1) or (self.s.attack_main(state) and health >= 3)

	def chi_you(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			return self.s.attack_main(state) or self.s.attack_shuriken(state) or self.s.attack_rolling_shuriken(state) or self.s.attack_chakram(state) or self.s.attack_caltrops(state) or self.s.attack_pistol(state)
		health = self.s.get_health_count(state)
		if health >= 5 and state.has("Chain Whip", self.player):
			return True
		if health >= 4 and state.has_any(("Axe", "Katana"), self.player):
			return True
		if health >= 3 and state.has("Flail Whip", self.player):
			return True
		return self.s.attack_pistol(state) or self.s.attack_ring_chakram(state)

	def kamaitachi(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			return self.s.attack_main(state) or self.s.attack_shuriken(state) or self.s.attack_rolling_shuriken(state) or self.s.attack_earth_spear(state) or self.s.attack_flare_gun(state) or self.s.attack_bomb(state) or self.s.attack_caltrops(state) or self.s.attack_pistol(state)
		health = self.s.get_health_count(state)
		if health >= 4:
			if self.s.attack_main(state) or self.s.attack_rolling_shuriken(state) or self.s.attack_ring_flare_gun(state) or (self.s.attack_earth_spear(state) and state.has("Feather", self.player)):
				return True
		if health >= 2:
			if self.s.attack_4(state) or self.s.attack_bomb(state) or self.s.attack_caltrops(state):
				return True
		return self.s.attack_5(state) or self.s.attack_ring_shuriken(state) or self.s.attack_chakram(state) or self.s.attack_pistol(state)

	def nuckelavee(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			if self.s.attack_far(state) or state.has('Katana', self.player) or self.s.attack_shuriken(state) or self.s.attack_bomb(state) or self.s.attack_chakram(state) or self.s.attack_caltrops(state) or self.s.attack_pistol(state):
				return True
			if state.has('Feather', self.player) and (state.has('Knife', self.player) or self.s.attack_earth_spear(state)):
				return True
			return self.s.state_lamp(state) and self.s.attack_flare_gun(state)
		if self.s.attack_far(state) or state.has("Katana", self.player) or self.s.attack_shuriken(state) or self.s.attack_bomb(state) or self.s.attack_ring_chakram(state) or self.s.attack_caltrops(state) or self.s.attack_pistol(state):
			return True
		if state.has("Feather", self.player) and (state.has("Knife", self.player) or self.s.attack_earth_spear(state)):
			return True
		return self.s.state_lamp(state) and self.s.attack_flare_gun(state)

	def nuwa(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			if self.s.attack_pistol(state):
				return True
			if self.s.attack_main(state) and (self.s.state_shield(state) or self.s.state_lamp(state) or state.has('Feather', self.player)):
				return True
			if self.s.attack_ring_chakram(state) and state.has('Feather', self.player):
				return True
			return self.s.attack_chakram(state) and self.s.state_shield(state) and self.s.state_lamp(state) and state.has('Feather', self.player)
		health = self.s.get_health_count(state)
		if health >= 5 and self.s.attack_ring_chakram(state) and state.has("Feather", self.player):
			return True
		if health >= 3 and self.s.attack_4(state) and state.has("Feather", self.player) and self.s.state_shield(state) and self.s.state_lamp(state):
			return True
		return state.has("Feather", self.player) and (self.s.attack_pistol(state) or (self.s.attack_dps(state) and self.s.state_lamp(state)))

	def oxhead_horseface(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			if state.has('Axe', self.player) or self.s.attack_ring_chakram(state) or self.s.attack_pistol(state):
				return True
			if self.s.state_shield(state) and state.has('Feather', self.player):
				return self.s.attack_main(state) or self.s.attack_ring_shuriken(state) or self.s.attack_rolling_shuriken(state) or (self.s.attack_shuriken(state) and self.s.attack_caltrops(state))
			return False
		health = self.s.get_health_count(state)
		if state.has("Feather", self.player):
			if self.flag_subweapon_only and health >= 6 and self.s.state_shield(state):
				if self.s.attack_ring_shuriken(state):
					return True
				if self.s.attack_shuriken(state) and (self.s.attack_rolling_shuriken(state) or self.s.attack_caltrops(state)):
					return True
				if self.s.attack_rolling_shuriken(state) and (self.s.attack_bomb(state) or self.s.attack_caltrops(state)):
					return True
				if self.s.attack_bomb(state) and self.s.attack_caltrops(state):
					return True
			return self.s.attack_pistol(state) or (health >= 4 and self.s.state_shield(state) and self.s.attack_4(state))
		return False

	def pazuzu(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			if self.s.attack_far(state) or state.has('Katana', self.player) or self.s.attack_shuriken(state) or self.s.attack_chakram(state) or self.s.attack_pistol(state):
				return True
			if self.s.attack_earth_spear(state) and state.has('Feather', self.player):
				return True
			return self.s.attack_flare_gun(state) and self.s.get_health_count(state) >= 1
		# Lamp can be used to reach pazuzu, so for lamp combat logic, we need one of the other ways of reaching him logically
		if self.s.attack_4(state) and self.s.state_lamp(state) and state.has_any(("Feather", "Grapple Claw"), self.player):
			return True
		health = self.s.get_health_count(state)
		if health >= 5 and state.has("Chain Whip", self.player):
			return True
		if health >= 4 and state.has_any(("Axe", "Katana"), self.player):
			return True
		if health >= 3 and state.has("Flail Whip", self.player):
			return True
		return self.s.attack_shuriken(state) or self.s.attack_chakram(state) or self.s.attack_pistol(state)

	def peryton(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			return self.s.attack_main(state) or self.s.attack_earth_spear(state) or self.s.attack_pistol(state)
		if self.s.attack_earth_spear(state):
			return True
		health = self.s.get_health_count(state)
		if self.flag_subweapon_only:
			return health >= 4 and (self.s.attack_ring_chakram(state) or self.s.attack_pistol(state))
		if health >= 7:
			if self.s.attack_main(state) and (self.s.attack_flare_gun(state) or (self.s.attack_rolling_shuriken(state) and state.has("Ring", self.player))):
				return True
		if health >= 4 and state.has_any(("Chain Whip", "Katana"), self.player):
			return True
		if health >= 3 and state.has("Axe", self.player):
			return True
		if health >= 2 and state.has("Flail Whip", self.player):
			return True
		return self.s.attack_4(state) and self.s.state_lamp(state)

	def skanda(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			return self.s.attack_main(state) or self.s.attack_pistol(state)
		health = self.s.get_health_count(state)
		if self.flag_subweapon_only:
			if health >= 8 and state.has("Feather", self.player):
				if self.s.attack_ring_shuriken(state) or self.s.attack_rolling_shuriken(state) or self.s.attack_earth_spear(state) or self.s.attack_chakram(state):
					return True
			if health >= 6 and state.has_all(("Feather", "Ring"), self.player):
				if self.s.attack_chakram(state) or self.s.attack_earth_spear(state):
					return True
			if health >= 6 and self.s.attack_caltrops(state):
				return True
		if health >= 6:
			if state.has_any(("Chain Whip", "Axe", "Katana"), self.player):
				return True
		if health >= 4:
			if state.has("Flail Whip", self.player):
				return True
		return self.s.attack_pistol(state) or (self.s.state_lamp(state) and self.s.attack_dps(state))

	def thunderbird(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			if self.s.attack_4(state) or self.s.attack_chakram(state) or self.s.attack_pistol(state):
				return True
			if state.has('Feather', self.player):
				if self.s.attack_shuriken(state) or self.s.attack_earth_spear(state) or self.s.attack_caltrops(state):
					return True
			if self.s.state_lamp(state):
				if self.s.attack_main(state) or self.s.attack_earth_spear(state) or self.s.attack_ring_flare_gun(state):
					return True
			return False
		if self.s.attack_4(state) or self.s.attack_pistol(state) or (self.s.attack_chakram(state) and state.has_any(("Feather", "Ring"), self.player)):
			return True
		if self.s.state_lamp(state):
			if self.s.attack_main(state) or self.s.attack_ring_shuriken(state) or self.s.attack_earth_spear(state) or (state.has("Feather", self.player) and self.s.attack_ring_flare_gun(state)):
				return True
		health = self.s.get_health_count(state)
		if health >= 6:
			if (self.s.attack_ring_shuriken(state) and state.has("Feather", self.player)) or (self.s.state_shield(state) and self.s.attack_subweapon(state) and state.has("Ring", self.player)):
				return True
		if health >= 4:
			if state.has("Feather", self.player) and (self.s.attack_earth_spear(state) or self.s.attack_caltrops(state)):
				return True
		if health >= 2:
			return self.s.attack_main(state) and self.s.state_shield(state)
		return False

	def vimana(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			return self.s.attack_main(state) or self.s.attack_subweapon(state)
		return self.s.get_health_count(state) >= 2 and (self.s.attack_main(state) or self.s.attack_subweapon(state))

	def zu(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			if self.s.attack_main(state) or self.s.attack_earth_spear(state) or self.s.attack_ring_flare_gun(state):
				return True
			if self.s.get_health_count(state) >= 4 and self.s.attack_pistol(state):
				return True
			if self.s.state_lamp(state):
				if self.s.attack_chakram(state) or self.s.attack_caltrops(state) or self.s.attack_pistol(state):
					return True
			return False
		if self.s.state_lamp(state):
			return self.s.attack_4(state) or self.s.attack_ring_chakram(state) or self.s.attack_caltrops(state) or self.s.attack_pistol(state)
		health = self.s.get_health_count(state)
		if health >= 3 and state.has("Flail Whip", self.player):
			return True
		return health >= 4 and state.has_any(("Chain Whip", "Axe"), self.player)

	def kulullu(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			if state.has('Helmet', self.player) and (self.s.attack_main(state) or self.s.attack_subweapon(state)):
				return True
			return self.s.attack_shuriken(state) or self.s.attack_chakram(state) or self.s.attack_pistol(state)
		health = self.s.get_health_count(state)
		if health >= 6 and state.has_all(("Helmet", "Chain Whip"), self.player):
			return True
		if health >= 5 and state.has_all(("Helmet", "Axe"), self.player):
			return True
		if health >= 4 and state.has_all(("Helmet", "Flail Whip"), self.player):
			return True
		if health >= 3:
			return self.s.attack_pistol(state) or self.s.attack_chakram(state) or self.s.attack_ring_shuriken(state)
		return False

	def left_side_children(self, state: CollectionState) -> bool:
		# hard logic is the same
		return self.s.attack_pistol(state) or self.s.attack_ring_chakram(state) or (self.s.attack_chakram(state) and self.s.state_lamp(state)) or (self.s.attack_main(state) and self.kulullu(state))

	def right_side_children(self, state: CollectionState) -> bool:
		health = self.s.get_health_count(state)
		if self.flag_hard_logic:
			if self.s.attack_pistol(state):
				return True
			if self.s.attack_main(state) and self.s.state_shield(state):
				return True
			if self.s.attack_chakram(state) and (self.s.state_shield(state) or self.s.state_lamp(state)):
				return True
			if health >= 4 and (self.s.state_shield(state) or self.s.state_lamp(state)):
				if self.s.attack_ring_shuriken(state):
					return True
				if self.s.attack_earth_spear(state) and self.s.attack_ring_bomb(state):
					return True
				if self.s.attack_caltrops(state) and self.s.attack_bomb(state):
					return True
			if health >= 2 or self.s.state_lamp(state):
				if self.s.attack_rolling_shuriken(state) and (self.s.attack_earth_spear(state) or self.s.attack_bomb(state) or self.s.attack_caltrops(state)):
					return True
			return False
		if health >= 8:
			if self.s.state_shield(state) and (self.s.attack_main(state) or self.s.attack_chakram(state) or self.s.attack_pistol(state)):
				return True
			if self.s.state_lamp(state):
				if self.s.attack_ring_shuriken(state) and (self.s.attack_earth_spear(state) or self.s.attack_rolling_shuriken(state)):
					return True
				if self.s.attack_rolling_shuriken(state) and (self.s.attack_caltrops(state) or self.s.attack_pistol(state) or (self.s.attack_earth_spear(state) and self.s.attack_bomb(state))):
					return True
				if self.s.attack_earth_spear(state) and self.s.attack_caltrops(state):
					return True
		if health >= 6:
			return self.s.state_lamp(state) and (self.s.attack_main(state) or self.s.attack_pistol(state))
		return False

	def angel_shield_children(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			if self.s.attack_main(state):
				return True
			if self.s.attack_pistol(state) and (self.s.attack_bomb(state) or self.s.attack_flare_gun(state) or self.s.attack_caltrops(state)):
				return True
			if self.s.attack_chakram(state) and self.s.get_health_count(state) >= 4:
				return True
			if self.s.attack_ring_flare_gun(state) and (self.s.attack_shuriken(state) or self.s.attack_rolling_shuriken(state) or self.s.attack_chakram(state) or self.s.attack_caltrops(state)):
				return True
			if self.s.attack_rolling_shuriken(state) and self.s.attack_caltrops(state):
				return True
			return False
		health = self.s.get_health_count(state)
		if self.flag_subweapon_only:
			if health >= 6 and self.s.attack_rolling_shuriken(state) and self.s.attack_caltrops(state):
				return True
			if health >= 5 and self.s.attack_flare_gun(state):
				if self.s.attack_ring_chakram(state):
					return True
				if self.s.attack_pistol(state) and state.has_all(("Ring", "Hermes' Boots"), self.player):
					return True
				if self.s.attack_bomb(state):
					if self.s.attack_pistol(state) and state.has("Hermes' Boots", self.player):
						return True
					if self.s.attack_caltrops(state) and (self.s.attack_shuriken(state) or self.s.attack_rolling_shuriken(state) or self.s.attack_earth_spear(state) or self.s.attack_chakram(state) or self.s.attack_pistol(state)):
						return True
				if self.s.attack_caltrops(state) and (self.s.attack_chakram(state) or self.s.attack_pistol(state)):
					return True
			return False
		if health >= 6 and state.has("Chain Whip", self.player):
			return True
		if health >= 5 and state.has("Axe", self.player):
			return True
		if health >= 4:
			if state.has("Flail Whip", self.player) or self.s.attack_empowered_key_sword(state):
				return True
		return False

	def ushumgallu(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			if state.has('Axe', self.player) or self.s.attack_chakram(state) or self.s.attack_pistol(state) or self.s.attack_ring_flare_gun(state):
				return True
			if self.s.attack_shuriken(state) and self.s.state_shield(state) and state.has('Grapple Claw', self.player):
				return True
			if state.has('Feather', self.player):
				if self.s.attack_main(state) or self.s.attack_caltrops(state):
					return True
				if self.s.state_shield(state) and (self.s.attack_shuriken(state) or self.s.attack_rolling_shuriken(state)):
					return True
			return False
		if self.s.get_health_count(state) >= 4 and state.has("Feather", self.player):
			if state.has_any(("Flail Whip", "Chain Whip", "Axe"), self.player) or self.s.attack_chakram(state) or self.s.attack_caltrops(state) or self.s.attack_pistol(state):
				return True
			if self.s.attack_ring_shuriken(state) and self.s.state_shield(state):
				return True
			return self.s.attack_rolling_shuriken(state) and self.s.state_shield(state)
		return False

	def mushussu(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			if self.s.attack_pistol(state):
				return True
			if state.has('Feather', self.player) and (state.has('Flail Whip', self.player) or self.s.attack_empowered_key_sword(state)):
				return True

			health = self.s.get_health_count(state)
			if state.has_all(('Flail Whip', "Hermes' Boots"), self.player) and health >= 4:
				return True
			if state.has_all(('Axe', "Hermes' Boots"), self.player) and health >= 6:
				return True
			if self.s.attack_ring_chakram(state) and health >= 2:
				return True
			if health >= 8:
				if self.s.attack_chakram(state) or self.s.attack_caltrops(state):
					return True
				if state.has('Feather', self.player):
					if self.s.attack_shuriken(state) and (state.has('Ring', self.player) or self.s.attack_rolling_shuriken(state) or self.s.attack_caltrops(state)):
						return True
					if self.s.attack_rolling_shuriken(state) and (self.s.attack_flare_gun(state) or self.s.attack_bomb(state) or self.s.attack_caltrops(state)):
						return True
					if self.s.attack_flare_gun(state) and self.s.attack_caltrops(state):
						return True
			if health >= 10:
				if self.s.attack_ring_bomb(state):
					return True
				if self.s.attack_ring_flare_gun(state) and self.s.attack_bomb(state):
					return True
				if state.has('Feather', self.player):
					if self.s.attack_rolling_shuriken(state) or (self.s.attack_shuriken(state) and self.s.attack_flare_gun(state)):
						return True
			return False
		health = self.s.get_health_count(state)
		if health >= 8 and state.has("Hermes' Boots", self.player) and state.has_any(("Axe", "Flail Whip"), self.player):
			return True
		# All other req's call for feather
		if state.has("Feather", self.player):
			if self.flag_subweapon_only and health >= 8:
				if self.s.attack_ring_shuriken(state):
					return True
				if self.s.attack_rolling_shuriken(state) and (self.s.attack_shuriken(state) or self.s.attack_bomb(state) or self.s.attack_caltrops(state)):
					return True
				if self.s.attack_ring_flare_gun(state) and (self.s.attack_bomb(state) or self.s.attack_caltrops(state)):
					return True
			if health >= 8 and self.s.attack_main(state):
				return True
			if health >= 6:
				if self.s.attack_chakram(state) or state.has("Katana", self.player):
					return True
			if health >= 4:
				if state.has_any(("Flail Whip", "Axe"), self.player) or self.s.attack_ring_chakram(state):
					return True
			return self.s.attack_pistol(state)
		return False

	def amphisbaena(self, state: CollectionState) -> bool:
		# Hard logic is the same
		if self.s.attack_main(state) or self.s.attack_shuriken(state) or self.s.attack_flare_gun(state) or self.s.attack_bomb(state) or self.s.attack_chakram(state) or self.s.attack_pistol(state):
			return True
		if self.s.attack_rolling_shuriken(state) and state.has("Hermes' Boots", self.player):
			return True
		return (self.s.attack_earth_spear(state) or self.s.attack_caltrops(state)) and (state.has("Hermes' Boots", self.player) or self.s.state_lamp(state))

	def sakit(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			# Similar logic except for health checks
			if self.s.attack_main(state) or self.s.attack_flare_gun(state) or self.s.attack_chakram(state) or self.s.attack_pistol(state):
				return True
			return self.s.attack_bomb(state) and (self.s.attack_shuriken(state) or self.s.attack_caltrops(state) or state.has("Ring", self.player) or self.s.attack_rolling_shuriken(state))
		health = self.s.get_health_count(state)
		if health >= 2:
			if self.s.attack_main(state) or self.s.attack_flare_gun(state) or self.s.attack_chakram(state) or self.s.attack_pistol(state):
				return True
			return self.s.attack_bomb(state) and (self.s.attack_shuriken(state) or self.s.attack_caltrops(state) or state.has("Ring", self.player) or (self.s.attack_rolling_shuriken(state) and health >= 4))
		return False

	def ellmac(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			if self.s.attack_main(state) or self.s.attack_shuriken(state) or self.s.attack_chakram(state) or self.s.attack_pistol(state):
				return True
			return self.s.attack_ring_bomb(state) and state.has('Feather', self.player)
		return self.s.get_health_count(state) >= 3 and (self.s.attack_4(state) or self.s.attack_shuriken(state) or self.s.attack_ring_chakram(state) or self.s.attack_pistol(state))

	def bahamut(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			return self.s.attack_main(state) or self.s.attack_flare_gun(state) or self.s.attack_caltrops(state) or self.s.attack_pistol(state)
		return self.s.get_health_count(state) >= 4 and (self.s.attack_main(state) or self.s.attack_flare_gun(state) or self.s.attack_caltrops(state) or self.s.attack_pistol(state))

	def viy(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			if self.s.attack_4(state) or self.s.attack_pistol(state) or self.s.attack_ring_chakram(state):
				return True
			if self.s.attack_main(state) and (self.s.attack_shuriken(state) or self.s.attack_rolling_shuriken(state) or self.s.attack_bomb(state) or self.s.attack_chakram(state) or self.s.get_health_count(state) >= 1):
				return True
			if self.s.attack_shuriken(state) and self.s.attack_chakram(state) and self.s.state_mobility(state) and self.s.state_shield(state):
				return True
			if self.flag_subweapon_only:
				return self.viy_subweapons(state)
			return False
		if self.s.get_health_count(state) < 5:
			return False
		if self.s.attack_ring_chakram(state) or self.s.attack_pistol(state) or (self.s.state_shield(state) and self.s.attack_shuriken(state) and self.s.attack_chakram(state)):
			return True
		if self.flag_subweapon_only:
			return self.viy_subweapons(state)
		return self.s.attack_4(state) or (self.s.state_mobility(state) and self.s.attack_main(state))

	def viy_subweapons(self, state: CollectionState) -> bool:
		if self.s.state_mobility(state) or not self.s.state_shield(state):
			if self.s.attack_ring_shuriken(state) and (self.s.attack_rolling_shuriken(state) or self.s.attack_earth_spear(state) or self.s.attack_caltrops(state)):
				return True
			if self.s.attack_rolling_shuriken(state) and (self.s.attack_earth_spear(state) or self.s.attack_chakram(state) or self.s.attack_caltrops(state)):
				return True
			if self.s.attack_chakram(state) and (self.s.attack_caltrops(state) or self.s.attack_earth_spear(state)):
				return True
			return self.s.attack_earth_spear(state) and self.s.attack_caltrops(state)
		return False

	def palenque(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			return state.has_any(('Axe', 'Katana', 'Knife'), self.player) or self.s.attack_rolling_shuriken(state) or self.s.attack_earth_spear(state) or self.s.attack_ring_chakram(state) or self.s.attack_pistol(state)
		return self.s.get_health_count(state) >= 6 and (self.s.attack_rolling_shuriken(state) or self.s.attack_chakram(state) or self.s.attack_earth_spear(state) or self.s.attack_pistol(state))

	def baphomet(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			if self.s.attack_whip(state) or state.has('Axe', self.player) or state.has_all(('Katana', 'Feather'), self.player) or self.s.attack_chakram(state) or self.s.attack_pistol(state):
				return True
			if self.flag_subweapon_only:
				if self.s.attack_shuriken(state) and (state.has('Ring', self.player) or self.s.attack_rolling_shuriken(state) or self.s.attack_caltrops(state)):
					return True
				return self.s.attack_rolling_shuriken(state) and self.s.attack_caltrops(state) and state.has('Feather', self.player)
			return False
		if self.s.get_health_count(state) < 7 or not self.s.state_shield(state):
			return False
		if self.s.attack_ring_chakram(state) or self.s.attack_pistol(state):
			return True
		if self.flag_subweapon_only:
			if self.s.attack_ring_shuriken(state) and self.s.attack_caltrops(state):
				return True
			return self.s.attack_rolling_shuriken(state) and self.s.attack_caltrops(state) and state.has_all(('Feather', 'Ring'), self.player)
		return state.has('Axe', self.player) or (self.s.attack_4(state) and state.has('Feather', self.player))

	def tiamat(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			if state.has('Feather', self.player) and state.has_any(('Leather Whip', 'Chain Whip', 'Flail Whip', 'Axe'), self.player):
				return True
			if self.flag_subweapon_only:
				return self.s.get_health_count(state) >= 8 and self.s.state_shield(state) and self.s.attack_caltrops(state) and self.s.attack_ring_flare_gun(state) and self.s.attack_bomb(state) and state.has('Feather', self.player)
			return False
		health = self.s.get_health_count(state)
		if self.flag_subweapon_only:
			return health >= 10 and self.s.attack_caltrops(state) and self.s.attack_bomb(state) and self.s.attack_flare_gun(state) and state.has_all(('Feather', 'Ring', 'Angel Shield'), self.player)
		if health < 8:
			return False
		return state.has('Feather', self.player) and (state.has_any(('Flail Whip', 'Axe'), self.player) or state.has_all(('Chain Whip', 'Angel Shield'), self.player))

	def mother(self, state: CollectionState) -> bool:
		if self.flag_hard_logic:
			if not state.has('Feather', self.player):
				return False
			if self.s.attack_main(state):
				return True
			if self.flag_subweapon_only:
				return self.s.attack_ring_chakram(state) and self.s.attack_flare_gun(state) and self.s.state_shield(state)
			return False
		if self.s.get_health_count(state) < 8 or not state.has('Feather', self.player):
			return False
		if self.flag_subweapon_only:
			return self.s.attack_ring_chakram(state) and self.s.attack_flare_gun(state) and self.s.state_shield(state) and (self.s.attack_bomb(state) or self.s.attack_caltrops(state))
		return self.s.attack_main(state)

	def hell_temple_bosses(self, state: CollectionState) -> bool:
		# Same hard logic
		if self.s.get_health_count(state) < 8 or not self.s.state_lamp(state):
			return False
		if self.flag_subweapon_only:
			return self.s.attack_ring_chakram(state) or (self.s.attack_pistol(state) and self.s.attack_bomb(state) and self.s.attack_earth_spear(state))
		return state.has('Flail Whip', self.player)
