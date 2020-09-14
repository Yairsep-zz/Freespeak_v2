
import logging
import os
from datetime import datetime
import time
import shutil
import numpy as np

from PyQt5 import QtCore

from Backend.BackendManager.VideoManager import VideoManager
from Backend.BackendManager.AudioManager import AudioManager

from Backend.Analysis.AudioAnalysis.TextSentimentAnalysis import analyze_text_sentiment
from Backend.Analysis.AudioAnalysis.VoiceEmotionsAnalysis import analyze_voice_emotions

from Backend.Evaluation.Visualisation.VoiceEmotionsVisualisation import visualize_voice_emotions
from Backend.Evaluation.Feedback.VoiceEmotionsFeedback import generate_voice_emotions_feedback

from Backend.Evaluation.Visualisation.TextSentimentVisualisation import visualize_text_sentiment
from Backend.Evaluation.Feedback.TextSentimentFeedback import generate_text_sentiment_feedback

from Backend.Evaluation.Visualisation.WordsPerMinuteVisualisation import visualize_wpm
from Backend.Evaluation.Feedback.WordsPerMinuteFeedback import generate_wpm_feedback

from Backend.Evaluation.Visualisation.FaceEmotionsVisualisation.FaceEmotionsPieChart import faceEmotionsPieChart
from Backend.Evaluation.Visualisation.FaceEmotionsVisualisation.FaceEmotionsTimeLine import faceEmotionsTimeLine
from Backend.Evaluation.Visualisation.FaceEmotionsVisualisation.FilterCsv import filterCsv
from Backend.Evaluation.Feedback.FaceEmotionsFeedback import generate_face_emotions_feedback

from Backend.Evaluation.Visualisation.HandPositionsVisualisation import visualize_hand_positions
from Backend.Evaluation.Feedback.HandPosotionsFeedback import generate_hand_pos_feedback
class Manager():
  def __init__(self):
    self.timer = QtCore.QTimer()
    self.time = QtCore.QTime(0, 0)
    self.numberOfWords = 0

    #self.video = VideoAdapter()
    #self.audio = AudioAdapter(self)
    logging.info("Initializing VideoManager(QThread)......")
    self.video = VideoManager()
    self.audioManager = AudioManager()

    self.audioInitialized = False
    self.videoInitialized = True
    logging.info("Manager initialized......")

  def connectEvents(self, timerEvent, videoFrameEvent):
    self.timer.timeout.connect(timerEvent)
    self.video.connectEvents(videoFrameEvent)
    logging.info("VideoManager connected videoFrameEvent......")

  def startVideo(self):
    logging.info("Starting VideoManager (first thread)......")
    self.video.start()

  def startRecording(self):
      logging.info('start recording pressed')
      self.video.startRecording()
      self.videoInitialized = True
      self.audioManager.startRecording()
      self.videoInitialized = True
      self.timer.start(100)
      self.time.start()

  def stopRecording(self):
      #LOL
      if not(self.videoInitialized) or not(self.audioInitialized):
        time.sleep(1.3)
      logging.info('stop recording pressed')

      self.timer.stop()
      self.video.stopRecording()
      self.audioManager.stopRecording()
      self.analyze_output()
      self.moveOutput()

  # def putText(self,stuff):
  #     logging.info('detected: ' + stuff)
  #     self.numberOfWords += len(stuff.split())

  def moveOutput(self):
    output_data_path = os.path.join(os.path.abspath(__file__ + "/../../../../"), 'resources', 'output_data')
    freespeak_path = os.path.abspath(__file__ + "/../../../../")
    presentations_path = os.path.join(freespeak_path, 'presentations')

    folderName = 'presentation' + str(datetime.now().strftime("%d%m%Y-%H%M%S"))
    newFolder = os.path.join(presentations_path, folderName)

    #handVisualizer.visualiser(outputDir)
    #emotionvisualiser.visualiser(outputDir)
    os.mkdir(newFolder)

    files = os.listdir(output_data_path)

    for f in files:
        if f != ".gitignore" and f != "version.txt":
            shutil.move(os.path.join(output_data_path, f), newFolder)

    versionFile = open(os.path.join(output_data_path, 'version.txt'), "w")
    versionFile.write(folderName)
    versionFile.close()

  # def analyzeAudio(self, wordsPerMinute):
  #     logging.info('starting analyzeAudio')
  #     audioFile = os.path.join('outputFiles', 'output.wav')
  #     textFile = os.path.join('outputFiles', 'output.txt')
  #     analyze_text_emotions(textFile)
  #     analyze_audio_emotions(audioFile)
  #     plotWPMGraph(wordsPerMinute)
  #     keep_duplicates()

  def analyze_output(self):
    raw_data_path = os.path.join(os.path.abspath(__file__ + "/../../../../"), 'resources', 'raw_data')
    output_data_path = os.path.join(os.path.abspath(__file__ + "/../../../../"), 'resources', 'output_data')

    logging.info("Analyzing voice emotions..............")
    voice_emotions_resources_path = os.path.join(os.path.abspath(__file__ + "/../../../../"), 'resources', 'voice_emotions_analysis_resources')
    voice_emotions_analysis_output = analyze_voice_emotions(os.path.join(raw_data_path, 'output.wav'), voice_emotions_resources_path)

    sizes = visualize_voice_emotions(voice_emotions_analysis_output, output_data_path)
    generate_voice_emotions_feedback(sizes, np.unique(voice_emotions_analysis_output), output_data_path)
    logging.info("Evaluating voice emotions done")

    logging.info("Analyzing text sentiment..............")
    text_output_path = os.path.join(raw_data_path, 'output.txt')
    score, magnitude = analyze_text_sentiment(text_output_path)

    visualize_text_sentiment(score, magnitude, output_data_path)
    generate_text_sentiment_feedback(score, magnitude, output_data_path)
    logging.info("Evaluating text sentiment done")

    logging.info("Analyzing wpm..............")
    wpm = self.audioManager.speechToText.get_word_count()
    visualize_wpm(wpm, output_data_path)
    generate_wpm_feedback(wpm, output_data_path)
    logging.info("Evaluating speaking speed done")

    logging.info("Analyzing face emotions..............")
    filterCsv(raw_data_path, output_data_path)
    faceEmotionsPieChart(raw_data_path, output_data_path)
    faceEmotionsTimeLine(raw_data_path, output_data_path)
    generate_face_emotions_feedback(output_data_path)
    logging.info("Evaluating face emotions done")

    logging.info("Analyzing hand positions..............")
    xCoords, yCoords = visualize_hand_positions(raw_data_path, output_data_path)
    generate_hand_pos_feedback(xCoords, yCoords, output_data_path)
    logging.info("Evaluating hand positions done")


  def getElapsedTime(self):
    return QtCore.QTime.fromMSecsSinceStartOfDay(self.time.elapsed())
