from ast import main
import os
import unicodedata
import numpy as np
from scipy.io.wavfile import read
import torch
from training import *
from training.text import clean_text
from string import punctuation, digits


def get_mask_from_lengths(lengths):
    max_len = torch.max(lengths).item()
    ids = torch.arange(0, max_len, out=torch.cuda.LongTensor(max_len))
    mask = (ids < lengths.unsqueeze(1)).bool()
    return mask


def load_wav_to_torch(full_path):
    sampling_rate, data = read(full_path)
    return torch.FloatTensor(data.astype(np.float32)), sampling_rate


def load_filepaths_and_text(filename, split="|"):
    with open(filename, encoding='utf-8') as f:
        filepaths_and_text = [line.strip().split(split) for line in f]
    return filepaths_and_text

def get_gpu_memory(gpu_index):
    """
    Get available memory of a GPU.

    Parameters
    ----------
    gpu_index : int
        Index of GPU

    Returns
    -------
    int
        Available GPU memory in GB
    """
    gpu_memory = torch.cuda.get_device_properties(gpu_index).total_memory
    memory_in_use = torch.cuda.memory_allocated(gpu_index)
    available_memory = gpu_memory - memory_in_use
    return available_memory // 1024 // 1024 // 1024


def get_available_memory():
    """
    Get available GPU memory in GB.

    Returns
    -------
    int
        Available GPU memory in GB
    """
    available_memory_gb = 0

    for i in range(torch.cuda.device_count()):
        available_memory_gb += get_gpu_memory(i)

    return available_memory_gb

def load_labels_file(filepath):
    """
    Load labels file

    Parameters
    ----------
    filepath : str
        Path to text file

    Returns
    -------
    list
        List of samples
    """
    with open(filepath, encoding='utf-8') as f:
        return [line.strip().split("|") for line in f]

def validate_dataset(filepath_and_text, dataset_directory, symbols):
    """
    Validate dataset

    Parameters
    ----------
    filelist : list
        List of samples
    dataset_directory : str
        Path to dataset
    symbols : list
        List of symbols
    """
    missing_files = set()
    invalid_characters = set()
    wavs = os.listdir(dataset_directory)
    for filename, text in filepath_and_text:
        text = clean_text(text, remove_invalid_characters=False)
        if filename not in wavs:
            missing_files.add(filename)
        invalid_characters_for_row = get_invalid_characters(text, symbols)
        if invalid_characters_for_row:
            invalid_characters.update(invalid_characters_for_row)

    assert not missing_files, f"Missing files: {(',').join(missing_files)}"
    assert (
        not invalid_characters
    ), f"Invalid characters in text (for alphabet): {','.join([f'{c} ({unicodedata.name(c)})' for c in invalid_characters])}"


def train_test_split(filepaths_and_text, train_size):
    """
    Split dataset into train & test data

    Parameters
    ----------
    filepaths_and_text : list
        List of samples
    train_size : float
        Percentage of entries to use for training (rest used for testing)

    Returns
    -------
    (list, list)
        List of train and test samples
    """
    train_filepaths_and_text = []
    test_filepaths_and_text = []
    for filepath, text in filepaths_and_text:
        if np.random.random() < train_size:
            train_filepaths_and_text.append([filepath, text])
        else:
            test_filepaths_and_text.append([filepath, text])
    return train_filepaths_and_text, test_filepaths_and_text  

def to_gpu(x):
    x = x.contiguous()

    if torch.cuda.is_available():
        x = x.cuda(non_blocking=True)
    return torch.autograd.Variable(x)


def get_invalid_characters(text, symbols):
    """
    Returns all invalid characters in text

    Parameters
    ----------
    text : str
        String to check
    symbols : list
        List of symbols that are valid

    Returns
    -------
    set
        All invalid characters
    """
    return set([c for c in text if c not in symbols and c not in punctuation and c not in digits])