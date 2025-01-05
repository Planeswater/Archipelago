from typing import NamedTuple


class ItemData(NamedTuple):
	category: str
	code: int
	progression: bool = False
	useful: bool = False
	trap: bool = False
	number: int = 1
	game_code: int = 0
	cost: int | None = None
	quantity: int = 1
	obtain_flag: int | None = None
	obtain_value: int | None = None


item_table: dict[str, ItemData] = {
	'Leather Whip':                     ItemData('MainWeapon', 2359000, progression=True, game_code=0, obtain_flag=0x863, obtain_value=1, number=0),  # Cannot be sent, only as a starting item
	'Chain Whip':                       ItemData('MainWeapon', 2359001, progression=True, game_code=1, obtain_flag=0x7d, obtain_value=1),
	'Flail Whip':                       ItemData('MainWeapon', 2359002, progression=True, game_code=2, obtain_flag=0x7e, obtain_value=1),
	# gonna reserve 2359003 in case we ever implement progressive whips
	'Knife':                            ItemData('MainWeapon', 2359004, progression=True, game_code=3, obtain_flag=0x7f, obtain_value=1),
	'Key Sword':                        ItemData('MainWeapon', 2359005, progression=True, game_code=4, obtain_flag=0x80, obtain_value=1),
	'Axe':                              ItemData('MainWeapon', 2359006, progression=True, game_code=5, obtain_flag=0x81, obtain_value=1),
	'Katana':                           ItemData('MainWeapon', 2359007, progression=True, game_code=6, obtain_flag=0x82, obtain_value=1),
	'Shuriken':                         ItemData('Subweapon', 2359008, progression=True, game_code=8, obtain_flag=0x83, obtain_value=1),
	'Rolling Shuriken':                 ItemData('Subweapon', 2359009, progression=True, game_code=9, obtain_flag=0x84, obtain_value=1),
	'Earth Spear':                      ItemData('Subweapon', 2359010, progression=True, game_code=10, obtain_flag=0x85, obtain_value=1),
	'Flare Gun':                        ItemData('Subweapon', 2359011, progression=True, game_code=11, obtain_flag=0x86, obtain_value=1),
	'Bomb':                             ItemData('Subweapon', 2359012, progression=True, game_code=12, obtain_flag=0x87, obtain_value=1),
	'Chakram':                          ItemData('Subweapon', 2359013, progression=True, game_code=13, obtain_flag=0x88, obtain_value=1),
	'Caltrops':                         ItemData('Subweapon', 2359014, progression=True, game_code=14, obtain_flag=0x89, obtain_value=1),
	'Pistol':                           ItemData('Subweapon', 2359015, progression=True, game_code=15, obtain_flag=0x8a, obtain_value=2),
	'Buckler':                          ItemData('Shield', 2359016, useful=True, game_code=16, obtain_flag=0x862, obtain_value=1),
	'Fake Silver Shield':               ItemData('Shield', 2359017, game_code=75, obtain_flag=0x82e, obtain_value=2),
	'Silver Shield':                    ItemData('Shield', 2359018, progression=True, game_code=17, obtain_flag=0x8c, obtain_value=1),
	'Angel Shield':                     ItemData('Shield', 2359019, progression=True, game_code=18, obtain_flag=0x8d, obtain_value=2),
	'Ankh Jewel':                       ItemData('Ankh Jewels', 2359020, progression=True, number=0, game_code=19, obtain_flag=0x852, obtain_value=1),  # Adjust ankh jewel amount based on settings
	'Ankh Jewel (Amphisbaena)':         ItemData('Ankh Jewels', 2359021, progression=True, number=0, game_code=19, obtain_flag=0x8e, obtain_value=1),
	'Ankh Jewel (Sakit)':               ItemData('Ankh Jewels', 2359022, progression=True, number=0, game_code=19, obtain_flag=0x8f, obtain_value=1),
	'Ankh Jewel (Ellmac)':              ItemData('Ankh Jewels', 2359023, progression=True, number=0, game_code=19, obtain_flag=0x90, obtain_value=1),
	'Ankh Jewel (Bahamut)':             ItemData('Ankh Jewels', 2359024, progression=True, number=0, game_code=19, obtain_flag=0x91, obtain_value=1),
	'Ankh Jewel (Viy)':                 ItemData('Ankh Jewels', 2359025, progression=True, number=0, game_code=19, obtain_flag=0x92, obtain_value=1),
	'Ankh Jewel (Palenque)':            ItemData('Ankh Jewels', 2359026, progression=True, number=0, game_code=19, obtain_flag=0x93, obtain_value=1),
	'Ankh Jewel (Baphomet)':            ItemData('Ankh Jewels', 2359027, progression=True, number=0, game_code=19, obtain_flag=0x94, obtain_value=1),
	'Ankh Jewel (Tiamat)':              ItemData('Ankh Jewels', 2359028, progression=True, number=0, game_code=19, obtain_flag=0x95, obtain_value=1),
	'Ankh Jewel (Mother)':              ItemData('Ankh Jewels', 2359029, progression=True, number=0, game_code=19, obtain_flag=0x853, obtain_value=1),
	'Hand Scanner':                     ItemData('Usable', 2359030, progression=True, game_code=20, obtain_flag=0x96, obtain_value=2),
	'Djed Pillar':                      ItemData('Usable', 2359031, progression=True, game_code=21, obtain_flag=0x97, obtain_value=2),
	'Mini Doll':                        ItemData('Usable', 2359032, progression=True, game_code=22, obtain_flag=0x98, obtain_value=2),
	'Magatama Jewel':                   ItemData('Usable', 2359033, progression=True, game_code=23, obtain_flag=0x99, obtain_value=2),
	'Cog of the Soul':                  ItemData('Usable', 2359034, progression=True, game_code=24, obtain_flag=0x9a, obtain_value=2),
	'Lamp of Time':                     ItemData('Usable', 2359035, progression=True, game_code=25, obtain_flag=0x9b, obtain_value=2),
	'Pochette Key':                     ItemData('Usable', 2359036, progression=True, game_code=26, obtain_flag=0x9c, obtain_value=2),
	'Dragon Bone':                      ItemData('Usable', 2359037, progression=True, game_code=27, obtain_flag=0x9d, obtain_value=2),
	'Crystal Skull':                    ItemData('Usable', 2359038, progression=True, game_code=28, obtain_flag=0x9e, obtain_value=2),
	'Vessel':                           ItemData('Usable', 2359039, progression=True, game_code=29, obtain_flag=0x9f, obtain_value=2),
	'Medicine of the Mind':             ItemData('Usable', 2359040, progression=True, number=0, game_code=77, obtain_flag=0x85c, obtain_value=1),  # Optionally swap counts with Vessel if a QoL option to skip the medicine process is added
	'Pepper':                           ItemData('Usable', 2359041, progression=True, game_code=30, obtain_flag=0x228, obtain_value=1),
	'Woman Statue':                     ItemData('Usable', 2359042, progression=True, game_code=31, obtain_flag=0xa1, obtain_value=2),
	'Maternity Statue':                 ItemData('Usable', 2359043, progression=True, number=0, game_code=81, obtain_flag=0x10b, obtain_value=2),  # Optionally swap counts with woman statue if a QoL option is added
	'Key of Eternity':                  ItemData('Usable', 2359044, progression=True, game_code=32, obtain_flag=0xa2, obtain_value=2),
	'Serpent Staff':                    ItemData('Usable', 2359045, progression=True, game_code=33, obtain_flag=0xa3, obtain_value=2),
	'Talisman':                         ItemData('Usable', 2359046, progression=True, game_code=34, obtain_flag=0xa4, obtain_value=2),
	'Diary':                            ItemData('Usable', 2359047, progression=True, game_code=72, obtain_flag=0x104, obtain_value=2),
	'Mulana Talisman':                  ItemData('Usable', 2359048, progression=True, game_code=73, obtain_flag=0x105, obtain_value=1),
	'Waterproof Case':                  ItemData('Inventory', 2359049, game_code=36, obtain_flag=0xa5, obtain_value=2),
	'Heatproof Case':                   ItemData('Inventory', 2359050, game_code=37, obtain_flag=0xa6, obtain_value=2),
	'Shell Horn':                       ItemData('Inventory', 2359051, game_code=38, obtain_flag=0xa7, obtain_value=2),
	'Glove':                            ItemData('Inventory', 2359052, useful=True, game_code=39, obtain_flag=0xa8, obtain_value=2),
	'Holy Grail':                       ItemData('Inventory', 2359053, progression=True, game_code=40, obtain_flag=0xa9, obtain_value=2),
	'Isis\' Pendant':                   ItemData('Inventory', 2359054, progression=True, game_code=41, obtain_flag=0xaa, obtain_value=2),
	'Crucifix':                         ItemData('Inventory', 2359055, useful=True, game_code=42, obtain_flag=0xab, obtain_value=2),
	'Helmet':                           ItemData('Inventory', 2359056, progression=True, game_code=43, obtain_flag=0xac, obtain_value=1),
	'Grapple Claw':                     ItemData('Inventory', 2359057, progression=True, game_code=44, obtain_flag=0xad, obtain_value=2),
	'Bronze Mirror':                    ItemData('Inventory', 2359058, progression=True, game_code=45, obtain_flag=0xae, obtain_value=2),
	'Eye of Truth':                     ItemData('Inventory', 2359059, progression=True, game_code=46, obtain_flag=0xaf, obtain_value=2),
	'Ring':                             ItemData('Inventory', 2359060, progression=True, game_code=47, obtain_flag=0xb0, obtain_value=1),
	'Scalesphere':                      ItemData('Inventory', 2359061, progression=True, game_code=48, obtain_flag=0xb1, obtain_value=2),
	'Gauntlet':                         ItemData('Inventory', 2359062, useful=True, game_code=49, obtain_flag=0xb2, obtain_value=2),
	'Anchor':                           ItemData('Inventory', 2359063, progression=True, game_code=50, obtain_flag=0x84c, obtain_value=2),
	'Plane Model':                      ItemData('Inventory', 2359064, progression=True, game_code=51, obtain_flag=0xb4, obtain_value=2),
	'Philosopher\'s Ocarina':           ItemData('Inventory', 2359065, progression=True, game_code=52, obtain_flag=0xb5, obtain_value=2),
	'Feather':                          ItemData('Inventory', 2359066, progression=True, game_code=53, obtain_flag=0xb6, obtain_value=2),
	'Book of the Dead':                 ItemData('Inventory', 2359067, progression=True, game_code=54, obtain_flag=0x32a, obtain_value=2),
	'Fairy Clothes':                    ItemData('Inventory', 2359068, useful=True, game_code=55, obtain_flag=0xb8, obtain_value=2),
	'Scriptures':                       ItemData('Inventory', 2359069, useful=True, game_code=56, obtain_flag=0xb9, obtain_value=2),
	'Hermes\' Boots':                   ItemData('Inventory', 2359070, progression=True, game_code=57, obtain_flag=0xba, obtain_value=2),
	'Fruit of Eden':                    ItemData('Inventory', 2359071, progression=True, game_code=58, obtain_flag=0xbb, obtain_value=2),
	'Twin Statue':                      ItemData('Inventory', 2359072, progression=True, game_code=59, obtain_flag=0xbc, obtain_value=2),
	'Bracelet':                         ItemData('Inventory', 2359073, useful=True, game_code=60, obtain_flag=0xbd, obtain_value=2),
	'Perfume':                          ItemData('Inventory', 2359074, useful=True, game_code=61, obtain_flag=0xbe, obtain_value=2),
	'Spaulder':                         ItemData('Inventory', 2359075, game_code=62, obtain_flag=0xbf, obtain_value=2),
	'Dimensional Key':                  ItemData('Inventory', 2359076, progression=True, game_code=63, obtain_flag=0xc0, obtain_value=2),
	'Ice Cape':                         ItemData('Inventory', 2359077, progression=True, game_code=64, obtain_flag=0xc1, obtain_value=2),
	'Origin Seal':                      ItemData('Inventory', 2359078, progression=True, game_code=65, obtain_flag=0xc2, obtain_value=2),
	'Birth Seal':                       ItemData('Inventory', 2359079, progression=True, game_code=66, obtain_flag=0xc3, obtain_value=2),
	'Life Seal':                        ItemData('Inventory', 2359080, progression=True, game_code=67, obtain_flag=0xc4, obtain_value=2),
	'Death Seal':                       ItemData('Inventory', 2359081, progression=True, game_code=68, obtain_flag=0xc5, obtain_value=2),
	'Sacred Orb (Surface)':             ItemData('Sacred Orb', 2359139, progression=True, game_code=69, obtain_flag=0xc8, obtain_value=1),
	'Sacred Orb (Gate of Guidance)':    ItemData('Sacred Orb', 2359140, progression=True, game_code=69, obtain_flag=0xc7, obtain_value=1),
	'Sacred Orb (Mausoleum of the Giants)': ItemData('Sacred Orb', 2359141, progression=True, game_code=69, obtain_flag=0xc9, obtain_value=1),
	'Sacred Orb (Temple of the Sun)':   ItemData('Sacred Orb', 2359142, progression=True, game_code=69, obtain_flag=0xca, obtain_value=1),
	'Sacred Orb (Spring in the Sky)':   ItemData('Sacred Orb', 2359143, progression=True, game_code=69, obtain_flag=0xcb, obtain_value=1),
	'Sacred Orb (Tower of Ruin)':       ItemData('Sacred Orb', 2359144, progression=True, game_code=69, obtain_flag=0xcf, obtain_value=1),
	'Sacred Orb (Chamber of Extinction)': ItemData('Sacred Orb', 2359145, progression=True, game_code=69, obtain_flag=0xcc, obtain_value=1),
	'Sacred Orb (Twin Labyrinths)':     ItemData('Sacred Orb', 2359146, progression=True, game_code=69, obtain_flag=0xcd, obtain_value=1),
	'Sacred Orb (Dimensional Corridor)':  ItemData('Sacred Orb', 2359147, progression=True, game_code=69, obtain_flag=0xd0, obtain_value=1),
	'Sacred Orb (Shrine of the Mother)':  ItemData('Sacred Orb', 2359148, progression=True, game_code=69, obtain_flag=0xce, obtain_value=1),
	'Treasures':                        ItemData('Inventory', 2359083, progression=True, game_code=71, obtain_flag=0x103, obtain_value=2),
	'Mobile Super X2':                  ItemData('Inventory', 2359084, useful=True, game_code=76, obtain_flag=0x2e6, obtain_value=2),
	'Provocative Bathing Suit':         ItemData('Inventory', 2359085, game_code=74, obtain_flag=0x106, obtain_value=2),
	'reader.exe':                       ItemData('Software', 2359086, progression=True, game_code=85, obtain_flag=0xe2, obtain_value=2),
	'xmailer.exe':                      ItemData('Software', 2359087, game_code=86, obtain_flag=0xe3, obtain_value=1),
	'yagomap.exe':                      ItemData('Software', 2359088, progression=True, game_code=87, obtain_flag=0xe4, obtain_value=2),
	'yagostr.exe':                      ItemData('Software', 2359089, progression=True, game_code=88, obtain_flag=0xe5, obtain_value=2),
	'bunemon.exe':                      ItemData('Software', 2359090, useful=True, game_code=89, obtain_flag=0xe6, obtain_value=2),
	'bunplus.com':                      ItemData('Software', 2359091, game_code=90, obtain_flag=0xe7, obtain_value=1),
	'torude.exe':                       ItemData('Software', 2359092, progression=True, game_code=91, obtain_flag=0xe8, obtain_value=2),
	'guild.exe':                        ItemData('Software', 2359093, progression=True, game_code=92, obtain_flag=0xe9, obtain_value=2),  # progression only if Hell Temple on
	'mantra.exe':                       ItemData('Software', 2359094, progression=True, game_code=93, obtain_flag=0xea, obtain_value=2),
	'emusic.exe':                       ItemData('Software', 2359095, game_code=94, obtain_flag=0xeb, obtain_value=1),
	'beolamu.exe':                      ItemData('Software', 2359096, game_code=95, obtain_flag=0xec, obtain_value=1),
	'deathv.exe':                       ItemData('Software', 2359097, useful=True, game_code=96, obtain_flag=0x14f, obtain_value=2),
	'randc.exe':                        ItemData('Software', 2359098, useful=True, game_code=97, obtain_flag=0xee, obtain_value=2),
	'capstar.exe':                      ItemData('Software', 2359099, game_code=98, obtain_flag=0xef, obtain_value=2),
	'move.exe':                         ItemData('Software', 2359100, useful=True, game_code=99, obtain_flag=0xf0, obtain_value=2),
	'mekuri.exe':                       ItemData('Software', 2359101, progression=True, game_code=100, obtain_flag=0xf1, obtain_value=2),  # progression if key fairy combo
	'bounce.exe':                       ItemData('Software', 2359102, game_code=101, obtain_flag=0xf2, obtain_value=2),
	'miracle.exe':                      ItemData('Software', 2359103, progression=True, game_code=102, obtain_flag=0xf3, obtain_value=2),  # progression if key fairy combo or NPC rando
	'mirai.exe':                        ItemData('Software', 2359104, progression=True, game_code=103, obtain_flag=0xf4, obtain_value=2),
	'lamulana.exe':                     ItemData('Software', 2359105, useful=True, game_code=104, obtain_flag=0xf5, obtain_value=2),
	'Map (Surface)':                    ItemData('Map', 2359106, game_code=70, obtain_flag=0xd1, obtain_value=2),
	'Map (Gate of Guidance)':           ItemData('Map', 2359107, game_code=70, obtain_flag=0xd2, obtain_value=2),
	'Map (Mausoleum of the Giants)':    ItemData('Map', 2359108, game_code=70, obtain_flag=0xd3, obtain_value=2),
	'Map (Temple of the Sun)':          ItemData('Map', 2359109, game_code=70, obtain_flag=0xd4, obtain_value=2),
	'Map (Spring in the Sky)':          ItemData('Map', 2359110, game_code=70, obtain_flag=0xd5, obtain_value=2),
	'Map (Inferno Cavern)':             ItemData('Map', 2359111, game_code=70, obtain_flag=0xd6, obtain_value=2),
	'Map (Chamber of Extinction)':      ItemData('Map', 2359112, game_code=70, obtain_flag=0xd7, obtain_value=2),
	'Map (Twin Labyrinths)':            ItemData('Map', 2359113, game_code=70, obtain_flag=0xd8, obtain_value=2),
	'Map (Endless Corridor)':           ItemData('Map', 2359114, game_code=70, obtain_flag=0xd9, obtain_value=2),
	'Map (Shrine of the Mother)':       ItemData('Map', 2359115, progression=True, game_code=70, obtain_flag=0xda, obtain_value=2),
	'Map (Gate of Illusion)':           ItemData('Map', 2359116, game_code=70, obtain_flag=0xdb, obtain_value=2),
	'Map (Graveyard of the Giants)':    ItemData('Map', 2359117, game_code=70, obtain_flag=0xdc, obtain_value=2),
	'Map (Temple of Moonlight)':        ItemData('Map', 2359118, game_code=70, obtain_flag=0xdd, obtain_value=2),
	'Map (Tower of the Goddess)':       ItemData('Map', 2359119, game_code=70, obtain_flag=0xde, obtain_value=2),
	'Map (Tower of Ruin)':              ItemData('Map', 2359120, game_code=70, obtain_flag=0xdf, obtain_value=2),
	'Map (Chamber of Birth)':           ItemData('Map', 2359121, game_code=70, obtain_flag=0xe0, obtain_value=2),
	'Map (Dimensional Corridor)':       ItemData('Map', 2359122, game_code=70, obtain_flag=0xe1, obtain_value=2),
	'Shuriken Ammo':                    ItemData('ShopInventory', 2359123, number=0, progression=True, game_code=107, quantity=10, cost=10),
	'Rolling Shuriken Ammo':            ItemData('ShopInventory', 2359124, number=0, progression=True, game_code=108, quantity=10, cost=10),
	'Earth Spear Ammo':                 ItemData('ShopInventory', 2359125, number=0, progression=True, game_code=109, quantity=10, cost=20),
	'Flare Gun Ammo':                   ItemData('ShopInventory', 2359126, number=0, progression=True, game_code=110, quantity=10, cost=40),
	'Bomb Ammo':                        ItemData('ShopInventory', 2359127, number=0, progression=True, game_code=111, quantity=10, cost=80),
	'Chakram Ammo':                     ItemData('ShopInventory', 2359128, number=0, progression=True, game_code=112, quantity=2, cost=55),
	'Caltrops Ammo':                    ItemData('ShopInventory', 2359129, number=0, progression=True, game_code=113, quantity=10, cost=30),
	'Pistol Ammo':                      ItemData('ShopInventory', 2359130, number=0, progression=True, game_code=114, quantity=1, cost=350),
	'5 Weights':                        ItemData('ShopInventory', 2359131, number=0, game_code=105, quantity=5, cost=10),
	'200 coins':                        ItemData('Resource', 2359132, number=0, game_code=-10, quantity=200),
	'100 coins':                        ItemData('Resource', 2359133, number=0, game_code=-10, quantity=100),
	'50 coins':                         ItemData('Resource', 2359134, number=0, game_code=-10, quantity=50),
	'30 coins':                         ItemData('Resource', 2359135, number=0, game_code=-10, quantity=30),
	'10 coins':                         ItemData('Resource', 2359136, number=0, game_code=-10, quantity=10),
	'1 Weight':                         ItemData('Resource', 2359137, number=0, game_code=-9, quantity=1),
	'Holy Grail (Full)':                ItemData('Inventory', 2359138, progression=False, game_code=83, number=0),  # Placeholder for Sending to Other Players
	# Gap in IDs for other possible items in pool before trap items
	'Bat Trap':                         ItemData('Trap', 2359160, trap=True, number=0),
	'Explosive Trap':                   ItemData('Trap', 2359161, trap=True, number=0),
}


def get_items_by_category():
	categories: dict[str, set[str]] = {}
	for name, data in item_table.items():
		categories.setdefault(data.category, set()).add(name)
	return categories


item_exclusion_order = ['Map (Surface)', 'Map (Gate of Guidance)', 'Map (Mausoleum of the Giants)', 'Map (Temple of the Sun)', 'Map (Spring in the Sky)', 'Map (Inferno Cavern)', 'Map (Chamber of Extinction)', 'Map (Twin Labyrinths)', 'Map (Endless Corridor)', 'Map (Gate of Illusion)', 'Map (Graveyard of the Giants)', 'Map (Temple of Moonlight)', 'Map (Tower of the Goddess)', 'Map (Tower of Ruin)', 'Map (Chamber of Birth)', 'Map (Dimensional Corridor)', 'beolamu.exe', 'emusic.exe', 'bunplus.com', 'xmailer.exe', 'Waterproof Case', 'Heatproof Case', 'bounce.exe', 'capstar.exe', 'Fake Silver Shield', 'Shell Horn']
