#!/usr/bin/env python3

import re

from .tools import icat, changelog
from .fixer import WowToolsFixer


IGNORE_TITLE_ID = [
    29,   # Gladiator %s https://www.wowhead.com/title=42
    30,   # Duelist %s https://www.wowhead.com/title=43
    31,   # Rival %s https://www.wowhead.com/title=44
    32,   # Challenger %s https://www.wowhead.com/title=45
    54,   # %s of the Ten Storms https://www.wowhead.com/title=86
    55,   # %s of the Emerald Dream https://www.wowhead.com/title=87
    57,   # Prophet %s https://www.wowhead.com/title=89
    58,   # %s the Malefic https://www.wowhead.com/title=90
    60,   # %s of the Ebon Blade https://www.wowhead.com/title=92
    63,   # Assassin %s https://www.wowhead.com/title=95
    64,   # Grand Master Alchemist %s https://www.wowhead.com/title=96
    65,   # Grand Master Blacksmith https://www.wowhead.com/title=97
    66,   # Iron Chef https://www.wowhead.com/title=98
    67,   # Grand Master Enchanter https://www.wowhead.com/title=99
    68,   # Grand Master Engineer https://www.wowhead.com/title=100
    69,   # Doctor %s https://www.wowhead.com/title=101
    70,   # Grand Master Angler https://www.wowhead.com/title=102
    71,   # Grand Master Herbalist https://www.wowhead.com/title=103
    72,   # Grand Master Scribe https://www.wowhead.com/title=104
    73,   # Grand Master Jewelcrafter https://www.wowhead.com/title=105
    74,   # Grand Master Leatherworker %s https://www.wowhead.com/title=106
    75,   # Grand Master Miner https://www.wowhead.com/title=107
    76,   # Grand Master Skinner %s https://www.wowhead.com/title=108
    77,   # Grand Master Tailor %s https://www.wowhead.com/title=109
    78,   # Combatant %s https://www.wowhead.com/title=110
    82,   # The Lion Hearted https://www.wowhead.com/title=114
    83,   # Champion of Elune https://www.wowhead.com/title=115
    84,   # Hero of Orgrimmar https://www.wowhead.com/title=116
    85,   # Plainsrunner https://www.wowhead.com/title=117
    86,   # Of the Darkspear https://www.wowhead.com/title=118
    87,   # %s the Forsaken https://www.wowhead.com/title=119
    91,   # Hero of Northrend https://www.wowhead.com/title=123
    147,  # Slayer of Stupid, Incompet[...] https://www.wowhead.com/title=188
    154,  # Private %s https://www.wowhead.com/title=195
    155,  # Corporal %s https://www.wowhead.com/title=196
    156,  # Sergeant %s https://www.wowhead.com/title=197
    157,  # Master Sergeant %s https://www.wowhead.com/title=198
    158,  # Sergeant Major %s https://www.wowhead.com/title=199
    159,  # Knight %s https://www.wowhead.com/title=200
    160,  # Knight-Lieutenant %s https://www.wowhead.com/title=201
    161,  # Knight-Captain %s https://www.wowhead.com/title=202
    162,  # Knight-Champion %s https://www.wowhead.com/title=203
    163,  # Lieutenant Commander %s https://www.wowhead.com/title=204
    164,  # Commander %s https://www.wowhead.com/title=205
    165,  # Marshal %s https://www.wowhead.com/title=206
    166,  # Field Marshal %s https://www.wowhead.com/title=207
    167,  # Grand Marshal %s https://www.wowhead.com/title=208
    168,  # Scout %s https://www.wowhead.com/title=209
    169,  # Grunt %s https://www.wowhead.com/title=210
    170,  # Sergeant %s https://www.wowhead.com/title=211
    171,  # Senior Sergeant %s https://www.wowhead.com/title=212
    172,  # First Sergeant %s https://www.wowhead.com/title=213
    173,  # Stone Guard %s https://www.wowhead.com/title=214
    174,  # Blood Guard %s https://www.wowhead.com/title=215
    175,  # Legionnaire %s https://www.wowhead.com/title=216
    176,  # Centurion %s https://www.wowhead.com/title=217
    177,  # Champion %s https://www.wowhead.com/title=218
    178,  # Lieutenant General %s https://www.wowhead.com/title=219
    179,  # General %s https://www.wowhead.com/title=220
    180,  # Warlord %s https://www.wowhead.com/title=221
    181,  # High Warlord %s https://www.wowhead.com/title=222
    224,  # Gob Squad Recruit https://www.wowhead.com/title=344
    226,  # Gob Squad Commando https://www.wowhead.com/title=347
    231,  # The Poisoned Mind https://www.wowhead.com/title=354
    232,  # %s the Bloodseeker https://www.wowhead.com/title=355
    233,  # The Locust https://www.wowhead.com/title=356
    234,  # The Swarmkeeper https://www.wowhead.com/title=357
    235,  # %s the Prime https://www.wowhead.com/title=358
    236,  # %s the Manipulator https://www.wowhead.com/title=359
    237,  # %s the Dissector https://www.wowhead.com/title=360
    238,  # The Lucid https://www.wowhead.com/title=361
    239,  # The Wind-Reaver https://www.wowhead.com/title=362
    245,  # Darkmaster %s https://www.wowhead.com/title=370
    309,  # %s, Guardian of the Alliance https://www.wowhead.com/title=447
    310,  # %s, Defender of the Alliance https://www.wowhead.com/title=448
    311,  # %s, Soldier of the Alliance https://www.wowhead.com/title=449
    312,  # %s, Guardian of the Horde https://www.wowhead.com/title=450
    313,  # %s, Defender of the Horde https://www.wowhead.com/title=451
    314,  # %s, Soldier of the Horde https://www.wowhead.com/title=452
    330,  # Master Assassin %s https://www.wowhead.com/title=473
    346,  # %s, Talon's Vengeance https://www.wowhead.com/title=489
    358,  # %s, Adventuring Instructor https://www.wowhead.com/title=507
    365,  # %s the Collector https://www.wowhead.com/title=514
    371,  # %s, No Good, Dirty, Rotten[...] https://www.wowhead.com/title=520
    387,  # %s the Elite Death Knight https://www.wowhead.com/title=637
    388,  # %s the Elite Demon Hunter https://www.wowhead.com/title=638
    389,  # %s the Elite Druid https://www.wowhead.com/title=639
    390,  # %s the Elite Hunter https://www.wowhead.com/title=640
    391,  # %s the Elite Mage https://www.wowhead.com/title=641
    392,  # %s the Elite Monk https://www.wowhead.com/title=642
    393,  # %s the Elite Paladin https://www.wowhead.com/title=643
    394,  # %s the Elite Priest https://www.wowhead.com/title=644
    395,  # %s the Elite Rogue https://www.wowhead.com/title=645
    396,  # %s the Elite Shaman https://www.wowhead.com/title=646
    397,  # %s the Elite Warlock https://www.wowhead.com/title=647
    398,  # %s the Elite Warrior https://www.wowhead.com/title=648
    399,  # %s the T-Shirt Enthusiast https://www.wowhead.com/title=649
    406,  # Sparking %s https://www.wowhead.com/title=658
    408,  # Pilgrim %s the Mallet Bearer https://www.wowhead.com/title=660
    413,  # %s, As Themselves https://www.wowhead.com/title=666
    436,  # %s the Avowed https://www.wowhead.com/title=690
]


class TitleFixer(WowToolsFixer):
    load_files = True

    def _store_init(self, titles):
        self.titles = titles
        self.id_to_old_title = {}
        self.register_old_titles()

        self.wt_title = {
            int(e['Mask_ID']): e for e in self.wt_get_table('chartitles')
        }
        self.wt_achiev = {
            int(e['ID']): e for e in self.wt_get_table('achievement')
        }

    def register_old_titles(self):
        for cat in self.titles:
            for subcat in cat['subcats']:
                for item in subcat['items']:
                    self.id_to_old_title[int(item['titleId'])] = item

    def simplify_name(self, name):
        name = re.sub(r'\s*%s,?\s*', '', name)
        name = name[:1].upper() + name[1:]
        return name

    def fuzzy_find_achievement(self, wt_title):
        def to_pattern(name):
            name = self.simplify_name(name)
            name = name.lower()
            name = re.sub(r'^the\s*', '', name)
            return name

        lname = to_pattern(wt_title['Name_lang'])
        lnameF = to_pattern(wt_title['Name1_lang'])

        # We try to find the shortest achievement reward description containing
        # the title we are looking for. This avoids problems of titles
        # containing other titles (e.g., Champion / Champion of the Alliance)
        matching_achievs = []
        for achiev in self.wt_achiev.values():
            lreward = achiev['Reward_lang'].lower()
            if lname in lreward or lnameF in lreward:
                matching_achievs.append(achiev)
        if not matching_achievs:
            # Second pass, now with achievement descriptions
            for achiev in self.wt_achiev.values():
                ldesc = achiev['Description_lang'].lower()
                if lname in ldesc or lnameF in ldesc:
                    matching_achievs.append(achiev)
        if not matching_achievs:
            return
        matching_achievs.sort(
            key=lambda a: (
                bool(a['Reward_lang']),
                len(a['Reward_lang']),
                int(a['ID']),
            )
        )
        return int(matching_achievs[0]['ID'])

    def get_title(self, title_id: int):
        if int(title_id) not in self.wt_title:
            return None
        wt_title = self.wt_title[int(title_id)]
        name = self.simplify_name(wt_title['Name_lang'])
        nameF = self.simplify_name(wt_title['Name1_lang'])
        res = {
            'titleId': int(title_id),
            'name': name,
            'type': 'title',
            'id': int(wt_title['ID']),
            'icon': 'inv_misc_questionmark',
        }
        if nameF != name:
            res['nameF'] = nameF
        ach_id = self.fuzzy_find_achievement(wt_title)
        if ach_id:
            wt_ach = self.wt_achiev[ach_id]
            res['id'] = ach_id
            res['type'] = 'achievement'
            res['icon'] = self.get_icon_name(int(wt_ach['IconFileID']))
        return res

    def fix_missing_title(self, title_id: int):
        title = self.get_title(title_id)
        changelog(
            f"Title {title_id} \"{title['name']}\" missing:"
            f" https://www.wowhead.com/title={title['id']}"
        )
        icat(self.titles, 'TODO', 'TODO')['items'].append(title)

    def fix_missing_titles(self):
        for title_id in self.wt_title:
            if (
                int(title_id) not in self.id_to_old_title
                and title_id not in IGNORE_TITLE_ID
            ):
                self.fix_missing_title(int(title_id))

    def fix_types_data(self):
        for cat in self.titles:
            for subcat in cat['subcats']:
                for item in subcat['items']:
                    fixed_title = self.get_title(int(item['titleId']))
                    if fixed_title:
                        item['titleId'] = fixed_title['titleId']
                        if item.get('id'):
                            # Keep link to achievement/quest/...
                            # XXX: title id and related thing id should not
                            # share a common field name
                            item['id'] = int(item['id'])
                        else:
                            item['id'] = int(fixed_title['id'])
                        item['name'] = fixed_title['name']
                        if fixed_title.get('nameF'):
                            item['nameF'] = fixed_title['nameF']
                        if not item.get('icon'):
                            item['icon'] = fixed_title['icon']
                    else:
                        item['id'] = int(item['id'])
                        item['titleId'] = int(item['titleId'])

    def run(self):
        self.fix_missing_titles()
        self.fix_types_data()
        return [self.titles]
