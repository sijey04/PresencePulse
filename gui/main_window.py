import tkinter as tk
from tkinter import ttk
from gui.attendance_window import AttendanceWindow

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Smart Attendance System")
        self.master.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        ttk.Button(self.master, text="Take Attendance", command=self.open_attendance).pack(pady=20)
        ttk.Button(self.master, text="Exit", command=self.master.quit).pack(pady=20)

    def open_attendance(self):
        try:
            attendance_window = tk.Toplevel(self.master)
            attendance_window.protocol("WM_DELETE_WINDOW", lambda: self.cleanup_attendance(attendance_window))
            AttendanceWindow(attendance_window)
        except Exception as e:
            print(f"Error opening attendance window: {e}")

    def cleanup_attendance(self, window):
        try:
            window.destroy()
        except Exception as e:
            print(f"Error cleaning up attendance window: {e}")

