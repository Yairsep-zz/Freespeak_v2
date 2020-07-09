import soundfile, librosa, joblib, os
import numpy as np
import matplotlib.pyplot as plt

from pydub.utils import make_chunks
from pydub import AudioSegment

import logging

def custom_file(audio_name, raw_data_path):
    test_size=0.2
    logging.info('starting speechEmotionsAnalysis')
    #load emotions recognition model
    model = joblib.load(raw_data_path + '\\emotions_model.pkl')
    logging.info('emotions_model loaded')

    myaudio = AudioSegment.from_file(audio_name, "wav")
    logging.info('wav audio loaded')

    chunk_length_ms = 3000
    chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of three secs
    logging.info('chunks created')
    # creating a new folder in resources if not already exists
    current_path = os.getcwd()
    new_path = os.path.join(current_path, raw_data_path + "\\wav_chunks")
    if(not os.path.isdir(new_path)):
        os.mkdir(new_path)

    y = []
    #Export all of the individual chunks as wav files
    for i, chunk in enumerate(chunks):
        file = raw_data_path + "\\wav_chunks\\chunk{0}.wav".format(i)
        logging.info("exporting" + file)
        chunk.export(file, format="wav")
        feature=extractFeature(file, mfcc=True, chroma=True, mel=True)
        y.append(feature)
        os.remove(file)
    logging.info('feature extraction done')
    y_pred = model.predict(y)
    logging.info('prediction done')

def extractFeature(file_name, mfcc, chroma, mel):
    with soundfile.SoundFile(file_name) as sound_file:
        X = sound_file.read(dtype="float32")
        sample_rate=sound_file.samplerate
        if chroma:
            stft=np.abs(librosa.stft(X))
        result=np.array([])
        if mfcc:
            mfccs=np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
            result=np.hstack((result, mfccs))
        if chroma:
            chroma=np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
            result=np.hstack((result, chroma))
        if mel:
            mel=np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
            result=np.hstack((result, mel))
    return result