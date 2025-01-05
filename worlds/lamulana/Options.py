from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, OptionDict, OptionList, PerGameCommonOptions

starting_location_ids = {
	'surface': 0,
	'guidance': 1,
	'mausoleum': 2,
	'sun': 3,
	'spring': 4,
	'inferno': 5,
	'extinction': 6,
	'twin (front)': 7,
	'endless': 8,
	'illusion': 9,
	'graveyard': 10,
	'moonlight': 11,
	'goddess': 12,
	'ruin': 13,
	'birth': 14,
	'twin (back)': 15,
	'gate of time (surface)': 16
}

starting_weapon_ids = {
	'Leather Whip': 0,
	'Knife': 1,
	'Key Sword': 2,
	'Axe': 3,
	'Katana': 4,
	'Shuriken': 5,
	'Rolling Shuriken': 6,
	'Earth Spear': 7,
	'Flare Gun': 8,
	'Bomb': 9,
	'Chakram': 10,
	'Caltrops': 11,
	'Pistol': 12
}

starting_location_names = {y: x for x, y in starting_location_ids.items()}
starting_weapon_names = {y: x for x, y in starting_weapon_ids.items()}


class ShopDensity(Range):
	"""The amount of randomized items placed in shops, with the remainder filled by ammo and weights.
# If set to 0, the only randomized item in a shop is Nebur's 4 guardian item."""
	range_start = 0
	range_end = 50
	default = 30
	display_name = "Shop Item Density"


class RandomizeCoinChests(Choice):
	"""Not supported - must be set to false.
# Randomizes coin chests. Including the escape chest has the potential
# to create rude item chains if NPCs or seals are randomized."""
	display_name = "Randomize coin chests"
	option_off = 0
	option_basic = 1
	option_include_escape_chest = 2
	alias_true = 1


class RandomizeTrapItems(Toggle):
	"""Not suppoted - must be set to false.
# Randomizes the 4 trap items and locations"""
	display_name = "Randomize Trap Items"


class RandomizeSeals(Toggle):
	"""Not supported - must be set to false.
# Individually randomizes which seal is required to break each wall seal"""
	display_name = "Randomize seals"


class RandomizeCursedChests(Toggle):
	"""Not supported - must be set to false.
# If on, a random number of chests will be cursed and require the Mulana Talisman to open.
# If off, CursedChestCount is ignored and the 4 vanilla cursed chests will still be cursed."""
	display_name = "Randomize Cursed Chests"


class CursedChestCount(Range):
	"""Not supported - value will be disregarded.
# The number of chests that will be cursed and require the Mulana Talisman to open.
# The maximum number (101) corresponds to every single chest (including coin and trap chests) being cursed.
# As a result, a random value will skew toward a higher percentage of cursed chests if coin or trap chests aren't randomized."""
	display_name = "Number of Cursed Chests"
	range_start = 0
	range_end = 101
	default = 4


class RandomizeNPCs(Toggle):
	"""Not supported - must be set to off.
# Randomizes all NPCs and shop locations"""
	display_name = "Randomize NPC/shop doors"


class RandomizeDracuetsShop(Toggle):
	"""Not supported - must be set to false.
# Randomize Dracuet's shop in Hell Temple. If NPCs are randomized, includes the Hell Temple shop in the randomized NPC pool"""
	display_name = "Randomize Dracuet's Shop"


class HellTempleReward(Toggle):
	"""Not supported - must be set to false.
# The final reward for beating Hell Temple may be required. A treasure that should not have been created."""
	display_name = "Hell Temple Final Reward"


class StartingLocation(Choice):
	"""Not supported - must be set to surface
# Set or randomize your starting location"""
	display_name = "Starting Location"
	option_surface = starting_location_ids['surface']
	option_gate_of_guidance = starting_location_ids['guidance']
	option_mausoleum_of_the_giants = starting_location_ids['mausoleum']
	option_temple_of_the_sun = starting_location_ids['sun']
	option_spring_in_the_sky = starting_location_ids['spring']
	option_inferno_cavern = starting_location_ids['inferno']
	option_chamber_of_extinction = starting_location_ids['extinction']
	option_twin_labyrinths_front = starting_location_ids['twin (front)']
	option_endless_corridor = starting_location_ids['endless']
	option_gate_of_illusion = starting_location_ids['illusion']
	option_graveyard_of_the_giants = starting_location_ids['graveyard']
	option_temple_of_moonlight = starting_location_ids['moonlight']
	option_tower_of_the_goddess = starting_location_ids['goddess']
	option_tower_of_ruin = starting_location_ids['ruin']
	option_chamber_of_birth = starting_location_ids['birth']
	option_twin_labyrinths_back = starting_location_ids['twin (back)']
	option_gate_of_time_surface = starting_location_ids['gate of time (surface)']


class StartingWeapon(Choice):
	"""Set or randomize your starting weapon"""
	display_name = "Starting Weapon"
	option_leather_whip = starting_weapon_ids['Leather Whip']
	option_knife = starting_weapon_ids['Knife']
	option_key_sword = starting_weapon_ids['Key Sword']
	option_axe = starting_weapon_ids['Axe']
	option_katana = starting_weapon_ids['Katana']
	option_shuriken = starting_weapon_ids['Shuriken']
	option_rolling_shuriken = starting_weapon_ids['Rolling Shuriken']
	option_earth_spear = starting_weapon_ids['Earth Spear']
	option_flare_gun = starting_weapon_ids['Flare Gun']
	option_bomb = starting_weapon_ids['Bomb']
	option_chakram = starting_weapon_ids['Chakram']
	option_caltrops = starting_weapon_ids['Caltrops']
	option_pistol = starting_weapon_ids['Pistol']


class SpecificItem(Choice):
	value: int
	option_start_with = 0
	option_own_world = 1
	option_different_world = 2
	option_any_world = 3
	alias_true = 3
	alias_false = 0


class HolyGrailShuffle(SpecificItem):
	"""Holy Grail placement. Starting with it is generally recommended."""
	display_name = "Holy Grail Shuffle"


class MiraiShuffle(SpecificItem):
	"""mirai.exe placement. Starting with it lets you warp more flexibly."""
	display_name = "mirai.exe Shuffle"


class HermesBootsShuffle(SpecificItem):
	"""Hermes' Boots placement. Starting with them lets you move faster from the beginning."""
	display_name = "Hermes' Boots Shuffle"


class TextTraxShuffle(SpecificItem):
	"""bunemon.exe placement. Often started with as quality of life to record shop inventories and NPC locations in-game"""
	display_name = "TextTrax Shuffle"


class RandomizeTransitions(Choice):
	"""Not supported - must be set to false/off.
# Randomizes transitions (ladders and side exits) between areas.
# "Exclude Oneways" will only include transitions that usually go both ways, whereas "Full" includes one-way transitions"""
	display_name = "Randomize Transitions"
	option_off = 0
	option_exclude_oneways = 1
	option_full = 2
	alias_true = 2


class RandomizeBacksideDoors(Choice):
	"""Not supported - must be set to false/off.
# Randomizes boss door destinations, as well as the required guardian for opening each pair of connected doors.
# "Full" adds the non-boss transitions (Extinction-Gate of Time and Dimensional-Endless Corridor) to the entrance pool.
# "Full" also makes a door pair require a key fairy, and at least 1 door pair be open from the start
# - unlike boss doors, these won't require the Bronze Mirror to go through."""
	display_name = "Randomize Backside Doors"
	option_off = 0
	option_boss_doors_only = 1
	option_full = 2
	alias_true = 2


class RequireIceCape(DefaultOnToggle):
	"""Requires the ice cape for swimming through lava. If off, you may instead need enough health to survive the swim"""
	display_name = "Require Ice Cape for Lava"


class RequireFlareGun(DefaultOnToggle):
	"""Logically requires the flare gun to do anything in the main area of Chamber of Extinction."""
	display_name = "Require Flare Gun for Chamber of Extinction"


class RequireKeyFairyCombo(DefaultOnToggle):
	"""Requires the software combination miracle + mekuri to summon key fairies.
# If off, you may need to grind for key fairies (5% chance)"""
	display_name = "Key Fairies expect miracle + mekuri"


class AutoScanGrailTablets(DefaultOnToggle):
	"""Quality of life - walking past a grail tablet scans it automatically.
# Otherwise, Hand Scanner and reader.exe are required to warp back to it."""
	display_name = "Automatically Scan Grail Tablets"


class BossCheckpoints(DefaultOnToggle):
	"""Quality of life - boss ankhs will trigger a quicksave prior to fighting the boss for fast retry.
# Otherwise, you will respawn at the last grail savepoint."""
	display_name = "Automatically Quicksave At Boss Ankhs"


class GuardianSpecificAnkhJewels(DefaultOnToggle):
	"""If on, each guardian fight has a specific ankh jewel needed to start the fight.
# This is currently not enforced in-game, only logically."""
	display_name = "Guardian-specific Ankh Jewels"


class AlternateMotherAnkh(DefaultOnToggle):
	"""Quality of life - If on, skips the mantra sequence to empower the key sword by adding a 9th ankh jewel.
# Mother's ankh will be like other bosses' and cannot be activated by an empowered key sword."""
	display_name = "Alternate Mother Ankh"


class AncientLaMulaneseLearned(DefaultOnToggle):
	"""Quality of Life - Ancient La-Mulanese is learned from the start, without having to read the 3 translation tablets.
# Ancient La-Mulanese is required to learn mantras."""
	display_name = "Ancient La-Mulanese readable from the start"


class HardCombatLogic(Toggle):
	"""If on, combat logic for bosses and room guardians is minimal:
# Would it be theoretically possible to defeat this boss with these items at low HP?"""
	display_name = "Hard Combat Logic"


# Add note about what happens when you set startingweapon to a main weapon and this is on - maybe overrides it and gives a random subweapon?
class SubweaponOnly(Toggle):
	"""If on, removes all main weapons from the item pool, and all subweapon ammo in shops is free.
# If your starting weapon is set to a main weapon, instead replaces it with a random subweapon.
# Also forces AlternateMotherAnkh to be on, since there is no key sword."""
	display_name = "Subweapon Only Mode"


class RaindropsInLogic(Toggle):
	"""Glitch logic - raindropping may be expected with Hermes' Boots and Grapple Claw"""
	display_name = "Raindrops In Logic"


class CatPausingInLogic(Toggle):
	"""Glitch logic - cat pausing may be expected without any items"""
	display_name = "Cat Pausing In Logic"


class LampGlitchInLogic(Toggle):
	"""Glitch Logic - using the lamp of time to pass through certain walls may be required"""
	display_name = "Lamp Glitch In Logic"


@dataclass
class LaMulanaOptions(PerGameCommonOptions):
	ShopDensity: ShopDensity
	RandomizeCoinChests: RandomizeCoinChests
	RandomizeTrapItems: RandomizeTrapItems

	RandomizeCursedChests: RandomizeCursedChests
	CursedChestCount: CursedChestCount
	
	RandomizeNPCs: RandomizeNPCs
	RandomizeDracuetsShop: RandomizeDracuetsShop
	HellTempleReward: HellTempleReward
	RandomizeSeals: RandomizeSeals
	
	StartingLocation: StartingLocation
	StartingWeapon: StartingWeapon
	
	HolyGrailShuffle: HolyGrailShuffle
	MiraiShuffle: MiraiShuffle
	HermesBootsShuffle: HermesBootsShuffle
	TextTraxShuffle: TextTraxShuffle
	
	RandomizeTransitions: RandomizeTransitions
	RandomizeBacksideDoors: RandomizeBacksideDoors
	
	RequireIceCape: RequireIceCape
	RequireFlareGun: RequireFlareGun
	RequireKeyFairyCombo: RequireKeyFairyCombo
	
	AutoScanGrailTablets: AutoScanGrailTablets
	BossCheckpoints: BossCheckpoints
	GuardianSpecificAnkhJewels: GuardianSpecificAnkhJewels
	AlternateMotherAnkh: AlternateMotherAnkh
	AncientLaMulaneseLearned: AncientLaMulaneseLearned
	
	HardCombatLogic: HardCombatLogic
	SubweaponOnly: SubweaponOnly
	RaindropsInLogic: RaindropsInLogic
	CatPausingInLogic: CatPausingInLogic
	LampGlitchInLogic: LampGlitchInLogic
