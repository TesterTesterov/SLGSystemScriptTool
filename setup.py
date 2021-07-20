import sys
import cx_Freeze

base = None 

if (sys.platform == 'win32'):
    base = "Win32GUI"


executables = [cx_Freeze.Executable("main.py",
                                    shortcutName="SLGSystemDataTool",
                                    shortcutDir="SLGSystemDataTool")]

cx_Freeze.setup(
        name="Name",
        version="1.0",
        description="Dual language GUI tool for (de)compiling and (de/en)crypting (with key finding) scripts of SLG "
                "System engine.\nДвуязычное средство с графическим интерфейсом для (де)компилирования и (рас)шифровки "
                "(с нахождением ключей) скриптов движка SLG System.",
        options={"build_exe": {"packages": ["os", "sys", "tkinter", "locale", "ctypes", "threading", "codecs",
                                            "struct", "time", "json", "copy"]}},
        executables=executables
)