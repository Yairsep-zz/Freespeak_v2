import cv2
import logging

class VideoWriter():
    def __init__(self, width, height):
      self.frameCount = 0
      self.fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
      self.width = width
      self.height = height
      self.open = False

    def writeFrame(self, frame):
      if self.open:
        self.videoOut.write(frame)

    def startRecording(self, fps):
        logging.info('videoWriter starting recording')
        #TODO: change destination path to resources/raw_data
        self.videoOut = cv2.VideoWriter('output.avi', self.fourcc, fps, (int(self.width),int(self.height)))
        self.open = True

    def stopRecording(self):
        self.open = False
        self.videoOut.release()
        logging.info('videoWriter stopped recording')
