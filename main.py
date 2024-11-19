import os
import sys
import tkinter as tk
from gui.main_window import MainWindow

def check_environment():
    print("=== Environment Information ===")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"PATH environment: {os.environ.get('PATH', 'Not set')}")
    print("============================")

def check_tcl_tk():
    print(f"Python version: {sys.version}")
    print(f"Tkinter version: {tk.TkVersion}")
    print(f"TCL_LIBRARY: {os.environ.get('TCL_LIBRARY', 'Not set')}")
    print(f"TK_LIBRARY: {os.environ.get('TK_LIBRARY', 'Not set')}")
    
    tcl_lib = os.path.join(sys.prefix, 'tcl', 'tcl8.6')
    tk_lib = os.path.join(sys.prefix, 'tcl', 'tk8.6')
    
    if os.path.exists(tcl_lib) and os.path.exists(tk_lib):
        os.environ['TCL_LIBRARY'] = tcl_lib
        os.environ['TK_LIBRARY'] = tk_lib
    else:
        print("Warning: Tcl/Tk libraries not found in expected location")

def main():
    check_environment()
    check_tcl_tk()
    try:
        root = tk.Tk()
        app = MainWindow(root)
        root.mainloop()
    except tk.TclError as e:
        print(f"Tkinter error: {e}")
        print("Tcl/Tk installation might be incomplete or incorrect.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()