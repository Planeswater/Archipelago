from .FileMod import FileMod
from .Dat import Dat
from .Items import item_table
from .LmFlags import GLOBAL_FLAGS, HEADERS, CARDS

FONT = \
        u"!\"&'(),-./0123456789:?ABCDEFGHIJKLMNOPQRSTUVWXYZ"\
        u"　]^_abcdefghijklmnopqrstuvwxyz…♪、。々「」ぁあぃいぅうぇえぉおか"\
        u"がきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほ"\
        u"ぼぽまみむめもゃやゅゆょよらりるれろわをんァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセ"\
        u"ゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリル"\
        u"レロワヲンヴ・ー一三上下不与世丘両中丸主乗乙乱乳予争事二人今介仕他付代以仮仲件会伝位低住体何作使"\
        u"供侵係保信俺倍倒値偉側偶備傷像僧元兄先光兜入全公具典内再冒冥出刀分切列初別利刻則前剣創力加助効勇"\
        u"勉動化匹十半協博印危去参双反取受叡口古召可台史右司合同名向否周呪味呼命品唯唱問喜営器噴四回囲図国"\
        u"土在地坂型域基堂報場塊塔墓増壁壇壊士声売壷変外多夜夢大天太央失奇契奥女好妊妖妻始姿娘婦子字存孤学"\
        u"宇守官宙定宝実客室宮家密寝対封専導小少尾屋屏属山岩崖崩嵐左巨己布帯帰常年幸幻幾広床底店度座庫廊廟"\
        u"弁引弟弱張強弾当形影役彼待後心必忍忘応念怒思急性怨恐息恵悔悟悪悲情惑想意愚愛感慈態憶我戦戻所扉手"\
        u"扱投抜押拝拡拳拾持指振探撃撮操支攻放敗教散数敵敷文料斧断新方旅族日早昇明昔星映時晩普晶智暗曲書最"\
        u"月有服望未末本杉村杖束来杯板析果架柱査格械棺検椿楼楽槍様槽模樹橋機欠次欲歓止正武歩歯歳歴死殊残段"\
        u"殺殿母毒毛気水氷永求汝池決治法波泥注洞洪流海消涙涯深済減湖満源溶滅滝火灯灼炎無然熱爆爪父版牛物特"\
        u"犬状狂独獄獅獣玄玉王珠現球理瓶生産用男画界略番発登白百的盤目直盾看真眠着知石研破碑示礼社祈祖神祠"\
        u"祭禁福私秘秤移種穴究空突窟立竜章竪端笛符第筒答箱範精系約納純紫細紹終経結続緑練罠罪罰義羽習翻翼老"\
        u"考者耐聖聞肉肩胸能脱腕自至船色若苦英荷華落葉蔵薇薔薬蛇血行術衛表裁装裏補製複要見覚親解言記訳証試"\
        u"話詳認誕誘語誠説読誰調論謁謎謝識議護谷貝財貧貯買貸資賢贄贖赤走起超足跡路踊蹴身車軽輝辞込辿近返迷"\
        u"追送逃通速造連進遊過道達違遠適選遺還郎部配重野量金針鉄銀銃銅録鍵鎖鏡長門閉開間関闇闘防限険陽階隠"\
        u"雄雑難雨霊青静面革靴音順領頭題顔願類風飛食館馬駄験骨高魂魔魚鳥鳴黄黒泉居転清成仏拠維視宿浮熟飾冷"\
        u"得集安割栄偽屍伸巻緒捨固届叩越激彫蘇狭浅Ⅱ［］：！？～／０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪ"\
        u"ＫＬＭＮＯＰＲＳＴＵＶＷＸＹａｂｄｅｇｈｉｌｍｏｐｒｓｔｕｘ辺薄島異温復称狙豊穣虫絶ＱＺｃｆｊｋ"\
        u"ｎｑｖｗｙｚ＋－旧了設更横幅似確置整＞％香ü描園為渡象相聴比較掘酷艇原民雷絵南米平木秋田県湯環砂"\
        u"漠角運湿円背負構授輪圏隙草植快埋寺院妙該式判（）警告収首腰芸酒美組各演点勝観編丈夫姫救’，．霧節"\
        u"幽技師柄期瞬電購任販Á;û+→↓←↑⓪①②③④⑤⑥⑦⑧⑨<”挑朝痛魅鍛戒飲憂照磨射互降沈醜触煮疲"\
        u"素競際易堅豪屈潔削除替Ü♡*$街極ＵＤＦ▲✖■●✕七並久五亜亡交仰余依便修個借倣働儀償優免六共冑"\
        u"冠冶凄凍凶刃制刺労勢勿包医卑単厄及吐含吸吹咆和員哮哺商善喰噂噛嚇因団困圧垂執塗塞境奪威婆嫌完害容"\
        u"寄寒寛察尋尽峙巡巧差幼建弄彩往徊従徘御微徳徴忌怖怪恨悠慢慮憑憧扇才払抱担拶拷挙挨捕排掛掟接揃揮故"\
        u"敏敢旋既旺昂昆春是暑暮暴朽材枚枝染柔株根案棒森業権歌油泳活派浴液測準潜烈烏焼燃爵片牽狩狼猛猟猫献"\
        u"猿獲率珍甦由甲病症痩療癒皮益盛監眼睡矛短砕硬磁礁禽秀程穏筋管築簡粉粘糞級給統継綿総線縁縛縦織羅羊"\
        u"群耳職肌股肢肪育脂脅脈脚腐膚膜臭致興舞般良花荒葬蛮被裂襲覆討託訪詰諸貢質赦趣距跳軍軟迂迎迫逆透途"\
        u"這遅遥避邪都酸銭鋭錬鎌鑑闊阻陥陰陸障離震露非預頼額養騙驚骸髪鱗鶏鹿鼻龍"

class DatMod(FileMod):

    def __init__(self, filename, local_config, options):
        super().__init__(Dat, filename, local_config, options, GLOBAL_FLAGS["dat_filler_items"])

    def place_item_in_location(self, item, item_id, location) -> None:
        params = {
            "item_id": item_id,
            "location": location,
            "item": item
        }
        super().set_params(params)
        for card_index in location.cards:
            params["card"] = self.file_contents.cards[card_index]
            params["entries"] = self.file_contents.cards[card_index].contents.entries

            if location.slot is None:
                self.__place_conversation_item(**params)
                if card_index == CARDS["xelpud_xmailer"]:
                    self.__update_xelpud_xmailer_flag(params["new_obtain_flag"])
            else:
                self.__place_shop_item(**params)

    def apply_mods(self):
        self.__rewrite_xelpud_flag_checks()
        self.__rewrite_xelpud_mulana_talisman_conversation()
        self.__rewrite_xelpud_talisman_conversation()
        self.__rewrite_xelpud_pillar_conversation()
        self.__update_slushfund_flags()

    def find_shop_flag(self, card_name, slot):
        shop_card = self.__find_card(card_name)
        entries = shop_card.contents.entries
        data_indices = [i for i, v in enumerate(entries) if v.header == HEADERS["data"]]
        return entries[data_indices[3]].contents.values[slot]

    # DAT Mod Methods

    def __place_conversation_item(self, card, entries, item_id, location, item, original_obtain_flag, new_obtain_flag, obtain_value):
        item_index = next((i for i, v in enumerate(entries) if v.header == HEADERS["item"] and v.contents.value == location.item_id), None)
        entries[item_index].contents.value = item_id

        flag_index = next((i for i, v in enumerate(entries) if v.header == HEADERS["flag"] and v.contents.address == original_obtain_flag), None)
        entries[flag_index].contents.address = new_obtain_flag
        entries[flag_index].contents.value = obtain_value

    def __place_shop_item(self, card, entries, item_id, location, item, original_obtain_flag, new_obtain_flag, obtain_value):
        # Override Other Player Item to Map if in a Shop to prevent quantity from selling out
        if item_id == item_table["Holy Grail (Full)"].game_code:
            item_id = item_table["Map (Surface)"].game_code
        data_indices = [i for i, v in enumerate(entries) if v.header == HEADERS["data"]]
        entries[data_indices[0]].contents.values[location.slot] = item_id
        item_cost = item.cost if item and item.cost is not None else 10
        entries[data_indices[1]].contents.values[location.slot] = item_cost
        item_quantity = item.quantity if item and item.quantity is not None else 1
        entries[data_indices[2]].contents.values[location.slot] = item_quantity
        entries[data_indices[3]].contents.values[location.slot] = new_obtain_flag
        if obtain_value > 1:
            entries[data_indices[6]].contents.values[location.slot] = new_obtain_flag

        # Set New Item Name In Shop Description

        # The item descriptions in a shop are always the 7th, 8th, and 9th lines, so we want to start from the 6th break
        break_indices = [i for i, v in enumerate(entries) if v.header == HEADERS["break"]]
        item_description_start_index = break_indices[6+location.slot]

        # The item name always appears between color entries
        color_indices = [i+item_description_start_index for i, v in enumerate(entries[item_description_start_index:]) if v.header == HEADERS["color"]]
        item_name_start_index = color_indices[0] + 1

        # Encode the new item name as Entries
        item_name = location.item.name if location.item and location.item.name is not None else "Unknown"
        item_name_entries = [self.__char_entry(codepoint) for codepoint in self.__encode(item_name)]

        # Remove the old item name
        del entries[item_name_start_index:color_indices[1]]
        removed_name_size = 2 * (color_indices[1] - color_indices[0] - 1)
        card.len_contents -= removed_name_size
        self.file_size -= removed_name_size

        # Add thew new item name
        entries[item_name_start_index:item_name_start_index] = item_name_entries
        added_name_size = 2 * len(item_name_entries)
        card.len_contents += added_name_size
        self.file_size += added_name_size

    def __rewrite_xelpud_flag_checks(self) -> None:
        card = self.__find_card("xelpud_conversation_tree")

        entries_to_remove = [
            CARDS["xelpud_howling_wind"],
            CARDS["xelpud_xmailer"],
            CARDS["xelpud_pillar"],
            CARDS["xelpud_mulana_talisman"]
        ]
        for entry_value in entries_to_remove:
            self.__remove_data_entry_by_value(card, entry_value)

        data_values_to_add = [
            [GLOBAL_FLAGS["diary_found"], 1, CARDS["xelpud_mulana_talisman"], 0],
            [GLOBAL_FLAGS["talisman_found"], 2, CARDS["xelpud_pillar"], 0],
            [GLOBAL_FLAGS["talisman_found"], 1, CARDS["xelpud_talisman"], 0],
            [GLOBAL_FLAGS["xmailer"], 0, CARDS["xelpud_xmailer"], 0]
        ]
        for data_values in data_values_to_add:
            self.__add_data_entry(card, data_values)

    def __update_xelpud_xmailer_flag(self, new_flag):
        card = self.__find_card("xelpud_conversation_tree")
        entries = card.contents.entries

        for entry in entries:
            if entry.header == HEADERS["data"] and entry.contents.values[0] == GLOBAL_FLAGS["xmailer"]:
                entry.contents.values[0] = new_flag
                break

    def __rewrite_xelpud_mulana_talisman_conversation(self) -> None:
        card = self.__find_card("xelpud_mulana_talisman")
        entries = card.contents.entries

        talisman_flag_entries = [(i, entry) for i, entry in enumerate(entries)
            if entry.header == HEADERS["flag"] and entry.contents.address == GLOBAL_FLAGS["mulana_talisman"]
        ]
        for _, flag_entry in talisman_flag_entries:
            flag_entry.contents.address = GLOBAL_FLAGS["diary_found"]
            flag_entry.contents.value = 2

        insert_index = max([i for i, _ in talisman_flag_entries])
        self.__add_flag_entry(card, insert_index, GLOBAL_FLAGS["mulana_talisman"], 2)

        diary_puzzle_index = next((i for i, entry in enumerate(entries)
            if entry.header == HEADERS["flag"] and entry.contents.address == GLOBAL_FLAGS["diary_chest_puzzle"]
        ), None)
        self.__remove_flag_entry(card, diary_puzzle_index)

    def __rewrite_xelpud_talisman_conversation(self) -> None:
        card = self.__find_card("xelpud_talisman")
        entries = card.contents.entries

        insert_index = max([i for i, entry in enumerate(entries)
            if entry.header == HEADERS["flag"] and entry.contents.address == GLOBAL_FLAGS["cant_leave_conversation"]
        ])

        self.__add_flag_entry(card, insert_index, GLOBAL_FLAGS["talisman_found"], 2)
        self.__add_flag_entry(card, insert_index, GLOBAL_FLAGS["xelpud_talisman"], 1)

    def __rewrite_xelpud_pillar_conversation(self) -> None:
        card = self.__find_card("xelpud_pillar")
        entries = card.contents.entries

        diary_chest_flag_index = next((i for i, entry in enumerate(entries)
            if entry.header == HEADERS["flag"] and entry.contents.address == GLOBAL_FLAGS["shrine_diary_chest"]
        ), None)
    
        self.__remove_flag_entry(card, diary_chest_flag_index)

        insert_index = max([i for i, entry in enumerate(entries)
            if entry.header == HEADERS["flag"] and entry.contents.address == GLOBAL_FLAGS["cant_leave_conversation"]
        ])
    
        self.__add_flag_entry(card, insert_index, GLOBAL_FLAGS["talisman_found"], 3)

    def __update_slushfund_flags(self) -> None:
        card = self.__find_card("slushfund_give_pepper")
        self.__add_flag_entry(card, len(card.contents.entries), GLOBAL_FLAGS["replacement_slushfund_conversation"], 1)
        card = self.__find_card("slushfund_give_anchor")
        self.__add_flag_entry(card, len(card.contents.entries), GLOBAL_FLAGS["replacement_slushfund_conversation"], 2)

    # Utility Methods

    def __find_card(self, card_name):
        card_index = CARDS[card_name]
        return self.file_contents.cards[card_index]

    def __remove_data_entry_by_value(self, card, value):
        entries = card.contents.entries
        entry_index = next((i for i, v in enumerate(entries) if v.header == HEADERS["data"] and v.contents.values[2] == value))
        next_index_to_delete = entry_index + 2

        size = 6 + (entries[entry_index].contents.num_values * 2)
        # Final Entry doesn't have a break after it
        if entry_index == (len(entries) - 1):
            size -= 2
            next_index_to_delete -= 1

        del entries[entry_index:next_index_to_delete]
        self.file_size -= size
        card.len_contents -= size

    def __add_data_entry(self, card, data_values):
        entries = card.contents.entries
        break_entry = Dat.Entry()
        break_entry.header = HEADERS["break"]
        break_entry.contents = Dat.Noop()
        break_entry.contents.no_value = bytearray()

        data = Dat.Data()
        data.num_values = len(data_values)
        data.values = data_values

        data_entry = Dat.Entry()
        data_entry.header = HEADERS["data"]
        data_entry.contents = data

        entries.append(break_entry)
        entries.append(data_entry)

        file_mod = (6 + (data.num_values * 2))
        self.file_size += file_mod
        card.len_contents += file_mod

    def __add_flag_entry(self, card, index, address, value):
        entries = card.contents.entries
        flag = Dat.Flag()
        flag.address = address
        flag.value = value

        flag_entry = Dat.Entry()
        flag_entry.header = HEADERS["flag"]
        flag_entry.contents = flag

        entries.insert(index, flag_entry)

        self.file_size += 6
        card.len_contents += 6

    def __remove_flag_entry(self, card, index):
        entries = card.contents.entries
        if index is not None:
            del entries[index]
            self.file_size -= 6
            card.len_contents -= 6

    def __decode(self, entries):
        text = [FONT[entry.header-0x100] for entry in entries]
        return ''.join(text)

    def __encode(self, text):
        return [self.__encode_char(char) for char in text]

    def __encode_char(self, char):
        if char == " ":
            return HEADERS["white_space"]
        encoded_char = FONT.find(char)
        if encoded_char == -1:
            encoded_char = FONT.find("?")
        return encoded_char + 0x100

    def __char_entry(self, codepoint):
        char_entry = Dat.Entry()
        char_entry.header = codepoint
        char_entry.contents = Dat.Noop()
        char_entry.contents.no_value = bytearray()
        return char_entry
