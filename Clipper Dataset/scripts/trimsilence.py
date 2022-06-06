import glob
import json
import multiprocessing
import os
from tqdm import tqdm
from pathlib import Path
from joblib import Parallel, delayed
#from ztts.audio import trim_long_silences
import librosa
import numpy as np
import soundfile as sf
import struct
import webrtcvad

int16_max = (2 ** 15) - 1
vad_moving_average_width = 8
vad_max_silence_length = 6

def trim_long_silences(wav, orig_sr, vad_window_length=30):
    """
    :param wav: the raw waveform as a numpy array of floats 
    :return: the same waveform with silences trimmed away (length <= original wav length)
    """
    target_sr = 16000
    wav = librosa.resample(wav, orig_sr=orig_sr, target_sr=target_sr)
    # Compute the voice detection window size
    samples_per_window = (vad_window_length * target_sr) // 1000
    
    # Trim the end of the audio to have a multiple of the window size
    wav = wav[:len(wav) - (len(wav) % samples_per_window)]
    
    # Convert the float waveform to 16-bit mono PCM
    pcm_wave = struct.pack("%dh" % len(wav), *(np.round(wav * int16_max)).astype(np.int16))
    
    # Perform voice activation detection
    voice_flags = []
    vad = webrtcvad.Vad(mode=3)
    for window_start in range(0, len(wav), samples_per_window):
        window_end = window_start + samples_per_window
        voice_flags.append(vad.is_speech(pcm_wave[window_start * 2:window_end * 2],
                                         sample_rate=target_sr))
    voice_flags = np.array(voice_flags)
    
    # Smooth the voice detection with a moving average
    def moving_average(array, width):
        array_padded = np.concatenate((np.zeros((width - 1) // 2), array, np.zeros(width // 2)))
        ret = np.cumsum(array_padded, dtype=float)
        ret[width:] = ret[width:] - ret[:-width]
        return ret[width - 1:] / width
    
    audio_mask = moving_average(voice_flags, vad_moving_average_width)
    audio_mask = np.round(audio_mask).astype(bool)
    
    start_ms, end_ms = np.Inf, np.NINF
    for i in range(0, len(audio_mask)):
        if audio_mask[i]:
            start_ms = (i * samples_per_window) / target_sr
            break

    for i in range(len(audio_mask) - 1, -1, -1):
        if audio_mask[i]:
            end_ms = (i * samples_per_window) / target_sr
            break

    return start_ms, end_ms

class Preprocessor:
    def __init__(self):
        #self.audio_dir = audio_dir
        #self.in_dir = [os.path.abspath(filename) for filename in glob.glob(os.path.join(self.audio_dir, f'**/*.wav'), recursive = True)]
        #self.in_dir = Path(".") / "Ingenous"
        self.in_dir = Path('.') / "MEGAsync Imports/Master file/Colab Folder"
        #print(self.in_dir)
        

    def build_from_path(self):
        Parallel(n_jobs=multiprocessing.cpu_count())(delayed(self.preprocess_wav)(wav_dir) for wav_dir in tqdm(list(self.in_dir.glob("**/*.wav"))))
        #print(list(self.in_dir.glob('*/*.wav')))               

    def preprocess_wav(self, wav_path):
        wav, sr = librosa.load(wav_path, sr=None)
        start, end = trim_long_silences(wav, sr)
        if start >= end:
            return
        wav = wav[int(np.round(start * sr)):int(np.round(end * sr))]
        sf.write(
            wav_path,
            wav,
            sr
        )

if __name__ == "__main__":
    preprocessor = Preprocessor()
    preprocessor.build_from_path()


