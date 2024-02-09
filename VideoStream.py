from threading import Thread
import cv2
import numpy as np


class VideoStream:
    def __init__(self, resolution=(640, 480), framerate=30, PiOrUSB=2, src=0):
        self.PiOrUSB = PiOrUSB

        if self.PiOrUSB == 1:  # PiCamera
            from picamera.array import PiRGBArray
            from picamera import PiCamera

            self.camera = PiCamera()
            self.camera.resolution = resolution
            self.camera.framerate = framerate
            self.rawCapture = PiRGBArray(self.camera, size=resolution)
            self.stream = self.camera.capture_continuous(
                self.rawCapture, format="bgr", use_video_port=True
            )
            self.frame = []

        elif self.PiOrUSB == 2:  # USB camera
            self.stream = cv2.VideoCapture(src)
            self.stream.set(3, resolution[0])
            self.stream.set(4, resolution[1])
            # self.stream.set(5, framerate)  # Uncomment if framerate setting is supported

            self.grabbed, self.frame = self.stream.read()

        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        if self.PiOrUSB == 1:  # PiCamera
            for f in self.stream:
                self.frame = f.array
                self.rawCapture.truncate(0)

                if self.stopped:
                    self.stream.close()
                    self.rawCapture.close()
                    self.camera.close()

        elif self.PiOrUSB == 2:  # USB camera
            while True:
                if self.stopped:
                    self.stream.release()
                    return

                self.grabbed, self.frame = self.stream.read()

    def read(self):
        # Check if the frame is None
        if self.frame is None:
            print("No Frame")
            return (
                None  # Return None or a placeholder image if the frame is not available
            )

        # Apply the VR effect to the frame before returning it
        try:
            # Resize the frame to 960x540 to maintain a 16:9 aspect ratio
            resized_frame = cv2.resize(self.frame, (960, 540))

            # Concatenate the two resized frames to create the VR effect
            vr_frame = np.concatenate((resized_frame, resized_frame), axis=1)

            # Since the concatenated frame is 1920x540, we need to add black borders
            # on the top and bottom to fill the 1920x1080 screen
            top_border_width = (1080 - 540) // 2
            bottom_border_width = 1080 - 540 - top_border_width
            vr_frame_with_borders = cv2.copyMakeBorder(
                vr_frame,
                top_border_width,
                bottom_border_width,
                0,
                0,
                cv2.BORDER_CONSTANT,
                value=[0, 0, 0],
            )

            return vr_frame_with_borders
        except Exception as e:
            print(f"Error applying VR effect: {e}")
            return self.frame  # Return the original frame in case of any error

    def stop(self):
        self.stopped = True
