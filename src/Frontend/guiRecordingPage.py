import os, time
import shutil
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets, uic

#from video.videoAdapter import VideoAdapter
#from audio.audioAdapter import AudioAdapter
#from video.utils.wpm import plotWPMGraph
#from emotionsAnalysis.fileAnalysis import analyze_text_emotions
#from emotionsAnalysis.fileAnalysis import analyze_audio_emotions
#from faceEmotionDetector.editEmotionsCsv import keep_duplicates


#import video.utils.handVisualizer as handVisualizer
#import video.utils.emotionvisualiser as emotionvisualiser

import logging

from Backend.BackendManager.Manager import Manager

# get the directory of this script
path = os.path.dirname(os.path.abspath(__file__))

WindowUI, WindowBase = uic.loadUiType(
    os.path.join(path, 'templates', 'recordingPage.ui'))

class RecordWindow(WindowBase, WindowUI):
    def __init__(self, parent=None):
        WindowBase.__init__(self, parent)
        self.setupUi(self)

        self.recording = False
        logging.info("Initializing Manager......")
        self.manager = Manager()

        logging.info("Connecting events.......")
        self.startStopButton.clicked.connect(self.onStartStopButtonPress)
        self.manager.connectEvents(timerEvent=self.timerEvent, videoFrameEvent=self.setFrame)

    def onStartStopButtonPress(self):
        if self.recording:
            self.manager.stopRecording()
            self.startStopButton.setText('start recording')
        else:
            self.manager.startRecording()
            self.startStopButton.setText("stop recording")
        self.recording = not self.recording

    def setFrame(self, frame):
        # print("hahaha")

        w = self.videoScreen.width() - 1
        h = self.videoScreen.height() - 1
        pixmap = QtGui.QPixmap.fromImage(frame)
        self.videoScreen.setPixmap(pixmap.scaled(w,h,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation))
        self.videoScreen.setMinimumSize(1,1)

    def putText(self,stuff):
        self.manager.putText(stuff)

    def timerEvent(self):
        elapsedTime = self.manager.getElapsedTime()
        self.timerWindow.setText(elapsedTime.toString("mm:ss:zzz")[:8])
