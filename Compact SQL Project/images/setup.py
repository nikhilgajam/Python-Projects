import sys
from cx_Freeze import setup, Executable
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], 'include_files': ["tcl86t.dll", "tk86t.dll"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
if sys.platform == "win32":
    pass
options = {
    'build_exe': {
        'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
        ],
    },
}

setup(  name = "Compact SQL",
        version = "1.0",
        description = "SQLLITE 3 based terminal",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Compact SQL.py", icon='images\icon.ico')])
