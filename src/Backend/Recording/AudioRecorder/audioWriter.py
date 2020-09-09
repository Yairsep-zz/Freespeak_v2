import os
import wave
import pyaudio

class AudioWriter():
    def __init__(self,rate):
        outputPath = os.path.abspath(__file__ + "/../../../../../") + '/resources/raw_data/' + 'output.wav'
        self.wf = wave.open(outputPath, 'wb')
        self.wf.setnchannels(1)
        self.wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        self.wf.setframerate(rate)

    def close(self):
        self.wf.close()

    def writeFrame(self,data):
        self.wf.writeframes(data)        