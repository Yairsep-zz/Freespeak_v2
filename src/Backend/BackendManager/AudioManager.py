import logging

from Backend.Recording.AudioRecorder.AudioWriter import AudioWriter
from Backend.Recording.AudioRecorder.AudioReader import AudioReader
from Backend.Recording.AudioRecorder.SpeechToText import SpeechToText


class AudioManager():
    RATE = 16000
    CHUNK = int(RATE / 10)  # 100ms

    def __init__(self):
        logging.info("Initializing AudioReader...")
        self.audioReader = AudioReader(self.RATE, self.CHUNK)
        logging.info("Initializing AudioWriter...")
        self.audioWriter = AudioWriter(self.audioReader.get_rate())
        self.audioReader.connect_events(self.audioWriter.writeFrame)
        logging.info("Initializing SpeechToText...")
        self.speechToText = SpeechToText(self.audioReader, self.RATE)

    def startRecording(self):
        #audioWriter muss hier vor audiReader gestartet werden
        self.audioWriter.start()
        self.audioReader.__enter__()
        self.speechToText.start()


    def stopRecording(self):
        #audioWriter muss hier nach audiReader geschlossen werden
        self.audioReader.stop()
        self.audioWriter.close()
        # self.speechToText.stopRecording()


