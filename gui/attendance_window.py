import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from core.face_detection import FaceDetector

class AttendanceWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Take Attendance")
        self.master.geometry("640x520")
        self.face_detector = FaceDetector()
        self.photo = None
        self.detected_faces = []
        self.attendance_status = tk.StringVar(value="Ready to mark attendance")
        self.create_widgets()
        self.update()
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        camera_frame = ttk.Frame(self.master)
        camera_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.canvas = tk.Canvas(camera_frame, width=640, height=480)
        self.canvas.pack()

        controls_frame = ttk.Frame(self.master)
        controls_frame.pack(fill=tk.X, pady=5, padx=10)

        self.status_label = ttk.Label(controls_frame, textvariable=self.attendance_status)
        self.status_label.pack(side=tk.LEFT, padx=5)

        ttk.Button(controls_frame, text="Mark Attendance", 
                  command=self.mark_attendance).pack(side=tk.RIGHT, padx=5)
        ttk.Button(controls_frame, text="Reset", 
                  command=self.reset_attendance).pack(side=tk.RIGHT, padx=5)

    def update(self):
        try:
            frame = self.face_detector.get_frame()
            if frame is not None:
                self.detected_faces = self.face_detector.get_face_count()
                self.update_status()
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.master.after(33, self.update)
        except Exception as e:
            print(f"Error in update loop: {e}")
            self.attendance_status.set(f"Error: {str(e)}")
            self.master.after(33, self.update)

    def update_status(self):
        if self.detected_faces:
            self.attendance_status.set(f"Detected {self.detected_faces} face(s)")
        else:
            self.attendance_status.set("No faces detected")

    def mark_attendance(self):
        if not self.detected_faces:
            self.attendance_status.set("No faces detected to mark attendance")
            return
        
        try:
            # Here you would add code to save attendance to database
            self.attendance_status.set(f"Attendance marked for {self.detected_faces} person(s)")
        except Exception as e:
            self.attendance_status.set(f"Error marking attendance: {str(e)}")

    def reset_attendance(self):
        self.detected_faces = []
        self.attendance_status.set("Ready to mark attendance")

    def on_closing(self):
        if hasattr(self, 'face_detector'):
            del self.face_detector
        self.master.destroy()

