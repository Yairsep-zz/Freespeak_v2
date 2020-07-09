import cv2
from PyQt5.QtCore import QThread
import logging
from videoWriter import VideoWriter

# Code to thread reading camera input.
# Source : Adrian Rosebrock
# https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/


class VideoReader(QThread):
    def __init__(self, src, width, height):
        super().__init__()
        self.src = src
        self.width = width
        self.height = height

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.running = False

        logging.info('opening video capture device')
        # start recording device
        self.stream = cv2.VideoCapture(self.src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        (self.grabbed, frame) = self.stream.read()
        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.width, self.height = self.size()

        # start writing device
        self.videoWriter = VideoWriter(self.width, self.height)
        self.recording = False

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    def run(self):
        logging.info('videoReader started')
        self.running = True
        while self.running and self.stream.isOpened():
            (self.grabbed, frame) = self.stream.read()
            if self.grabbed and self.recording:
                self.videoWriter.writeFrame(frame)
            self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def read(self):
        # return the frame most recently read
        return self.frame

    def size(self):
        # return size of the capture device
        return self.stream.get(cv2.CAP_PROP_FRAME_WIDTH), self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def fps(self):
        return self.stream.get(cv2.CAP_PROP_FPS)

    def stop(self):
       # indicate that the thread should be stopped
       self.running = False
       self.stopRecording()
       self.stream.release()
       logging.info('videoReader stopped')

    def startRecording(self):
        self.videoWriter.startRecording(self.fps())
        self.recording = True

    def stopRecording(self):
        self.recording = False
        self.videoWriter.stopRecording()

if __name__ == "__main__":
    # Test the Video Reader
    with VideoReader(src=cv2.CAP_ANY, width=300, height=200) as videoReader:
        while True:
            cv2.imshow('frame',videoReader.read())
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
