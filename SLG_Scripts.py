#НЕ АКТУАЛЬНО! ИСПОЛЬЗУЙТЕ SLG_Scripts_NEW!
#NOT ACTUAL! USE SLG_Scripts_NEW INSTEAD!


import struct
import os
import sys


class SLG_Scripts:
    #Библиотека.
    #Команда, структура, название...
    command_library = [
        ['01', 'HH', ''],
        ['02', 'I', ''], #?..
        ['03', 'ZZZZ', ''],  #!!! #HHIBHsIB #IBIBiBIB #ZIBZIB
        ['06', 'Z', ''], #BI
        ['08', 'IZ', ''], #!!! #ISi #IBi #IHs #Iz
        ['09', 'ISI', ''],  # ?
        ['0a', 'ISI', ''],
        ['0b', 'IIIIIIIIIII', ''], #IIIIIIIIIII
        ['0c', 'ISI', ''], #?
        ['0e', '', ''],
        ['0f', 'IISNg', 'MESSAGE'], #?

        ['10', '', 'WAIT_FOR_CLICK'],
        ['12', 'BBH', ''],  # ?
        ['13', 'ING', 'CHOICE'],
        ['14', '', ''],
        ['1e', 'I', ''], # ?
        ['1d', 'SZ', ''], #?
        ['1f', 'ISZ', 'PLAY_VOICE'],

        ['22', 'ZSZ', 'PLAY_SE'],
        ['29', 'IS', ''], #?
        ['2a', 'BBHS', ''],  # ?
        ['2d', '', 'EVENT_START'],
        ['2e', '', ''], #EOF?
        ['2f', 'I', ''],

        ['30', 'I', ''],
        ['3b', 'ZZZ', ''], #ISISIS
        ['3c', 'BBHSS', ''],
        ['3d', 'ZZZZZ', ''], #??? #ISISISISIS
        ['3e', 'ZZZ', ''], #??? #ISISIS
        ['3f', 'BIBIBI', ''], #?

        ['40', 'Z', ''],  #?
        ['43', 'S', 'PLAY_VIDEO'],  #?
        ['47', '', 'END'],  #?
        ['49', 'SZ', 'PLAY_BGM'],
        ['4b', 'ZSZS', ''], #??? #IBSISbH #IBSIBS

        ['53', 'S', 'INIT_IMG'],
        ['56', '', ''],

        ['62', '', ''],
        ['63', 'ZZ', ''], #??? #ISIS
        ['66', 'ZIBZIB', ''], #? #HHBSISBHS #HHBSISSSH
        ['67', 'ISIS', ''], #?
        ['68', '', ''],
        ['69', 'IZZZZ', ''], #IZIBZIB
        ['6e', 'II', ''] #VER: 1,
    ]
    structs_library = [
        ['00', 'i'],
        ['01', 'I'],
        ['02 02', 'BH'], #b?
        ['02 3e', 'HI'], #TODO: DELETE KOSTIL!
        ['08 06', 'BHIZ'], #TODO: DELETE KOSTIL!
        ['12 06', 'BHI'], #TODO: DELETE KOSTIL! #BH
        ['69', 'BHIZZZZ', ''], #TODO: DELETE KOSTIL!
        ['03 00', 'BHZZZZ'], #b? #!!! # Странная конструкция... #BHZZZZ №BHZZIZ
        ['03 01', 'BH'], #b?
        ['03 12', 'BH'], #b?
        ['03 13', 'BH'], #b?
        ['03 14', 'BH'], #b?
        ['03 15', 'BH'], #b? #II
        ['03 16', 'BH'], #b? #II
        ['03 17', 'BH'], #b? #I
        ['04 00', 's'],
        ['04 01', 's'],
        ['04 02', 'BH'],
        ['04 03', 's'], #BH
        ['04 04', 's'],
        ['04 05', 's'], #BH
        ['04 06', 's'],
        ['04 09', 's'],
        ['04 0a', 's'], #?
        ['04 0b', 's'],
        ['04 0d', 's'], #?
        ['04 0f', 's'],
        ['04 10', 's'],
        ['04 12', 'H'],
        ['04 14', 'H'],
        ['04 15', 's'],
        ['04 16', 's'],
        ['04 17', 's'],
        ['04 1a', 's'], #VER: 1?
        ['ff ff', 'h'], #b?
    ]

    #Инициализация.
    def __init__(self, dir, encoding, version):
        self.__version = version

        self.__dir = dir
        self.__chkScriptFiles()
        self.__encoding = encoding

        #main.lb, main.lbn:
        self.__mainlib = []

        #main.ev:
        self.__evlib = []

        #main.sfn
        self.__file_list = []

        #Размеры разделов, требующих дополнения:
        self.__nominal_size = dict()
        self.__nominal_size["main.cg"] = 0
        self.__nominal_size["main.lb"] = 0
        self.__nominal_size["main.sw"] = 0
        self.__nominal_size["main.tko"] = 0
        self.__nominal_size["main.ev"] = 0

    #Взаимодействие с пользователем.
    def decompile(self, out_dir, out_name):
        self.__evlib = self.__decompileEvLib()
        self.__mainlib = self.__decompileMainLib()
        self.__file_list = self.__decompileFileList()
        if (out_name == ""):
            self.__createFiles(out_dir)
        else:
            if (out_dir != ''):
                os.makedirs(out_dir, exist_ok=True)
        self.__set_nominal_sizes(out_dir)
        self.__decompileMain(out_dir, out_name)
        self.__decompileRest(out_dir)
    def getStatFull(self):
        #TODO: Сделать полную статистику, когда всё будет готово.
        pass
    def getStatEvLib(self):
        return self.__evlib
    def getStatMainLib(self):
        return self.__mainlib
    def getFileList(self):
        return self.__file_list
    def getNominalSizes(self):
        return self.__nominal_size

    #Технические функции декомпиляции..
    def __decompileEvLib(self):
        liber = []
        file_in = open(self.__dir + os.sep + "main.ev", 'rb')
        current_bytes = file_in.read(64)
        while (current_bytes != b''):
            arrayer = []
            arrayer.append(self.__findStringInBytes(current_bytes))
            current_bytes = file_in.read(4)
            arrayer.append(struct.unpack('I', current_bytes)[0])
            liber.append(arrayer)
            current_bytes = file_in.read(64)
        file_in.close()
        i = len(liber)
        while (i >= 0):
            i -= 1
            if (liber[i] == ['', 0]):
                liber.pop(i)
        return liber
    def __decompileMainLib(self):
        liber = [[], []]
        file_in = open(self.__dir + os.sep + "main.lb", 'rb')
        current_bytes = file_in.read(4)
        while (current_bytes != b''):
            liber[0].append(struct.unpack('I', current_bytes)[0])
            current_bytes = file_in.read(4)
        file_in.close()
        i = len(liber[0])
        while (i >= 0):
            i -= 1
            if (liber[0][i] == 0):
                liber[0].pop(i)

        file_in = open(self.__dir + os.sep + "main.lbn", 'rb')
        current_bytes = file_in.read(64)
        while (current_bytes != b''):
            strings = []
            strings.append(self.__findStringInBytes(current_bytes))
            current_bytes = file_in.read(64)
            news = self.__findStringInBytes(current_bytes)
            if (news[-1] == '/'):
                news = news[:-1] + "_"
            strings.append(news)
            liber[1].append(strings)
            current_bytes = file_in.read(64)
        file_in.close()

        kostil = 0
        while (len(liber[0]) > len(liber[1])):
            strings = []
            strings.append("__remaining_" + str(kostil))
            strings.append("__remaining.txt")
            liber[1].append(strings)
            kostil += 1

        libers = []
        for i in range(len(liber[0])):
            arrayer = []
            arrayer.append(liber[0][i])
            arrayer.append(liber[1][i])
            libers.append(arrayer)
        return libers
    def __decompileFileList(self):
        liber = []
        file_in = open(self.__dir + os.sep + "main.sfn", 'rb')
        current_bytes = file_in.read(64)
        while (current_bytes != b''):
            news = self.__findStringInBytes(current_bytes)
            try:
                if (news[-1] == '/'):
                    news = news[:-1] + "_"
            except:
                pass
            liber.append(news)
            current_bytes = file_in.read(64)
        file_in.close()
        return liber
    def __decompileMain(self, out_dir, out_name):
        filer = self.__mainlib.copy()
        filer.sort(key=lambda file: file[0])

        file_in = open(self.__dir + os.sep + "main.sd", 'rb')
        if (out_name == ""):
            file_out = open(os.path.join(out_dir, filer[0][1][1]), 'a', encoding=self.__encoding)
            file_out.write("##: " + filer[0][1][0] + "\n")
        else:
            current_file = -1
            file_out = open(os.path.join(out_dir, out_name), 'w', encoding=self.__encoding)

        current_bytes = file_in.read(1)
        current_pos = 1
        is_match = True
        current_file = 0
        current_string = 0
        grouper = 0

        while (current_bytes != b''):
            # Начало команды в current_pos - 1 указано здесь.
            for test in filer:
                if ((current_pos - 1) == test[0]):
                    if (out_name == ""):
                        file_out.close()
                        file_out = open(os.path.join(out_dir, test[1][1]), 'a', encoding=self.__encoding)
                        file_out.write("##: " + test[1][0] + "\n")
                    else:
                        file_out.write("##: " + test[1][0] + " at " + test[1][1] + "\n")
                elif (test[0] > (current_pos - 1)):
                    break
            for test in self.__evlib:
                if ((current_pos - 1) == test[1]):
                    file_out.write("#2: " + test[0] + "\n")
                elif (test[1] > (current_pos - 1)):
                    break

            # Определение команды.
            hex_bytes = current_bytes.hex()
            command_number = -1
            for i in range(len(self.command_library)):
                if (hex_bytes == self.command_library[i][0]):
                    command_number = i
                    break

            # Соответствующая обработка.
            if (command_number == -1):
                if (is_match):
                    file_out.write("#0:")
                is_match = False
                file_out.write(" " + current_bytes.hex())
                current_bytes = file_in.read(1)
                current_pos += 1
            else:
                if (not (is_match)):
                    file_out.write("\n")
                file_out.write("#1: ")
                is_match = True
                if (self.command_library[command_number][2] == ''):
                    file_out.write(hex_bytes)
                else:
                    file_out.write(self.command_library[command_number][2])
                # Определение текущего файла и строки.
                if (self.__version == 0):
                    current_file = struct.unpack('B', file_in.read(1))[0]
                    current_pos += 1
                else:
                    current_file = struct.unpack('H', file_in.read(2))[0]
                    current_pos += 2
                current_line = struct.unpack('H', file_in.read(2))[0]
                current_pos += 2

                #TODO: DELETE HINT!
                #file_out.write(' on pos ' + str(current_pos-4) +
                #               " on file " + str(current_file) +
                #               " on line " + str(current_line))
                #!!!
                file_out.write(' ' + str(current_file) +
                               " " + str(current_line))

                file_out.write("\n")

                current_values = []
                for i in self.command_library[command_number][1]:
                    if (i.upper() == 'B'):
                        val, file_in, current_pos = self.__getB(file_in, current_pos, i)
                        current_values.append(val)
                    elif (i.upper() == 'H'):
                        val, file_in, current_pos = self.__getH(file_in, current_pos, i)
                        current_values.append(val)
                    elif (i.upper() == 'I'):
                        val, file_in, current_pos = self.__getI(file_in, current_pos, i)
                        current_values.append(val)
                    elif (i == 'S'):
                        val, file_in, current_pos = self.__getS(file_in, current_pos)
                        current_values.append(val)
                    elif (i == 's'):
                        val, file_in, current_pos = self.__gets(file_in, current_pos)
                        current_values.append(val)
                    elif (i == 'N'):
                        grouper, file_in, current_pos = self.__getN(file_in, current_pos)
                    elif (i.upper() == 'G'):
                        val, file_in, current_pos = self.__getG(file_in, current_pos, grouper, i)
                        current_values.append(val)
                    elif (i == 'Z'):
                        val, file_in, current_pos = self.__getZ(file_in, current_pos, grouper)
                        current_values.append(val)

                file_out.write(str(current_values))
                file_out.write('\n')

                current_bytes = file_in.read(1)
                current_pos += 1

        file_in.close()
        file_out.close()
    def __decompileRest(self, out_dir):
        out_file = open(os.path.join(out_dir, "__compile_order.txt"), 'w', encoding=self.__encoding)
        out_file.write("##COMPILATION ORDER:")
        for i in self.__mainlib:
            out_file.write("\n" + i[1][0] + " " + i[1][1])
        out_file.close()

        in_file = open(os.path.join(self.__dir, "main.sfn"), 'rb')
        out_file = open(os.path.join(out_dir, "__main_sfn.txt"), 'w', encoding=self.__encoding)
        out_file.write("##DATA FROM main.sfn SECTION:")
        current_bytes = in_file.read(64)
        while (current_bytes != b''):
            out_file.write("\n" + self.__findStringInBytes(current_bytes))
            current_bytes = in_file.read(64)
        in_file.close()
        out_file.close()

        in_file = open(os.path.join(self.__dir, "main.swn"), 'rb')
        out_file = open(os.path.join(out_dir, "__main_swn.txt"), 'w', encoding=self.__encoding)
        out_file.write("##DATA FROM main.swn SECTION:")
        current_bytes = in_file.read(64)
        while (current_bytes != b''):
            out_file.write("\n" + self.__findStringInBytes(current_bytes))
            current_bytes = in_file.read(64)
        in_file.close()
        out_file.close()

        in_file = open(os.path.join(self.__dir, "main.sw"), 'rb')
        out_file = open(os.path.join(out_dir, "__main_sw.txt"), 'w', encoding=self.__encoding)
        out_file.write("##DATA FROM main.sw SECTION:")
        current_bytes = in_file.read(4)
        while (current_bytes != b''):
            out_file.write("\n" + str(struct.unpack('i', current_bytes)[0]))
            current_bytes = in_file.read(4)
        in_file.close()
        out_file.close()

        in_file = open(os.path.join(self.__dir, "main.cg"), 'rb')
        out_file = open(os.path.join(out_dir, "__main_cg.txt"), 'w', encoding=self.__encoding)
        out_file.write("##DATA FROM main.cg SECTION:")
        current_bytes = in_file.read(4)
        while (current_bytes != b''):
            out_file.write("\n" + str(struct.unpack('i', current_bytes)[0]))
            current_bytes = in_file.read(4)
        in_file.close()
        out_file.close()

    #Отдельные файловые технические функции.
    def __createFiles(self, out_dir):
        #А здесь де-факто... И совпадения есть не всегда...
        for i in self.__mainlib:
            file_name = os.path.join(out_dir, i[1][1])
            full_name = file_name.split(os.sep)
            full_name.pop(-1)
            dirs_name = ''
            for k in full_name:
                dirs_name += k
                dirs_name += os.sep
            os.makedirs(dirs_name, exist_ok=True)
            file_out = open(file_name, 'w', encoding=self.__encoding)
            file_out.close()
    def __set_nominal_sizes(self, out_dir):
        need_to_resize = ["main.cg", "main.lb", "main.sw", "main.tko", "main.ev"]
        for i in need_to_resize:
            self.__nominal_size[i] = os.path.getsize(os.path.join(self.__dir, i))
        out_file = open(os.path.join(out_dir, "__nominal_size.txt"), 'w', encoding=self.__encoding)
        out_file.write("##NOMINAL SIZES OF HARD SIZED SECTIONS:")
        for i in self.__nominal_size:
            out_file.write("\n" + i + "\n" + str(self.__nominal_size[i]))
        out_file.close()

    #Технические функции распаковки структур.
    def __getB(self, file_in, current_pos, i):
        dummy = struct.unpack(i, file_in.read(1))[0]
        current_pos += 1
        return dummy, file_in, current_pos
    def __getH(self, file_in, current_pos, i):
        dummy = struct.unpack(i, file_in.read(2))[0]
        current_pos += 2
        return dummy, file_in, current_pos
    def __getI(self, file_in, current_pos, i):
        dummy = struct.unpack(i, file_in.read(4))[0]
        current_pos += 4
        return dummy, file_in, current_pos
    def __getS(self, file_in, current_pos):
        symb = file_in.read(1)
        current_pos += 1
        byte_str = b''
        while (symb != b'\x00'):
            byte_str += symb
            symb = file_in.read(1)
            current_pos += 1
        dummy = byte_str.decode(self.__encoding)
        assert symb == b'\x00', "IMPOSSIBLE STRING CLOSING ON " + str(current_pos) + "!"
        return dummy, file_in, current_pos
    def __gets(self, file_in, current_pos):
        lens = struct.unpack('B', file_in.read(1))[0]
        current_pos += 1
        dummy = file_in.read(lens).decode(self.__encoding)
        current_pos += lens
        assert file_in.read(1) == b'\x00',\
            "IMPOSSIBLE sTRING CLOSING ON " + str(current_pos) + "!"
        current_pos += 1
        return dummy, file_in, current_pos
    def __getN(self, file_in, current_pos):
        dummy = struct.unpack('B', file_in.read(1))[0]
        current_pos += 1
        return dummy, file_in, current_pos
    def __getG(self, file_in, current_pos, grouper, i):
        dummy = []
        if (i == 'G'):
            for z in range(grouper):
                dummy.append(struct.unpack('I', file_in.read(4))[0])
                current_pos += 4
        for k in range(grouper):
            symb = file_in.read(1)
            current_pos += 1
            byte_str = b''
            while (symb != b'\x00'):
                byte_str += symb
                symb = file_in.read(1)
                current_pos += 1
            dummy.append(byte_str.decode(self.__encoding))
            assert symb == b'\x00',\
                "IMPOSSIBLE STRING CLOSING ON " + str(current_pos) + "!"
        return dummy, file_in, current_pos
    def __getZ(self, file_in, current_pos, grouper):
        dummy = []
        struct_byter = ''
        struct_num = -1
        while (struct_num == -1):
            if (struct_byter == ''):
                struct_byter = file_in.read(1).hex()
            else:
                struct_byter += " " + file_in.read(1).hex()
            current_pos += 1
            for k in range(len(self.structs_library)):
                if (struct_byter == self.structs_library[k][0]):
                    struct_num = k
            if (len(struct_byter) > 100):
                print("Z STRUCT UNRESOLVED BUG!!! " + str(current_pos) + " " + struct_byter[:32])
                sys.exit()
        dummy.append(struct_byter)
        for k in self.structs_library[struct_num][1]:
            if (k.upper() == 'B'):
                val, file_in, current_pos = self.__getB(file_in, current_pos, k)
                dummy.append(val)
            elif (k.upper() == 'H'):
                val, file_in, current_pos = self.__getH(file_in, current_pos, k)
                dummy.append(val)
            elif (k.upper() == 'I'):
                val, file_in, current_pos = self.__getI(file_in, current_pos, k)
                dummy.append(val)
            elif (k == 'S'):
                val, file_in, current_pos = self.__getS(file_in, current_pos)
                dummy.append(val)
            elif (k == 's'):
                val, file_in, current_pos = self.__gets(file_in, current_pos)
                dummy.append(val)
            elif (k == 'N'):
                grouper, file_in, current_pos = self.__getN(file_in, current_pos)
            elif (k.upper() == 'G'):
                val, file_in, current_pos = self.__getG(file_in, current_pos, grouper, k)
                dummy.append(val)
            elif (k == 'Z'):
                val, file_in, current_pos = self.__getZ(file_in, current_pos, grouper)
                dummy.append(val)
        return dummy, file_in, current_pos

    #Прочие технические функции.
    def __chkScriptFiles(self):
        files = os.listdir(self.__dir)
        if (files != ['main.cg', 'main.ev', 'main.lb', 'main.lbn', 'main.sd', 'main.sfn', 'main.sw', 'main.swn', 'main.tko']):
            raise SLG_ScriptsError("Not a Sengokuhime's script!")
    def __findStringInBytes(self, byter):
        limiter = 0
        while (byter[limiter] != 0):
            limiter += 1
        return byter[:limiter].decode(self.__encoding)

class SLG_ScriptsError(Exception):
    def __init__(self, text):
        self.txt = text