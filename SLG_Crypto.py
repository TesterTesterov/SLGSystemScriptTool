import struct
import time


class SLG_Crypto:
    common_script_attacks = ((2, 0, 0, 2, 0),
                             (2, 0, 2, 0, 0),
                             (2, 2, 0, 0, 0),
                             (2, 0, 0, 0, 0),
                             (2, 0, 0, 0, 2))
    basic_keys = ([0xbf8766f5, 'Sengoku Hime 5, 6'],
                  [0xca92f12b, 'Sengoku Hime 4'],
                  [0x08461c4d, 'Sengoku Hime 4 Trial'],
                  [0x3e9f9d19, 'Sangoku Hime 2'],
                  [0x5e950de7, 'Sangoku Hime 2 Trial'],
                  [0x00501e37, 'Sangoku Hime 1 Renewal (!)'])  # !

    # Инициализаторы.
    def __init__(self, script, typer, mode, key):
        self._script = ''
        self.set_script(script)
        self._type = []
        self.set_type(typer)
        self._mode = -1
        self.set_mode(mode)
        # 0 -- остановиться, 1 -- продожить.
        self._key = 0
        self.set_key(key)

        self._known_keys = self._get_known_keys()

    # Связь с пользователем.
    ##Установщики.
    def set_script(self, new_script):
        self._script = new_script

    def set_type(self, new_type):
        if (str(type(new_type)) == "<class 'list'>"):
            self._type = tuple(self._type)
        if (str(type(new_type)) != "<class 'tuple'>"):
            self._type = self.common_script_attacks[0]
            return False
        self._type = new_type
        return True

    def set_mode(self, new_mode):
        if ((new_mode != 1) and (new_mode != 0)):
            self._mode = 0
            return False
        else:
            self._mode = new_mode
            return True

    def set_key(self, new_key):
        self._key = new_key

    ##Получальщики.
    def get_script(self):
        return self._script

    def get_type(self):
        return self._type

    def get_mode(self):
        return self._mode

    def get_key(self):
        return self._key

    @staticmethod
    def _get_known_keys():
        zlo = []
        for i in SLG_Crypto.basic_keys:
            zlo.append(i)
        try:
            new_file = open('known_user_keys.txt', 'r')
            keyers = new_file.readlines()
            barada = []
            for i in range(len(keyers)):
                if ((i % 2) == 0):
                    barada.append(int(keyers[i][2:], 16))
                else:
                    barada.append(keyers[i])
                    zlo.append(barada)
                    barada.clear()
        except FileNotFoundError:
            new_file = open('known_user_keys.txt', 'w')
            new_file.close()
        except Exception as ex:
            print(ex)
        zlo = tuple(zlo)
        return zlo

    ##Связисты с техметодами.
    def attack(self, txt_file, mode):  # 0 -- script, 1 -- dat.
        is_found = False
        start_key = 0
        file_output = open(txt_file, 'w')
        file_output.close()

        froms = []
        from_file = open(self._script, 'rb')
        for i in range(5):
            froms.append(from_file.read(1)[0])
        from_file.close()
        froms = tuple(froms)
        for i in self._known_keys:
            result = self._chk_sootv(i[0], froms, self._type, mode)
            if (result):
                is_found = True
                print(
                    "\n=== Найден стандартный ключ: " + hex(i[0]) + " к " + i[1] + ".\n=== Standart Key Found: " + hex(
                        i[0]) + ' to ' + i[1] + ".")
                file_output = open(txt_file, 'a')
                file_output.write(
                    "\n=== Найден стандартный ключ: " + hex(i[0]) + " к " + i[1] + ".\n=== Standart Key Found: " + hex(
                        i[0]) + ' to ' + i[1] + ".")
                self._key = result
                file_output.close()
                if (self._mode == 0):
                    print("\n=== Поиск прерван.\n=== Search Terminated.")
                    file_output = open(txt_file, 'a')
                    file_output.write("\n=== Поиск прерван.\n=== Search Terminated.")
                    file_output.close()
                    return is_found

        while (True):
            result = self._attack_new_key(start_key, mode)
            if (result == False):
                print("\n=== Поиск окончен.\n=== Search Complete.")
                file_output = open(txt_file, 'a')
                file_output.write("\n=== Поиск окончен.\n=== Search Complete.")
                file_output.close()
                break
            else:
                try:
                    print("\n=== Найден ключ: " + hex(result) + ".\n=== Key Found: " + hex(result) + ".")
                    file_output = open(txt_file, 'a')
                    file_output.write("\n=== Найден ключ: " + hex(result) + ".\n=== Key Found: " + hex(result) + ".")
                    self._key = result
                    file_output.close()
                    is_found = True
                except:
                    print("\n=== ПРОБЛЕМА! PROBLEM!", result)
                    file_output = open(txt_file, 'a')
                    file_output.write("\n=== ПРОБЛЕМА! PROBLEM!")
                    file_output.write(result)
                    file_output.close()
                    break
                if (self._mode == 0):
                    print("\n=== Поиск прерван.\n=== Search Terminated.")
                    file_output = open(txt_file, 'a')
                    file_output.write("\n=== Поиск прерван.\n=== Search Terminated.")
                    file_output.close()
                    is_found = True
                    break
                else:
                    start_key = result + 1
                    continue
        return is_found

    def decrypt(self, out_file, mode):
        if (mode == 0):
            self._decrypt_script(out_file)
        else:
            self._decrypt_dat(out_file)
        print('\n=== Успешно расшифровано!\n=== Successfully Decrypted!')

    def encrypt(self, out_file, mode):
        if (mode == 0):
            self._encrypt_script(out_file)
        else:
            self._encrypt_dat(out_file)
        print('\n=== Успешно зашифровано!\n=== Successfully Encrypted!')

    # Технические методы.
    def _attack_new_key(self, starter, mode):
        froms = []
        from_file = open(self._script, 'rb')
        for i in range(5):
            froms.append(from_file.read(1)[0])
        from_file.close()
        froms = tuple(froms)

        this_key = starter
        timer_zero = time.time()
        test_time_val = 10_000_000  # 10_000_000
        test_count = 0

        while (this_key < 0x100_000_000):
            if (((test_count % test_time_val) == 0) and (test_count != 0)):
                time_new = time.time()
                print(hex(this_key), time_new - timer_zero, 'Ключ ещё не найден.../Key still not found...')
                timer_zero = time_new

            result = self._chk_sootv(this_key, froms, self._type, mode)
            if (result):
                return this_key

            this_key += 1
            test_count += 1
        return False

    def _decrypt_script(self, out_file):
        this_key = self._key
        enc_file = open(self._script, 'rb')
        dec_file = open(out_file, 'wb')

        new_byte = enc_file.read(1)
        while (new_byte != b''):
            this_key = self._convert_key(this_key, 0)
            dec_file.write(struct.pack('B', new_byte[0] ^ (this_key % 256)))
            new_byte = enc_file.read(1)

        enc_file.close()
        dec_file.close()

    def _encrypt_script(self, out_file):
        self._decrypt_script(out_file)

    def _decrypt_dat(self, out_file):
        this_key = self._key
        enc_file = open(self._script, 'rb')
        dec_file = open(out_file, 'wb')

        new_byte = enc_file.read(1)
        while (new_byte != b''):
            this_key = self._convert_key(this_key, 1)
            dec_file.write(struct.pack('B', (new_byte[0] - (this_key >> 16)) & 0xff))
            new_byte = enc_file.read(1)

        enc_file.close()
        dec_file.close()

    def _encrypt_dat(self, out_file):
        this_key = self._key
        enc_file = open(self._script, 'rb')
        dec_file = open(out_file, 'wb')

        new_byte = enc_file.read(1)
        while (new_byte != b''):
            this_key = self._convert_key(this_key, 1)
            dec_file.write(struct.pack('B', (new_byte[0] + ((this_key >> 16) & 0xff)) % 256))
            new_byte = enc_file.read(1)

        enc_file.close()
        dec_file.close()

    # Подсобные техметоды.
    def _convert_key(self, key, mode):
        key *= 0x343fd
        key += 0x269ec3
        key &= 0xffffffff
        if (mode == 0):
            key >>= 16
            key &= 0x7fff
        return key

    def _chk_sootv(self, key, froms, toes, mode):
        if (len(froms) != len(toes)):
            raise TypeError("Некорректные длины!\nIncorrect lens!")
        rez = 0
        for i in range(len(froms)):
            key = self._convert_key(key, mode)
            if (mode == 0):
                rez = froms[i] ^ (key & 0xff)
            elif (mode == 2):
                rez = (froms[i] + (key >> 16)) & 0xff
            else:
                rez = (froms[i] - (key >> 16)) & 0xff
            if (rez == toes[i]):
                continue
            else:
                return False
        return True
