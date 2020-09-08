import cv2
import logging
import pathlib
import os.path

class VideoWriter():
    def __init__(self, width, height):
      self.frameCount = 0
      self.fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
      self.width = width
      self.height = height
      self.open = False
      self.outputPath = os.path.abspath(__file__ + "/../../../../../") + '/resources/raw_data/'

    def writeFrame(self, frame):
      if self.open:
        self.videoOut.write(frame)

    def startRecording(self, fps):
        logging.info('videoWriter starting recording')
        self.videoOut = cv2.VideoWriter(self.outputPath + 'output.avi', self.fourcc, fps, (int(self.width),int(self.height)))
        self.open = True

    def stopRecording(self):
        self.open = False
        self.videoOut.release()
        logging.info('videoWriter stopped recording')
