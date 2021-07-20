from SLG_Crypto import SLG_Crypto
from SLG_Scripts_NEW import SLG_Scripts_NEW
from SLGScriptTool_GUI import SLGScriptTool_GUI

import json
import os

test_mode = False

def main():
    #file1 = 'compiled_sengokuhime3\\main.sd'
    #file2 = 'scripts_library\\main_sengokuhime3\\main.sd'
    #file_one = open(file1, 'rb')
    #file_two = open(file2, 'rb')
    #while True:
    #
    #file_one.close()
    #file_two.close()
    #exit()
    new_GUI = SLGScriptTool_GUI()
    return True

#Здесь куча разных тестовых функций.
#Просто не обращайте на них внимания.
#Используются они в тестах и при разработке...
#Но удалять жалко.

def chksootv(if_size, version, game_name, base_name):
    dir1 = "{}_{}".format(base_name, game_name)
    dir2 = "compiled_{}_{}".format(base_name, game_name)
    files = ["{}.bl", "{}.sw", "{}.sb", "{}.sbn", "{}.snm", "{}.sfn", "{}.ev", "{}.tko", "{}.lb", "{}.lbn", "{}.sd"]
    if (version >= 3):
        files[0] = "{}.bl"
    for i in range(len(files)):
        files[i] = files[i].format(base_name)
    for i in files:
        filer1 = os.path.join(dir1, i)
        filer2 = os.path.join(dir2, i)
        size1 = os.path.getsize(filer1)
        size2 = os.path.getsize(filer2)
        if (if_size):
            if (size1 != size2):
                print('Size mismatch!', filer1, filer2, size1, size2)
                exit()
        file_one = open(filer1, 'rb')
        file_two = open(filer2, 'rb')
        while True:
            byte_one = file_one.read(1)
            byte_two = file_two.read(1)
            if (byte_one == b''):
                break
            if (byte_one[0] != byte_two[0]):
                print('Byte mismatch!', filer1, filer2, byte_one, byte_two, file_one.tell())
                file_one.close()
                file_two.close()
                exit()
        file_one.close()
        file_two.close()
    print("Test Success!")

def compare(filer1, filer2):
    print(filer1, filer2, 'CHECK!')
    file1 = open(filer1, 'rb')
    file2 = open(filer2, 'rb')

    while True:
        byte1 = file1.read(1)
        byte2 = file2.read(1)
        if (byte1 != byte2):
            print(file1.tell(), file2.tell())
            print('СКВЕРНО!\\INVALID!')
            exit()
        if ((byte1 == b'') and (byte2 == b'')):
            break
    print("СДОБНО!\\VALID!")
    file1.close()
    file2.close()

def special_crypto(in_dir, out_dir):
    all_files = []
    file_names = []
    for root, dirs, files in os.walk(in_dir):
        for name in files:
            all_files.append(name)
    for i in all_files:
        SengokuHimeCrypt = SLG_Crypto(os.path.join(in_dir, i), (2, 0, 0, 2, 0), 0, 0xbf8766f5)
        SengokuHimeCrypt.encrypt(os.path.join(out_dir, i), 0)
        del SengokuHimeCrypt
    #SengokuHimeCrypt = SLG_Crypto('-main;main.sd', (2, 0, 0, 2, 0), 0, -1)

if (__name__ == '__main__'):
    if (test_mode):
        #SengokuHime6 = SLG_Crypto("main;main.sd", (2, 0, 0, 2, 0), 0, -1)
        #SengokuHime6.attack("result.txt", 0)
        #exit()
        #files = ["main.sw", "main.snm", "main.sfn", "main.bl", "main.ev", "main.tko", "main.lb", "main.lbn", "main.sd", "main.sb", "main.sbn"]
        #for i in files:
        #    SangokuHime1 = SLG_Crypto('main;' + i, (2, 0, 0, 2, 0), 0, 0xbf8766f5)
        #    SangokuHime1.decrypt(i, 0)
        #    del SangokuHime1
        #exit()
        variant = 0
        variant2 = 0
        game_name = "Shihen69"
        decompile_name = "decompile_Shihen69"
        #game_ver = 4.2
        game_ver =  0
        encoding = 'cp932'
        #base_name = 'main'
        #base_name = 'event000_0.sd'
        base_name = 'sys.sd'
        all_files = []
        if (True):
            mode = 1
            if (mode == 0):
                for root, dirs, files in os.walk(game_name):
                    for name in files:
                        new_file = os.path.join(root, name)
                        print(new_file)
                        base_name = new_file[len(game_name)+1:]
                        print(base_name)
                        all_files.append(os.path.join(root, name))
                        Shihen69 = SLG_Scripts_NEW(game_name, base_name, encoding, game_ver)
                        Shihen69.decompile('decompile_' + game_name + '\{}'.format(base_name.replace('.sd', '.txt')), 0)
            else:
                for root, dirs, files in os.walk(decompile_name):
                    for name in files:
                        new_file = os.path.join(root, name)
                        base_name = new_file[len(decompile_name)+1:]
                        all_files.append(os.path.join(root, name))
                        print(os.path.join('compile_' + game_name, base_name.replace('txt', 'sd')), 'decompile_' + game_name + '\{}'.format(base_name.replace('.sd', '.txt')))
                        Shihen69 = SLG_Scripts_NEW(os.path.join('compile_' + game_name, base_name.replace('txt', 'sd')), base_name, encoding, game_ver)
                        Shihen69.compile('decompile_' + game_name + '\{}'.format(base_name.replace('.sd', '.txt')), 0)
                        #compare(os.path.join('compile_' + game_name, base_name.replace('txt', 'sd')), game_name + '\{}'.format(base_name.replace('.txt', '.sd')))
            exit()

        if (variant == 0):
            if (variant2 == 0):
                Sengokuhime1 = SLG_Scripts_NEW(game_name, base_name, encoding, game_ver)
                Sengokuhime1.decompile('decompile_' + game_name + '\{}.txt'.format(base_name), 0)
        #    else:
        #        Sengokuhime1 = SLG_Scripts_NEW('{}_'.format(base_name) + game_name, base_name, encoding, game_ver)
        #        Sengokuhime1.decompile('2decompile_' + game_name, 1)
        #else:
        #    if (variant2 == 0):
        #        Sengokuhime1 = SLG_Scripts_NEW('compiled_{}_'.format(base_name) + game_name, base_name, encoding, game_ver)
        #        Sengokuhime1.compile('decompile_' + game_name + '\{}.txt'.format(base_name), 0)
        #    else:
        #        Sengokuhime1 = SLG_Scripts_NEW('2compiled_{}_'.format(base_name) + game_name, base_name, encoding, game_ver)
        #        Sengokuhime1.compile('2decompile_' + game_name, 1)
        #chksootv(True, game_ver, game_name, base_name)
        #special_crypto('2compiled_{}_'.format(base_name) + game_name,
        #               "C:\\Users\\Александр\\Desktop\\Tester\\SLGSystemDataTool"
        #               "\\build\\SLGSystemDataTool 1.0\\script\\main")

        #json_string = '[1, 2, "3", [4, 5, "6"]]'
        #zlo = json.loads(json_string)
        #print(zlo[3][2])

        #SengokuHime4 = SLG_Crypto('-main;main.sd', (2, 0, 0, 2, 0), 0, -1)
        #SengokuHime4.attack('result.txt', 1)
        #SengokuHime4.decrypt('-super-main.sd', 1)
        #del SengokuHime4
    else:
        if (main()):
            print("Успешно завершено!/Successfully finished!")
        else:
            print("Неудачно завершено!/Incorrectly finished!")