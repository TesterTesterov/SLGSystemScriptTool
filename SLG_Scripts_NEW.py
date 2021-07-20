import struct
import os
import sys
import json
import time
import copy

from SLG_Command_lib import SLG_Command_lib, SLG_Command_lib_ver0, SLG_Command_lib_ver1, SLG_Command_lib_ver2, \
    SLG_Command_lib_ver3_0, \
    SLG_Command_lib_ver3_1, SLG_Command_lib_ver4_0, SLG_Command_lib_ver4_1

from SLG_Scripts import SLG_ScriptsError


class SLG_Scripts_NEW():
    possible_encodings = ('cp932', 'shift-jis', 'windows-1251', 'windows-1252',
                          'utf-8', 'utf-16', 'utf-16le', 'utf-32', 'utf-32le',
                          'cp936', 'cp949', 'cp950')
    game_versions = [[0.0, ['Shihen69']],
                     [1.0, ['Sengoku Hime 1']],
                     [2.0, ['Sengoku Hime 2', 'Sengoku Hime 3']],
                     [3.0, ['Sengoku Hime 4']],
                     [3.1, ['Sangoku Hime 1 Renewal']],
                     [4.0, ['Sengoku Hime 5']],
                     [4.1, ['Sengoku Hime 6']]]

    # Инициализация.
    def __init__(self, dir, base_name, encoding, version):
        self._struct_normal = 'STRUCT'
        self._struct_command = 'COMMAND'
        self._group_start = 'GROUP'
        self._test_mode = False
        # This one is for help to hack another game on this engine scripts.

        self._version = version

        self._dir = dir
        self._base_name = base_name
        # self._chk_script_files()
        self._encoding = encoding
        self._code_lib = self._get_code_lib_from_version()

        # main.lb, main.lbn:
        self._main_lib = []

        # main.ev:
        self._ev_lib = []
        self._new_ev_lib = []

        # main.sb, main.sbn. Размерность в main.snm.
        self._eff_lib = []

        # main.sw, main.swn:
        self._var_lib = []

        # Размеры разделов, требующих дополнения:
        self._nominal_size = dict()
        self._nominal_size["{}.cg".format(self._base_name)] = 0
        self._nominal_size["{}.bl".format(self._base_name)] = 0
        self._nominal_size["{}.lb".format(self._base_name)] = 0
        self._nominal_size["{}.sw".format(self._base_name)] = 0
        self._nominal_size["{}.tko".format(self._base_name)] = 0
        self._nominal_size["{}.ev".format(self._base_name)] = 0
        self._nominal_size["{}.sb".format(self._base_name)] = 0

    # Взаимодействие с пользователем.
    def get_stat_ev_lib(self):
        return self._ev_lib

    def get_stat_main_lib(self):
        return self._main_lib

    def get_nominal_sizes(self):
        return self._nominal_size

    def decompile(self, outer, mode):
        timer = time.time()
        if (int(self._version) == 0):
            if (os.path.split(outer)[0] != ''):
                os.makedirs(os.path.split(outer)[0], exist_ok=True)
            self._decompile_zero(outer)
        else:
            self._ev_lib = self._decompile_ev_lib()
            self._main_lib = self._decompile_main_lib()
            self._var_lib = self._decompile_var_lib()
            if (mode == 0):  # Один файл.
                if (os.path.split(outer)[0] != ''):
                    os.makedirs(os.path.split(outer)[0], exist_ok=True)
            else:  # Директории.
                self._create_files(outer)
                os.makedirs(outer, exist_ok=True)
                self._set_compile_order(outer)
            if (self._version >= 3):
                self._new_ev_lib = self._decompile_new_ev_lib(outer, mode)
            if (self._version >= 4):
                self._eff_lib = self._decompile_eff_lib()
            self._set_nominal_sizes(outer, mode)
            self._decompile_main(outer, mode)
            self._decompile_var(outer, mode)
            self._decompile_rest(outer, mode)
        print('Время декомпиляции/Decompilation time:', time.time() - timer)

    def compile(self, iner, mode):
        timer = time.time()
        if (int(self._version) == 0):
            os.makedirs(os.path.split(self._dir)[0], exist_ok=True)
            self._compile_zero(iner)
        else:
            self._var_lib = self._compile_var_lib(iner, mode)
            self._nominal_size = dict(self._get_nominal_sizes(iner, mode))
            self._main_lib = self._compile_main_lib_names(iner, mode)
            if (self._version >= 3):
                self._new_ev_lib = self._compile_new_ev_lib_names(iner, mode)
            os.makedirs(self._dir, exist_ok=True)

            tko_lib, self._ev_lib, self._new_ev_lib, self._main_lib, self._eff_lib = self._compile_main(iner, mode)
            self._compile_main_lib()
            self._compile_ev()
            if (self._version >= 3):
                self._compile_new_ev(iner, mode)
            if (self._version >= 4):
                self._compile_eff_lib()
            self._compile_var()
            self._compile_tko(tko_lib)
            self._compile_rest(iner, mode)
        print('Время компиляции/Compiling time:', time.time() - timer)

    # Технические функции компиляции...
    def _compile_eff_lib(self):
        out_file_name = open(os.path.join(self._dir, "{}.sbn".format(self._base_name)), 'wb')
        out_file_value = open(os.path.join(self._dir, "{}.sb".format(self._base_name)), 'wb')
        effer = self._eff_lib.copy()
        for i in effer:
            out_file_name.write(self._get_string_to_bytes(i[0], 64))
            out_file_value.write(struct.pack('I', i[1]))
        out_file_name.close()
        out_file_value.write(bytes(self._nominal_size["{}.sb".format(self._base_name)] - out_file_value.tell()))
        out_file_value.close()
        out_file = open(os.path.join(self._dir, "{}.snm".format(self._base_name)), 'wb')
        out_file.write(struct.pack('I', len(self._eff_lib)))
        out_file.close()

    def _compile_new_ev(self, iner, mode):
        in_dir = iner
        if (mode == 0):
            in_dir = os.path.split(iner)[0]
        in_file = open(os.path.join(in_dir, "__{}_bl_rest.txt".format(self._base_name)), 'r', encoding=self._encoding)
        out_file = open(os.path.join(self._dir, "{}.bl".format(self._base_name)), 'wb')
        in_file.readline()
        out_file.write(bytes.fromhex(in_file.readline()))
        in_file.close()
        if (self._version >= 4):
            for i in self._new_ev_lib:
                out_file.write(struct.pack('I', i[1]))
                out_file.write(struct.pack('I', int(i[0])))
            out_file.write(bytes(self._code_lib.bl_new_point - out_file.tell()))
            in_file2 = open(os.path.join(in_dir, "__{}_bl_rest2.bin".format(self._base_name)), 'rb')
            out_file.write(in_file2.read())
            in_file2.close()
        else:
            for i in self._new_ev_lib:
                out_file.write(self._get_string_to_bytes(i[0], 64))
                out_file.write(struct.pack('I', i[1]))
            out_file.write(bytes(self._nominal_size["{}.bl".format(self._base_name)] - out_file.tell()))
        out_file.close()

    def _compile_new_ev_lib_names(self, iner, mode):
        in_dir = iner
        if (mode == 0):
            in_dir = os.path.split(iner)[0]
        in_file = open(os.path.join(in_dir, "__{}_bl_rest.txt".format(self._base_name)), 'r', encoding=self._encoding)
        in_file.readline()
        in_file.readline()
        new_names = json.load(in_file)
        in_file.close()
        new_ev_lib = []
        for i in new_names:
            arr = []
            arr.append(i)
            arr.append(0)
            new_ev_lib.append(arr)
        return new_ev_lib

    def _compile_main_lib(self):
        file_names = open(os.path.join(self._dir, "{}.lbn".format(self._base_name)), 'wb')
        file_offsets = open(os.path.join(self._dir, "{}.lb".format(self._base_name)), 'wb')
        for i in self._main_lib:
            file_offsets.write(struct.pack('I', i[0]))
            file_names.write(self._get_string_to_bytes(i[1][0], 64))
            new_string = i[1][1]
            if (i[1][1][-1] == '_'):
                new_string = i[1][1][:-1] + '/'
            file_names.write(self._get_string_to_bytes(new_string, 64))
        file_names.close()
        file_offsets.write(bytes(self._nominal_size["{}.lb".format(self._base_name)] - file_offsets.tell()))

    def _compile_tko(self, tko_lib):
        file_out = open(os.path.join(self._dir, "{}.tko".format(self._base_name)), 'wb')
        for i in tko_lib:
            file_out.write(struct.pack('I', i))
        file_out.write(bytes(self._nominal_size["{}.tko".format(self._base_name)] - file_out.tell()))
        file_out.close()

    def _compile_ev(self):
        file_out = open(os.path.join(self._dir, "{}.ev".format(self._base_name)), 'wb')
        for i in self._ev_lib:
            file_out.write(self._get_string_to_bytes(i[0], 64))
            file_out.write(struct.pack('I', i[1]))
        file_out.write(bytes(self._nominal_size["{}.ev".format(self._base_name)] - file_out.tell()))
        file_out.close()

    def _compile_main_lib_names(self, iner, mode):
        in_dir = iner
        libra = []
        if (mode == 0):
            in_dir = os.path.split(iner)[0]
        in_file = open(os.path.join(in_dir, "__{}_order.txt".format(self._base_name)), 'r', encoding=self._encoding)
        in_file.readline()
        string_names = json.load(in_file)
        in_file.close()
        for i in string_names:
            arr = []
            arr.append(0)
            arr.append(i)
            libra.append(arr)
        return libra

    def _compile_var(self):
        out_values = open(os.path.join(self._dir, "{}.sw".format(self._base_name)), 'wb')
        if (self._version >= 4):
            for i in self._var_lib:
                out_values.write(struct.pack('i', i))
        else:
            out_names = open(os.path.join(self._dir, "{}.swn".format(self._base_name)), 'wb')
            for i in self._var_lib:
                out_names.write(self._get_string_to_bytes(i[0], 64))
                out_values.write(struct.pack('i', i[1]))
            out_values.write(bytes(self._nominal_size["{}.sw".format(self._base_name)] - out_values.tell()))
            out_names.close()
        out_values.close()

    def _compile_var_lib(self, iner, mode):
        in_dir = iner
        if (mode == 0):
            in_dir = os.path.split(iner)[0]
        in_file = open(os.path.join(in_dir, "__var_lib.txt"), 'r', encoding=self._encoding)
        in_file.readline()
        zlo = json.load(in_file)
        in_file.close()
        return zlo

    def _get_nominal_sizes(self, iner, mode):
        in_dir = iner
        if (mode == 0):
            in_dir = os.path.split(iner)[0]
        in_file = open(os.path.join(in_dir, "__nominal_size.txt"), 'r', encoding=self._encoding)
        in_file.readline()
        zlo = json.load(in_file)
        in_file.close()
        return zlo

    def _compile_rest(self, iner, mode):
        in_dir = iner
        if (mode == 0):
            in_dir = os.path.split(iner)[0]
        in_file = open(os.path.join(in_dir, "__{}_sfn.txt".format(self._base_name)), 'r', encoding=self._encoding)
        in_file.readline()
        stringer = json.load(in_file)
        in_file.close()
        out_file = open(os.path.join(self._dir, "{}.sfn".format(self._base_name)), 'wb')
        for i in stringer:
            out_file.write(self._get_string_to_bytes(i, 64))
        out_file.close()

        if ((self._version == 1) or (self._version == 2)):
            in_file = open(os.path.join(in_dir, "__{}_cg.txt".format(self._base_name)), 'r', encoding=self._encoding)
            in_file.readline()
            dater = json.load(in_file)
            in_file.close()
            out_file = open(os.path.join(self._dir, "{}.cg".format(self._base_name)), 'wb')
            for i in dater:
                out_file.write(struct.pack('i', i))
            out_file.write(bytes(self._nominal_size["{}.cg".format(self._base_name)] - out_file.tell()))
            out_file.close()

    def _compile_zero(self, iner):
        name = ''
        mes_num = 0
        event_section = []  # name, offset.
        variable_section = []  # var, value.
        img_eff_section = []  # value1, value2, name. #image effect, flag.
        img_ev_section = []  # value1, value2, name. #image event, flag.
        jump_section = []
        name, mes_num, event_section, variable_section, img_eff_section, img_ev_section, jump_section = self._compile_zero_data(
            iner)
        file_in = open(iner, 'r', encoding=self._encoding)
        if (self._dir != ''):
            os.makedirs(self._dir, exist_ok=True)
        file_out = open(os.path.join(self._dir, self._base_name), 'wb')
        file_out.write(self._get_string_to_bytes(name, 256))
        file_out.write(struct.pack('I', mes_num))
        file_out.write(bytes(128))

        file_out.write(struct.pack('I', len(event_section)))
        for i in event_section:
            file_out.write(self._get_string_to_bytes(i[0], 64))
            file_out.write(struct.pack('I', i[1]))
        file_out.write(struct.pack('I', len(variable_section)))
        for i in variable_section:
            file_out.write(self._get_string_to_bytes(i[0], 64))
            file_out.write(struct.pack('I', i[1]))
        file_out.write(struct.pack('I', len(img_eff_section)))
        for i in img_eff_section:
            file_out.write(struct.pack('I', i[0]))
            file_out.write(struct.pack('I', i[1]))
            file_out.write(self._get_string_to_bytes(i[2], 256))
            file_out.write(struct.pack('I', i[3]))
        file_out.write(struct.pack('I', len(img_ev_section)))
        for i in img_ev_section:
            file_out.write(struct.pack('I', i[0]))
            file_out.write(struct.pack('I', i[1]))
            file_out.write(self._get_string_to_bytes(i[2], 256))
            file_out.write(struct.pack('I', i[3]))

        new_line = ''
        while (new_line != '#CODE:\n'):
            new_line = file_in.readline()

        count_mes = 0
        count_spec = 0
        while True:
            new_line = file_in.readline()
            if (new_line == ''):
                break
            if (self._safe_substring_analysis(new_line, '$', 0)):
                continue
            if (self._safe_substring_analysis(new_line, '#', 0)):
                if (self._safe_substring_analysis(new_line, '1', 1)):
                    command_arr = json.loads(new_line[4:])
                    command_index = self._code_lib.get_index_from_command(command_arr[0])
                    file_out.write(self._get_bytes_from_command_arr(command_arr))
                    arguments = self._get_command_args(file_in)

                    if ((self._code_lib.command_library[command_index][0] == '15') or
                            (self._code_lib.command_library[command_index][0] == '16')):
                        arguments[0] = count_mes
                        count_mes += 1
                    elif (self._code_lib.command_library[command_index][0] == '19'):
                        jump_index = jump_section[1].index(arguments[0][1:].rstrip())
                        arguments[0] = jump_section[0][jump_index]
                    elif (self._code_lib.command_library[command_index][0] == '28'):
                        arguments[0] = count_spec
                        count_spec += 1

                    new_bytes = self._assemble_command_args(arguments,
                                                            self._code_lib.command_library[command_index][1])
                    file_out.write(new_bytes)

        file_in.close()
        file_out.close()

    def _compile_zero_data(self, iner):
        name = ''
        mes_num = 0
        event_section = []  # name, offset.
        variable_section = []  # var, value.
        img_eff_section = []  # value1, value2, name. #image effect.
        img_ev_section = []  # value1, value2, name. #image event.
        jump_section = [[], []]  # offset, number.

        file_in = open(iner, 'r', encoding=self._encoding)
        name = file_in.readline()[:-1]
        assert file_in.readline() == "#EVENTS:\n"
        event_section = self._get_command_args(file_in)
        assert file_in.readline() == "#VARIABLES:\n"
        variable_section = self._get_command_args(file_in)
        assert file_in.readline() == '#IMAGE_EFFECTS:\n'
        img_eff_section = self._get_command_args(file_in)
        assert file_in.readline() == '#IMAGE_EVENTS:\n'
        img_ev_section = self._get_command_args(file_in)
        assert file_in.readline() == '#CODE:\n'

        current_offset = 0

        while True:
            new_line = file_in.readline()
            if (new_line == ''):
                break
            if (self._safe_substring_analysis(new_line, '$', 0)):
                continue
            if (self._safe_substring_analysis(new_line, '#', 0)):
                if (self._safe_substring_analysis(new_line, '0', 1)):  # Команда.
                    current_offset += len(bytes.fromhex(new_line[4:]))
                elif (self._safe_substring_analysis(new_line, '1', 1)):  # Команда.
                    command_arr = json.loads(new_line[4:])
                    command_index = self._code_lib.get_index_from_command(command_arr[0])
                    current_offset += len(self._get_bytes_from_command_arr(command_arr))
                    arguments = self._get_command_args(file_in)

                    if ((self._code_lib.command_library[command_index][0] == '15') or
                            (self._code_lib.command_library[command_index][0] == '16')):
                        arguments[0] = 0
                        mes_num += 1
                    elif ((self._code_lib.command_library[command_index][0] == '19') or
                          (self._code_lib.command_library[command_index][0] == '28')):
                        arguments[0] = 0

                    new_bytes = self._assemble_command_args(arguments,
                                                            self._code_lib.command_library[command_index][1])
                    current_offset += len(new_bytes)

                elif (self._safe_substring_analysis(new_line, '2', 1)):  # Событие.
                    this_name = new_line.split(' ')[2].rstrip()
                    for z in range(len(event_section)):
                        if (event_section[z][0] == this_name):
                            event_section[z][1] = current_offset
                elif (self._safe_substring_analysis(new_line, '3', 1)):  # Эффект.
                    this_index = int(new_line.split(' ')[1])
                    img_eff_section[this_index][1] = current_offset
                elif (self._safe_substring_analysis(new_line, '4', 1)):  # Метка.
                    this_number = new_line.split(' ')[1].rstrip()
                    jump_section[0].append(current_offset)
                    jump_section[1].append(this_number)

        file_in.close()
        return name, mes_num, event_section, variable_section, img_eff_section, img_ev_section, jump_section

    def _compile_main(self, iner, mode):
        scenario_string_num = 0
        message_num = 0
        ev_lib = []
        eff_lib = []
        tko_lib = []
        new_ev_lib = []
        label_lib = []
        index_label_lib = []
        if (self._version >= 3):
            new_ev_lib = self._new_ev_lib.copy()
            label_lib, index_label_lib = self._set_label_lib(iner, mode)
        main_lib = self._main_lib.copy()
        # MESSAGE [scenario_string_num, message_num, ...]
        # CHOICE [scenario_string_num, ...]

        next_file = 0
        compile_list = []
        if (mode == 1):
            file_in = open(os.path.join(iner, '__compile_order.txt'), 'r', encoding=self._encoding)
            file_in.readline()
            compile_list = json.load(file_in)
            file_in.close()

        file_out = open(os.path.join(self._dir, "{}.sd".format(self._base_name)), 'wb')
        from_file = iner
        if (mode == 1):
            from_file = os.path.join(iner, "__boot.txt")
        file_in = open(from_file, 'r', encoding=self._encoding)
        while True:
            current_pos = file_out.tell()
            new_line = file_in.readline()
            if ((new_line == '') and (mode == 0)):
                break
            if (mode == 0):
                neo_usl = (new_line[1] == '#')
            else:
                neo_usl = (new_line == '') or self._safe_substring_analysis(new_line, '#', 1)
            if (self._safe_substring_analysis(new_line, '$', 0)):
                continue
            if (self._safe_substring_analysis(new_line, '#', 0)):
                if (self._safe_substring_analysis(new_line, '0', 1)):
                    file_out.write(bytes.fromhex(new_line[4:]))
                elif (self._safe_substring_analysis(new_line, '1', 1)):
                    command_arr = json.loads(new_line[4:])
                    command_index = self._code_lib.get_index_from_command(command_arr[0])
                    file_out.write(self._get_bytes_from_command_arr(command_arr))
                    arguments = self._get_command_args(file_in)
                    if (self._code_lib.command_library[command_index][2] == 'MESSAGE'):
                        tko_lib.append(current_pos)
                        arguments[0] = scenario_string_num
                        scenario_string_num += 1
                        arguments[1] = message_num
                        message_num += 1
                    elif (self._code_lib.command_library[command_index][2] == 'CHOICE'):
                        tko_lib.append(current_pos)
                        arguments[0] = scenario_string_num
                        scenario_string_num += 1
                    if (self._version >= 3):
                        if (self._code_lib.command_library[command_index][2] == 'JUMP'):
                            label_num = int(arguments[0][1:])
                            label_index = index_label_lib.index(label_num)
                            arguments[0] = label_lib[label_index]
                    new_bytes = self._assemble_command_args(arguments,
                                                            self._code_lib.command_library[command_index][1])
                    file_out.write(new_bytes)
                elif (self._safe_substring_analysis(new_line, '2', 1)):
                    new_event = new_line.split(' ')[1].rstrip()
                    arr = []
                    arr.append(new_event)
                    arr.append(current_pos)
                    ev_lib.append(arr)
                elif (self._safe_substring_analysis(new_line, '3', 1)):
                    new_event = new_line.split(' ')[1].rstrip()
                    for i in new_ev_lib:
                        if (new_event == i[0]):
                            i[1] = current_pos
                elif (self._safe_substring_analysis(new_line, '5', 1)):
                    new_effect = new_line.split(' ')[1].rstrip()
                    arr = []
                    arr.append(new_effect)
                    arr.append(current_pos)
                    eff_lib.append(arr)
            if (neo_usl):
                if ((mode == 1) and (next_file >= len(compile_list))):
                    break
                if (mode == 1):
                    file_in.close()
                    file_in = open(os.path.join(iner, compile_list[next_file][1]), 'r', encoding=self._encoding)
                    wanted_string = "##: " + compile_list[next_file][0] + "\n"
                    while True:
                        new_line = file_in.readline()
                        if (new_line == wanted_string):
                            break
                new_event = new_line.split(' ')[1].rstrip()
                new_file = ''
                if (mode == 0):
                    new_file = new_line.split(' ')[3].rstrip()
                else:
                    new_file = compile_list[next_file][1]
                for i in main_lib:
                    if ((new_event == i[1][0]) and (new_file == i[1][1])):
                        i[0] = current_pos
                        break
                if (mode == 1):
                    next_file += 1
        file_out.close()
        file_in.close()
        return tko_lib, ev_lib, new_ev_lib, main_lib, eff_lib

    # Специальные технические функции для компиляции.
    def _set_label_lib(self, iner, mode):
        label_lib = []
        index_label_lib = []

        next_file = 0
        compile_list = []
        if (mode == 1):
            file_in = open(os.path.join(iner, '__compile_order.txt'), 'r', encoding=self._encoding)
            file_in.readline()
            compile_list = json.load(file_in)
            file_in.close()

        from_file = iner
        if (mode == 1):
            from_file = os.path.join(iner, "__boot.txt")
        file_in = open(from_file, 'r', encoding=self._encoding)

        current_pos = 0

        while True:
            new_line = file_in.readline()
            if ((new_line == '') and (mode == 0)):
                break
            neo_usl = False
            if (mode == 0):
                neo_usl = (new_line[1] == '#')
            else:
                neo_usl = (new_line == '') or self._safe_substring_analysis(new_line, '#', 1)
            if (self._safe_substring_analysis(new_line, '0', 1)):
                current_pos += len(bytes.fromhex(new_line[4:]))
            elif (self._safe_substring_analysis(new_line, '1', 1)):
                command_arr = json.loads(new_line[4:])
                command_index = self._code_lib.get_index_from_command(command_arr[0])

                current_pos += len(self._get_bytes_from_command_arr(command_arr))
                arguments = self._get_command_args(file_in)
                if (self._code_lib.command_library[command_index][2] == 'MESSAGE'):
                    arguments[0] = 0
                    arguments[1] = 0
                elif (self._code_lib.command_library[command_index][2] == 'CHOICE'):
                    arguments[0] = 0
                if (self._version >= 3):
                    if (self._code_lib.command_library[command_index][2] == 'JUMP'):
                        arguments[0] = 0
                new_bytes = self._assemble_command_args(arguments,
                                                        self._code_lib.command_library[command_index][1])
                current_pos += len(new_bytes)
            elif (self._safe_substring_analysis(new_line, '4', 1)):
                new_label = int(new_line.split(' ')[1].rstrip())
                index_label_lib.append(new_label)
                label_lib.append(current_pos)
            elif (neo_usl):
                if ((mode == 1) and (next_file >= len(compile_list))):
                    break
                if (mode == 1):
                    file_in.close()
                    file_in = open(os.path.join(iner, compile_list[next_file][1]), 'r', encoding=self._encoding)
                    wanted_string = "##: " + compile_list[next_file][0] + "\n"
                    while True:
                        new_line = file_in.readline()
                        if (new_line == wanted_string):
                            break
                    next_file += 1
        file_in.close()
        return label_lib, index_label_lib

    def _safe_substring_analysis(self, stringz, substring, index):
        if (len(stringz) <= index):
            return False
        else:
            if (stringz[index] == substring):
                return True
            else:
                return False

    def _assemble_command_args(self, arguments, comm_stru):
        grouper = 1
        grouper_flag = False
        byter = b''
        k = 0
        while (k < len(arguments)):
            if (comm_stru[k].upper() == 'B'):
                byter += self._ass_group_magic(self._set_B, [arguments[k], comm_stru[k]], grouper, grouper_flag)
                k += 1
            elif (comm_stru[k].upper() == 'H'):
                byter += self._ass_group_magic(self._set_H, [arguments[k], comm_stru[k]], grouper, grouper_flag)
                k += 1
            elif (comm_stru[k].upper() == 'I'):
                byter += self._ass_group_magic(self._set_I, [arguments[k], comm_stru[k]], grouper, grouper_flag)
                k += 1
            elif (comm_stru[k] == 'S'):
                byter += self._ass_group_magic(self._set_S, [arguments[k]], grouper, grouper_flag)
                k += 1
            elif (comm_stru[k] == 's'):
                byter += self._ass_group_magic(self._set_s, [arguments[k]], grouper, grouper_flag)
                k += 1
            elif (comm_stru[k] == 'G'):
                new_byte, grouper = self._set_G(arguments[k])
                byter += new_byte
                grouper_flag = True
                comm_stru = comm_stru[:k] + comm_stru[k + 1:]
            elif (comm_stru[k] == 'g'):
                new_byte, grouper = self._set_g(arguments[k])
                byter += new_byte
                grouper_flag = True
                comm_stru = comm_stru[:k] + comm_stru[k + 1:]
            elif (comm_stru[k] == 'N'):
                grouper_flag = False
                comm_stru = comm_stru[:k] + comm_stru[k + 1:]
            elif (comm_stru[k] == 'M'):
                byter += self._ass_group_magic(self._set_M, [arguments[k]], grouper, grouper_flag)
                k += 1
            elif (comm_stru[k] == 'R'):
                byter += self._ass_group_magic(self._set_R, [arguments[k]], grouper, grouper_flag)
                k += 1
            elif (comm_stru[k] == 'Z'):
                byter += self._ass_group_magic(self._set_Z, [arguments[k]], grouper, grouper_flag)
                k += 1
        return byter

    def _ass_group_magic(self, func, args, grouper, grouper_flag):
        if (grouper_flag):
            arger = []
            if (len(args) == 1):
                for x in range(1, len(args[0])):
                    arger.append(args[0][x])
            else:
                for x in range(1, len(args[0])):
                    arr = []
                    arr.append(args[0][x])
                    arr.append(args[1])
                    arger.append(arr)
            byter = b''
            for f in range(grouper):
                byter += self._get_val_from_n_arg(func, arger[f])
            return byter
        else:
            return self._get_val_from_n_arg(func, args)

    def _get_command_args(self, file_in):
        all_lines = ''
        while True:
            new_line = file_in.readline()
            all_lines += new_line
            if ((new_line.rstrip('\n') == "[]") or (new_line.rstrip('\n') == "]")):
                break
        return json.loads(all_lines)

    def _get_bytes_from_command_arr(self, command_arr):
        byters = b''
        byters += bytes.fromhex(
            self._code_lib.command_library[self._code_lib.get_index_from_command(command_arr[0])][0]
        )
        command_arr.pop(0)
        for i in range(len(command_arr)):
            byters += struct.pack(self._code_lib.postcommand_data[i], command_arr[i])
        return byters

    # Сборка аргументов.
    def _set_B(self, arguments, command):
        return struct.pack(command, arguments)

    def _set_H(self, arguments, command):
        return struct.pack(command, arguments)

    def _set_I(self, arguments, command):
        return struct.pack(command, arguments)

    def _set_S(self, arguments):
        byters = arguments.encode(self._encoding) + b'\x00'
        return byters

    def _set_s(self, arguments):
        str_byters = arguments.encode(self._encoding)
        byters = struct.pack('B', len(str_byters))
        byters += str_byters
        byters += b'\x00'
        return byters

    def _set_G(self, arguments):
        grouper = len(arguments) - 1
        new_byte = struct.pack('I', grouper)
        return new_byte, grouper

    def _set_g(self, arguments):  # I
        grouper = len(arguments) - 1
        new_byte = struct.pack('B', grouper)
        return new_byte, grouper

    def _set_Z(self, arguments):
        byter = b''
        typer = arguments[0]
        strer = ''
        if (typer == self._struct_normal):
            struct_index = self._code_lib.get_index_from_struct(arguments[1])
            byter += bytes.fromhex(self._code_lib.structs_library[struct_index][0])
            strer = self._code_lib.structs_library[struct_index][1]
        elif (typer == self._struct_command):
            command_arr = arguments[1]
            command_index = self._code_lib.get_index_from_command(command_arr[0])
            byter += self._get_bytes_from_command_arr(command_arr)
            strer = self._code_lib.command_library[command_index][1]
        byter += self._assemble_command_args(arguments[2], strer)
        return byter

    def _set_M(self, arguments):
        byter = b''
        byter += self._set_S(arguments[0])
        byter += self._set_B(arguments[1], 'B')
        byter += self._set_H(arguments[2], 'H')
        byter += self._set_I(arguments[3], 'i')
        byter += self._set_I(arguments[4], 'i')
        return byter

    def _set_R(self, arguments):
        byter = b''
        byter += self._set_I(arguments[0], 'I')
        byter += self._set_Z(arguments[1])
        return byter

    # Технические функции декомпиляции..
    def _decompile_eff_lib(self):
        eff_lib = []
        in_file_name = open(os.path.join(self._dir, "{}.sbn".format(self._base_name)), 'rb')
        in_file_value = open(os.path.join(self._dir, "{}.sb".format(self._base_name)), 'rb')
        while True:
            current_bytes = in_file_name.read(64)
            value_bytes = in_file_value.read(4)
            if (current_bytes == b''):
                break
            arr = []
            arr.append(self._find_string_in_bytes(current_bytes))
            arr.append(struct.unpack('I', value_bytes)[0])
            eff_lib.append(arr)
        return eff_lib

    def _decompile_new_ev_lib(self, outer, mode):
        out_dir = outer
        if (mode == 0):
            out_dir = os.path.split(outer)[0]
        out_file = open(os.path.join(out_dir, "__{}_bl_rest.txt".format(self._base_name)), 'w', encoding=self._encoding)
        in_file = open(os.path.join(self._dir, "{}.bl".format(self._base_name)), 'rb')
        out_file.write("##REST OF DATA FROM THE {}.BL:\n".format(self._base_name.upper()))
        out_file.write(in_file.read(128).hex(' '))
        out_file.write('\n')
        new_ev_lib = []
        stringer = []
        if (self._version >= 4):
            while True:
                arr = []
                new_offset = struct.unpack('I', in_file.read(4))[0]
                new_string = str(struct.unpack('I', in_file.read(4))[0])
                if ((new_string == '0') and (new_offset == 0)):
                    break
                stringer.append(new_string)
                arr.append(str(new_string))
                arr.append(new_offset)
                new_ev_lib.append(arr)
            in_file.seek(self._code_lib.bl_new_point, 0)
            out_file2 = open(os.path.join(out_dir, "__{}_bl_rest2.bin".format(self._base_name)), 'wb')
            out_file2.write(in_file.read())
            out_file2.close()
        else:
            while True:
                arr = []
                new_string = self._find_string_in_bytes(in_file.read(64))
                if (new_string == ''):
                    break
                new_offset = struct.unpack('I', in_file.read(4))[0]
                arr.append(new_string)
                stringer.append(new_string)
                arr.append(new_offset)
                new_ev_lib.append(arr)
        json.dump(stringer, out_file, indent=4, ensure_ascii=False)
        out_file.close()
        in_file.close()
        return new_ev_lib

    def _decompile_ev_lib(self):
        liber = []
        file_in = open(self._dir + os.sep + "{}.ev".format(self._base_name), 'rb')
        current_bytes = file_in.read(64)
        while (current_bytes != b''):
            arrayer = []
            arrayer.append(self._find_string_in_bytes(current_bytes))
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

    def _decompile_main_lib(self):
        libers = []
        file_values = open(os.path.join(self._dir, "{}.lb".format(self._base_name)), 'rb')
        file_names = open(os.path.join(self._dir, "{}.lbn".format(self._base_name)), 'rb')
        while True:
            name_bytes = file_names.read(64)
            offset_bytes = file_values.read(4)
            if (name_bytes == b''):
                break
            firstly = []
            secondary = []
            firstly.append(struct.unpack('I', offset_bytes)[0])
            secondary.append(self._find_string_in_bytes(name_bytes))
            name_bytes = file_names.read(64)
            neo_str = self._find_string_in_bytes(name_bytes)
            if (neo_str[-1] == '/'):
                neo_str = neo_str[:-1] + '_'
            secondary.append(neo_str)
            firstly.append(secondary)
            libers.append(firstly)
        file_values.close()
        file_names.close()
        return libers

    def _decompile_var_lib(self):
        arrayer = []
        in_file_val = open(os.path.join(self._dir, "{}.sw".format(self._base_name)), 'rb')
        if (self._version >= 4):
            while True:
                value_bytes = in_file_val.read(4)
                if (value_bytes == b''):
                    break
                arrayer.append(struct.unpack('i', value_bytes)[0])
        else:
            in_file_name = open(os.path.join(self._dir, "{}.swn".format(self._base_name)), 'rb')
            while (True):
                current_bytes = in_file_name.read(64)
                value_bytes = in_file_val.read(4)
                if (current_bytes == b''):
                    break
                arr = []
                arr.append(self._find_string_in_bytes(current_bytes))
                arr.append(struct.unpack('i', value_bytes)[0])
                arrayer.append(arr)
            in_file_name.close()
        in_file_val.close()
        return arrayer

    def _decompile_zero(self, outer):
        file_in = open(os.path.join(self._dir, self._base_name), 'rb')
        if (os.path.split(outer)[0] != ''):
            os.makedirs(os.path.split(outer)[0], exist_ok=True)
        file_out = open(outer, 'w', encoding=self._encoding, )
        file_out.write(self._find_string_in_bytes(file_in.read(256)))
        file_out.write('\n')
        mess_num = struct.unpack('I', file_in.read(4))[0]
        if (self._test_mode):
            print(mess_num)
        file_in.seek(128, 1)

        event_section = []  # name, offset.
        variable_section = []  # var, value.
        img_eff_section = []  # value1, value2, name. #image effect, flag.
        img_ev_section = []  # value1, value2, name. #image event, flag.

        ev_section_len = struct.unpack('I', file_in.read(4))[0]
        for i in range(ev_section_len):
            arr = []
            arr.append(self._find_string_in_bytes(file_in.read(64)))
            arr.append(struct.unpack('I', file_in.read(4))[0])
            event_section.append(arr)
        file_out.write("#EVENTS:\n")
        dummy_event_section = copy.deepcopy(event_section)
        for i in range(len(dummy_event_section)):
            dummy_event_section[i][1] = '<EVENT_OFFSET>'
        json.dump(dummy_event_section, file_out, indent=4, ensure_ascii=False)
        var_section_len = struct.unpack('I', file_in.read(4))[0]
        for i in range(var_section_len):
            arr = []
            arr.append(self._find_string_in_bytes(file_in.read(64)))
            arr.append(struct.unpack('I', file_in.read(4))[0])
            variable_section.append(arr)
        file_out.write("\n#VARIABLES:\n")
        json.dump(variable_section, file_out, indent=4, ensure_ascii=False)
        img_eff_section_len = struct.unpack('I', file_in.read(4))[0]
        for i in range(img_eff_section_len):
            arr = []
            arr.append(struct.unpack('I', file_in.read(4))[0])
            arr.append(struct.unpack('I', file_in.read(4))[0])
            arr.append(self._find_string_in_bytes(file_in.read(256)))  # 260?..
            arr.append(struct.unpack('I', file_in.read(4))[0])
            img_eff_section.append(arr)
        file_out.write("\n#IMAGE_EFFECTS:\n")
        dummy_img_eff_section = copy.deepcopy(img_eff_section)
        for i in range(len(dummy_img_eff_section)):
            dummy_img_eff_section[i][1] = '<IMAGE_EFFECT_OFFSET>'
        json.dump(dummy_img_eff_section, file_out, indent=4, ensure_ascii=False)
        img_ev_section_len = struct.unpack('I', file_in.read(4))[0]
        for i in range(img_ev_section_len):
            arr = []
            arr.append(struct.unpack('I', file_in.read(4))[0])
            arr.append(struct.unpack('I', file_in.read(4))[0])
            arr.append(self._find_string_in_bytes(file_in.read(256)))  # 260?..
            arr.append(struct.unpack('I', file_in.read(4))[0])
            img_ev_section.append(arr)
        file_out.write("\n#IMAGE_EVENTS:\n")
        json.dump(img_ev_section, file_out, indent=4, ensure_ascii=False)

        file_out.write("\n#CODE:\n")
        code_beginning = file_in.tell()
        if (self._test_mode):
            print(code_beginning)

        superanalysis = False
        if superanalysis:
            file_out.write("\n#ALL_GARANTEE_COMMANDS:\n")
            posser = []
            # possibler = ['03', '05', '06', '07', '0c', '0e', '0f', '15', '16', '1a',
            #             '1c', '1d', '20', '21', '23', '25', '28', '2a', '2b', '33',
            #             '36', '3a', '3c', '3d', '41', '42', '43', '44', '45', '48']
            possibler = []
            for i in self._code_lib.command_library:
                possibler.append(i[0])
            for i in event_section:
                file_in.seek(i[1] + code_beginning)
                new_byte = file_in.read(1).hex(' ')
                while (new_byte in possibler):
                    if (new_byte == ''):
                        break
                    command_number = self._code_lib.find_command_index(bytes.fromhex(new_byte))
                    # self._dissasemble_command_args(file_in, 'S')
                    self._dissasemble_command_args(file_in,
                                                   self._code_lib.command_library[command_number][1])
                    new_byte = file_in.read(1).hex(' ')
                file_in.seek(-1, 1)
                file_out.write(file_in.read(20).hex(' '))
                file_out.write('\n')
                try:
                    posser.index(new_byte)
                except:
                    posser.append(new_byte)
            posser.sort()
            file_out.write("\n#POSSIBLE_COMMANDS:\n")
            posser.sort()
            json.dump(posser, file_out, indent=4, ensure_ascii=False)
            file_in.close()
            exit()

        event_section.sort(key=lambda file: file[1])  # #2
        event_count = 0
        img_eff_section.sort(key=lambda file: file[1])  # #3
        img_eff_count = 0
        jump_section = []
        jump_find_section = []
        if (not (self._test_mode)):
            jump_section = self._get_zero_jump_section(file_in)
            jump_find_section = jump_section.copy()
        file_in.seek(code_beginning)
        jump_section.sort()
        jump_count = 0
        is_match = True

        # Спецсчётчики.
        while True:
            current_pos = file_in.tell()
            code_pos = current_pos - code_beginning

            # Анализ на начало чего-то.
            if (len(event_section) > 0):
                while (code_pos == event_section[0][1]):  # Событие.
                    file_out.write('#2: ' + str(event_count) + ' ' + event_section[0][0] + '\n')
                    event_section.pop(0)
                    event_count += 1
                    if (len(event_section) == 0):
                        break
            if (len(img_eff_section) > 0):
                while (code_pos == img_eff_section[0][1]):  # Визуальный эффект.
                    file_out.write('#3: ' + str(img_eff_count) + ' ' + img_eff_section[0][2] + ' ' + str(
                        img_eff_section[0][0]) + '\n')
                    img_eff_count += 1
                    img_eff_section.pop(0)
                    if (len(img_eff_section) == 0):
                        break
            if (len(jump_section) > 0):
                if (code_pos == jump_section[0]):  # Прыжок.
                    file_out.write('#4: ' + str(jump_count) + '\n')
                    jump_count += 1
                    jump_section.pop(0)
            # Основная часть.
            command_bytes = file_in.read(1)
            if (command_bytes == b''):
                break
            command_number = self._code_lib.find_command_index(command_bytes)

            if (command_number == -1):
                if (is_match):
                    file_out.write("#0:")
                is_match = False
                file_out.write(" " + self._code_lib.to_fully_hex(command_bytes[0:1]))
                continue

            if (not (is_match)):
                file_out.write('\n')
                is_match = True
            file_out.write("#1: ")

            command_arr = self._get_command_arr(file_in, command_number)
            json.dump(command_arr, file_out, ensure_ascii=False)

            if (self._test_mode):
                file_out.write(" " + str(current_pos) + " " + str(code_pos))
            file_out.write("\n")
            arguments = \
                self._dissasemble_command_args(file_in,
                                               self._code_lib.command_library[command_number][1])
            if ((self._code_lib.command_library[command_number][0] == '15') or
                    (self._code_lib.command_library[command_number][0] == '16')):
                arguments[0] = '<MESSAGE_NUMBER>'
            elif (self._code_lib.command_library[command_number][0] == '28'):
                arguments[0] = '<COUNT>'
            elif (self._code_lib.command_library[command_number][0] == '19'):
                arguments[0] = '*' + str(jump_find_section.index(arguments[0]))

            json.dump(arguments, file_out, ensure_ascii=False, indent=4)
            file_out.write('\n')

        print("Некорректно неиспользуемые события\Incorrectly unused events:", len(event_section))
        for i in event_section:
            print(i)
        print("Некорректно неиспользованные эффекты\Incorrectly unused effects:", len(img_eff_section))
        for i in img_eff_section:
            print(i, img_eff_count, i[2], i[0])
            img_eff_count += 1
        print("Некорректно неиспользованные метки\Incorrectly unused labels:", len(jump_section))
        for i in jump_section:
            print(i, jump_count)
            jump_count += 1

        file_in.close()
        file_out.close()

    def _get_zero_jump_section(self, file_in):
        file_in.seek(388, 0)

        ev_section_len = struct.unpack('I', file_in.read(4))[0]
        for i in range(ev_section_len):
            file_in.read(68)
        var_section_len = struct.unpack('I', file_in.read(4))[0]
        for i in range(var_section_len):
            file_in.read(68)
        img_eff_section_len = struct.unpack('I', file_in.read(4))[0]
        for i in range(img_eff_section_len):
            file_in.read(268)
        img_ev_section_len = struct.unpack('I', file_in.read(4))[0]
        for i in range(img_ev_section_len):
            file_in.read(268)

        jump_section = []

        # Спецсчётчики.
        while True:
            command_bytes = file_in.read(1)
            if (command_bytes == b''):
                break
            command_number = self._code_lib.find_command_index(command_bytes)

            if (command_number == -1):
                continue

            arguments = \
                self._dissasemble_command_args(file_in,
                                               self._code_lib.command_library[command_number][1])
            if (self._code_lib.command_library[command_number][0] == '19'):
                new_jump = arguments[0]
                if (not (new_jump in jump_section)):
                    jump_section.append(new_jump)

        jump_section.sort()
        return jump_section

    def _decompile_main(self, outer, mode):
        filer = self._main_lib.copy()
        eventer = self._ev_lib.copy()
        new_eventer = []
        effer = []
        label_lib = []
        label_new_lib = []
        if (self._version >= 3):
            new_eventer = self._new_ev_lib.copy()
            new_eventer.sort(key=lambda file: file[1])
            if (not (self._test_mode)):
                label_lib = self._get_label_lib()
                label_new_lib = label_lib.copy()
                label_new_lib.sort()
        if (self._version >= 4):
            effer = self._eff_lib.copy()
            effer.sort(key=lambda file: file[1])
        filer.sort(key=lambda file: file[0])

        is_match = True

        file_in = open(os.path.join(self._dir, "{}.sd".format(self._base_name)), 'rb')
        if (mode == 0):
            file_out = open(outer, 'w', encoding=self._encoding)
        else:
            file_out = open(os.path.join(outer, "__boot.txt"), 'w', encoding=self._encoding)
        while True:
            current_pos = file_in.tell()

            # Анализ на начало чего-то.
            test = 0
            while (test < len(eventer)):
                if (current_pos == eventer[test][1]):
                    if (not (is_match)):
                        is_match = True
                        file_out.write('\n')
                    file_out.write("#2: " + eventer[test][0] + "\n")
                    eventer.pop(test)
                elif (eventer[test][1] > current_pos):
                    break
                else:
                    test += 1
            if (self._version >= 3):
                test = 0
                while (test < len(new_eventer)):
                    if (current_pos == new_eventer[test][1]):
                        if (not (is_match)):
                            is_match = True
                            file_out.write('\n')
                        file_out.write("#3: " + new_eventer[test][0] + "\n")
                        new_eventer.pop(test)
                    elif (new_eventer[test][1] > current_pos):
                        break
                    else:
                        test += 1
                for test in range(len(label_new_lib)):
                    if (current_pos < label_new_lib[test]):
                        break
                    elif (current_pos == label_new_lib[test]):
                        if (not (is_match)):
                            is_match = True
                            file_out.write('\n')
                        file_out.write("#4: " + str(label_lib.index(label_new_lib[test])) + "\n")
                        label_new_lib.pop(test)
                        break
                if ((self._version >= 4) and (len(effer) > 0)):
                    if (current_pos == effer[0][1]):
                        if (not (is_match)):
                            is_match = True
                            file_out.write('\n')
                        file_out.write("#5: " + effer[0][0])
                        file_out.write('\n')
                        effer.pop(0)
            test = 0
            while (test < len(filer)):
                if (current_pos == filer[test][0]):
                    if (not (is_match)):
                        is_match = True
                        file_out.write('\n')
                    if (mode == 0):
                        file_out.write("##: " + filer[test][1][0] + " at " + filer[test][1][1] + "\n")
                    else:
                        file_out.close()
                        file_out = open(os.path.join(outer, filer[test][1][1]), 'a', encoding=self._encoding)
                        file_out.write("##: " + filer[test][1][0] + "\n")
                    filer.pop(test)
                elif (filer[test][0] > current_pos):
                    break
                else:
                    test += 1

            command_byte = file_in.read(1)
            if (command_byte == b''):
                break
            command_number = self._code_lib.find_command_index(command_byte)

            if (command_number == -1):
                if (is_match):
                    file_out.write("#0:")
                is_match = False
                file_out.write(" " + self._code_lib.to_fully_hex(command_byte))
                continue

            if (not (is_match)):
                file_out.write('\n')
                is_match = True
            file_out.write("#1: ")

            command_arr = self._get_command_arr(file_in, command_number)
            json.dump(command_arr, file_out, ensure_ascii=False)

            if (self._test_mode):
                file_out.write(" " + str(current_pos))
            file_out.write("\n")
            arguments = \
                self._dissasemble_command_args(file_in,
                                               self._code_lib.command_library[command_number][1])
            if (self._code_lib.command_library[command_number][2] == 'MESSAGE'):
                arguments[0] = '*'
                arguments[1] = '**'
            elif (self._code_lib.command_library[command_number][2] == 'CHOICE'):
                arguments[0] = '*'
            if (self._version >= 3):
                if ((self._code_lib.command_library[command_number][2] == 'JUMP') and (not (self._test_mode))):
                    arguments[0] = '*' + str(label_lib.index(arguments[0]))
            json.dump(arguments, file_out, ensure_ascii=False, indent=4)
            file_out.write('\n')
        file_in.close()
        file_out.close()

        print("Некорректно неиспользуемые файлы:/Incorrectly unused files:")
        for i in filer:
            print(i)
        print("Некорректно неиспользуемые события:/Incorrectly unused events:")
        for i in eventer:
            print(i)
        if (self._version >= 3):
            print("Некорректно неиспользуемые новособытия:/Incorrectly unused neoevents:")
            for i in new_eventer:
                print(i)
        print("Некорректно неиспользуемые эффекты:/Incorrectly unused effects:")
        for i in effer:
            print(i)

    def _decompile_var(self, outer, mode):
        out_dir = outer
        if (mode == 0):
            out_dir = os.path.split(outer)[0]
        out_file = open(os.path.join(out_dir, "__var_lib.txt"), 'w', encoding=self._encoding)
        out_file.write("##VARIABLES DATA:\n")
        json.dump(self._var_lib, out_file, indent=4, ensure_ascii=False)
        out_file.close()

    def _decompile_rest(self, outer, mode):
        out_dir = outer
        if (mode == 0):
            out_dir = os.path.split(outer)[0]

        out_file = open(os.path.join(out_dir, "__{}_order.txt".format(self._base_name)), 'w', encoding=self._encoding)
        out_file.write("##{}.LIB NAMES ORDER:\n".format(self._base_name.upper()))
        aspar = []
        for i in self._main_lib:
            arr = []
            arr.append(i[1][0])
            arr.append(i[1][1])
            aspar.append(arr)
        json.dump(aspar, out_file, indent=4, ensure_ascii=False)
        aspar.clear()
        out_file.close()

        in_file = open(os.path.join(self._dir, "{}.sfn".format(self._base_name)), 'rb')
        out_file = open(os.path.join(out_dir, "__{}_sfn.txt".format(self._base_name)), 'w', encoding=self._encoding)
        out_file.write("##DATA FROM {}.SFN SECTION:\n".format(self._base_name.upper()))
        current_bytes = in_file.read(64)
        while (current_bytes != b''):
            aspar.append(self._find_string_in_bytes(current_bytes))
            current_bytes = in_file.read(64)
        in_file.close()
        json.dump(aspar, out_file, indent=4, ensure_ascii=False)
        out_file.close()
        aspar.clear()

        if ((self._version == 1) or (self._version == 2)):
            in_file = open(os.path.join(self._dir, "{}.cg".format(self._base_name)), 'rb')
            out_file = open(os.path.join(out_dir, "__{}_cg.txt".format(self._base_name)), 'w', encoding=self._encoding)
            out_file.write("##DATA FROM {}.CG SECTION:\n".format(self._base_name.upper()))
            current_bytes = in_file.read(4)
            while (current_bytes != b''):
                aspar.append(struct.unpack('i', current_bytes)[0])
                current_bytes = in_file.read(4)
            in_file.close()
            json.dump(aspar, out_file, indent=4, ensure_ascii=False)
            out_file.close()

    # Новые технические функции для декомпиляции в NEW.
    def _get_label_lib(self):
        label_lib = []

        file_in = open(os.path.join(self._dir, "{}.sd".format(self._base_name)), 'rb')
        while True:
            current_pos = file_in.tell()

            command_byte = file_in.read(1)
            if (command_byte == b''):
                break
            command_number = self._code_lib.find_command_index(command_byte)
            if (command_number == -1):
                continue

            command_arr = self._get_command_arr(file_in, command_number)
            arguments = \
                self._dissasemble_command_args(file_in,
                                               self._code_lib.command_library[command_number][1])
            if (self._code_lib.command_library[command_number][2] == 'JUMP'):
                try:
                    label_lib.index(arguments[0])
                except:
                    label_lib.append(arguments[0])
        file_in.close()
        return label_lib

    def _get_command_arr(self, file_in, command_number):
        command_arr = []
        command_arr.append(self._code_lib.get_true_name(command_number))
        for i in self._code_lib.postcommand_data:
            command_arr.append(struct.unpack(i, file_in.read(
                self._code_lib.get_len_from_stucture(i)))[0])
        return command_arr

    def _dissasemble_command_args(self, file_in, comm_stru):
        arguments = []
        grouper = 1
        grouper_flag = False
        for k in comm_stru:
            if (k.upper() == 'B'):
                val = self._diss_group_magic(self._get_B, [file_in, k], grouper, grouper_flag)
                arguments.append(val)
            elif (k.upper() == 'H'):
                val = self._diss_group_magic(self._get_H, [file_in, k], grouper, grouper_flag)
                arguments.append(val)
            elif (k.upper() == 'I'):
                val = self._diss_group_magic(self._get_I, [file_in, k], grouper, grouper_flag)
                arguments.append(val)
            elif (k == 'S'):
                val = self._diss_group_magic(self._get_S, [file_in], grouper, grouper_flag)
                arguments.append(val)
            elif (k == 's'):
                val = self._diss_group_magic(self._get_s, [file_in], grouper, grouper_flag)
                arguments.append(val)
            elif (k == 'G'):
                grouper = self._get_G(file_in, k)
                grouper_flag = True
            elif (k == 'g'):
                grouper = self._get_g(file_in, k)
                grouper_flag = True
            elif (k == 'N'):
                grouper_flag = False
            elif (k == 'M'):
                val = self._diss_group_magic(self._get_M, [file_in], grouper, grouper_flag)
                arguments.append(val)
            elif (k == 'R'):
                val = self._diss_group_magic(self._get_R, [file_in], grouper, grouper_flag)
                arguments.append(val)
            elif (k == 'Z'):
                val = self._diss_group_magic(self._get_Z, [file_in], grouper, grouper_flag)
                arguments.append(val)
        return arguments

    def _diss_group_magic(self, func, args, grouper, grouper_flag):
        if (grouper_flag):
            new = []
            new.append(self._group_start)
            for f in range(grouper):
                new.append(self._get_val_from_n_arg(func, args))
            return new
        else:
            return self._get_val_from_n_arg(func, args)

    def _get_val_from_n_arg(self, func, args):
        checker = 1
        if_get_spec = False
        try:
            str(func).index('<bound method SLG_Scripts_NEW._set_M')
            # if_get_M = True
            if_get_spec = True
        except:
            pass
        try:  # !!!
            str(func).index('<bound method SLG_Scripts_NEW._set_R')
            if_get_spec = True
        except:
            pass
        if ((isinstance(args, list)) and (not (if_get_spec))):
            checker = len(args)
            neo = args[0]
        else:
            neo = args
        if (checker == 0):
            return func()
        elif (checker == 1):
            return func(neo)
        elif (checker == 2):
            return func(args[0], args[1])
        elif (checker == 3):
            return func(args[0], args[1], args[2])
        else:
            raise AttributeError("Неподдерживаемое число аргументов:", checker, len(args))

    def _get_code_lib_from_version(self):
        if (self._version == 0):
            return SLG_Command_lib_ver0()
        if (self._version == 1):
            return SLG_Command_lib_ver1()
        elif (self._version == 2):
            return SLG_Command_lib_ver2()
        elif (self._version == 3.0):
            return SLG_Command_lib_ver3_0()
        elif (self._version == 3.1):
            return SLG_Command_lib_ver3_1()
        elif (self._version == 4.0):
            return SLG_Command_lib_ver4_0()
        elif (self._version == 4.1):
            return SLG_Command_lib_ver4_1()
        else:
            return SLG_Command_lib()

    # Отдельные файловые технические функции.
    def _set_compile_order(self, outer):
        filer = self._main_lib.copy()
        filer.sort(key=lambda file: file[0])
        file_out = open(os.path.join(outer, "__compile_order.txt"), 'w', encoding=self._encoding)
        file_out.write("##COMPILATION_ORDER:\n")
        newf = []
        for i in filer:
            newf.append(i[1])
        json.dump(newf, file_out, indent=4, ensure_ascii=False)
        file_out.close()

    def _create_files(self, out_dir):
        # А здесь де-факто... И совпадения есть не всегда...
        for i in self._main_lib:
            file_name = os.path.join(out_dir, i[1][1])
            full_name = file_name.split(os.sep)
            full_name.pop(-1)
            dirs_name = ''
            for k in full_name:
                dirs_name += k
                dirs_name += os.sep
            if (dirs_name != ''):
                os.makedirs(dirs_name, exist_ok=True)
            file_out = open(file_name, 'w', encoding=self._encoding)
            file_out.close()

    def _set_nominal_sizes(self, outer, mode):
        out_dir = outer
        if (mode == 0):
            out_dir = os.path.split(outer)[0]
        need_to_resize = []
        if ((int(self._version) == 1) or (int(self._version) == 2)):
            need_to_resize = ["{}.cg", "{}.lb", "{}.sw", "{}.tko", "{}.ev"]
        elif (int(self._version) == 3):
            need_to_resize = ["{}.bl", "{}.lb", "{}.sw", "{}.tko", "{}.ev"]
        elif (int(self._version) == 4):
            need_to_resize = ["{}.lb", "{}.sb", "{}.tko", "{}.ev"]
        for i in need_to_resize:
            i = i.format(self._base_name)
            self._nominal_size[i] = os.path.getsize(os.path.join(self._dir, i))
        out_file = open(os.path.join(out_dir, "__nominal_size.txt"), 'w', encoding=self._encoding)
        out_file.write("##NOMINAL SIZES OF HARD SIZED SECTIONS:\n")
        artas = []
        for i in self._nominal_size:
            arr = []
            arr.append(i)
            arr.append(self._nominal_size[i])
            artas.append(arr)
            del arr
        json.dump(artas, out_file, indent=4, ensure_ascii=False)
        out_file.close()
        del artas

    # Технические функции распаковки структур.
    def _get_B(self, file_in, i):
        dummy = struct.unpack(i, file_in.read(1))[0]
        return dummy

    def _get_H(self, file_in, i):
        dummy = struct.unpack(i, file_in.read(2))[0]
        return dummy

    def _get_I(self, file_in, i):
        dummy = struct.unpack(i, file_in.read(4))[0]
        return dummy

    def _get_S(self, file_in):
        symb = file_in.read(1)
        byte_str = b''
        while (symb != b'\x00'):
            byte_str += symb
            symb = file_in.read(1)
        dummy = byte_str.decode(self._encoding)
        assert symb == b'\x00', "IMPOSSIBLE STRING CLOSING ON " + str(file_in.tell()) + "!"
        return dummy

    def _get_s(self, file_in):
        lens = struct.unpack('B', file_in.read(1))[0]
        dummy = file_in.read(lens).decode(self._encoding)
        assert file_in.read(1) == b'\x00', \
            "IMPOSSIBLE sTRING CLOSING ON " + str(file_in.tell()) + "!"
        return dummy

    def _get_G(self, file_in, i):
        grouper = struct.unpack('I', file_in.read(4))[0]
        return grouper

    def _get_g(self, file_in, i):
        grouper = struct.unpack('B', file_in.read(1))[0]
        return grouper

    def _get_Z(self, file_in):
        dummy = []
        struct_num = self._code_lib.find_struct_index(file_in)

        if (struct_num == -1):
            new_byte = file_in.read(1)
            command_num = self._code_lib.find_command_index(new_byte)
            if (command_num == -1):
                file_in.seek(-1, 1)
                print("Z STRUCT UNRESOLVED BUG!!! " +
                      str(file_in.tell()) + "| " + file_in.read(32).hex(' '))
                file_in.close()
                sys.exit()
            else:
                dummy.append(self._struct_command)
                command_arr = self._get_command_arr(file_in, command_num)
                dummy.append(command_arr)
                dummy.append(self._dissasemble_command_args(file_in,
                                                            self._code_lib.command_library[command_num][1]))
            # dummy.append(self._struct_terminate)
            # sys.exit()
        else:
            dummy.append(self._struct_normal)
            dummy.append(self._code_lib.structs_library[struct_num][0])
            dummy.append(self._dissasemble_command_args(file_in,
                                                        self._code_lib.structs_library[struct_num][1]))
        return dummy

    def _get_M(self, file_in):
        dummy = []
        dummy.append(self._get_S(file_in))
        dummy.append(self._get_B(file_in, 'B'))
        dummy.append(self._get_H(file_in, 'H'))
        dummy.append(self._get_I(file_in, 'i'))
        dummy.append(self._get_I(file_in, 'i'))
        return dummy

    def _get_R(self, file_in):
        dummy = []
        dummy.append(self._get_I(file_in, 'I'))
        dummy.append(self._get_Z(file_in))
        return dummy

    # Прочие технические функции.
    def _chk_script_files(self):
        files = os.listdir(self._dir)
        if (files != ['main.cg', 'main.ev', 'main.lb', 'main.lbn', 'main.sd', 'main.sfn', 'main.sw', 'main.swn',
                      'main.tko']):
            raise SLG_ScriptsError("Not a Sengokuhime's script!")

    def _find_string_in_bytes(self, byter):
        limiter = 0
        if (len(byter) == 0):
            return ''
        try:
            while (byter[limiter] != 0):
                limiter += 1
                if (limiter >= len(byter)):
                    break
        except:
            print(byter.hex(' '))
            exit()
        return byter[:limiter].decode(self._encoding)

    def _get_string_to_bytes(self, string, byte_num):
        byter = string.encode(self._encoding)
        byter += bytes(byte_num - len(byter))
        return byter
