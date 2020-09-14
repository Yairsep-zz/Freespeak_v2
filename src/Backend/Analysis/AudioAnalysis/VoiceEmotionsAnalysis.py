import soundfile, librosa, joblib, os, argparse, logging
import numpy as np
import matplotlib.pyplot as plt

from pydub.utils import make_chunks
from pydub import AudioSegment

def analyze_voice_emotions(raw_audio_path, resources_path):
    print(AudioSegment.ffmpeg)
    logging.info('starting speechEmotionsAnalysis')

    model_path = os.path.join(resources_path, 'emotions_model.pkl')

    model = joblib.load(model_path)
    logging.info('emotions_model loaded')

    myaudio = AudioSegment.from_wav(raw_audio_path, "wav")
    logging.info('wav audio loaded')

    chunk_length_ms = 3000
    chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of three secs
    logging.info('chunks created')
    # creating a new folder in resources if not already exists

    new_path = os.path.join(resources_path, 'wav_chunks')
    if(not os.path.isdir(new_path)):
        os.mkdir(new_path)

    y = []
    #Export all of the individual chunks as wav files
    for i, chunk in enumerate(chunks):
        file = new_path + "\\chunk{0}.wav".format(i)
        logging.info("exporting" + file)
        chunk.export(file, format="wav")
        feature=extractFeature(file, mfcc=True, chroma=True, mel=True)
        y.append(feature)
        os.remove(file)
    logging.info('feature extraction done')
    y_pred = model.predict(y)
    logging.info('prediction done')

    # data for evaluation
    return y_pred

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


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
#     # parser.add_argument('audio_path')
#     parser.add_argument('model_path')
#     parser.add_argument('raw_audio_path')
#     args = parser.parse_args()

#     # analyze_voice_emotions(args.audio_path, args.model_path, args.raw_audio_path)
#     analyze_voice_emotions(args.model_path, args.raw_audio_path)