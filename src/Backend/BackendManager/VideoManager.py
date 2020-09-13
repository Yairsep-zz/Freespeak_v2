import logging
import datetime
import cv2
import time

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

from Backend.Recording.VideoRecorder.VideoReader import VideoReader
from Backend.Analysis.VideoAnalysis.HandPositionsAnalysis import HandDetector
from Backend.Analysis.VideoAnalysis.FaceEmotionsAnalysis import FaceEmotionDetector
from Backend.Analysis.Utils.CsvWriter import CsvWriter

class VideoManager(QThread):
  changePixmap = pyqtSignal(QImage)
  def __init__(self):
    super().__init__()
    self.queue_size = 5
    self.height = 200
    self.width = 300
    self.showFps = True
    self.video_source = cv2.CAP_ANY

    self.running = False
    self.recording = False

    #self.changePixmap = pyqtSignal(QImage)

    logging.info('Initializing VideoReader.....')
    self.video_capture = VideoReader(
            src=self.video_source, width=self.width, height=self.height)
    self.width, self.height = self.video_capture.size()
    print("VideoManager initialized/started.......")

    logging.info('opening csv writers')
    self.handPositionsWriter = CsvWriter('handPositions.csv', ["Time", "x", "y"])
    self.emotionsWriter = CsvWriter('emotions.csv', ["Time", "Emotions"])

    logging.info('opening faceEmotionDetector')
    self.faceEmotionDetector = FaceEmotionDetector('resources/face_emotions_analysis_resources/')


  def connectEvents(self, videoFrameEvent):
    self.changePixmap.connect(videoFrameEvent)

  def startRecording(self):
    logging.info('VideoManager starting recording')
    self.recording = True
    self.handPositionsWriter.start()
    self.emotionsWriter.start()
    self.video_capture.startRecording()

  def stopRecording(self):
    self.recording = False
    self.handPositionsWriter.stop()
    self.emotionsWriter.stop()
    self.video_capture.stopRecording()
    logging.info('VideoManager recording stopped')

  def run(self):
    logging.info('Starting VideoReader (second thread)')
    self.video_capture.start()

    # start_time = datetime.datetime.now()
    # num_frames = 0
    # fps = 0
    # index = 0
    handDetector = HandDetector(self.height, self.width)
    self.running = True
    while self.running:
        frame = self.video_capture.read()
        frame = cv2.flip(frame, 1)
        # index += 1

        # elapsed_time = (datetime.datetime.now() -
        #                 start_time).total_seconds()
        # num_frames += 1
        # fps = num_frames / elapsed_time #TODO: division by zero
        # print("frame ",  index, num_frames, elapsed_time, fps)

        handPositions = handDetector.detect(frame)
        emotions = self.faceEmotionDetector.detect(frame)

        if self.recording:
           self.handPositionsWriter.writerows(handPositions)
           self.emotionsWriter.writerows(emotions)

        if (frame is not None):
            # if (self.showFps):
            #     detector_utils.draw_fps_on_image("FPS : " + str(int(fps)),
            #
            time.sleep(0.5)
            h, w, ch = frame.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(
                frame.data, w, h, bytesPerLine, QImage.Format_RGB888)
            self.changePixmap.emit(convertToQtFormat)
        else:
            logging.warning('None Frame was read!')
            break

  # def stop(self):
  #     self.handPositionsWriter.stop()
  #     self.emotionsWriter.stop()
  #     self.video_capture.stop()

  #     self.running = False
  #     logging.info('videoAdapter stopped')
