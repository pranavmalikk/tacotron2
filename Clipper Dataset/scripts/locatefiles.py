import os
from numpy import datetime_as_string
from pathlib import Path
from sklearn import datasets
import glob
import torchaudio


from torch.utils.data import Dataset 

class ClipperDataset(Dataset):
    def __init__(self, audio_dir):
        #self.audio_dir = audio_dir
        self.audio_dir = [os.path.abspath(filename) for filename in glob.glob(os.path.join(audio_dir, f'**/*.wav'), recursive = True)]

    def __len__(self):
        return len(self.audio_dir)

    def __getitem__(self, index):
        #audio_sample_path = self.get_audio_sample_path(index)
        signal, sr = torchaudio.load(self.audio_dir[0])
        return signal, sr

    #def _get_audio_sample_path_(self, index):   

if __name__ == "__main__":
    AUDIO_FILE = "Igneous/"
    AUDIO_FILE_DEEP = "Igneous/Igneous-fim:s5e20-00-06-02/"

    clipper = ClipperDataset(AUDIO_FILE_DEEP)
    print(len(clipper))

    signal, sr = clipper[0]
    print(signal, sr)
