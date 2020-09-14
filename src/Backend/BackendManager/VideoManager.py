import logging
import datetime
import cv2
import time
import os

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QThread, QMutex, QWaitCondition
from PyQt5.QtGui import QImage, QPixmap

from Backend.Recording.VideoRecorder.VideoReader import VideoReader
from Backend.Analysis.VideoAnalysis.HandPositionsAnalysis import HandDetector
from Backend.Analysis.VideoAnalysis.FaceEmotionsAnalysis import FaceEmotionDetector
from Backend.Analysis.Utils.CsvWriter import CsvWriter

class VideoManager(QThread):
  changePixmap = pyqtSignal(QImage)
  def __init__(self, mutex, condition):
    super().__init__()
    self.queue_size = 5
    self.height = 200
    self.width = 300
    self.showFps = True
    self.video_source = cv2.CAP_ANY

    self.mutex = mutex
    self.condition = condition

    self.running = False
    self.recording = False

    logging.info('Initializing VideoReader.....')
    self.video_capture = VideoReader(
            src=self.video_source, width=self.width, height=self.height)
    self.width, self.height = self.video_capture.size()
    print("VideoManager initialized/started.......")

    logging.info('Initializing csv writers.....')
    self.handPositionsWriter = CsvWriter('handPositions.csv', ["Time", "x", "y"])
    self.emotionsWriter = CsvWriter('emotions.csv', ["Time", "Emotions"])

    logging.info('Initializing faceEmotionDetector.....')

    self.faceEmotionDetector = FaceEmotionDetector(os.path.join('resources', 'face_emotions_analysis_resources'))
    self.handDetector = HandDetector(self.height, self.width)

  def connectEvents(self, videoFrameEvent):
    self.changePixmap.connect(videoFrameEvent)

  def startRecording(self):
    logging.info('VideoManager starting recording')
    self.recording = True
    logging.info('Starting hand positions csv writer......')
    self.handPositionsWriter.start()
    logging.info('Starting emotions csv writer......')
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

    start_time = datetime.datetime.now()
    num_frames = 0
    fps = 0
    index = 0

    self.running = True
    while self.running:
        frame = self.video_capture.read()
        frame = cv2.flip(frame, 1)
        index += 1

        handPositions = self.handDetector.detect(frame)
        emotions = self.faceEmotionDetector.detect(frame)

        if self.recording:
           self.handPositionsWriter.writerows(handPositions)
           self.emotionsWriter.writerows(emotions)

        elapsed_time = (datetime.datetime.now() -
                        start_time).total_seconds()
        num_frames += 1
        fps = num_frames / elapsed_time #TODO: division by zero
        # print("frame ",  index, num_frames, elapsed_time, fps)

        if (frame is not None):
            if (self.showFps):
               self.handDetector.show_fps(fps, frame)

            h, w, ch = frame.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(
                frame.data, w, h, bytesPerLine, QImage.Format_RGB888)

            self.changePixmap.emit(convertToQtFormat)
            self.condition.wait(self.mutex)
        else:
            logging.warning('None Frame was read!')
            break

  # def stop(self):
  #     self.handPositionsWriter.stop()
  #     self.emotionsWriter.stop()
  #     self.video_capture.stop()

  #     self.running = False
  #     logging.info('videoAdapter stopped')
