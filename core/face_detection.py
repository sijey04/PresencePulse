import cv2
import numpy as np

class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Try different camera indices and backends
        camera_indices = [0, 1]
        backends = [cv2.CAP_DSHOW, cv2.CAP_ANY]
        
        self.video_capture = None
        self.current_faces = []
        
        for index in camera_indices:
            for backend in backends:
                try:
                    cap = cv2.VideoCapture(index, backend)
                    if cap.isOpened():
                        # Set camera properties for better quality
                        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                        cap.set(cv2.CAP_PROP_FPS, 30)
                        
                        self.video_capture = cap
                        print(f"Successfully opened camera {index} with backend {backend}")
                        return
                    cap.release()
                except Exception as e:
                    print(f"Failed to open camera {index} with backend {backend}: {str(e)}")
        
        if self.video_capture is None:
            raise RuntimeError("Could not initialize any camera")

    def get_frame(self):
        if self.video_capture is None:
            return self._create_error_frame("No camera available")
        
        ret, frame = self.video_capture.read()
        if not ret:
            return self._create_error_frame("Failed to capture frame")
        
        try:
            # Improve face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)  # Improve contrast
            
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            self.current_faces = faces
            
            # Draw rectangles and add face count
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, 'Face', (x, y-10), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Add face count to frame
            cv2.putText(frame, f'Faces: {len(faces)}', (10, 30), 
                      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        except Exception as e:
            print(f"Error processing frame: {str(e)}")
            return self._create_error_frame(str(e))

    def get_face_count(self):
        return len(self.current_faces)

    def _create_error_frame(self, error_message):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(frame, error_message, (50, 240), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return frame

    def __del__(self):
        if self.video_capture is not None:
            self.video_capture.release()

