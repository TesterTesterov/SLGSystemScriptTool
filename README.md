# SLGSystemScriptTool
## English

Dual languaged GUI tool for (de)compiling and (de/en)crypting (with key finding) scripts of SLG System engine. Supports all known versions of SLG System: 0, 1, 2, 3 (3.0, 3.1), 4 (4.0, 4.1), but may lack of support of some it's variations. If this tool does not support a game, write an "Issue" here with attached unsupported scripts and highlighting the game name. With this tool you can: decompile and compile script of SLG System, (en/de)crypt script of any game on SLG System, find key of any game on SLG System via cryptoattack.

It has following features:
- Help module.
- Crypto module (for (en/de)cryptions and cryptoattacks).
- Scripts version 0 module (separate module because version 0 scripts are too different from the rest).
- Script older versions module.

For data editing see [SLGSystemDataTool](https://github.com/TesterTesterov/SLGSystemDataTool).

### Tested with
- [Shihen 69 \~Shin'en no Messiah\~](https://vndb.org/v1117)
- [Sangoku Hime \~Ransei, Tenka Sanbun no Kei\~ Renewal](https://vndb.org/r37064)
- [Sengoku Hime \~Senran no Yo ni Honoo Tatsu\~](https://vndb.org/v1120)
- [Sengoku Hime 2 \~Senran no Yo, Gun'yuu Arashi no Gotoku\~](https://vndb.org/v3071)
- [Sengoku Hime 3 \~Tenka o Kirisaku Hikari to Kage\~](https://vndb.org/v6763)
- [Sengoku Hime 4 \~Souha Hyakkei, Hana Mamoru Chikai\~](https://vndb.org/v11237)
- [Sengoku Hime 5 \~Senka Tatsu Haou no Keifu\~](https://vndb.org/v13636)
- [Sengoku Hime 6 \~Tenka Kakusei, Shingetsu no Kirameki\~](https://vndb.org/v16629)

## Russian

Двуязычное средство с графическим интерфейсом пользователя для (де)компилирования и (рас)шифровки (с нахождением ключей) скриптов движка SLG System. Поддерживает все известные версии SLG System: 0, 1, 2, 3 (3.0, 3.1), 4 (4.0, 4.1), хотя может и не поддерживать некоторые их вариации. Коль средство не поддерживает какую-то игру, пишите в "Issues" к сему средству, приложив скрипты и указав игру. С сим средством вы можете: декомпилировать и компилировать скрипты SLG System, (рас)шифровывать скрипты любых игр, находить ключ любой игры на SLG System посредством криптоатаки.

У неё есть следующие функции:
- Справочный модуль.
- Криптографический модуль (для (рас)шифровки и криптоатак).
- Модуль для работы со скриптами версии 0 (отдельный модуль, понеже скрипты версии 0 слишком отличаются от остальных).
- Модуль для работы со скриптами более старых версий.

С работы с форматами данных движка используйте [SLGSystemDataTool](https://github.com/TesterTesterov/SLGSystemDataTool).

### Протестировано с
- [Псалтырь 69: Мессия пустоты](https://vndb.org/v1117)
- [Принцессы Троецарствия: Неспокойные времена, план Трёх царств (Обновлённая версия)](https://vndb.org/r37064)
- [Принцессы Сэнгоку: Огни мира войны](https://vndb.org/v1120)
- [Принцессы Сэнгоку 2: В мире войны буря бушует меж феодалами](https://vndb.org/v3071)
- [Принцессы Сэнгоку 3: Свет и тьма рассекают мир](https://vndb.org/v6763)
- [Принцессы Сэнгоку 4: Все средства для победы, клятва защитить цветы](https://vndb.org/v11237)
- [Принцессы Сэнгоку 5: Родословная правителя, потушившего пламя войны](https://vndb.org/v13636)
- [Принцессы Сэнгоку 6: Пробуждение державы, блеск новой Луны](https://vndb.org/v16629)

# Usage / Использование
## English

### Cryptoattack
1. Start the tool.
2. Go to "Crypto Module" and focus on the right half of the screen.
3. Choose the main.sd **(and only the main.sd!)** script.
4. Choose the output text file (with the cryptoattack result).
5. Choose the attack type. Almost all games are weak for "2 0 0 2 0", but an earlier games may be weak for "2 0 2 0 0". **There is only one possible type for each main.sd!**
6. Choose the attack mode of operation -- find only one possible key (may not work depending on settings) or all.
7. Choose the attack mode of attack. Earlier games (elder of version 2 and version 3) use second (i-(key>>16)&0xff), but version 4 games use first (i^(key&0xff)).
8. Run it! **If you picked attack mode and type correctly, you'll likely get first correct key in 1 minute!** If you can't get any key in 5 minutes, just try other settings.

![0eng](https://user-images.githubusercontent.com/66121918/126317326-cf0989f0-eda1-4ce0-af9d-67a753a7041a.JPG)

### (En/de)cryption
1. Start the tool.
2. Go to "Crypto Module" and focus on the left half of the screen.
3. Choose the processing mode (per file or per folder).
4. Choose the input and output files or folders.
5. Choose the key. You can choose known key in the ComboBox vidjet, but also can write your own key **(in hex form!)**
6. Choose the encryption mode. Earlier games (elder of version 2 and version 3) scripts use second (i-(key>>16)&0xff), but version 4 games use first (i^(key&0xff)). Almost all supplement data files use the first mode.
7. Run it! Soon it will be (de/en)crypted...

![1eng](https://user-images.githubusercontent.com/66121918/126318751-1d82a0d0-d7ea-437d-8b32-186a27a47689.JPG)

### Version 0 Script (De)compilation
1. Start the tool.
2. Go to "0-Version Script".
3. Choose the processing mode (per file or per folder).
4. Choose the input and output files or folders.
5. Choose the encoding (of both script and decompiled file). If you want to create script with different encoding, just decompile it with old encoding, change encoding of decompiled script (txt) and create a new script with new encoding.
6. Run it! Soon it will be (de)compiled...

![2eng](https://user-images.githubusercontent.com/66121918/126334134-ea4b75ab-987a-42c5-90af-e391358cda82.JPG)

### Other Versions Script (De)compilation
1. Start the tool.
2. Go to "1+ Versions Scripts".
3. Choose the decompilation mode (to file or to folder). This mode is also complitation mode: from file or from folder.
4. Choose the script folder and base (name of script files without extension). You may want to click at "..." button at the right of "script name" field and choose the ".sd" script, and boyh name without extension and folder will be filled authomatically.
5. Choose the decompiled txt script file or folder. Do note, even if you decompile it to one file, there will be some technical files starting "__" in the same folder.
6. Choose the encoding (of both script and decompiled file). If you want to create script with different encoding, just decompile it with old encoding, change encoding of decompiled script (txt) and create a new script with new encoding.
7. Choose the version via ComboBox vidget.
8. Run it! Soon it will be (de)compiled... But, to be fair, even if commonly (de)compilation takes about 1 minute, compilation from multiple files (from a folder) takes several minutes.

![3eng](https://user-images.githubusercontent.com/66121918/126354852-13e86389-5889-4567-9a25-2f0d2e4384cf.JPG)

## Russian

### Криптоатаки
1. Запустите средство.
2. Перейдите во вкладку "Криптомодуль" и сосредоточьте взгляд на правой части экрана.
3. Выберите скрипт main.sd **(обязательно скрипт именно с таким названием!)**
4. Выберите выходной текстовый файл (для вывода результатов криптоатаки).
5. Выберите тип атаки. Обычно все игры уязвимы пред "2 0 0 2 0", но ранние могут быть уязвимы лишь пред "2 0 2 0 0". **Для каждого main.sd есть лишь один корректный тип криптоатаки!**
6. Выберите режим обработки атаки -- находить один возможный ключ (что может и не работать в зависимости от настроек) иль все.
7. Выберите режим собственно атаки. В ранних играх (версии 3 и поздние 2-й версии) используйте второй (i-(key>>16)&0xff), но для тех, что на 4, первый -- (i^(key&0xff)).
8. Запускайте! **Коль вы выбрали правильные режим и тип атаки, то скорее всего получите первый корректный ключ аж за минуту!** Коль не можете получить никакого ключа за 5 минут, просто попробуйте иные настройки.

![0rus](https://user-images.githubusercontent.com/66121918/126317942-0f711f4e-a7d8-4848-aec2-14aaed99545e.JPG)

### (Рас)шифрование
1. Запустите средство.
2. Перейдите на вкладку "Криптомодуль" и сосредоточьте взгляд на левой части экрана.
3. Выберите режим обработки (по файлу или по папке).
4. Выберите входные и выходные файлы или папки.
5. Выберите ключ. Можно как выбрать уже известный ключ с помощью виджета ComboBox, так и написать свой **(в шестнадцатеричной форме!)**
6. Выберите режим шифрования. В ранних играх (версии 3 и поздние 2-й версии) используйте второй (i-(key>>16)&0xff), но для тех, что на 4, первый -- (i^(key&0xff)). Почти все файлы вспомогательных структур данных используют первый режим.
7. Запускайте! Вскоре нужное будет (рас)шифровано...

![1rus](https://user-images.githubusercontent.com/66121918/126319073-48f41471-5955-47f2-ba77-28dd122bd4e2.JPG)

### (Де)компиляция скриптов версии 0
1. Запустите средство.
2. Перейдите на вкладку "Скрипт версии 0".
3. Выберите режим обработки (по файлу или по папке).
4. Выберите входные и выходные файлы или папки.
5. Выберите кодировку (что применяется как для компилированного скрипта, так и декомпилированного txt). Ежели вы хотите сменить кодировку скрипта, то сперва декомпилируйте скрипт со старой, затем измените кодировку полученного текстового файла и создайте скрипт с новой кодировкой.
6. Запускайте! Вскоре нужное будет (де)компилировано...

![2rus](https://user-images.githubusercontent.com/66121918/126334424-0bef5941-b941-4f2b-af96-4c38a85a43f7.JPG)

### (Де)компиляция скриптов остальных версий
1. Запустите средство.
2. Перейдите на вкладку "Скрипты версий 1+".
3. Выберите режим рекомпиляции (в файл или папку). Сей режим также относится и к компиляции: из файла иль из папки.
4. Выберите папку и основу имени скрипта (имя скрипта без расширения). Может быть удобно кликнуть на кнопку "..." с правой части подраздела "имени скрипта" и выбрать скрипт ".sd", после чего папка и основа имени скрипта будет заполнены автоматически.
5. Выберите файл или папку декомпилированного скрипта в текстовом формате. Заметьте, что, даже ежели вы декомпилируете скрипт в один файл, в той же директории появятся технические файлы, имена коих начинаются с "__".
5. Выберите кодировку (что применяется как для компилированного скрипта, так и декомпилированного txt). Ежели вы хотите сменить кодировку скрипта, то сперва декомпилируйте скрипт со старой, затем измените кодировку полученного текстового файла и создайте скрипт с новой кодировкой.
8. Посредством виджета ComboBox выберите версию.
9. Запускайте! Вскоре нужное будет (де)компилировано... Хотя, справедливости ради, если обычно (де)компиляция выполняется примерно за минуту, то компиляция из множества файлов (из папки) может занять уже несколько минут.

![3rus](https://user-images.githubusercontent.com/66121918/126354889-764c8e56-a6b6-47c1-b9ff-f897ee99ed10.JPG)

# Line and Message Breaks Help / Помощь по организации переносов по строкам и сообщениям
Sometimes there could be a very big problem: text may not fully get in textbox. But with this tool thou don't need to cut some part of text, no. Thou can use line and message breaks. Methods are below.
### For line breaks insert in the current message this.
```
\n
```
### For message breaks duplicate the message command and "WAIT_FOR_CLICK" (if existed). It's preferable to edit "postcommand args", but not mandatory. It has worked in my tests even without editing them.
### Example below is from Sengoku Hime 4.
Old code.
```
#1: ["MESSAGE", 159, 43]
[
    "*",
    "**",
    "？？？",
    [
        "GROUP",
        [
            "「追加ができたぞー♪　皆、どんどん食べてくれ」",
            0,
            0,
            -4276546,
            -1
        ]
    ]
]
#1: ["WAIT_FOR_CLICK", 159, 45]
[]
```
New code.
```
#1: ["MESSAGE", 159, 43]
[
    "*",
    "**",
    "？？？",
    [
        "GROUP",
        [
            "「追加ができたぞー♪　皆、どんどん食べてくれ」",
            0,
            0,
            -4276546,
            -1
        ]
    ]
]
#1: ["WAIT_FOR_CLICK", 159, 44]
[]
#1: ["MESSAGE", 159, 45]
[
    "*",
    "**",
    "？？？",
    [
        "GROUP",
        [
            "「追加ができたぞー♪　皆、どんどん食べてくれ」",
            0,
            0,
            -4276546,
            -1
        ]
    ]
]
#1: ["WAIT_FOR_CLICK", 159, 46]
[]
```

## На русском
Иногда можно столкнуться с одной большой-пребольшой проблемой: текст может не полностью влезать в текстовое окно. Однако, с сим средством вам не нужно обрезать его, отнюдь. Вы можете организовывать переносы по строкам и сообщениям. Методы указаны ниже.
### Для переносов по строкам добавьте в текущее сообщение следующее.
```
\n
```
### Для переносов по сообщениям продублируйте текущую команду сообщения и "WAIT_FOR_CLICK" (при наличии). Рекомендуется также изменить т.н. "посткомандные аргументы", но это не обязательно, так как в моих тестах работало и без изменений их.
### Пример ниже представлен для Принцесс Сэнгоку 4.
Старый код.
```
#1: ["MESSAGE", 159, 43]
[
    "*",
    "**",
    "？？？",
    [
        "GROUP",
        [
            "「追加ができたぞー♪　皆、どんどん食べてくれ」",
            0,
            0,
            -4276546,
            -1
        ]
    ]
]
#1: ["WAIT_FOR_CLICK", 159, 45]
[]
```
Новый код.
```
#1: ["MESSAGE", 159, 43]
[
    "*",
    "**",
    "？？？",
    [
        "GROUP",
        [
            "「追加ができたぞー♪　皆、どんどん食べてくれ」",
            0,
            0,
            -4276546,
            -1
        ]
    ]
]
#1: ["WAIT_FOR_CLICK", 159, 44]
[]
#1: ["MESSAGE", 159, 45]
[
    "*",
    "**",
    "？？？",
    [
        "GROUP",
        [
            "「追加ができたぞー♪　皆、どんどん食べてくれ」",
            0,
            0,
            -4276546,
            -1
        ]
    ]
]
#1: ["WAIT_FOR_CLICK", 159, 46]
[]
```

# Some information about SLG System engine / Некоторая информация про движок SLG System
## English

SLG System Engine is not very popular, but also not very obsqure engine, used in Gesen 18 (may be not only whose) games. It's in fact some sort of modified Tenka Touitsu ADVANCE engine. There are a lot of good visual novels and jRPG's uses it, such as Sengoku Hime and Sankoku Hime series.

Oldest versions of it, such as Shihen 69's version or version "0", does use just a simple script .sd. Older versions does use multicomponent script from a group of files, that differ depending of the game version. The main file of it is .sd, but you cannot simply edit only one this file, because it will break offset-links between files and so the game won't run correctly. You need to edit all files synchronically and reflect changes in one file in others.

Since third version of the engine (or even the latest games of second version) commonly use DRM and the scripts and files of supplement structures encryption.

## Русский

SLG System является не слишком популярным, но и не слишком неизвестным движком, используемым в играх Gesen 18 и, вероятно, Unicorn-A. На самом деле является своего рода модификацией движка Тэнка то:ицу ADVANCE. На нём написано немало сдобный визуальных новелл и японских ролевых игр (jRPG), например серии Принцессы Сэнгоку и Принцессы Троецарствия.

Версия "0" данного движка используют однофайловые скрипты .sd, более поздние -- многокомпонентные скрипты из ряда файлов, которые меняются зависимости от версий и число которых обычно составляет от 9 до 11, причём все файлы связаны. Главным файлом таких многокомпонентных скриптов является .sd, хотя работать только с одним сим файлом, не меняя другие в соответствии со сделанными изменениями, нельзя, так как связность между ними сломается и игра не будет работать корректно.

Игры на движке, начиная с третьей версии (или даже последних игр второй версии) обычно содержат технические средства защиты цифровых прав, DRM, а также шифрование скриптов и файлов вспомогательных структур данных.
