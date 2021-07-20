# 0 -- Shihen69.
# 1 -- Sengoku Hime 1.
# 2 -- Sengoku Hime 2, Sengoku Hime 3.
# 3:
## 3.0 -- Sengoku Hime 4.
## 3.1 -- Sangoku Hime 1 Renewal.
# 4:
## 4.0 -- Sengoku Hime 5.
## 4.1 -- Sengoku Hime 6.

class SLG_Command_lib():
    # Библиотека.
    # Команда, структура, название...
    command_library = [
        ['ff', 'I', 'SAMPLE'],
    ]
    structs_library = [
        ['ff ff', 'I'],
    ]
    postcommand_data = ['B', 'B']

    def __init__(self):
        self._max_struct_len = self._find_max_struct_len()
        self._max_struct_elem = (self._max_struct_len + 1) // 3

    def get_index_from_struct(self, struct):
        for i in range(len(self.structs_library)):
            if (struct == self.structs_library[i][0]):
                return i
        return -1

    def get_index_from_command(self, command):
        for i in range(len(self.command_library)):
            if (command == self.command_library[i][2]):
                return i
        for i in range(len(self.command_library)):
            if (command == self.command_library[i][0]):
                return i
        return -1

    def _find_max_struct_len(self):
        maxer = 0
        indexer = -1
        for i in self.structs_library:
            if (len(i[0]) > maxer):
                maxer = len(i[0])
        return maxer

    def find_command_index(self, byer):
        nou = 0
        if (str(type(byer)) == "<class 'bytes'>"):
            nou = byer[0]
        elif (str(type(byer)) == "<class 'int'>"):
            nou = byer
        else:
            raise TypeError("Incorrect type: " + str(type(byer)) +
                            "!\nНекорректный тип: " + str(type(byer)) + "!")
        hexer = self.to_fully_hex(nou)

        result = -1
        for i in range(len(self.command_library)):
            if (hexer == self.command_library[i][0]):
                result = i
                break
        return result

    def find_struct_index(self, infer):
        index = -1
        backer = infer.tell()
        curr_num = self._max_struct_elem
        bytez = infer.read(curr_num)
        infer.seek(backer, 0)

        while (curr_num > 0):
            this_hex = bytez[:curr_num].hex(' ')
            for m in range(len(self.structs_library)):
                if (this_hex == self.structs_library[m][0]):
                    index = m
                    break
            if (index != -1):
                break
            curr_num -= 1
        if (index != -1):
            infer.read((len(self.structs_library[index][0]) + 1) // 3)

        return index

    def get_true_name(self, index):
        if (self.command_library[index][2] == ''):
            return self.command_library[index][0]
        else:
            return self.command_library[index][2]

    @staticmethod
    def get_len_from_stucture(stru):
        if (stru.upper() == 'Q'):
            return 8
        elif (stru.upper() == 'I'):
            return 4
        elif (stru.upper() == 'H'):
            return 2
        elif (stru.upper() == 'B'):
            return 1
        else:
            return 0

    @staticmethod
    def to_fully_hex(inter):
        if (str(type(inter)) == "<class 'bytes'>"):
            nou = inter[0]
        elif (str(type(inter)) == "<class 'int'>"):
            nou = inter
        else:
            raise TypeError("Incorrect type: " + str(type(inter)) +
                            "!\nНекорректный тип: " + str(type(inter)) + "!")
        zlo = hex(nou)[2:]
        if (len(zlo) == 1):
            zlo = "0" + zlo
        return zlo


class SLG_Command_lib_ver1(SLG_Command_lib):
    # Sengoku Hime 1.

    ##Библиотека.
    # Команда, структура, название...
    command_library = [
        ['01', 'HH', ''],
        ['02', 'I', ''],  # ?..
        ['03', 'ZZZZ', ''],
        ['06', 'Z', ''],
        ['08', 'IZ', ''],
        ['09', 'ISI', ''],  # ?
        ['0a', 'ISI', ''],
        ['0b', 'IGI', ''],
        ['0c', 'ISI', ''],  # ?
        ['0e', '', ''],
        ['0f', 'IISgS', 'MESSAGE'],  # ? #IISNg

        ['10', '', 'WAIT_FOR_CLICK'],
        ['12', 'BBH', ''],  # ?
        ['13', 'IgIS', 'CHOICE'],  # ING
        ['14', '', ''],
        ['17', 'IIZ', ''],
        ['1e', 'I', ''],  # ?
        ['1d', 'SZ', ''],  # ?
        ['1f', 'ISZ', 'PLAY_VOICE'],

        ['22', 'ZSZ', 'PLAY_SE'],
        ['28', '', ''],  # !!!
        ['29', 'IS', ''],  # ?
        ['2a', 'BBHS', ''],  # ?
        ['2d', '', 'EVENT_START'],
        ['2e', '', ''],  # EOF?
        ['2f', 'I', ''],

        ['30', 'I', ''],
        ['3b', 'ZZZ', ''],  # ISISIS
        ['3c', 'BBHSS', ''],
        ['3d', 'ZZZZZ', ''],  # ??? #ISISISISIS
        ['3e', 'ZZZ', ''],  # ??? #ISISIS
        ['3f', 'BIBIBI', ''],  # ?

        ['40', 'Z', ''],  # ?
        ['43', 'S', 'PLAY_VIDEO'],  # ?
        ['47', '', 'END'],  # ?
        ['49', 'SZ', 'PLAY_BGM'],
        ['4b', 'ZSZS', ''],  # ??? #IBSISbH #IBSIBS

        ['50', '', ''],
        ['51', '', ''],
        ['53', 'S', 'INIT_IMG'],
        ['56', '', ''],

        ['62', '', ''],
        ['63', 'ZZ', ''],
        ['66', 'ZZZZ', ''],
        ['67', '', ''],
        ['68', '', ''],
        ['69', 'IZZZZ', ''],
        ['6b', 'ZZ', ''],
        ['6d', 'ZZ', ''],
        ['6c', 'ZZZ', ''],
        ['6e', 'II', ''],
        ['6f', 'III', ''],

        ['70', 'II', ''],
        ['71', 'II', '']
    ]
    structs_library = [
        ['00', 'i'],
        ['01', 'I'],

        ['02 02', 'BH'],
        ['03 00', 'BHZZZZ'],  # BHZZZZ
        ['03 01', 'BHZZZZ'],  # BH
        ['03 12', 'BH'],
        ['03 13', 'BH'],
        ['03 14', 'BH'],
        ['03 15', 'BH'],
        ['03 16', 'BH'],
        ['03 17', 'BH'],

        ['04', 'Bs'],  # TEMP
    ]
    postcommand_data = ['B', 'H']

    def __init__(self):
        super(SLG_Command_lib_ver1, self).__init__()


class SLG_Command_lib_ver2(SLG_Command_lib_ver1):
    # Sengoku Hime 2, Sengoku Hime 3.
    postcommand_data = ['H', 'H']

    def __init__(self):
        super(SLG_Command_lib_ver2, self).__init__()


class SLG_Command_lib_ver3_0(SLG_Command_lib_ver2):
    # Sengoku Hime 4,

    # Новая библиотека, ибо старая, увы, уже не подходит (???).
    # 66 ZZZZ -> SZZ.
    # 67 '' -> ZZB???
    # 0a ISI -> IZ
    # 0c ISI -> IZ
    # 09 ISI -> IZ
    # 6d ZZ -> ''.
    # 13 БОЛЕЕ НЕ CHOICE! IgIS -> IZ
    # 68 '' -> ZZB.
    # 62 '' -> ZZZZZZZZ.
    # 28 '' -> ZZZZ.
    # 63 ZZ -> ZZZZ.
    # 71 II -> S.
    # 30 I -> ZSZ.
    # 3b ZZZ -> IZSZZS.
    # 2e '' -> ZSBZ.
    # 1d SZ -> ''.
    # 56 '' -> S.
    # 1e I -> ''.
    # 1f Больше не PLAY_VOICE! ISZ -> ''.
    # 14 '' -> IgIS. -> CHOICE.
    # 50 '' -> ZI.
    # 53 Больше не INIT_IMG! S -> ZZ.
    # 3c BBHSS -> I.
    # 70 II -> ISZ.
    # 51 '' -> II.
    # 2d EVENT_START -> END.
    # 43 Больше не PLAY_VIDEO! S -> ZZ.
    # 2f I -> ZSZ.
    # 47 Больше не END! '' -> ZZ.
    # 49 Больше не PLAY_BGM! SZ -> Z.
    # ef BIBIBI -> ZZ.
    command_library = [
        ['01', 'HH', ''],
        ['02', 'I', ''],  # ?..
        ['03', 'ZZZZ', ''],
        ['06', 'Z', ''],
        ['08', 'IZ', ''],
        ['09', 'IZ', ''],  # ?
        ['0a', 'IZ', ''],
        ['0b', 'IGI', ''],
        ['0c', 'IZ', ''],  # ?
        ['0e', '', ''],
        ['0f', 'IISgM', 'MESSAGE'],  # !!! #IISNg

        ['10', '', ''],
        ['11', '', 'WAIT_FOR_CLICK'],
        ['12', 'BBH', ''],  # ?
        ['13', 'I', 'JUMP'],
        ['14', 'IgIS', 'CHOICE'],
        ['15', '', ''],
        ['16', 'IZI', ''],
        ['17', 'ZSZS', ''],  # !!!
        ['18', 'I', ''],
        ['19', 'ISZ', ''],
        ['1b', 'ZSZii', ''],
        ['1c', 'IZ', ''],  # ?
        ['1e', '', ''],
        ['1d', '', ''],
        ['1f', '', ''],  # Больше не PLAY_VOICE!

        ['20', 'I', ''],
        ['21', 'II', ''],
        ['22', 'ZSZ', 'PLAY_SE'],
        ['26', 'ZZZZZZ', ''],
        ['27', 'ZZZZ', ''],
        ['28', 'ZZZZ', ''],
        ['29', 'IS', ''],  # ?
        ['2a', 'BBHS', ''],  # ?
        ['2d', '', 'END'],
        ['2e', 'ZSBZ', ''],  # !!!
        ['2f', 'ZSIZI', ''],

        ['30', 'ZSZ', ''],
        ['31', '', ''],
        ['33', 'SZZ', ''],
        ['36', 'ZS', ''],
        ['38', 'ZZZZ', ''],
        ['39', '', ''],
        ['3a', 'IZZZZ', ''],
        ['3b', 'IZSZZS', ''],  # !!!
        ['3c', 'I', ''],
        ['3d', 'ZZ', ''],
        ['3e', 'ZZZ', ''],  # ??? #ISISIS
        ['3f', 'ZZ', ''],  # ?

        ['40', 'Z', ''],  # ?
        ['41', 'ZZZ', ''],
        ['43', 'ZZ', ''],
        ['44', 'ZZZZ', ''],
        ['45', 'ZZZZ', ''],
        ['46', '', ''],
        ['47', 'ZZ', ''],
        ['49', 'Z', ''],
        ['4b', 'ZSZS', ''],
        ['4c', 'ZZZZZ', ''],
        ['4d', '', ''],
        ['4e', 'ZZZ', ''],
        ['4f', 'ZZ', ''],

        ['50', 'ZI', ''],
        ['51', 'II', ''],
        ['52', 'II', ''],
        ['53', 'ZZ', ''],
        ['54', 'ZZZ', ''],
        ['56', 'S', ''],
        ['57', 'ZS', ''],
        ['5a', 'ZZ', ''],
        ['5c', 'ZZ', ''],
        ['5d', 'SZ', ''],
        ['5e', 'ZZ', ''],  # ?
        ['5f', 'ZZZZZZ', ''],

        ['61', 'ZZZZZZ', ''],
        ['62', 'ZZZZZZZZ', ''],
        ['63', 'ZZZZ', ''],
        ['66', 'SZZ', ''],
        ['67', 'ZZS', ''],
        ['68', 'ZZS', ''],  # !!!
        ['69', 'IZZZZ', ''],
        ['69', '', ''],
        ['6a', 'ZZZZZ', ''],  # !!!
        ['6b', '', ''],
        ['6d', '', ''],  # !!!
        ['6c', 'ZZZ', ''],
        ['6e', 'II', ''],
        ['6f', 'III', ''],

        ['70', 'ISZ', ''],
        ['71', 'S', ''],
        ['72', '', ''],
        ['73', 'ZZZZZZ', ''],
        ['7b', 'Z', ''],
        ['7d', 'ZZ', ''],
        ['7e', 'ZZ', ''],
        ['7f', 'Z', ''],

        ['80', 'ZZZ', ''],
        ['81', 'ZI', ''],
        ['82', 'Z', ''],
        ['83', 'ZZ', ''],
        ['84', 'ZSZ', ''],
    ]

    def __init__(self):
        super(SLG_Command_lib_ver3_0, self).__init__()


class SLG_Command_lib_ver3_1(SLG_Command_lib_ver2):
    # Sangoku Hime 3 Renewal.

    # 2e ZSBZ -> SZS
    # 17 ZSZS -> SZS.
    command_library = [
        ['01', 'HH', ''],
        ['02', 'I', ''],  # ?..
        ['03', 'ZZZZ', ''],
        ['06', 'Z', ''],
        ['08', 'IZ', ''],
        ['09', 'IZ', ''],  # ?
        ['0a', 'IZ', ''],
        ['0b', 'IGI', ''],
        ['0c', 'IZ', ''],  # ?
        ['0e', '', ''],
        ['0f', 'IISgM', 'MESSAGE'],  # !!! #IISNg

        ['10', '', ''],
        ['11', '', 'WAIT_FOR_CLICK'],
        ['12', 'BBH', ''],  # ?
        ['13', 'I', 'JUMP'],  # Больше не CHOICE! #Теперь JUMP? Ещё и прыжки обрабатывать?..
        ['14', 'IgIS', 'CHOICE'],  # Новый CHOICE!
        ['15', '', ''],
        ['16', 'IZI', ''],
        ['17', 'SZS', ''],  # !!!
        ['18', 'I', ''],
        ['19', 'ISZ', ''],
        ['1b', 'ZSZii', ''],
        ['1c', 'IZ', ''],  # ?
        ['1e', '', ''],
        ['1d', '', ''],
        ['1f', '', ''],  # Больше не PLAY_VOICE!

        ['20', 'I', ''],
        ['21', 'II', ''],
        ['22', 'ZSZ', 'PLAY_SE'],
        ['26', 'ZZZZZZ', ''],
        ['27', 'ZZZZ', ''],
        ['28', 'ZZZZ', ''],
        ['29', 'IS', ''],  # ?
        ['2a', 'BBHS', ''],  # ?
        ['2d', '', 'END'],
        ['2e', 'SZS', ''],  # !!!
        ['2f', 'ZSIZI', ''],

        ['30', 'ZSZ', ''],
        ['31', '', ''],
        ['33', 'SZZ', ''],
        ['36', 'ZS', ''],
        ['38', 'ZZZZ', ''],
        ['39', '', ''],
        ['3a', 'IZZZZ', ''],
        ['3b', 'IZSZZS', ''],  # !!!
        ['3c', 'I', ''],
        ['3d', 'ZZ', ''],
        ['3e', 'ZZZ', ''],  # ??? #ISISIS
        ['3f', 'ZZ', ''],  # ?

        ['40', 'Z', ''],  # ?
        ['41', 'ZZZ', ''],
        ['43', 'ZZ', ''],
        ['44', 'ZZZZ', ''],
        ['45', 'ZZZZ', ''],
        ['46', '', ''],
        ['47', 'ZZ', ''],
        ['49', 'Z', ''],
        ['4b', 'ZSZS', ''],
        ['4c', 'ZZZZZ', ''],
        ['4d', '', ''],
        ['4e', 'ZZZ', ''],
        ['4f', 'ZZ', ''],

        ['50', 'ZI', ''],
        ['51', 'II', ''],
        ['52', 'II', ''],
        ['53', 'ZZ', ''],
        ['54', 'ZZZ', ''],
        ['56', 'S', ''],
        ['57', 'ZS', ''],
        ['5a', 'ZZ', ''],
        ['5c', 'ZZ', ''],
        ['5d', 'SZ', ''],
        ['5e', 'ZZ', ''],  # ?
        ['5f', 'ZZZZZZ', ''],

        ['61', 'ZZZZZZ', ''],
        ['62', 'ZZZZZZZZ', ''],
        ['63', 'ZZZZ', ''],
        ['66', 'SZZ', ''],
        ['67', 'ZZS', ''],
        ['68', 'ZZS', ''],  # !!!
        ['69', 'IZZZZ', ''],
        ['69', '', ''],
        ['6a', 'ZZZZZ', ''],  # !!!
        ['6b', '', ''],
        ['6d', '', ''],  # !!!
        ['6c', 'ZZZ', ''],
        ['6e', 'II', ''],
        ['6f', 'III', ''],

        ['70', 'ISZ', ''],
        ['71', 'S', ''],
        ['72', '', ''],
        ['73', 'ZZZZZZ', ''],
        ['7b', 'Z', ''],
        ['7d', 'ZZ', ''],
        ['7e', 'ZZ', ''],
        ['7f', 'Z', ''],

        ['80', 'ZZZ', ''],
        ['81', 'ZI', ''],
        ['82', 'Z', ''],
        ['83', 'ZZ', ''],
        ['84', 'ZSZ', ''],
    ]
    bl_new_point = 0x4080

    def __init__(self):
        super(SLG_Command_lib_ver3_1, self).__init__()


class SLG_Command_lib_ver4_0(SLG_Command_lib_ver3_1):
    # От ver3_1

    # 01: HHI -> HHGIZ
    # 01: HH -> HHI.
    # 33: SZZ -> SZZZZ.
    # +8b: ZZ.
    # +48 ZSZ.
    # +55: I.
    # 53: ZZ -> ZZZ.
    # +8c: ZZ.
    # 56: S -> -.
    # 52: II -> ZZ.
    # 4f: ZZ -> ZI.
    # +85: ZZ.
    # 4d: - -> ZZZ.
    # +8a: Z.
    # 2e: SZS -> ZSBZ.
    # +8d: SI.
    # 17: SZS -> ZSBZ.
    # 50: ZI -> II?
    # 54: ZZZ -> Z.
    # 3e: ZZZ -> ZZ.

    ###->4.2?
    # +8f: Z.
    # +8e: Z.
    # +90: ZZ.
    # +91: Z.
    # +92: ZZZ.
    # +93: ZZ.
    # +94: ZZ.

    command_library = [
        ['01', 'HHI', ''],
        ['02', 'I', ''],  # ?..
        ['03', 'ZZZZ', ''],
        ['06', 'Z', ''],
        ['08', 'IZ', ''],
        ['09', 'IZ', ''],  # ?
        ['0a', 'IZ', ''],
        ['0b', 'IGI', ''],
        ['0c', 'IZ', ''],  # ?
        ['0e', '', ''],
        ['0f', 'IISgM', 'MESSAGE'],  # !!! #IISNg

        ['10', '', ''],
        ['11', '', 'WAIT_FOR_CLICK'],
        ['12', 'BBH', ''],  # ?
        ['13', 'I', 'JUMP'],  # Больше не CHOICE! #Теперь JUMP? Ещё и прыжки обрабатывать?..
        ['14', 'IgIS', 'CHOICE'],  # Новый CHOICE!
        ['15', '', ''],
        ['16', 'IZI', ''],
        ['17', 'ZSBZ', ''],  # !!!
        ['18', 'I', ''],
        ['19', 'ISZ', ''],
        ['1b', 'ZSZii', ''],
        ['1c', 'IZ', ''],  # ?
        ['1e', '', ''],
        ['1d', '', ''],
        ['1f', '', ''],  # Больше не PLAY_VOICE!

        ['20', 'I', ''],
        ['21', 'II', ''],
        ['22', 'ZSZ', 'PLAY_SE'],
        ['26', 'ZZZZZZ', ''],
        ['27', 'ZZZZ', ''],
        ['28', 'ZZZZ', ''],
        ['29', 'IS', ''],  # ?
        ['2a', 'BBHS', ''],  # ?
        ['2d', '', 'END'],
        ['2e', 'ZSBZ', ''],  # !!!
        ['2f', 'ZSIZI', ''],

        ['30', 'ZSZ', ''],
        ['31', '', ''],
        ['33', 'SZZZZ', ''],
        ['36', 'ZS', ''],
        ['38', 'ZZZZ', ''],
        ['39', '', ''],
        ['3a', 'IZZZZ', ''],
        ['3b', 'IZSZZS', ''],  # !!!
        ['3c', 'I', ''],
        ['3d', 'ZZ', ''],
        ['3e', 'ZZ', ''],  # ??? #ISISIS
        ['3f', 'ZZ', ''],  # ?

        ['40', 'Z', ''],  # ?
        ['41', 'ZZZ', ''],
        ['43', 'ZZ', ''],
        ['44', 'ZZZZ', ''],
        ['45', 'ZZZZ', ''],
        ['46', '', ''],
        ['47', 'ZZ', ''],
        ['48', 'ZSZ', ''],
        ['49', 'Z', ''],
        ['4b', 'ZSZS', ''],
        ['4c', 'ZZZZZ', ''],
        ['4d', 'ZZZ', ''],
        ['4e', 'ZZZ', ''],
        ['4f', 'ZI', ''],

        ['50', 'II', ''],
        ['51', 'II', ''],
        ['52', 'ZZ', ''],
        ['53', 'ZZZ', ''],
        ['54', 'Z', ''],
        ['55', 'I', ''],
        ['56', '', ''],
        ['57', 'ZS', ''],
        ['5a', 'ZZ', ''],
        ['5c', 'ZZ', ''],
        ['5d', 'SZ', ''],
        ['5e', 'ZZ', ''],  # ?
        ['5f', 'ZZZZZZ', ''],

        ['61', 'ZZZZZZ', ''],
        ['62', 'ZZZZZZZZ', ''],
        ['63', 'ZZZZ', ''],
        ['66', 'SZZ', ''],
        ['67', 'ZZS', ''],
        ['68', 'ZZS', ''],  # !!!
        ['69', 'IZZZZ', ''],
        ['69', '', ''],
        ['6a', 'ZZZZZ', ''],
        ['6b', '', ''],
        ['6d', '', ''],
        ['6c', 'ZZZ', ''],
        ['6e', 'II', ''],
        ['6f', 'III', ''],

        ['70', 'ISZ', ''],
        ['71', 'S', ''],
        ['72', '', ''],
        ['73', 'ZZZZZZ', ''],
        ['7b', 'Z', ''],
        ['7d', 'ZZ', ''],
        ['7e', 'ZZ', ''],
        ['7f', 'Z', ''],

        ['80', 'ZZZ', ''],
        ['81', 'ZI', ''],
        ['82', 'Z', ''],
        ['83', 'ZZ', ''],
        ['84', 'ZSZ', ''],
        ['85', 'ZZ', ''],
        ['8a', 'Z', ''],
        ['92', 'ZZZ', ''],
        ['8b', 'ZZ', ''],
        ['8c', 'ZZ', ''],
        ['8d', 'SI', ''],
        ['8e', 'Z', ''],
        ['8f', 'Z', ''],

        ['90', 'ZZ', ''],
        ['91', 'Z', ''],
        ['93', 'ZZ', ''],
        ['94', 'ZZ', ''],
    ]

    def __init__(self):
        super(SLG_Command_lib_ver4_0, self).__init__()


class SLG_Command_lib_ver4_1(SLG_Command_lib_ver4_0):
    # 21: II -> ZZ.

    command_library = [
        ['01', 'HHGR', ''],
        ['02', 'I', ''],  # ?..
        ['03', 'ZZZZ', ''],
        ['06', 'Z', ''],
        ['08', 'IZ', ''],
        ['09', 'IZ', ''],  # ?
        ['0a', 'IZ', ''],
        ['0b', 'IGI', ''],
        ['0c', 'IZ', ''],  # ?
        ['0e', '', ''],
        ['0f', 'IISgM', 'MESSAGE'],  # !!! #IISNg

        ['10', '', ''],
        ['11', '', 'WAIT_FOR_CLICK'],
        ['12', 'BBH', ''],  # ?
        ['13', 'I', 'JUMP'],  # Больше не CHOICE! #Теперь JUMP? Ещё и прыжки обрабатывать?..
        ['14', 'IgIS', 'CHOICE'],  # Новый CHOICE!
        ['15', '', ''],
        ['16', 'IZI', ''],
        ['17', 'ZSBZ', ''],  # !!!
        ['18', 'I', ''],
        ['19', 'ISZ', ''],
        ['1b', 'ZSZii', ''],
        ['1c', 'IZ', ''],  # ?
        ['1e', '', ''],
        ['1d', '', ''],
        ['1f', '', ''],  # Больше не PLAY_VOICE!

        ['20', 'I', ''],
        ['21', 'ZZ', ''],
        ['22', 'ZSZ', 'PLAY_SE'],
        ['26', 'ZZZZZZ', ''],
        ['27', 'ZZZZ', ''],
        ['28', 'ZZZZ', ''],
        ['29', 'IS', ''],  # ?
        ['2a', 'BBHS', ''],  # ?
        ['2d', '', 'END'],
        ['2e', 'ZSBZ', ''],  # !!!
        ['2f', 'ZSIZI', ''],

        ['30', 'ZSZ', ''],
        ['31', '', ''],
        ['33', 'SZZZZ', ''],
        ['36', 'ZS', ''],
        ['38', 'ZZZZ', ''],
        ['39', '', ''],
        ['3a', 'IZZZZ', ''],
        ['3b', 'IZSZZS', ''],  # !!! #IZSZZS
        ['3c', 'I', ''],
        ['3d', 'ZZ', ''],
        ['3e', 'ZZ', ''],  # ??? #ISISIS
        ['3f', 'ZZ', ''],  # ?

        ['40', 'Z', ''],  # ?
        ['41', 'ZZZ', ''],
        ['43', 'ZZ', ''],
        ['44', 'ZZZZ', ''],
        ['45', 'ZZZZ', ''],
        ['46', '', ''],
        ['47', 'ZZ', ''],
        ['48', 'ZSZ', ''],
        ['49', 'Z', ''],
        ['4b', 'ZSZS', ''],
        ['4c', 'ZZZZZ', ''],
        ['4d', 'ZZZ', ''],
        ['4e', 'ZZZ', ''],
        ['4f', 'ZI', ''],

        ['50', 'II', ''],
        ['51', 'II', ''],
        ['52', 'ZZ', ''],
        ['53', 'ZZZ', ''],
        ['54', 'Z', ''],
        ['55', 'I', ''],
        ['56', '', ''],
        ['57', 'ZS', ''],
        ['5a', 'ZZ', ''],
        ['5c', 'ZZ', ''],
        ['5d', 'SZ', ''],
        ['5e', 'ZZ', ''],  # ?
        ['5f', 'ZZZZZZ', ''],

        ['61', 'ZZZZZZ', ''],
        ['62', 'ZZZZZZZZ', ''],
        ['63', 'ZZZZ', ''],
        ['66', 'SZZ', ''],
        ['67', 'ZZS', ''],
        ['68', 'ZZS', ''],  # !!!
        ['69', 'IZZZZ', ''],
        ['69', '', ''],
        ['6a', 'ZZZZZ', ''],
        ['6b', '', ''],
        ['6d', '', ''],
        ['6c', 'ZZZ', ''],
        ['6e', 'II', ''],
        ['6f', 'III', ''],

        ['70', 'ISZ', ''],
        ['71', 'S', ''],
        ['72', '', ''],
        ['73', 'ZZZZZZ', ''],
        ['7b', 'Z', ''],
        ['7d', 'ZZ', ''],
        ['7e', 'ZZ', ''],
        ['7f', 'Z', ''],

        ['80', 'ZZZ', ''],
        ['81', 'ZI', ''],
        ['82', 'Z', ''],
        ['83', 'ZZ', ''],
        ['84', 'ZSZ', ''],
        ['85', 'ZZ', ''],
        ['8a', 'Z', ''],
        ['8b', 'ZZ', ''],
        ['8c', 'ZZ', ''],
        ['8d', 'SI', ''],
        ['8e', 'Z', ''],
        ['8f', 'Z', ''],

        ['90', 'ZZ', ''],
        ['91', 'Z', ''],
        ['92', 'ZZZ', ''],
        ['93', 'ZZ', ''],
        ['94', 'ZZ', ''],
    ]

    def __init__(self):
        super(SLG_Command_lib_ver4_1, self).__init__()


# Далее идут воистину древние да дикие варианты.
# There are wild and ancient variants next.

class SLG_Command_lib_ver0(SLG_Command_lib_ver1):
    # Полностью иная структура команд -- по 2 байта, а не 1.
    # Отсюда же идут постфиксы (кои, впрочем, нулевые).

    ##Библиотека.
    # Команда, структура, название...
    command_library = [
        ['00', '', 'NULL'],
        ['03', 'Z', ''],  # PAUSE? #+
        ['05', 'SZZ', ''],  # +
        ['06', 'I', ''],  # 45-> #+
        ['07', 'I', ''],  # +
        ['08', 'ZZZZ', ''],  # + #*?
        ['0c', 'Z', ''],  # 03-> #ПУСТЬ.
        ['0e', 'IZ', ''],  # +
        ['0f', 'IZ', ''],  # 45-> #+ #MOV?

        ['10', 'IZ', ''],  # ?
        ['11', 'IGI', ''],  # +
        ['14', '', ''],  # ?
        ['15', 'IZZBSSGS', 'NARRATION'],  # +
        ['16', 'IZZSSSGS', 'REPLICA'],  # +
        ['19', 'I', 'JUMP'],  # +
        ['1a', 'gIS', 'CHOICE'],  # 06-> #+
        ['1c', '', ''],  # ПУСТЬ
        ['1d', 'ZZSZZZZZZ', 'SHOW_VISUAL'],  # +
        ['1e', 'ZZZZZZZ', ''],  # +

        ['20', 'SZ', 'PLAY_BGM'],
        ['21', 'Z', ''],  # +
        ['23', 'ZSZ', 'PLAY_SE'],  # +
        ['24', 'ZZ', ''],  # +
        ['25', 'Z', 'END'],  # +
        ['26', '', ''],  # ?
        ['27', 'Z', ''],  # ?
        ['28', 'I', 'COUNT'],  # +
        ['2a', '', ''],  # +
        ['2b', 'I', ''],  # +
        ['2e', 'IGI', ''],  # +

        ['33', '', ''],  # ? #ПУСТЬ! #MATH?
        ['36', 'S', 'PLAY_VIDEO'],  # +
        ['3a', 'ZZSZ', 'LOAD_DATA'],  # 33->> #MATH+? #+
        ['3c', 'ZZZZZ', ''],  # 15-> #+?
        ['3d', 'ZZZZ', ''],  # 33-> #MATH+? #+

        ['41', 'ZZ', ''],  # 33-> #MATH+? #+
        ['42', 'Z', ''],  # +
        ['43', 'Z', ''],  # +
        ['44', 'Z', ''],  # 06-> #+
        ['45', 'S', 'SET_CHAPTER_NAME'],  # +
        ['47', 'Z', ''],  # +
        ['48', 'ZZZ', ''],  # 33-> #MATH+? #+
        ['49', '', ''],  # ?
        ['4a', 'Z', ''],  # + Так, ежели 4b.
        ['4b', 'Z', ''],  # 0e->43-> #??? Так, ежели 4a.
    ]
    # Структуры те же. Пошли отсюда.

    postcommand_data = []  # А вот она уже с нормальных версий.

    def __init__(self):
        super(SLG_Command_lib_ver0, self).__init__()
