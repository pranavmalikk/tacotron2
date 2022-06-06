import json
import random
from matplotlib import pyplot as plt
import pandas as pd
import torch
import torchaudio
import os
import glob
from botocore import UNSIGNED
from botocore.config import Config
import matplotlib.pyplot as plt
from IPython.display import Audio, display
import random
import torch
import re
from pathlib import Path
from torch.utils.data import Dataset, DataLoader
from typing import Any, Callable, cast, Dict, List, Optional, Tuple
import torchaudio
from torch import Tensor


with open("../config.json") as f:
    conf = json.loads(f.read())

CLIPPER_DATASET = conf['CLIPPER_DATAPATH']

def print_stats(waveform, sample_rate=None, src=None):
    if src:
        print("-" * 10)
        print("Source:", src)
        print("-" * 10)
    if sample_rate:
        print("Sample Rate:", sample_rate)
    print("Shape:", tuple(waveform.shape))
    print("Dtype:", waveform.dtype)
    print(f" - Max:     {waveform.max().item():6.3f}")
    print(f" - Min:     {waveform.min().item():6.3f}")
    print(f" - Mean:    {waveform.mean().item():6.3f}")
    print(f" - Std Dev: {waveform.std().item():6.3f}")
    print()
    print(waveform)
    print()

def plot_waveform(waveform, sample_rate, title="Waveform", xlim=None, ylim=None):
    waveform = waveform.numpy()

    num_channels, num_frames = waveform.shape
    time_axis = torch.arange(0, num_frames) / sample_rate

    figure, axes = plt.subplots(num_channels, 1)
    if num_channels == 1:
        axes = [axes]
    for c in range(num_channels):
        axes[c].plot(time_axis, waveform[c], linewidth=1)
        axes[c].grid(True)
        if num_channels > 1:
            axes[c].set_ylabel(f'Channel {c+1}')
        if xlim:
            axes[c].set_xlim(xlim)
        if ylim:
            axes[c].set_ylim(ylim)
    figure.suptitle(title)
    plt.show(block=False)

def plot_specgram(waveform, sample_rate, title="Spectrogram", xlim=None):
    waveform = waveform.numpy()
    num_channels, num_frames = waveform.shape
    time_axis = torch.arange(0, num_frames) / sample_rate

    figure, axes = plt.subplots(num_channels, 1)
    if num_channels == 1:
        axes = [axes]
    for c in range(num_channels):
        axes[c].specgram(waveform[c], Fs=sample_rate)
        if num_channels > 1:
            axes[c].set_ylabel(f'Channel {c+1}')
        if xlim:
            axes[c].set_xlim(xlim)
    figure.suptitle(title)
    plt.show(block=False)

def play_audio(waveform, sample_rate):
    waveform = waveform.numpy()

    num_channels, num_frames = waveform.shape
    if num_channels == 1:
        display(Audio(waveform[0], rate=sample_rate))
    elif num_channels == 2:
        display(Audio((waveform[0], waveform[1]), rate=sample_rate))
    else:
        raise ValueError("Waveform with more than 2 channels are not supported.")

def _get_sample(path, resample=None):
    effects = [
        ["remix", "1"]
    ]
    if resample:
        effects.extend([
        ["lowpass", f"{resample // 2}"],
        ["rate", f'{resample}'],
        ])
    return torchaudio.sox_effects.apply_effects_file(path, effects=effects)

def get_sample(path, *, resample=None):
    return _get_sample(path, resample=resample)

def inspect_file(path):
    print("-" * 10)
    print("Source:", path)
    print("-" * 10)
    print(f" - File size: {os.path.getsize(path)} bytes")
    print(f" - {torchaudio.info(path)}")

wav_path = sorted([os.path.abspath(path) for path in glob.glob(os.path.join('AK2/', f'**/*.wav') , recursive = True)])





def load_audio_item(filepath: str, path: str) -> Tuple[Tensor, int, str, str]:
    relpath = os.path.relpath(filepath, path)
    label, filename = os.path.split(relpath)
    waveform, sample_rate = torchaudio.load(filepath)
    return waveform, sample_rate, label, filename

print(load_audio_item('AK2/', ))

class AudioFolder(Dataset):
    """Create a Dataset from Local Files.
    Args:
        root (str): Path to the directory where the dataset is found or downloaded.
        suffix (str) : Audio file type, defaulted to ".WAV".
        transform (callable, optional): A function/transform that  takes in the audio waveform
            and returns a transformed version. E.g, ``transforms.Spectrogram``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
        loader (callable, optional): A function to load an image given its path.
        is_valid_file (callable, optional): A function that takes path of an Image file
            and check if the file is a valid file (used to check of corrupt files)
    """


    def __init__(
            self,
            root: str,
            suffix: str = ".wav",
            transform: Optional[Callable] = None,
            target_transform: Optional[Callable] = None,
            loader: Optional[Callable] = None,
            is_valid_file: Optional[Callable] = None
        ):

        #(self._path, suffix=suffix, prefix=True)
        self._path = root
        walker = sorted([os.path.abspath(self.path) for self.path in glob.glob(os.path.join(self.path, f'**/*.wav') , recursive = True)])
        self._walker = list(walker)

    def __getitem__(self, n: int) -> Tuple[Tensor, int, str, str]:
        """Load the n-th sample from the dataset.
        Args:
            n (int): The index of the sample to be loaded
        Returns:
            tuple: ``(waveform, sample_rate, label, filename)``
        """
        fileid = self._walker[n]
        return load_audio_item(fileid, self._path)


        #path, target = self.samples[index]
        #sample = self.loader(path)
        #if self.transform is not None:
        #    sample = self.transform(sample)
        #if self.target_transform is not None:
        #    target = self.target_transform(target)

        #return sample, target



    def __len__(self) -> int:
        return len(self._walker)

speech_commands_dataset = AudioFolder('AK2/')

print(len(speech_commands_dataset))



# class CustomDataset(Dataset):
#     def __init__(self, directory):
#         self.directory = directory
#         self.images = Path(self.directory).glob("**/*.wav")
#         print(self.images)

#     def __len__(self):
#         return len(self.images)

#     #def __getitem__(self, index):
        

# dataset = CustomDataset('AK2/')


# sample_rate, audio_data = torchaudio.load(filenames)


# class RandomClip:
#     def __init__(self, sample_rate, clip_length):
#         self.vad = torchaudio.transforms.Vad(
#             sample_rate=sample_rate, trigger_level=7.0)

#     def __call__(self, audio_data):
#         audio_length = audio_data.shape[0]
#         if audio_length > self.clip_length:
#             offset = random.randint(0, audio_length-self.clip_length)
#             audio_data = audio_data[offset:(offset+self.clip_length)]

#         return self.vad(audio_data) # remove silences at the beggining/end

# clip_transform = RandomClip(sample_rate, 64000) # 8 seconds clip
# transformed_audio = clip_transform(audio_data)