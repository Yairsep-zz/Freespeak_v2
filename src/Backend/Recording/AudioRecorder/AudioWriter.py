import os
import wave
import pyaudio

class AudioWriter():
    def __init__(self,rate):
        self.outputPath = os.path.abspath(__file__ + "/../../../../../") + '/resources/raw_data/' + 'output.wav'
        self.rate = rate
        self.open = False

    def start(self):
        self.wf = wave.open(self.outputPath, 'wb')
        self.wf.setnchannels(1)
        self.wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        self.wf.setframerate(self.rate)
        self.open = True


    def close(self):
        self.open = False
        self.wf.close()


    def writeFrame(self,data):
        if self.open:
            self.wf.writeframes(data)