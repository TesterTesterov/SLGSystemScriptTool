# SLGSystemScriptTool
## English

Dual languaged GUI tool for (de)compiling and (de/en)crypting (with key finding) scripts of SLG System engine. Supports all known versions of SLG System: 0, 1, 2, 3 (3.0, 3.1), 4 (4.0, 4.1), but may lack of support of some it's variations. If this tool does not support a game, write an "Issue" here with attached unsupported scripts and highlighting the game name. With this tool you can: decompile and compile script of SLG System, (en/de)crypt script of any game on SLG System, find key of any game on SLG System via cryptoattack.

It has following features:
- Help module.
- Crypto module (for (en/de)cryptions and cryptoattacks).
- Scripts version 0 module (separate module because version 0 scripts are too different from the rest).
- Script older versions module.

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



## Russian


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
