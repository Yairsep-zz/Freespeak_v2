import os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from Frontend.guiRecordingPage import RecordWindow
from Frontend.guiResultPage import ResultScreen
import logging

# get the directory of this script
path = os.path.dirname(os.path.abspath(__file__))

WindowUI, WindowBase = uic.loadUiType(
    os.path.join(path, 'templates', 'guiManager.ui'))


class GuiManager(WindowBase, WindowUI):
    def __init__(self, parent=None):
        WindowBase.__init__(self, parent)
        self.setupUi(self)
        logging.info("Initializing guiRecordingPage......")
        self.recordWindow = RecordWindow(self)
        logging.info("Initializing ResultScreen......")
        self.resultScreen = ResultScreen(self)

        self.stackedWidget.addWidget(self.recordWindow)
        self.stackedWidget.addWidget(self.resultScreen)

        self.checkForResultsActivation()
        self.recordWindow.startStopButton.clicked.connect(self.checkForResultsActivation)

        # connect buttons
        self.switchPageButton.clicked.connect(self.switchPage)

    def switchPage(self):
        if(self.stackedWidget.currentIndex() == 0):
            index = 1
            self.switchPageButton.setText('Record Presentation')
        else:
            index = 0
            self.switchPageButton.setText('Analyze Results')

        self.stackedWidget.setCurrentIndex(index)
        self.resultScreen.version = self.version
        self.resultScreen.load()

    def checkForResultsActivation(self):
        # check if results exist
        self.switchPageButton.setEnabled(False)
        workingDirPath = os.getcwd()
        versionFilePath = os.path.join(workingDirPath, 'outputFiles', 'version.txt')
        if os.path.isfile(versionFilePath):
            with open(versionFilePath, 'r') as versionFile:
                self.version = versionFile.read()
                if len(self.version) > 0 and os.path.isdir(
                    os.path.join(workingDirPath, 'presentations', self.version)):
                    self.switchPageButton.setEnabled(True)
