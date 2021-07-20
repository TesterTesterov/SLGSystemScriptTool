import locale
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ctypes
import threading
import codecs

from SLG_Crypto import SLG_Crypto
from SLG_Scripts_NEW import SLG_Scripts_NEW


class SLGScriptTool_GUI:
    top_name_lib = {
        "eng": "SLGSystemScriptTool by Tester",
        "rus": "SLGSystemScriptTool от Tester-а"
    }
    strings_lib = {
        "eng": (
            "РУССКИЙ",
            "ENGLISH",

            "Main Section",
            "Crypto Module",
            "0-Version Script",
            "1+ Versions Scripts"
        ),
        "rus": (
            "РУССКИЙ",
            "ENGLISH",

            "Главный раздел",
            "Криптомодуль",
            "Скрипт версии 0",
            "Скрипты версий 1+"
        )
    }
    _top_relief_lib = {
        "eng": (
            tk.RAISED,
            tk.SUNKEN
        ),
        "rus": (
            tk.SUNKEN,
            tk.RAISED
        )
    }

    def __init__(self):
        self._window = tk.Tk()
        self._width = 600
        self._height = 400

        self._lang = self._define_language()
        self._current_panel = 0
        self._window.geometry('{}x{}+{}+{}'.format(
            self._width,
            self._height,
            self._window.winfo_screenwidth() // 2 - self._width // 2,
            self._window.winfo_screenheight() // 2 - self._height // 2))
        self._window.resizable(width=False, height=False)
        self._window["bg"] = 'grey'

        self._top_buttons = []
        self._top_buttons.append(tk.Button(master=self._window,
                                           command=self.to_Russian,
                                           relief=tk.RAISED,
                                           font=('Helvetica', 14)))
        self._top_buttons.append(tk.Button(master=self._window,
                                           command=self.to_English,
                                           relief=tk.RAISED,
                                           font=('Helvetica', 14)))
        self._top_buttons[0].place(relx=0.0, rely=0.0, relwidth=0.5, relheight=0.1)
        self._top_buttons[1].place(relx=0.5, rely=0.0, relwidth=0.5, relheight=0.1)

        self._razdel_button = []
        for i in range(4):
            self._razdel_button.append(tk.Button(master=self._window,
                                                 relief=tk.RAISED,
                                                 borderwidth=8,
                                                 font=('Helvetica', 12)))
            self._razdel_button[i].place(relx=0.025 + (0.5 * (i % 2)), rely=0.1125 * (int(not (i < 2)) + 1),
                                         relwidth=0.45, relheight=0.1)
            # self._razdel_button[i]["text"] = str(i) #Сие для тестов.
        self._razdel_button[0]["command"] = self.to_zero_panel
        self._razdel_button[1]["command"] = self.to_first_panel
        self._razdel_button[2]["command"] = self.to_second_panel
        self._razdel_button[3]["command"] = self.to_third_panel

        self._frame = []
        self._frame.append(SLG_MainFrame(self._window))
        self._frame.append(SLG_CryptoFrame(self._window))
        self._frame.append(SLG_ScriptZeroFrame(self._window))
        self._frame.append(SLG_ScriptLaterFrame(self._window))

        self._change_language()
        self._change_frame()
        self._window.mainloop()

    def to_zero_panel(self):
        self._current_panel = 0
        self._change_frame()

    def to_first_panel(self):
        self._current_panel = 1
        self._change_frame()

    def to_second_panel(self):
        self._current_panel = 2
        self._change_frame()

    def to_third_panel(self):
        self._current_panel = 3
        self._change_frame()

    def _change_frame(self):
        for i in range(len(self._frame)):
            if (i == self._current_panel):
                self._frame[i].place(relx=0.025, rely=0.35, relwidth=0.95, relheight=0.635)
                self._razdel_button[i]["relief"] = tk.SUNKEN
                self._razdel_button[i]["state"] = tk.DISABLED
            else:
                self._frame[i].place_forget()
                self._razdel_button[i]["relief"] = tk.RAISED
                self._razdel_button[i]["state"] = tk.NORMAL

    def to_Russian(self):
        self._lang = 'rus'
        self._change_language()

    def to_English(self):
        self._lang = 'eng'
        self._change_language()

    def _change_language(self):
        failer = True
        for i in self.strings_lib:
            if (self._lang == i):
                failer = False
        if (failer):
            print("Verily, sorry I am!\nThis language is not supportred!")
            self._lang = 'eng'
        for i in range(len(self._top_buttons)):  # 2
            self._top_buttons[i]["text"] = self.strings_lib[self._lang][i]  # 0, 1.
            self._top_buttons[i]["relief"] = self._top_relief_lib[self._lang][i]
        for i in range(len(self._frame)):  # 4
            self._razdel_button[i]["text"] = self.strings_lib[self._lang][i + 2]  # 2, 3, 4, 5.
            self._frame[i].translate_to(self._lang)
        self._window.title(self.top_name_lib[self._lang])

    def _define_language(self):
        is_rus = False
        windll = ctypes.windll.kernel32
        superlocale = locale.windows_locale[windll.GetUserDefaultUILanguage()][:2]
        if (superlocale == 'ru'):
            is_rus = True
        elif (superlocale == 'uk'):
            is_rus = True
        elif (superlocale == 'sr'):
            is_rus = True
        elif (superlocale == 'bg'):
            is_rus = True
        elif (superlocale == 'kk'):
            is_rus = True
        elif (superlocale == 'be'):
            is_rus = True
        elif (superlocale == 'hy'):
            is_rus = True
        elif (superlocale == 'az'):
            is_rus = True

        if (is_rus):
            return 'rus'
        else:
            return 'eng'

    @staticmethod
    def show_message(self, title, message):
        messagebox.showinfo(title, message)


class SLG_MasterFrame(tk.Frame):
    strings_lib = {
        'eng': ('none'),
        'rus': ('ничего')
    }

    def __init__(self, master):
        super(SLG_MasterFrame, self).__init__()
        self.master = master
        self["background"] = 'white'
        self["relief"] = tk.RAISED
        self["borderwidth"] = 5

    def translate_to_eng(self):
        self.translate_to('eng')

    def translate_to_rus(self):
        self.translate_to('rus')

    def translate_to(self, language):
        pass


class SLG_MainFrame(SLG_MasterFrame):
    strings_lib = {
        'eng': (
            'About SLG System',
            'About tool',
            'Game\'s versions',
            'Game\'s keys',
            'Help',
            '''SLG System Engine is not very popular, but also not very obsqure engine, used in Gesen 18 (may be not '''
            '''only whose) games. It's in fact some sort of modified Tenka Touitsu ADVANCE engine. There are a lot '''
            '''of good visual novels and jRPG's uses it, such as Sengoku Hime and Sankoku Hime series.\n\nOldest '''
            '''versions of it, such as Shihen 69's version or version "0", does use just a simple script .sd. Older '''
            '''versions does use multicomponent script from a group of files, that differ depending of the game '''
            '''version. The main file of it is .sd, but you cannot simply edit only one this file, because it will '''
            '''break offset-links between files and so the game won't run correctly. You need to edit all files '''
            '''synchronically and reflect changes in one file in others.\n\nSince third version of the engine (or '''
            '''even the latest games of second version) commonly use DRM and the scripts and files of supplement '''
            '''structures encryption.''',

            '''COMMMON DATA ABOUT THE TOOL.\n\n\n'''
            '''Dual languaged GUI tool for (de)compiling and (de/en)crypting (with key finding) scripts of SLG '''
            '''System engine. Supports all known versions of SLG System: 0, 1, 2, 3 (3.0, 3.1), 4 (4.0, 4.1), but '''
            '''may lack of support of some it's variations. If this tool does not support a game, write an "Issue" '''
            '''on github page with attached unsupported scripts and highlighting the game name. With this tool you '''
            '''can: decompile and compile script of SLG System, (en/de)crypt script of any game on SLG System, find '''
            '''key of any game on SLG System via cryptoattack.\n\nIt has following features:\n- Help module.\n- '''
            '''Crypto module (for (en/de)cryptions and cryptoattacks).\n- Scripts version 0 module (separate module '''
            '''because version 0 scripts are too different from the rest).\n- Script older versions module.\n\n> '''
            '''Tested with\n- Shihen 69 \~Shin'en no Messiah\~;\n- Sengoku Hime \~Ransei, Tenka Sanbun no Kei\~ '''
            '''Renewal;\n- Sengoku Hime \~Senran no Yo ni Honoo Tatsu\~;\n- Sengoku Hime 2 \~Senran no Yo, Gun'yuu '''
            '''Arashi no Gotoku\~;\n- Sengoku Hime 3 \~Tenka o Kirisaku Hikari to Kage\~;\n- Sengoku Hime 4 \~Souha '''
            '''Hyakkei, Hana Mamoru Chikai\~;\n- Sengoku Hime 5 \~Senka Tatsu Haou no Keifu\~;\n- Sengoku Hime 6 '''
            ''''\~Tenka Kakusei, Shingetsu no Kirameki\~. ''',
            
            '''THE TOOL USAGE: CRYPTOATTACKS.\n\n\n'''
            '''1. Start the tool.\n2. Go to "Crypto Module" and focus on the right half of the screen.\n3. Choose '''
            '''the main.sd **(and only the main.sd!)** script.\n4. Choose the output text file (with the '''
            '''cryptoattack result).\n5. Choose the attack type. Almost all games are weak for "2 0 0 2 0", but an '''
            '''earlier games may be weak for "2 0 2 0 0". **There is only one possible type for each main.sd!**\n6. '''
            '''Choose the attack mode of operation -- find only one possible key (may not work depending on '''
            '''settings) or all.\n7. Choose the attack mode of attack. Earlier games (elder of version 2 and version '''
            '''3) use second (i-(key>>16)&0xff), but version 4 games use first (i^(key&0xff)).\n8. Run it! **If you '''
            '''picked attack mode and type correctly, you'll likely get first correct key in 1 minute!** If you '''
            '''can't get any key in 5 minutes, just try other settings.''',

            '''THE TOOL USAGE: (DE/EN)CRYPTION\n\n\n'''
            '''1. Start the tool.\n2. Go to "Crypto Module" and focus on the left half of the screen.\n3. Choose the '''
            '''processing mode (per file or per folder).\n4. Choose the input and output files or folders.\n5. '''
            '''Choose the key. You can choose known key in the ComboBox vidjet, but also can write your own key '''
            '''''''**(in hex form!)**\n6. Choose the encryption mode. Earlier games (elder of version 2 and version '''
            '''3) scripts use second (i-(key>>16)&0xff), but version 4 games use first (i^(key&0xff)). Almost all '''
            '''supplement data files use the first mode.\n7. Run it! Soon it will be (de/en)crypted...''',
            
            '''THE TOOL USAGE: VERSION 0 SCRIPTS (DE)COMPILATION\n\n\n'''
            '''1. Start the tool.\n2. Go to "0-Version Script".\n3. Choose the processing mode (per file or per '''
            '''folder).\n4. Choose the input and output files or folders.\n5. Choose the encoding (of both script '''
            '''and decompiled file). If you want to create script with different encoding, just decompile it with '''
            '''old encoding, change encoding of decompiled script (txt) and create a new script with new '''
            '''encoding.\n6. Run it! Soon it will be (de)compiled...''',
            
            '''THE TOOL USAGE: ELDER VERSIONS SCRIPTS (DE)COMPILATION\n\n\n'''
            '''1. Start the tool.\n2. Go to "1+ Versions Scripts".\n3. Choose the decompilation mode (to file or to '''
            '''folder). This mode is also complitation mode: from file or from folder.\n4. Choose the script '''
            '''folder and base (name of script files without extension). You may want to click at "..." button at '''
            '''the right of "script name" field and choose the ".sd" script, and boyh name without extension and '''
            '''folder will be filled authomatically.\n5. Choose the decompiled txt script file or folder. Do note, '''
            '''even if you decompile it to one file, there will be some technical files starting "__" in the same '''
            '''folder.\n6. Choose the encoding (of both script and decompiled file). If you want to create script '''
            '''with different encoding, just decompile it with old encoding, change encoding of decompiled script '''
            '''''''(txt) and create a new script with new encoding.\n7. Choose the version via ComboBox vidget.\n8. '''
            '''Run it! Soon it will be (de)compiled... But, to be fair, even if commonly (de)compilation takes '''
            '''about 1 minute, compilation from multiple files (from a folder) takes several minutes.''',
            
            '''LINE AND MESSAGE BREAKS HELP\n\n\n'''
            '''Sometimes there could be a very big problem: text may not fully get in textbox. But with this tool '''
            '''thou don't need to cut some part of text, no. Thou can use line and message breaks. Methods are '''
            '''below.\n### For line breaks insert in the current message this.\n```\n\\n\n```\n### For message '''
            '''breaks duplicate the message command and "WAIT_FOR_CLICK" (if existed). It's preferable to edit '''
            '''''''"postcommand args", but not mandatory. It has worked in my tests even without editing them.\n### '''
            '''Example below is from Sengoku Hime 4.\n>>> Old code.\n```\n#1: ["MESSAGE", 159, 43]\n[\n    "*",\n    '''
            '''''''"**",\n    "？？？",\n    [\n        "GROUP",\n        [\n            '''
            '''''''"「追加ができたぞー♪　皆、どんどん食べてくれ」",\n            0,\n            0,\n            -4276546,\n  '''
            '''''''-1\n        ]\n    ]\n]\n#1: ["WAIT_FOR_CLICK", 159, 45]\n[]\n```\n>>> New code.\n```\n#1: '''
            '''''''["MESSAGE", 159, 43]\n[\n    "*",\n    "**",\n    "？？？",\n    [\n        "GROUP",\n        [\n  '''
            '''''''"「追加ができたぞー♪　皆、どんどん食べてくれ」",\n            0,\n            0,\n            -4276546,\n  '''
            '''''''-1\n        ]\n    ]\n]\n#1: ["WAIT_FOR_CLICK", 159, 44]\n[]\n#1: ["MESSAGE", 159, 45]\n[\n    '''
            '''''''"*",\n    "**",\n    "？？？",\n    [\n        "GROUP",\n        [\n            '''
            '''''''"「追加ができたぞー♪　皆、どんどん食べてくれ」",\n            0,\n            0,\n            -4276546,\n  '''
            '''''''-1\n        ]\n    ]\n]\n#1: ["WAIT_FOR_CLICK", 159, 46]\n[]\n```''',
        ),
        'rus': (
            'О движке SLG System',
            'О средстве',
            'Версии игр',
            'Ключи игр',
            'Справка',
            '''SLG System является не слишком популярным, но и не слишком неизвестным движком, используемым в играх '''
            '''Gesen 18 и, вероятно, Unicorn-A. На самом деле является своего рода модификацией движка Тэнка то:ицу '''
            '''ADVANCE. На нём написано немало сдобный визуальных новелл и японских ролевых игр (jRPG), например '''
            '''серии Принцессы Сэнгоку и Принцессы Троецарствия.\n\nВерсия "0" данного движка используют '''
            '''однофайловые скрипты .sd, более поздние -- многокомпонентные скрипты из ряда файлов, которые меняются '''
            '''зависимости от версий и число которых обычно составляет от 9 до 11, причём все файлы связаны. Главным '''
            '''файлом таких многокомпонентных скриптов является .sd, хотя работать только с одним сим файлом, не '''
            '''меняя другие в соответствии со сделанными изменениями, нельзя, так как связность между ними сломается '''
            '''и игра не будет работать корректно.\n\nИгры на движке, начиная с третьей версии (или даже последних '''
            '''игр второй версии) обычно содержат технические средства защиты цифровых прав, DRM, а также шифрование '''
            '''скриптов и файлов вспомогательных структур данных.''',

            '''ОБЩИЕ СВЕДЕНИЯ О СРЕДСТВЕ.\n\n\n'''
            '''Двуязычное средство с графическим интерфейсом пользователя для (де)компилирования и (рас)шифровки (с '''
            '''нахождением ключей) скриптов движка SLG System. Поддерживает все известные версии SLG System: 0, 1, '''
            '''2, 3 (3.0, 3.1), 4 (4.0, 4.1), хотя может и не поддерживать некоторые их вариации. Коль средство не '''
            '''поддерживает какую-то игру, пишите в "Issues" к сему средству, приложив скрипты и указав игру. С сим '''
            '''средством вы можете: декомпилировать и компилировать скрипты SLG System, (рас)шифровывать скрипты '''
            '''любых игр, находить ключ любой игры на SLG System посредством криптоатаки.\n\nУ неё есть следующие '''
            '''функции:\n- Справочный модуль.\n- Криптографический модуль (для (рас)шифровки и криптоатак).\n- '''
            '''Модуль для работы со скриптами версии 0 (отдельный модуль, понеже скрипты версии 0 слишком отличаются '''
            '''от остальных).\n- Модуль для работы со скриптами более старых версий.\n\n> Протестировано с\n- '''
            '''Псалтырь 69: Мессия пустоты;\n- Принцессы Троецарствия: Неспокойные времена, план Трёх царств '''
            '''(Обновлённая версия);\n- Принцессы Сэнгоку: Огни мира войны;\n- Принцессы Сэнгоку 2: В мире войны '''
            '''буря бушует меж феодалами;\n- Принцессы Сэнгоку 3: Свет и тьма рассекают мир;\n- Принцессы Сэнгоку 4: '''
            '''Все средства для победы, клятва защитить цветы;\n- Принцессы Сэнгоку 5: Родословная правителя, '''
            '''потушившего пламя войны;\n- Принцессы Сэнгоку 6: Пробуждение державы, блеск новой Луны.''',

            '''ИСПОЛЬЗОВАНИЕ СРЕДСТВА: КРИПТОАТАКИ.\n\n\n'''
            '''1. Запустите средство.\n2. Перейдите во вкладку "Криптомодуль" и сосредоточьте взгляд на правой части '''
            '''экрана.\n3. Выберите скрипт main.sd **(обязательно скрипт именно с таким названием!)**\n4. Выберите '''
            '''выходной текстовый файл (для вывода результатов криптоатаки).\n5. Выберите тип атаки. Обычно все игры '''
            '''уязвимы пред "2 0 0 2 0", но ранние могут быть уязвимы лишь пред "2 0 2 0 0". **Для каждого main.sd '''
            '''есть лишь один корректный тип криптоатаки!**\n6. Выберите режим обработки атаки -- находить один '''
            '''возможный ключ (что может и не работать в зависимости от настроек) иль все.\n7. Выберите режим '''
            '''собственно атаки. В ранних играх (версии 3 и поздние 2-й версии) используйте второй '''
            '''''''(i-(key>>16)&0xff), но для тех, что на 4, первый -- (i^(key&0xff)).\n8. Запускайте! **Коль вы '''
            '''выбрали правильные режим и тип атаки, то скорее всего получите первый корректный ключ аж за '''
            '''минуту!** Коль не можете получить никакого ключа за 5 минут, просто попробуйте иные настройки.''',

            '''ИСПОЛЬЗОВАНИЕ СРЕДСТВА: (РАС)ШИФРОВАНИЕ\n\n\n'''
            '''1. Запустите средство.\n2. Перейдите на вкладку "Криптомодуль" и сосредоточьте взгляд на левой части '''
            '''экрана.\n3. Выберите режим обработки (по файлу или по папке).\n4. Выберите входные и выходные файлы '''
            '''или папки.\n5. Выберите ключ. Можно как выбрать уже известный ключ с помощью виджета ComboBox, так и '''
            '''написать свой **(в шестнадцатеричной форме!)**\n6. Выберите режим шифрования. В ранних играх (версии '''
            '''3 и поздние 2-й версии) используйте второй (i-(key>>16)&0xff), но для тех, что на 4, первый -- '''
            '''(i^(key&0xff)). Почти все файлы вспомогательных структур данных используют первый режим.\n7. '''
            ''''Запускайте! Вскоре нужное будет (рас)шифровано...''',

            '''ИСПОЛЬЗОВАНИЕ СРЕДСТВА: (ДЕ)КОМПИЛЯЦИЯ СКРИПТОВ ВЕРСИИ 0\n\n\n'''
            '''1. Запустите средство.\n2. Перейдите на вкладку "Скрипт версии 0".\n3. Выберите режим обработки (по '''
            '''файлу или по папке).\n4. Выберите входные и выходные файлы или папки.\n5. Выберите кодировку (что '''
            '''применяется как для компилированного скрипта, так и декомпилированного txt). Ежели вы хотите сменить '''
            '''кодировку скрипта, то сперва декомпилируйте скрипт со старой, затем измените кодировку полученного '''
            '''текстового файла и создайте скрипт с новой кодировкой.\n6. Запускайте! Вскоре нужное будет '''
            '''(де)компилировано...''',
            
            '''ИСПОЛЬЗОВАНИЕ СРЕДСТВА: (ДЕ)КОМПИЛЯЦИЯ СКРИПТОВ СТАРШИХ ВЕРСИЙ\n\n\n'''
            '''1. Запустите средство.\n2. Перейдите на вкладку "Скрипты версий 1+".\n3. Выберите режим рекомпиляции '''
            '''''''(в файл или папку). Сей режим также относится и к компиляции: из файла иль из папки.\n4. Выберите '''
            '''папку и основу имени скрипта (имя скрипта без расширения). Может быть удобно кликнуть на кнопку "..." '''
            '''с правой части подраздела "имени скрипта" и выбрать скрипт ".sd", после чего папка и основа имени '''
            '''скрипта будет заполнены автоматически.\n5. Выберите файл или папку декомпилированного скрипта в '''
            '''текстовом формате. Заметьте, что, даже ежели вы декомпилируете скрипт в один файл, в той же '''
            '''директории появятся технические файлы, имена коих начинаются с "__".\n5. Выберите кодировку (что '''
            '''применяется как для компилированного скрипта, так и декомпилированного txt). Ежели вы хотите сменить '''
            '''кодировку скрипта, то сперва декомпилируйте скрипт со старой, затем измените кодировку полученного '''
            '''текстового файла и создайте скрипт с новой кодировкой.\n8. Посредством виджета ComboBox выберите '''
            '''версию.\n9. Запускайте! Вскоре нужное будет (де)компилировано... Хотя, справедливости ради, если '''
            '''обычно (де)компиляция выполняется примерно за минуту, то компиляция из множества файлов (из папки) '''
            '''может занять уже несколько минут.''',
            
            '''СПРАВКА О ПЕРЕНОСАХ ПО СТРОКАМ И СООБЩЕНИЯМ\n\n\n'''
            '''Иногда можно столкнуться с одной большой-пребольшой проблемой: текст может не полностью влезать в '''
            '''текстовое окно. Однако, с сим средством вам не нужно обрезать его, отнюдь. Вы можете организовывать '''
            '''переносы по строкам и сообщениям. Методы указаны ниже.\n### Для переносов по строкам добавьте в '''
            '''текущее сообщение следующее.\n```\n\\n\n```\n### Для переносов по сообщениям продублируйте текущую '''
            '''команду сообщения и "WAIT_FOR_CLICK" (при наличии). Рекомендуется также изменить т.н. "посткомандные '''
            '''аргументы", но это не обязательно, так как в моих тестах работало и без изменений их.\n### Пример '''
            '''ниже представлен для Принцесс Сэнгоку 4.\n>>> Старый код.\n```\n#1: ["MESSAGE", 159, 43]\n[\n    '''
            '''''''"*",\n    "**",\n    "？？？",\n    [\n        "GROUP",\n        [\n            '''
            '''''''"「追加ができたぞー♪　皆、どんどん食べてくれ」",\n            0,\n            0,\n            -4276546,\n '''
            '''''''-1\n        ]\n    ]\n]\n#1: ["WAIT_FOR_CLICK", 159, 45]\n[]\n```\n>>> Новый код.\n```\n#1: '''
            '''''''["MESSAGE", 159, 43]\n[\n    "*",\n    "**",\n    "？？？",\n    [\n        "GROUP",\n        [\n  '''
            '''''''"「追加ができたぞー♪　皆、どんどん食べてくれ」",\n            0,\n            0,\n            -4276546,\n '''
            '''''''-1\n        ]\n    ]\n]\n#1: ["WAIT_FOR_CLICK", 159, 44]\n[]\n#1: ["MESSAGE", 159, 45]\n[\n    '''
            '''''''"*",\n    "**",\n    "？？？",\n    [\n        "GROUP",\n        [\n            '''
            '''''''"「追加ができたぞー♪　皆、どんどん食べてくれ」",\n            0,\n            0,\n            -4276546,\n '''
            '''''''-1\n        ]\n    ]\n]\n#1: ["WAIT_FOR_CLICK", 159, 46]\n[]\n```''',
        )
    }

    def __init__(self, master):
        super(SLG_MainFrame, self).__init__(master)
        self.master = master
        self["background"] = 'white'
        self["relief"] = tk.RAISED
        self["borderwidth"] = 5
        self._language = ''

        self._main_button = []
        self._help_func = [self._engine_help, self._tool_help, self._version_help, self._keys_help]
        butter = 0.135
        yutter = 0.25
        wider = 0.315
        yider = 0.2
        for i in range(4):
            self._main_button.append(tk.Button(master=self,
                                               command=self._help_func[i],
                                               relief=tk.RAISED,
                                               font=('Helvetica', 13)))
            self._main_button[i].place(relx=abs((i % 2) - butter) - wider * (i % 2),
                                       rely=abs(int(i > 1) - yutter) - yider * int(i > 1),
                                       relwidth=wider, relheight=yider)

        self._possible_keys = ''
        for i in SLG_Crypto.basic_keys:
            self._possible_keys += hex(i[0]) + ' - ' + i[1] + ';\n'
        self._possible_keys = self._possible_keys[:-2] + '.'
        self._possible_versions = ''
        for i in SLG_Scripts_NEW.game_versions:
            self._possible_versions += str(i[0]) + ' - '
            for k in i[1]:
                self._possible_versions += k + ', '
            self._possible_versions = self._possible_versions[:-2] + ';\n'
        self._possible_versions = self._possible_versions[:-2] + '.'

    def _engine_help(self):
        print("Engine help!/Помощь о движке!")
        SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][4],
                                       self.strings_lib[self._language][5])

    def _tool_help(self):
        print("Tool help!/Помощь о средстве!")
        for i in range(6):
            SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][4],
                                           self.strings_lib[self._language][6+i])

    def _version_help(self):
        print("Version help!/Помощь о версиях!")
        SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][4],
                                       self._possible_versions)

    def _keys_help(self):
        print("Keys help!/Помощь о ключах!")
        SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][4],
                                       self._possible_keys)

    def translate_to(self, language):
        self._language = language
        for i in range(len(self._main_button)):  # 4
            self._main_button[i]["text"] = self.strings_lib[self._language][i]
        # 4 -- справка.
        # 5 -- помощь о движке.
        # 6 -- помощь о средстве..
        # 7-9 -- использование.
        # 10 -- добавление строк/сообщений.


class SLG_CryptoFrame(SLG_MasterFrame):
    strings_lib = {
        'eng': ('(En/de)cryption',
                'Cryptoattacks',
                'Choose encrypted main.sd script:',
                'Choose output .txt file:',
                'Choose the cryptoattack type:',
                'Choose the cryptoattack modes:',
                'Begin cryptoattack!',
                '...',
                '...',
                'First possible key',
                'All possible keys',
                'main.sd script',
                'main.sd',
                'All files',
                '*',
                'Text files',
                '*.txt',
                'Error!',
                'Cryptoattack type is not correct!',
                'Such main.sd script is not exist!',
                'Text file with such name cannot be created!',
                'i^(key&0xff)',
                '(i-(key>>16))&0xff',
                '(i+(key>>16))&0xff',
                'Choose the processing mode:',
                'Choose the input file/folder:',
                'Choose the output file/folder:',
                'Choose the parameters:',
                'Decrypt',
                'Encrypt',
                'Per file',
                'Per folder',
                'There is no such input file!',
                'There is no such input folder!',
                'Output file with such name cannot be created!',
                'Output folder with such name cannot be created!',
                'The encryption key is incorrect!',
                'Input and output files should be different!',
                'Input and output folders should be different!'),
        'rus': ('(Рас)шифрование',
                'Криптоатаки',
                'Выберите шифрованный скрипт main.sd:',
                'Выберите выходной текстовый файл:',
                'Выберите тип криптоатаки:',
                'Выберите режимы криптоатаки:',
                'Начать криптоатаку!',
                '...',
                '...',
                'Первый возможный ключ',
                'Все возможные ключи',
                'Скрипт main.sd',
                'main.sd',
                'Все файлы',
                '*',
                'Текстовые файлы',
                '*.txt',
                'Ошибка!',
                'Тип криптоатаки некорректен!',
                'Такого скрипта main.sd не существует!',
                'Текстовый файл с таким названием невозможно создать!',
                'i^(key&0xff)',
                '(i-(key>>16))&0xff',
                '(i+(key>>16))&0xff',
                'Выберите режим обработки:',
                'Выберите файл/папку ввода:',
                'Выберите файл/папку вывода:',
                'Выберите параметры:',
                'Расшифровать',
                'Зашифровать',
                'По файлу',
                'По папке',
                'Нет такого файла (на ввод)!',
                'Нет такой папки (на ввод)!',
                'Нельзя создать файл с таким названием (на вывод)!',
                'Нельзя создать папку с таким названием (на выход)!',
                'Ключ шифрования некорректен!',
                'Файл на ввод и файл на вывод не должны быть одинаковыми!',
                'Папка на ввод и папка на вывод не должны быть одинаковыми!')
    }

    def __init__(self, master):
        super(SLG_CryptoFrame, self).__init__(master)
        self.master = master
        self["background"] = 'white'
        self["relief"] = tk.RAISED
        self["borderwidth"] = 5

        self._language = ''

        self._attack_sd_var = tk.StringVar()
        self._attack_txt_var = tk.StringVar()
        self._attack_type = tk.StringVar()
        first_string = ''
        for i in SLG_Crypto.common_script_attacks[0]:
            first_string += str(i)
            first_string += ' '
        first_string = first_string.rstrip()
        self._attack_type.set(first_string)
        self._attack_mode = tk.IntVar()
        self._attack_mode.set(0)
        self._attack_mode_two = tk.IntVar()
        self._attack_mode_two.set(0)

        self._attack_frame = []
        for i in range(2):
            self._attack_frame.append(tk.LabelFrame(master=self,  # Шифрование, криптоатаки.
                                                    font=('Helvetica', 14),
                                                    bg='white',
                                                    relief=tk.RAISED))
            self._attack_frame[i].place(relx=0.0 + i * 0.5, rely=0.0, relwidth=0.5, relheight=1.0)
        self._attack_label = []
        for i in range(4):  # .sd, .txt, режим, тип.
            self._attack_label.append(tk.Label(
                master=self._attack_frame[1],
                bg='white',
                font=('Helvetica', 10)
            ))
            self._attack_label[i].place(relx=0.0, rely=0.2 * i, relwidth=1.0, relheight=0.1)
        self._attack_button = tk.Button(master=self._attack_frame[1],
                                        command=self._cryptoattack,
                                        font=('Helvetica', 14))
        self._attack_button.place(relx=0.0, rely=0.9, relwidth=1.0, relheight=0.1)

        self._attack_file_text = []
        self._attack_file_btn = []
        for i in range(2):
            self._attack_file_text.append(tk.Entry(
                master=self._attack_frame[1],
                font=('Helvetica', 8),
                borderwidth=5
            ))
            self._attack_file_btn.append(tk.Button(
                master=self._attack_frame[1],
                relief=tk.RAISED,
                font=('Helvetica', 14),
            ))
            widther = 0.85
            self._attack_file_text[i].place(relx=0.0, rely=0.1 + (0.2 * i), relwidth=widther, relheight=0.1)
            self._attack_file_btn[i].place(relx=widther, rely=0.1 + (0.2 * i), relwidth=1.0 - widther, relheight=0.1)
        self._attack_file_btn[0]["command"] = self._attack_what_sd
        self._attack_file_text[0]["textvariable"] = self._attack_sd_var
        self._attack_file_btn[1]["command"] = self._attack_what_txt
        self._attack_file_text[1]["textvariable"] = self._attack_txt_var

        self._attack_typer_txt = tk.Entry(
            master=self._attack_frame[1],
            font=('Helvetica', 8),
            borderwidth=5,
            textvariable=self._attack_type,
        )
        self._attack_typer_cmb = ttk.Combobox(
            master=self._attack_frame[1],
            font=('Helvetica', 12),
            values=SLG_Crypto.common_script_attacks,
            textvariable=self._attack_type,
            state='readonly'
        )
        self._attack_typer_txt.place(relx=0.0, rely=0.5, relwidth=0.5, relheight=0.1)
        self._attack_typer_cmb.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.1)

        self._attack_radio = []
        for i in range(2):
            self._attack_radio.append(tk.Radiobutton(master=self._attack_frame[1],
                                                     background='white',
                                                     font=('Helvetica', 7),
                                                     variable=self._attack_mode,
                                                     value=i))
            self._attack_radio[i].place(relx=0.0 + (0.5 * i), rely=0.7, relwidth=0.5, relheight=0.1)

        self._attack_radio_two = []
        for i in range(3):
            self._attack_radio_two.append(tk.Radiobutton(master=self._attack_frame[1],
                                                         background='white',
                                                         font=('Helvetica', 6 + (2 * int(i == 0))),
                                                         variable=self._attack_mode_two,
                                                         value=i))
            self._attack_radio_two[i].place(relx=0.0 + (0.33 * i), rely=0.8, relwidth=0.33, relheight=0.1)

        # Подмодуль шифровки/дешифровки:
        self._proc_mode = tk.IntVar()
        self._proc_mode.set(0)
        self._old_proc_mode = self._proc_mode.get()
        self._proc_mode.trace_add('write', self._crypto_changer)
        self._crypto_input = tk.StringVar()
        self._crypto_output = tk.StringVar()
        key_variants = []
        for i in SLG_Crypto.basic_keys:
            new_string = hex(i[0])
            new_string += ' - '
            new_string += i[1]
            key_variants.append(new_string)
        key_variants = tuple(key_variants)
        self._crypto_key = tk.StringVar()
        self._crypto_mode = tk.IntVar()
        self._crypto_mode.set(0)

        self._crypto_label = []
        for i in range(4):
            self._crypto_label.append(tk.Label(
                master=self._attack_frame[0],
                bg='white',
                font=('Helvetica', 10)
            ))
            self._crypto_label[i].place(relx=0.0, rely=0.2 * i, relwidth=1.0, relheight=0.1)

        self._crypto_main_btn = []
        for i in range(2):
            self._crypto_main_btn.append(tk.Button(
                master=self._attack_frame[0],
                relief=tk.RAISED,
                font=('Helvetica', 14),
            ))
            self._crypto_main_btn[i].place(relx=0.5 * i, rely=0.9, relwidth=0.5, relheight=0.1)
        self._crypto_main_btn[0]["command"] = self._decrypt_base
        self._crypto_main_btn[1]["command"] = self._encrypt_base
        self._crypto_proc_mode = []
        for i in range(2):
            self._crypto_proc_mode.append(tk.Radiobutton(master=self._attack_frame[0],
                                                         background='white',
                                                         font=('Helvetica', 12),
                                                         variable=self._proc_mode,
                                                         value=i))
            self._crypto_proc_mode[i].place(relx=0.5 * i, rely=0.1, relwidth=0.5, relheight=0.1)

        self._crypto_file_txt = []
        self._crypto_file_btn = []
        for i in range(2):
            self._crypto_file_txt.append(tk.Entry(
                master=self._attack_frame[0],
                font=('Helvetica', 8),
                borderwidth=5
            ))
            self._crypto_file_btn.append(tk.Button(
                master=self._attack_frame[0],
                relief=tk.RAISED,
                font=('Helvetica', 14),
            ))
            widther = 0.85
            self._crypto_file_txt[i].place(relx=0.0, rely=0.3 + (0.2 * i), relwidth=widther, relheight=0.1)
            self._crypto_file_btn[i].place(relx=widther, rely=0.3 + (0.2 * i), relwidth=1.0 - widther, relheight=0.1)
        self._crypto_file_txt[0]["textvariable"] = self._crypto_input
        self._crypto_file_txt[1]["textvariable"] = self._crypto_output
        self._crypto_file_btn[0]["command"] = self._crypto_what_input
        self._crypto_file_btn[1]["command"] = self._crypto_what_output

        self._crypto_typer_txt = tk.Entry(
            master=self._attack_frame[0],
            font=('Helvetica', 8),
            borderwidth=5,
            textvariable=self._crypto_key,
        )
        self._crypto_typer_cmb = ttk.Combobox(
            master=self._attack_frame[0],
            font=('Helvetica', 12),
            values=key_variants,
            textvariable=self._crypto_key,
            state='readonly'
        )
        wider = 0.25
        self._crypto_typer_txt.place(relx=0.0, rely=0.7, relwidth=wider, relheight=0.1)
        self._crypto_typer_cmb.place(relx=wider, rely=0.7, relwidth=1.0 - wider, relheight=0.1)

        self._crypto_key.trace_add('write', self._crypto_chkey)
        self._crypto_key.set(key_variants[0])

        self._crypto_mode_rbtn = []
        for i in range(2):
            self._crypto_mode_rbtn.append(tk.Radiobutton(master=self._attack_frame[0],
                                                         background='white',
                                                         font=('Helvetica', 10),
                                                         variable=self._crypto_mode,
                                                         value=i))
            self._crypto_mode_rbtn[i].place(relx=0.5 * i, rely=0.8, relwidth=0.5, relheight=0.1)

        self._kill_all_reptiloids = 0

    # Методы криптоатак:
    def _cryptoattack(self):
        input_file = self._attack_sd_var.get()
        if (not (os.path.isfile(input_file))):
            SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17],
                                           self.strings_lib[self._language][19])
            return False
        output_file = self._attack_txt_var.get()
        if (not (os.path.isfile(output_file))):
            try:
                new_file = open(output_file, 'w')
                new_file.close()
            except:
                SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17],
                                               self.strings_lib[self._language][20])
                return False
        attack_type = self._correct_attack_type(self._attack_type.get())
        if (attack_type == False):
            SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17],
                                           self.strings_lib[self._language][18])
            return False
        stat = False
        if (stat):
            print('Входной .sd файл:', input_file)
            print('Выходной текстовый файл:', output_file)
            print('Тип атаки:', attack_type)
            print('Режим атаки:', self._attack_mode.get())
            print('Режим атаки два:', self._attack_mode_two.get())
        print("Криптоатака начата!/Cryptoattack started!")
        self._attack_button["state"] = tk.DISABLED
        hack_thread = threading.Thread(target=self._crypto_attack, args=(input_file, attack_type,
                                                                         self._attack_mode.get(), output_file,
                                                                         self._attack_mode_two.get()))
        hack_thread.start()
        return True

    def _crypto_attack(self, input_file, attack_type, attack_mode, output_file, attack_mode_two):
        try:
            HackEmAll = SLG_Crypto(input_file, attack_type, attack_mode, -1)
            HackEmAll.attack(output_file, attack_mode_two)
            del HackEmAll
        except Exception as ex:
            SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17], str(ex))
        finally:
            self._attack_button["state"] = tk.NORMAL

    def _correct_attack_type(self, typer):
        new_type = []
        exer = typer.split(' ')
        try:
            for i in exer:
                new_type.append(int(i))
        except:
            return False
        return tuple(new_type)

    def _attack_what_sd(self):
        ftypes = [(self.strings_lib[self._language][11], self.strings_lib[self._language][12]),
                  (self.strings_lib[self._language][13], self.strings_lib[self._language][14])]
        dialg = filedialog.Open(self._attack_frame[1], filetypes=ftypes, initialdir=os.getcwd())
        file = dialg.show()
        if (file != ''):
            self._attack_sd_var.set(file)

    def _attack_what_txt(self):
        ftypes = [(self.strings_lib[self._language][15], self.strings_lib[self._language][16]),
                  (self.strings_lib[self._language][13], self.strings_lib[self._language][14])]
        dialg = filedialog.Open(self._attack_frame[1], filetypes=ftypes, initialdir=os.getcwd())
        file = dialg.show()
        if (file != ''):
            self._attack_txt_var.set(file)

    # Методы (де)шифрования:
    def _encrypt_base(self):
        def _enc_thread_start(inper, outer):
            for i in range(len(self._crypto_main_btn)):
                self._crypto_main_btn[i]["state"] = tk.DISABLED
            print('Encryption/Шифрование:', inper, '->', outer)
            enc_thread = threading.Thread(target=self._encrypt, args=(inper,
                                                                      outer,
                                                                      int(self._crypto_key.get(), 16),
                                                                      self._crypto_mode.get()))
            enc_thread.start()

        if (not (self._crypto_is_correct_data())):
            return False
        if (self._proc_mode.get() == 0):  # Файл.
            _enc_thread_start(self._crypto_input.get(), self._crypto_output.get())
        else:  # Директория.
            for root, dirs, files in os.walk(self._crypto_input.get()):
                self._kill_all_reptiloids = len(files)
                for file in files:
                    new_file_base = os.path.join(root, file)[len(self._crypto_input.get()) + 1:]
                    new_file_in = os.path.join(self._crypto_input.get(), new_file_base)
                    new_file_out = os.path.join(self._crypto_output.get(), new_file_base)
                    # print(new_file_base, ":", new_file_in, new_file_out)
                    _enc_thread_start(new_file_in, new_file_out)
        return True

    def _encrypt(self, input_file, output_file, enc_key, enc_mode):
        try:
            EncryptEmAll = SLG_Crypto(input_file, (2, 0, 0, 2, 0), 0, enc_key)
            EncryptEmAll.encrypt(output_file, enc_mode)
            del EncryptEmAll
        except Exception as ex:
            SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17], str(ex))
        finally:
            self._kill_all_reptiloids -= 1
            if (self._kill_all_reptiloids <= 0):
                for i in range(len(self._crypto_main_btn)):
                    self._crypto_main_btn[i]["state"] = tk.NORMAL

    def _decrypt_base(self):
        def _dec_thread_start(inper, outer):
            for i in range(len(self._crypto_main_btn)):
                self._crypto_main_btn[i]["state"] = tk.DISABLED
            print('Decryption/Дешифрование:', inper, '->', outer)
            dec_thread = threading.Thread(target=self._decrypt, args=(inper,
                                                                      outer,
                                                                      int(self._crypto_key.get(), 16),
                                                                      self._crypto_mode.get()))
            dec_thread.start()

        if (not (self._crypto_is_correct_data())):
            return False
        if (self._proc_mode.get() == 0):  # Файл.
            _dec_thread_start(self._crypto_input.get(), self._crypto_output.get())
        else:  # Директория.
            for root, dirs, files in os.walk(self._crypto_input.get()):
                self._kill_all_reptiloids = len(files)
                for file in files:
                    new_file_base = os.path.join(root, file)[len(self._crypto_input.get()) + 1:]
                    new_file_in = os.path.join(self._crypto_input.get(), new_file_base)
                    new_file_out = os.path.join(self._crypto_output.get(), new_file_base)
                    # print(new_file_base, ":", new_file_in, new_file_out)
                    _dec_thread_start(new_file_in, new_file_out)
        return True

    def _decrypt(self, input_file, output_file, enc_key, enc_mode):
        try:
            DecryptEmAll = SLG_Crypto(input_file, (2, 0, 0, 2, 0), 0, enc_key)
            DecryptEmAll.decrypt(output_file, enc_mode)
            del DecryptEmAll
        except Exception as ex:
            SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17], str(ex))
        finally:
            self._kill_all_reptiloids -= 1
            if (self._kill_all_reptiloids <= 0):
                for i in range(len(self._crypto_main_btn)):
                    self._crypto_main_btn[i]["state"] = tk.NORMAL

    def _crypto_is_correct_data(self):
        if (self._proc_mode.get() == 0):  # Файл.
            if (not (os.path.isfile(self._crypto_input.get()))):
                SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17],
                                               self.strings_lib[self._language][32])
                return False
            if (not (os.path.isfile(self._crypto_output.get()))):
                try:
                    if (os.path.split(self._crypto_output.get())[0] != ''):
                        os.makedirs(os.path.split(self._crypto_output.get())[0], exist_ok=True)
                    zlo = open(self._crypto_output.get(), 'wb')
                    zlo.close()
                except:
                    SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17],
                                                   self.strings_lib[self._language][34])
                    return False
            if (self._crypto_output.get() == self._crypto_input.get()):
                SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17],
                                               self.strings_lib[self._language][37])
                return False
        else:  # Директория.
            if (not (os.path.isdir(self._crypto_input.get()))):
                SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17],
                                               self.strings_lib[self._language][33])
                return False
            if (not (os.path.isdir(self._crypto_output.get()))):
                try:
                    os.makedirs(self._crypto_output.get(), exist_ok=True)
                except:
                    SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17],
                                                   self.strings_lib[self._language][35])
                    return False
            if (self._crypto_output.get() == self._crypto_input.get()):
                SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17],
                                               self.strings_lib[self._language][38])
                return False
        try:
            int(self._crypto_key.get(), 16)
        except:
            SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17],
                                           self.strings_lib[self._language][36])
            return False
        return True

    def _crypto_what_input(self):
        if (self._proc_mode.get() == 0):  # По файлу.
            ftypes = [(self.strings_lib[self._language][13], self.strings_lib[self._language][14])]
            dialg = filedialog.Open(self._attack_frame[0], filetypes=ftypes, initialdir=os.getcwd())
            file = dialg.show()
            if (file != ''):
                self._crypto_input.set(file)
        else:  # По папке.
            direr = filedialog.askdirectory()
            if (direr != ''):
                self._crypto_input.set(direr)

    def _crypto_what_output(self):
        if (self._proc_mode.get() == 0):  # По файлу.
            ftypes = [(self.strings_lib[self._language][13], self.strings_lib[self._language][14])]
            dialg = filedialog.Open(self._attack_frame[0], filetypes=ftypes, initialdir=os.getcwd())
            file = dialg.show()
            if (file != ''):
                self._crypto_output.set(file)
        else:  # По папке.
            direr = filedialog.askdirectory()
            if (direr != ''):
                self._crypto_output.set(direr)

    def _crypto_changer(self, *args):
        if (self._old_proc_mode == self._proc_mode.get()):
            return False
        else:
            self._old_proc_mode = self._proc_mode.get()
        if (self._old_proc_mode == 0):
            self._crypto_input.set('')
            self._crypto_output.set('')
        else:
            self._crypto_input.set(os.path.split(self._crypto_input.get())[0])
            self._crypto_output.set(os.path.split(self._crypto_output.get())[0])
        return True

    def _crypto_chkey(self, *args):
        true_key = self._crypto_key.get().split(' - ')[0]
        self._crypto_key.set(true_key)
        # self._crypto_typer_txt["textvariable"] = self._crypto_key
        # self._crypto_typer_cmb["textvariable"] = self._crypto_key
        self._crypto_typer_txt.update()
        self._crypto_typer_cmb.update()

    # Прочие методы:
    def translate_to(self, language):
        self._language = language
        for i in range(len(self._attack_frame)):  # 2
            self._attack_frame[i]["text"] = self.strings_lib[language][i]
        for i in range(len(self._attack_label)):  # 4
            self._attack_label[i]["text"] = self.strings_lib[language][i + 2]
        self._attack_button["text"] = self.strings_lib[language][6]  # 1
        for i in range(len(self._attack_file_btn)):  # 2
            self._attack_file_btn[i]["text"] = self.strings_lib[language][i + 7]
        for i in range(len(self._attack_radio)):  # 2
            self._attack_radio[i]["text"] = self.strings_lib[language][i + 9]
        for i in range(len(self._attack_radio_two)):  # 3
            self._attack_radio_two[i]["text"] = self.strings_lib[language][i + 21]
        # 24+
        for i in range(len(self._crypto_label)):  # 4
            self._crypto_label[i]["text"] = self.strings_lib[language][i + 24]
        for i in range(len(self._crypto_main_btn)):  # 2
            self._crypto_main_btn[i]["text"] = self.strings_lib[language][i + 28]
        for i in range(len(self._crypto_proc_mode)):  # 2
            self._crypto_proc_mode[i]["text"] = self.strings_lib[language][i + 30]

        for i in range(len(self._crypto_file_btn)):  # Не считается!
            self._crypto_file_btn[i]["text"] = self.strings_lib[language][i + 7]
        for i in range(len(self._crypto_mode_rbtn)):  # Не считается!
            self._crypto_mode_rbtn[i]["text"] = self.strings_lib[language][i + 21]
        # 39+


class SLG_ScriptZeroFrame(SLG_MasterFrame):
    strings_lib = {
        "eng": (
            "Choose the processing mode:",
            'Choose the sd script or folder with them:',
            'Choose the decompiled txt script or folder with them:',
            'Choose the encoding:',
            'Decompile!',
            'Compile!',
            'Per file',
            'Per folder',
            '...',
            'Sd scripts',
            '*.sd',
            'Text files',
            '*.txt',
            'All files',
            '*',
            'Error',
            'There is no such encoding.',
            'Sd script and decompiled txt script are the same file!',
            'Both sd script and decompiled txt script are not exist!',
            'Sd script folder and decompiled txt script folder are the same folder!',
            'Both sd script folder and decompiled txt script folder are not exist!',
            'It is impossible to create sd script with such name!',
            'It is impossible to create decompiled txt script with such name!',
            'It is impossible to create sd script folder with such name!',
            'It is impossible to create decompiled txt script folder with such name!'
        ),
        "rus": (
            "Выберите режим обработки:",
            'Выберите скрипт sd или папку с ними:',
            'Выберите декомпилированный скрипт txt или папку с ними:',
            'Выберите кодировку:',
            'Декомпилировать!',
            'Компилировать!',
            'По файлу',
            'По папке',
            '...',
            'Скрипты sd',
            '*.sd',
            'Текстовые файлы',
            '*.txt',
            'Все файлы',
            '*',
            'Ошибка',
            'Такой кодировки не существует.',
            'Скрипт sd и декомпилированный скрипт txt являются тем же файлом!',
            'Скрипта sd и декомпилированного скрипта txt не существует!',
            'Папки со скриптами sd и декомпилированными скриптами txt являются той же папкой!',
            'Папок со скриптами sd и декомпилированными скриптами txt не существует!',
            'Создать скрипт sd с таким названием невозможно!',
            'Создать декомпилированный скрипт txt с таким названием невозможно!',
            'Создать папку со скриптами sd с таким названием невозможно!',
            'Создать папку с декомпилированными скриптами txt с таким названием невозможно!'
        )
    }

    def __init__(self, master):
        super(SLG_ScriptZeroFrame, self).__init__(master)
        self.master = master
        self["background"] = 'white'
        self["relief"] = tk.RAISED
        self["borderwidth"] = 5

        self._language = ''

        self._file_sd_var = tk.StringVar()
        self._file_sd_var.set('')
        self._file_txt_var = tk.StringVar()
        self._file_txt_var.set('')
        self._proc_mode = tk.IntVar()
        self._proc_mode.set(0)
        self._old_proc_mode = self._proc_mode.get()
        self._encoding = tk.StringVar()
        self._possible_encodings = SLG_Scripts_NEW.possible_encodings
        self._encoding.set(self._possible_encodings[0])
        self._kill_all_reptiloids = 0

        self._main_label = []
        for i in range(4):  # режим обработки, .sd, .txt, кодировка.
            self._main_label.append(tk.Label(
                master=self,
                bg='white',
                font=('Helvetica', 12)
            ))
            self._main_label[i].place(relx=0.0, rely=0.2 * i, relwidth=1.0, relheight=0.1)

        self._main_button = []
        for i in range(2):  # Декомпилировать, компилировать.
            self._main_button.append(tk.Button(master=self,
                                               command=self,
                                               font=('Helvetica', 14)))
            self._main_button[i].place(relx=0.5 * i, rely=0.8, relwidth=0.5, relheight=0.2)
        self._main_button[0]["command"] = self._decompile_base
        self._main_button[1]["command"] = self._compile_base

        self._proc_rdb = []
        for i in range(2):
            self._proc_rdb.append(tk.Radiobutton(master=self,
                                                 background='white',
                                                 font=('Helvetica', 12),
                                                 variable=self._proc_mode,
                                                 value=i))
            self._proc_rdb[i].place(relx=0.0 + (0.5 * i), rely=0.1, relwidth=0.5, relheight=0.1)

        self._filer_txt = []
        self._filer_btn = []
        for i in range(2):
            self._filer_txt.append(tk.Entry(
                master=self,
                font=('Helvetica', 8),
                borderwidth=5
            ))
            self._filer_btn.append(tk.Button(
                master=self,
                relief=tk.RAISED,
                font=('Helvetica', 14),
            ))
            widther = 0.85
            self._filer_txt[i].place(relx=0.0, rely=0.3 + (0.2 * i), relwidth=widther, relheight=0.1)
            self._filer_btn[i].place(relx=widther, rely=0.3 + (0.2 * i), relwidth=1.0 - widther, relheight=0.1)
        self._filer_txt[0]["textvariable"] = self._file_sd_var
        self._filer_txt[1]["textvariable"] = self._file_txt_var
        self._filer_btn[0]["command"] = self._what_sd
        self._filer_btn[1]["command"] = self._what_txt

        self._proc_mode.trace_add('write', self._ch_proc_mode)

        self._enc_txt = tk.Entry(
            master=self,
            font=('Helvetica', 12),
            borderwidth=5,
            textvariable=self._encoding,
        )
        self._enc_cmb = ttk.Combobox(
            master=self,
            font=('Helvetica', 12),
            values=self._possible_encodings,
            textvariable=self._encoding,
            state='readonly'
        )
        self._enc_txt.place(relx=0.0, rely=0.7, relwidth=0.5, relheight=0.1)
        self._enc_cmb.place(relx=0.5, rely=0.7, relwidth=0.5, relheight=0.1)

    def _decompile_base(self):
        def _start_thread(sd, txt):
            DecompileEmAll = threading.Thread(target=self._decompile, args=(sd, txt, self._encoding.get()))
            for i in self._main_button:
                i["state"] = tk.DISABLED
            print('Decompilation/Декомпиляция:', sd, '->', txt)
            DecompileEmAll.start()

        if (not (self._is_correct_data())):
            return False
        if (self._proc_mode.get() == 0):  # Файл.
            _start_thread(self._file_sd_var.get(), self._file_txt_var.get())
        else:  # Директория.
            for root, dirs, files in os.walk(self._file_sd_var.get()):
                self._kill_all_reptiloids = len(files)
                for file in files:
                    new_file_base = os.path.join(root, file)[len(self._file_sd_var.get()) + 1:]
                    new_file_sd = os.path.join(self._file_sd_var.get(), new_file_base)
                    new_file_txt = os.path.join(self._file_txt_var.get(), new_file_base).replace('.sd', '.txt')
                    _start_thread(new_file_sd, new_file_txt)
        return True

    def _decompile(self, sder, txter, encer):
        try:
            namer = os.path.split(sder)
            game_name = namer[0]
            base_name = namer[1]
            DecompileEmAll = SLG_Scripts_NEW(game_name, base_name, encer, 0)
            DecompileEmAll.decompile(txter, 0)
            del DecompileEmAll
        except Exception as ex:
            SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][15], str(ex))
        finally:
            self._kill_all_reptiloids -= 1
            if (self._kill_all_reptiloids <= 0):
                for i in self._main_button:
                    i["state"] = tk.NORMAL

    def _compile_base(self):
        def _start_thread(sd, txt):
            CompileEmAll = threading.Thread(target=self._compile, args=(sd, txt, self._encoding.get()))
            for i in self._main_button:
                i["state"] = tk.DISABLED
            print('Compilation/Компиляция:', txt, '->', sd)
            CompileEmAll.start()

        if (not (self._is_correct_data())):
            return False
        if (self._proc_mode.get() == 0):  # Файл.
            _start_thread(self._file_sd_var.get(), self._file_txt_var.get())
        else:  # Директория.
            for root, dirs, files in os.walk(self._file_txt_var.get()):
                self._kill_all_reptiloids = len(files)
                for file in files:
                    new_file_base = os.path.join(root, file)[len(self._file_txt_var.get()) + 1:]
                    new_file_txt = os.path.join(self._file_txt_var.get(), new_file_base)
                    new_file_sd = os.path.join(self._file_sd_var.get(), new_file_base).replace('.txt', '.sd')
                    _start_thread(new_file_sd, new_file_txt)
        return True

    def _compile(self, sder, txter, encer):
        try:
            namer = os.path.split(sder)
            game_name = namer[0]
            base_name = namer[1]
            CompileEmAll = SLG_Scripts_NEW(game_name, base_name, encer, 0)
            CompileEmAll.compile(txter, 0)
            del CompileEmAll
        except Exception as ex:
            SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][15], str(ex))
        finally:
            self._kill_all_reptiloids -= 1
            if (self._kill_all_reptiloids <= 0):
                for i in self._main_button:
                    i["state"] = tk.NORMAL

    def _is_correct_data(self):
        if (self._proc_mode.get() == 0):  # Файл
            if ((not (os.path.isfile(self._file_sd_var.get()))) and (not (os.path.isfile(self._file_txt_var.get())))):
                print(self._file_txt_var.get(), os.path.isfile(self._file_txt_var.get()))
                SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][15],
                                               self.strings_lib[self._language][18])
                return False
            if (not (os.path.isfile(self._file_sd_var.get()))):
                try:
                    if (os.path.split(self._file_sd_var.get())[0] != ''):
                        os.makedirs(os.path.split(self._file_sd_var.get())[0], exist_ok=True)
                    zlo = open(self._file_sd_var.get(), 'w')
                    zlo.close()
                except Exception as ex:
                    SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][15],
                                                   self.strings_lib[self._language][21])
                    return False
            if (not (os.path.isfile(self._file_txt_var.get()))):
                try:
                    if (os.path.split(self._file_txt_var.get())[0] != ''):
                        os.makedirs(os.path.split(self._file_txt_var.get())[0], exist_ok=True)
                    zlo = open(self._file_txt_var.get(), 'w')
                    zlo.close()
                except:
                    SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][15],
                                                   self.strings_lib[self._language][22])
                    return False
            if (self._file_sd_var.get() == self._file_txt_var.get()):
                SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][15],
                                               self.strings_lib[self._language][17])
                return False
        else:  # Директория.
            if ((not (os.path.isdir(self._file_sd_var.get()))) and (not (os.path.isdir(self._file_txt_var.get())))):
                SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][15],
                                               self.strings_lib[self._language][20])
                return False
            if (not (os.path.isdir(self._file_sd_var.get()))):
                try:
                    os.makedirs(self._file_sd_var.get(), exist_ok=True)
                except:
                    SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][15],
                                                   self.strings_lib[self._language][23])
                    return False
            if (not (os.path.isdir(self._file_txt_var.get()))):
                try:
                    os.makedirs(self._file_txt_var.get(), exist_ok=True)
                except:
                    SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][15],
                                                   self.strings_lib[self._language][24])
                    return False
            if (self._file_sd_var.get() == self._file_txt_var.get()):
                SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][15],
                                               self.strings_lib[self._language][19])
                return False
        try:
            codecs.lookup(self._encoding.get())
        except:
            SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][15],
                                           self.strings_lib[self._language][16])
            return False
        return True

    def _what_sd(self):
        if (self._proc_mode.get() == 0):  # По файлу.
            ftypes = [(self.strings_lib[self._language][9], self.strings_lib[self._language][10]),
                      (self.strings_lib[self._language][13], self.strings_lib[self._language][14])]
            dialg = filedialog.Open(self, filetypes=ftypes, initialdir=os.getcwd())
            file = dialg.show()
            if (file != ''):
                self._file_sd_var.set(file)
        else:  # По папке.
            direr = filedialog.askdirectory()
            if (direr != ''):
                self._file_sd_var.set(direr)

    def _what_txt(self):
        if (self._proc_mode.get() == 0):  # По файлу.
            ftypes = [(self.strings_lib[self._language][11], self.strings_lib[self._language][12]),
                      (self.strings_lib[self._language][13], self.strings_lib[self._language][14])]
            dialg = filedialog.Open(self, filetypes=ftypes, initialdir=os.getcwd())
            file = dialg.show()
            if (file != ''):
                self._file_txt_var.set(file)
        else:  # По папке.
            direr = filedialog.askdirectory()
            if (direr != ''):
                self._file_txt_var.set(direr)

    def _ch_proc_mode(self, *args):
        if (self._old_proc_mode == self._proc_mode.get()):
            return False
        else:
            self._old_proc_mode = self._proc_mode.get()
        if (self._old_proc_mode == 0):
            self._file_sd_var.set('')
            self._file_txt_var.set('')
        else:
            self._file_sd_var.set(os.path.split(self._file_sd_var.get())[0])
            self._file_txt_var.set(os.path.split(self._file_txt_var.get())[0])
        return True

    def translate_to(self, language):
        self._language = language
        for i in range(len(self._main_label)):  # 4
            self._main_label[i]["text"] = self.strings_lib[self._language][i]
        for i in range(len(self._main_button)):  # 2
            self._main_button[i]["text"] = self.strings_lib[self._language][i + 4]
        for i in range(len(self._proc_rdb)):  # 2
            self._proc_rdb[i]["text"] = self.strings_lib[self._language][i + 6]
        for i in range(len(self._filer_btn)):  # 2, но считается за 1.
            self._filer_btn[i]["text"] = self.strings_lib[self._language][8]
        # 9, 10, 11, 12 -- спецификации файлов...
        # 13-14 -- общая спецификация файлов.
        # 15 -- error, 16 -- encoding error.
        # 17, 18 -- ошибки файлов.
        # 19, 20 -- ошибки директорий.
        # 21, 22 -- невозможность создания файлов.
        # 23, 24 -- невозможность создания директорий.


class SLG_ScriptLaterFrame(SLG_MasterFrame):
    strings_lib = {
        "eng": (
            "Choose the decompilation mode:",
            "Choose the script folder:",
            "Choose the script name (without ext.):",
            "Choose the decompiled txt script or folder with them:",
            "Choose the encoding:",
            "Choose the version:",
            "Decompile!",
            "Compile!",
            "File",
            "Folder (File division)",
            "...",
            'Sd script',
            '*.sd',
            'All files',
            '*',
            'Text files',
            '*.txt',
            'Error',
            'There is no such encoding!',
            'Compiled and decompiled scripts names are the same!',
            'Both compiled and decompiled scripts are not exist!',
            'Both decompiled script folder and compiled script are not exist!',
            'Compiled and decompiled script folders are the same!',
            'It is impossible to create decompiled script with such name!',
            'It is impossible to create compiled script folder with such name!',
            'It is impossible to create decompiled script folder with such name!',
            'It is impossible to create compiled script with such name!'
        ),
        "rus": (
            "Выберите режим декомпиляции:",
            "Выберите папку со скриптом:",
            "Выберите название скрипта (без расш.):",
            "Выберите декомпилированный скрипт txt или папку с ними:",
            "Выберите кодировку:",
            "Выберите версию:",
            "Декомпилировать!",
            "Компилировать!",
            "Файл",
            "Папка (Разделение по файлам)",
            "...",
            'Скрипт sd',
            '*.sd',
            'Все файлы',
            '*',
            'Текстовые файлы',
            '*.txt',
            'Ошибка',
            'Такой кодировки не существует!',
            'Имена скриптов (компилированного и декомпилированного) совпадают!',
            'Как компилированного, так и декомпилированного скрипта не существует!',
            'Папки с декомпилированным скриптом не существует, как и компилированного скрипта!',
            'Папки компилированного и декомпилированного скрипта совпадают!',
            'Создать декомпилированный скрипт с таким названием невозможно!',
            'Создать папку с компилированными скриптами с таким названием невозможно!',
            'Создать папку с декомпилированным скриптом с таким названием невозможно!',
            'Создать компилированный скрипт с таким названием невозможно!'
        )
    }

    def __init__(self, master):
        super(SLG_ScriptLaterFrame, self).__init__(master)
        self.master = master
        self["background"] = 'white'
        self["relief"] = tk.RAISED
        self["borderwidth"] = 5

        self._language = ''
        self._script_dir = tk.StringVar()
        self._script_base = tk.StringVar()
        self._dec_scr = tk.StringVar()
        self._proc_mode = tk.IntVar()
        self._proc_mode.set(0)
        self._old_proc_mode = self._proc_mode.get()
        self._encoding = tk.StringVar()
        self._possible_encodings = SLG_Scripts_NEW.possible_encodings
        self._encoding.set(self._possible_encodings[0])
        self._version = tk.StringVar()
        poss_ver = []
        for i in SLG_Scripts_NEW.game_versions:
            strer = str(i[0]) + ' - '
            for k in i[1]:
                strer += k
                strer += ', '
            strer = strer[:-2] + '.'
            poss_ver.append(strer)
        poss_ver.pop(0)
        poss_ver = tuple(poss_ver)
        self._possible_versions = poss_ver

        self._main_label = []
        for i in range(6):  # режим обработки, .sd, .txt, кодировка.
            self._main_label.append(tk.Label(
                master=self,
                bg='white',
                font=('Helvetica', 10 + 2 * (int((i % 3) == 0)))
            ))
            self._main_label[i].place(relx=0.5 * int((i % 3) == 2),
                                      rely=0.2 * (i - int(i > 1) - int(i > 4)),
                                      relwidth=0.5 * (1 + int((i % 3) == 0)),
                                      relheight=0.1)

        self._main_button = []
        for i in range(2):  # Декомпилировать, компилировать.
            self._main_button.append(tk.Button(master=self,
                                               command=self,
                                               font=('Helvetica', 14)))
            self._main_button[i].place(relx=0.5 * i, rely=0.8, relwidth=0.5, relheight=0.2)
        self._main_button[0]["command"] = self._decompile_base
        self._main_button[1]["command"] = self._compile_base

        self._proc_rdb = []
        for i in range(2):
            self._proc_rdb.append(tk.Radiobutton(master=self,
                                                 background='white',
                                                 font=('Helvetica', 12),
                                                 variable=self._proc_mode,
                                                 value=i))
            self._proc_rdb[i].place(relx=0.0 + (0.5 * i), rely=0.1, relwidth=0.5, relheight=0.1)

        self._filer_txt = []  # 0 -- директория, 1 -- база, 2 -- выход.
        self._filer_btn = []
        for i in range(3):
            self._filer_txt.append(tk.Entry(
                master=self,
                font=('Helvetica', 8),
                borderwidth=5
            ))
            self._filer_btn.append(tk.Button(
                master=self,
                relief=tk.RAISED,
                font=('Helvetica', 14),
            ))
            modifier = 0.5 * (1 + int((i % 3) == 2))
            otter = 0.5 * int((i % 3) == 1)
            miner = 0.2 * int(i > 0)
            widther = 0.85
            self._filer_txt[i].place(relx=otter + modifier * 0.0, rely=0.3 + (0.2 * i) - miner,
                                     relwidth=modifier * widther, relheight=0.1)
            self._filer_btn[i].place(relx=otter + modifier * widther, rely=0.3 + (0.2 * i) - miner,
                                     relwidth=modifier * (1.0 - widther), relheight=0.1)
        self._filer_txt[0]["textvariable"] = self._script_dir
        self._filer_txt[1]["textvariable"] = self._script_base
        self._filer_txt[2]["textvariable"] = self._dec_scr
        self._filer_btn[0]["command"] = self._what_script_dir
        self._filer_btn[1]["command"] = self._what_script_base
        self._filer_btn[2]["command"] = self._what_dec_scr

        self._proc_mode.trace_add('write', self._ch_proc_mode)

        self._prm_txt = []  # 0 - кодировка.
        self._prm_cmb = []  # 1 - версия.
        for i in range(2):
            param = 0
            values = []
            if (i == 0):
                param = self._encoding
                values = self._possible_encodings
            else:
                param = self._version
                values = self._possible_versions
            self._prm_txt.append(tk.Entry(
                master=self,
                font=('Helvetica', 8),
                borderwidth=5,
                textvariable=param,
            ))
            self._prm_cmb.append(ttk.Combobox(
                master=self,
                font=('Helvetica', 10 + 2 * int(i == 0)),
                values=values,
                textvariable=param,
                state='readonly'
            ))
            wider = 0.5 * (1 - int(i == 1))
            modifier = 0.5
            morer = 1.0 * int((i % 2) == 1)
            if (i == 0):
                self._prm_txt[i].place(relx=modifier * (0.0 + morer), rely=0.7, relwidth=modifier * wider,
                                       relheight=0.1)
            self._prm_cmb[i].place(relx=modifier * (wider + morer), rely=0.7, relwidth=modifier * (1.0 - wider),
                                   relheight=0.1)
        self._version.trace_add('write', self._ch_ver)
        self._version.set(self._possible_versions[0])

    def _decompile_base(self):
        if (not (self._is_correct_data())):
            return False
        for i in self._main_button:
            i["state"] = tk.DISABLED
        DecompileEmAll = threading.Thread(target=self._decompile, args=(self._script_dir.get(),
                                                                        self._script_base.get(),
                                                                        self._dec_scr.get(),
                                                                        self._encoding.get(),
                                                                        float(self._version.get()),
                                                                        self._proc_mode.get()))
        print('Decompilation/Декомпиляция:', os.path.join(self._script_dir.get(), self._script_base.get()),
              '->', self._dec_scr.get())
        DecompileEmAll.start()
        return True

    def _decompile(self, sd_dir, sd_base, comper, encer, verser, procer):
        try:
            DecompileEmAll = SLG_Scripts_NEW(sd_dir, sd_base, encer, verser)
            DecompileEmAll.decompile(comper, procer)
            del DecompileEmAll
        except Exception as ex:
            SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17], str(ex))
        finally:
            for i in self._main_button:
                i["state"] = tk.NORMAL

    def _compile_base(self):
        if (not (self._is_correct_data())):
            return False
        for i in self._main_button:
            i["state"] = tk.DISABLED
        CompileEmAll = threading.Thread(target=self._compile, args=(self._script_dir.get(),
                                                                    self._script_base.get(),
                                                                    self._dec_scr.get(),
                                                                    self._encoding.get(),
                                                                    float(self._version.get()),
                                                                    self._proc_mode.get()))
        print('Compilation/Компиляция:', self._dec_scr.get(), '->',
              os.path.join(self._script_dir.get(), self._script_base.get()))
        CompileEmAll.start()
        return True

    def _compile(self, sd_dir, sd_base, comper, encer, verser, procer):
        try:
            DecompileEmAll = SLG_Scripts_NEW(sd_dir, sd_base, encer, verser)
            DecompileEmAll.compile(comper, procer)
            del DecompileEmAll
        except Exception as ex:
            SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17], str(ex))
        finally:
            for i in self._main_button:
                i["state"] = tk.NORMAL

    def _is_correct_data(self):
        is_comp_exist = os.path.isfile(os.path.join(self._script_dir.get(), self._script_base.get() + '.sd'))
        if (self._proc_mode.get() == 0):  # Файл.
            is_dec_exist = os.path.isfile(self._dec_scr.get())
            if ((not is_comp_exist) and (not is_dec_exist)):
                SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17],
                                               self.strings_lib[self._language][20])
                return False
            if (not is_dec_exist):
                out_dir = os.path.split(self._dec_scr.get())[0]
                try:
                    if (out_dir != ''):
                        os.makedirs(out_dir, exist_ok=True)
                    zlo = open(self._dec_scr.get(), 'w')
                    zlo.close()
                except:
                    SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17],
                                                   self.strings_lib[self._language][23])
                    return False
        else:  # Директория.
            is_dec_exist = os.path.isdir(self._dec_scr.get())
            if ((not is_comp_exist) and (not is_dec_exist)):
                SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17],
                                               self.strings_lib[self._language][21])
                return False
            if (not is_dec_exist):
                out_dir = self._dec_scr.get()
                try:
                    if (out_dir != ''):
                        os.makedirs(out_dir, exist_ok=True)
                except:
                    SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17],
                                                   self.strings_lib[self._language][25])
                    return False
        if (not (is_comp_exist)):
            try:
                if (self._script_dir.get() != ''):
                    os.makedirs(self._script_dir.get(), exist_ok=True)
            except:
                SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17],
                                               self.strings_lib[self._language][24])
                return False
            try:
                zlo = open(os.path.join(self._script_dir.get(), self._script_base.get() + '.sd'), 'wb')
                zlo.close()
            except:
                SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17],
                                               self.strings_lib[self._language][26])
                return False

        out_dir = os.path.split(self._dec_scr.get())[0]
        out_baser = os.path.split(self._dec_scr.get())[1].split('.')
        out_baser.pop()
        out_base = ''
        for i in out_baser:
            out_base += i + '.'
        out_base = out_base[:-1]
        if ((out_base == self._script_base.get()) and (out_dir == self._script_dir.get())):
            SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17],
                                           self.strings_lib[self._language][19])
            return False
        if (out_dir == self._script_dir.get()):
            SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17],
                                           self.strings_lib[self._language][22])
            return False
        try:
            codecs.lookup(self._encoding.get())
        except:
            SLGScriptTool_GUI.show_message(self, self.strings_lib[self._language][17],
                                           self.strings_lib[self._language][18])
            return False
        return True

    def _what_script_dir(self):
        direr = filedialog.askdirectory()
        if (direr != ''):
            self._script_dir.set(direr)

    def _what_script_base(self):
        ftypes = [(self.strings_lib[self._language][11], self.strings_lib[self._language][12]),
                  (self.strings_lib[self._language][13], self.strings_lib[self._language][14])]
        init_dir = os.getcwd()
        if ((self._script_dir.get() != '') and (os.path.isdir(self._script_dir.get()))):
            init_dir = self._script_dir.get()
        dialg = filedialog.Open(self, filetypes=ftypes, initialdir=init_dir)
        file = dialg.show()
        if (file != ''):
            direr = os.path.split(file)[0]
            self._script_dir.set(direr)
            zlo = os.path.split(file)[1]
            zler = zlo.split('.')
            zler.pop()
            zlo = ''
            for i in zler:
                zlo += i + '.'
            zlo = zlo[:-1]
            self._script_base.set(zlo)

    def _what_dec_scr(self):
        if (self._proc_mode.get() == 0):  # По файлу.
            ftypes = [(self.strings_lib[self._language][15], self.strings_lib[self._language][16]),
                      (self.strings_lib[self._language][13], self.strings_lib[self._language][14])]
            dialg = filedialog.Open(self, filetypes=ftypes, initialdir=os.getcwd())
            file = dialg.show()
            if (file != ''):
                self._dec_scr.set(file)
        else:  # По папке.
            direr = filedialog.askdirectory()
            if (direr != ''):
                self._dec_scr.set(direr)

    def _ch_proc_mode(self, *args):
        if (self._old_proc_mode == self._proc_mode.get()):
            return False
        else:
            self._old_proc_mode = self._proc_mode.get()
        if (self._old_proc_mode == 0):
            self._dec_scr.set('')
        else:
            self._dec_scr.set(os.path.split(self._dec_scr.get())[0])

    def _ch_ver(self, *args):
        self._version.set(self._version.get().split(' - ')[0])
        self._prm_txt[1].update()
        self._prm_cmb[1].update()

    def translate_to(self, language):
        self._language = language
        for i in range(len(self._main_label)):  # 6
            self._main_label[i]["text"] = self.strings_lib[self._language][i]
        for i in range(len(self._main_button)):  # 2
            self._main_button[i]["text"] = self.strings_lib[self._language][i + 6]
        for i in range(len(self._proc_rdb)):  # 2
            self._proc_rdb[i]["text"] = self.strings_lib[self._language][i + 8]
        for i in self._filer_btn:  # 1 (считается за).
            i["text"] = self.strings_lib[self._language][10]
        # 11, 12 -- main.sd.
        # 13, 14 -- все файлы.
        # 15, 16 -- текстовые файлы.
        # 17 -- ошибка.
        # 18 -- кодировка.
        # 19 -- совпадение имён.
        # 20, 21 -- взаимное отсутствие.
        # 22 -- та же папка.
        # 23, 24, 25, 26 -- невозможно создать.
