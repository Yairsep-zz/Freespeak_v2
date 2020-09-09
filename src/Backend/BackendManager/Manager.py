
import logging
import os
import datetime
import time
import shutil

from PyQt5 import QtCore

from Backend.BackendManager.VideoManager import VideoManager

class Manager():
  def __init__(self):
    self.timer = QtCore.QTimer()
    self.time = QtCore.QTime(0, 0)
    self.numberOfWords = 0

    #self.video = VideoAdapter()
    #self.audio = AudioAdapter(self)
    print("Starting VideoManager......")
    self.video = VideoManager()

    self.audioInitialized = False
    self.videoInitialized = True

  def connectEvents(self, timerEvent, videoFrameEvent):
    self.timer.timeout.connect(timerEvent)
    self.video.changePixmap.connect(videoFrameEvent)
    print("VideoManager connected videoFrameEvent......")
    self.video.start()
    # self.video.connectEvents(videoFrameEvent)

  def startRecording(self):
      logging.info('start recording pressed')
      self.video.startRecording()
      self.videoInitialized = True
      #self.audio.start()
      self.videoInitialized = True
      self.timer.start(100)
      self.time.start()

  def stopRecording(self):
      if not(self.videoInitialized) or not(self.audioInitialized):
        time.sleep(1)
      logging.info('stop recording pressed')

      # with open(os.path.join('outputFiles', 'wordsPerMinute.txt'), 'w') as wpmFile:
      #   #TODO: wpm analysis class aufrufen
      #     wordsPerMinute = self.numberOfWords*60000/self.time.elapsed()
      #     self.numberOfWords = 0
      #     logging.info('wpm file written')

      self.timer.stop()
      self.video.stopRecording()
      #self.audio.stopRecording()
      #self.analyzeAudio(wordsPerMinute)
      #self.moveOutput()

  def putText(self,stuff):
      logging.info('detected: ' + stuff)
      self.numberOfWords += len(stuff.split())

  def moveOutput(self):
      workingDir = os.getcwd()
      outputDir = os.path.join(workingDir, 'outputFiles')
      folderName = 'presentation' + str(datetime.now().strftime("%d%m%Y-%H%M%S"))
      newFolder = os.path.join(workingDir, 'presentations', folderName)

      #handVisualizer.visualiser(outputDir)
      #emotionvisualiser.visualiser(outputDir)
      os.mkdir(newFolder)

      files = os.listdir(outputDir)

      for f in files:
          if f != ".gitignore" and f != "version.txt":
              shutil.move(os.path.join(outputDir, f), newFolder)

      versionFile = open(os.path.join(outputDir, 'version.txt'), "w")
      versionFile.write(folderName)
      versionFile.close()

  def analyzeAudio(self, wordsPerMinute):
      logging.info('starting analyzeAudio')
      #audioFile = os.path.join('outputFiles', 'output.wav')
      #textFile = os.path.join('outputFiles', 'output.txt')
      #analyze_text_emotions(textFile)
      #analyze_audio_emotions(audioFile)
      #plotWPMGraph(wordsPerMinute)
      #keep_duplicates()

  def getElapsedTime(self):
    return QtCore.QTime.fromMSecsSinceStartOfDay(self.time.elapsed())
