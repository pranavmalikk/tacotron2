import os
import glob
from posixpath import basename
import shutil
from importlib_metadata import metadata
from path import Path
import soundfile as sf
import pyloudnorm as pyln
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from pyloudnorm import util
import librosa
import ffmpeg
from shutil import copy, rmtree
import json
import re
import tqdm
import unidecode
import pyfoal
import torch
from pydub import AudioSegment
import wave
import contextlib
import numpy as np
import torch
import torchaudio
import re
import boto3
from botocore import UNSIGNED
from botocore.config import Config
import matplotlib.pyplot as plt
from IPython.display import Audio, display
import random
import ast
import pickle
from trimsilence import Preprocessor
#import soundfilemanipulation 

#Have to be one path outside of MEGAsync imports (within cloud drive)

source_directory = 'MEGAsync Imports/Master file/Sliced Dialogue/'
colab_files = 'MEGAsync Imports/Master file/Colab Folder'

EMOTIONS = ['Neutral', 'Happy', 'Amused', 'Sad', 'Annoyed', 'Angry', 'Disgust', 'Sarcastic', 'Smug', 'Fear', 'Anxious', 'Confused', 'Surprised', 'Tired', 'Whispering', 'Shouting', 'Whining', 'Crazy']

EPISODES = {
    'Rainbow Roadtrip': 'fim:rainbow roadtrip',
    's1e1': 'fim:s1e1',
    's1e2': 'fim:s1e2',
    's1e3': 'fim:s1e3',
    's1e4': 'fim:s1e4',
    's1e5': 'fim:s1e5',
    's1e6': 'fim:s1e6',
    's1e7': 'fim:s1e7',
    's1e8': 'fim:s1e8',
    's1e9': 'fim:s1e9',
    's1e10': 'fim:s1e10',
    's1e11': 'fim:s1e11',
    's1e12': 'fim:s1e12',
    's1e13': 'fim:s1e13',
    's1e14': 'fim:s1e14',
    's1e15': 'fim:s1e15',
    's1e16': 'fim:s1e16',
    's1e17': 'fim:s1e17',
    's1e18': 'fim:s1e18',
    's1e19': 'fim:s1e19',
    's1e20': 'fim:s1e20',
    's1e21': 'fim:s1e21',
    's1e22': 'fim:s1e22',
    's1e23': 'fim:s1e23',
    's1e24': 'fim:s1e24',
    's1e25': 'fim:s1e25',
    's1e26': 'fim:s1e26',
    's2e1': 'fim:s2e1',
    's2e2': 'fim:s2e2',
    's2e3': 'fim:s2e3',
    's2e4': 'fim:s2e4',
    's2e5': 'fim:s2e5',
    's2e6': 'fim:s2e6',
    's2e7': 'fim:s2e7',
    's2e8': 'fim:s2e8',
    's2e9': 'fim:s2e9',
    's2e10': 'fim:s2e10',
    's2e11': 'fim:s2e11',
    's2e12': 'fim:s2e12',
    's2e13': 'fim:s2e13',
    's2e14': 'fim:s2e14',
    's2e15': 'fim:s2e15',
    's2e16': 'fim:s2e16',
    's2e17': 'fim:s2e17',
    's2e18': 'fim:s2e18',
    's2e19': 'fim:s2e19',
    's2e20': 'fim:s2e20',
    's2e21': 'fim:s2e21',
    's2e22': 'fim:s2e22',
    's2e23': 'fim:s2e23',
    's2e24': 'fim:s2e24',
    's2e25': 'fim:s2e25',
    's2e26': 'fim:s2e26',
    's3e1': 'fim:s3e1',
    's3e2': 'fim:s3e2',
    's3e3': 'fim:s3e3',
    's3e4': 'fim:s3e4',
    's3e5': 'fim:s3e5',
    's3e6': 'fim:s3e6',
    's3e7': 'fim:s3e7',
    's3e8': 'fim:s3e8',
    's3e9': 'fim:s3e9',
    's3e10': 'fim:s3e10',
    's3e11': 'fim:s3e11',
    's3e12': 'fim:s3e12',
    's3e13': 'fim:s3e13',
    's4e1': 'fim:s4e1',
    's4e2': 'fim:s4e2',
    's4e3': 'fim:s4e3',
    's4e4': 'fim:s4e4',
    's4e5': 'fim:s4e5',
    's4e6': 'fim:s4e6',
    's4e7': 'fim:s4e7',
    's4e8': 'fim:s4e8',
    's4e9': 'fim:s4e9',
    's4e10': 'fim:s4e10',
    's4e11': 'fim:s4e11',
    's4e12': 'fim:s4e12',
    's4e13': 'fim:s4e13',
    's4e14': 'fim:s4e14',
    's4e15': 'fim:s4e15',
    's4e16': 'fim:s4e16',
    's4e17': 'fim:s4e17',
    's4e18': 'fim:s4e18',
    's4e19': 'fim:s4e19',
    's4e20': 'fim:s4e20',
    's4e21': 'fim:s4e21',
    's4e22': 'fim:s4e22',
    's4e23': 'fim:s4e23',
    's4e24': 'fim:s4e24',
    's4e25': 'fim:s4e25',
    's4e26': 'fim:s4e26',
    's5e1': 'fim:s5e1',
    's5e2': 'fim:s5e2',
    's5e3': 'fim:s5e3',
    's5e4': 'fim:s5e4',
    's5e5': 'fim:s5e5',
    's5e6': 'fim:s5e6',
    's5e7': 'fim:s5e7',
    's5e8': 'fim:s5e8',
    's5e9': 'fim:s5e9',
    's5e10': 'fim:s5e10',
    's5e11': 'fim:s5e11',
    's5e12': 'fim:s5e12',
    's5e13': 'fim:s5e13',
    's5e14': 'fim:s5e14',
    's5e15': 'fim:s5e15',
    's5e16': 'fim:s5e16',
    's5e17': 'fim:s5e17',
    's5e18': 'fim:s5e18',
    's5e19': 'fim:s5e19',
    's5e20': 'fim:s5e20',
    's5e21': 'fim:s5e21',
    's5e22': 'fim:s5e22',
    's5e23': 'fim:s5e23',
    's5e24': 'fim:s5e24',
    's5e25': 'fim:s5e25',
    's5e26': 'fim:s5e26',
    's6e1': 'fim:s6e1',
    's6e2': 'fim:s6e2',
    's6e3': 'fim:s6e3',
    's6e4': 'fim:s6e4',
    's6e5': 'fim:s6e5',
    's6e6': 'fim:s6e6',
    's6e7': 'fim:s6e7',
    's6e8': 'fim:s6e8',
    's6e9': 'fim:s6e9',
    's6e10': 'fim:s6e10',
    's6e11': 'fim:s6e11',
    's6e12': 'fim:s6e12',
    's6e13': 'fim:s6e13',
    's6e14': 'fim:s6e14',
    's6e15': 'fim:s6e15',
    's6e16': 'fim:s6e16',
    's6e17': 'fim:s6e17',
    's6e18': 'fim:s6e18',
    's6e19': 'fim:s6e19',
    's6e20': 'fim:s6e20',
    's6e21': 'fim:s6e21',
    's6e22': 'fim:s6e22',
    's6e23': 'fim:s6e23',
    's6e24': 'fim:s6e24',
    's6e25': 'fim:s6e25',
    's6e26': 'fim:s6e26',
    's7e1': 'fim:s7e1',
    's7e2': 'fim:s7e2',
    's7e3': 'fim:s7e3',
    's7e4': 'fim:s7e4',
    's7e5': 'fim:s7e5',
    's7e6': 'fim:s7e6',
    's7e7': 'fim:s7e7',
    's7e8': 'fim:s7e8',
    's7e9': 'fim:s7e9',
    's7e10': 'fim:s7e10',
    's7e11': 'fim:s7e11',
    's7e12': 'fim:s7e12',
    's7e13': 'fim:s7e13',
    's7e14': 'fim:s7e14',
    's7e15': 'fim:s7e15',
    's7e16': 'fim:s7e16',
    's7e17': 'fim:s7e17',
    's7e18': 'fim:s7e18',
    's7e19': 'fim:s7e19',
    's7e20': 'fim:s7e20',
    's7e21': 'fim:s7e21',
    's7e22': 'fim:s7e22',
    's7e23': 'fim:s7e23',
    's7e24': 'fim:s7e24',
    's7e25': 'fim:s7e25',
    's7e26': 'fim:s7e26',
    's8e1': 'fim:s8e1',
    's8e2': 'fim:s8e2',
    's8e3': 'fim:s8e3',
    's8e4': 'fim:s8e4',
    's8e5': 'fim:s8e5',
    's8e6': 'fim:s8e6',
    's8e7': 'fim:s8e7',
    's8e8': 'fim:s8e8',
    's8e9': 'fim:s8e9',
    's8e10': 'fim:s8e10',
    's8e11': 'fim:s8e11',
    's8e12': 'fim:s8e12',
    's8e13': 'fim:s8e13',
    's8e14': 'fim:s8e14',
    's8e15': 'fim:s8e15',
    's8e16': 'fim:s8e16',
    's8e17': 'fim:s8e17',
    's8e18': 'fim:s8e18',
    's8e19': 'fim:s8e19',
    's8e20': 'fim:s8e20',
    's8e21': 'fim:s8e21',
    's8e22': 'fim:s8e22',
    's8e23': 'fim:s8e23',
    's8e24': 'fim:s8e24',
    's8e25': 'fim:s8e25',
    's8e26': 'fim:s8e26',
    's9e1': 'fim:s9e1',
    's9e2': 'fim:s9e2',
    's9e3': 'fim:s9e3',
    's9e4': 'fim:s9e4',
    's9e5': 'fim:s9e5',
    's9e6': 'fim:s9e6',
    's9e7': 'fim:s9e7',
    's9e8': 'fim:s9e8',
    's9e9': 'fim:s9e9',
    's9e10': 'fim:s9e10',
    's9e11': 'fim:s9e11',
    's9e12': 'fim:s9e12',
    's9e13': 'fim:s9e13',
    's9e14': 'fim:s9e14',
    's9e15': 'fim:s9e15',
    's9e16': 'fim:s9e16',
    's9e17': 'fim:s9e17',
    's9e18': 'fim:s9e18',
    's9e19': 'fim:s9e19',
    's9e20': 'fim:s9e20',
    's9e21': 'fim:s9e21',
    's9e22': 'fim:s9e22',
    's9e23': 'fim:s9e23',
    's9e24': 'fim:s9e24',
    's9e25': 'fim:s9e25',
    's9e26': 'fim:s9e26',
    'EQG Dance Magic': 'eqg:dance magic',
    'EQG Forgotten Friendship': 'eqg:forgotten friendship',
    'EQG Friendship Games': 'eqg:friendship games',
    'EQG Legend of Everfree': 'eqg:legend of everfree',
    'EQG Mirror Magic': 'eqg:mirror magic',
    'EQG Movie Magic': 'eqg:movie magic',
    'EQG Original': 'eqg:original',
    'EQG Rainbow Rocks': 'eqg:rainbow rocks',
    'EQG Roller Coaster of Friendship': 'eqg:roller coaster of friendship',
    'EQG RoF Special Source':
    'eqg:roller coaster of friendship',
    'EQG Holidays Unwrapped': 'eqg:holidays unwrapped',
    'MLP Movie': 'fim:mlp movie',
    '214 outtakes': 'outtakes:s2e14',
    '421 outtakes': 'outtakes:s4e21',
    '506 outtakes': 'outtakes:s5e6',
    '509 outtakes': 'outtakes:s5e9',
    '624 outtakes': 'outtakes:s6e24',
    '713 outtakes': 'outtakes:s7e13',
    '819 outtakes': 'outtakes:s8e19',
    '823 outtakes': 'outtakes:s8e23',
    '922 outtakes': 'outtakes:s9e22',
    '924 outtakes': 'outtakes:s9e24',
    's2e4_Street Magic With Trixie': 'eqg:s2e4',
    's2e5_Sic Skateboard': 'eqg:s2e5',
    's2e6_Street Chic': 'eqg:s2e6',
    's2e7_Game Stream': 'eqg:s2e7',
    's2e8_Best in Show The Preshow': 'eqg:s2e8',
    'Arizona': None,
    'Oleander and Fred': None,
    'Pom': None,
    'Tianhuo': None,
    'Velvet': None,
    'TFH': None,
    'Noise samples': None,
    'Applejack': None,
    'Fluttershy': None,
    'Nightmare Moon': None,
    'Pinkie Pie': None,
    'Rainbow Dash': None,
    'Rarity': None,
    'Spike': None,
}


# def normalize_volume(directory, ext = '.wav'):
#     wav_dataset = sorted([os.path.abspath(wav_files) for wav_files in glob.glob(os.path.join(directory, f'**/*{ext}'), recursive = True)])
#     for files in wav_dataset:
#         data, rate = sf.read(files)
#         print(data)
        #meter = pyln.Meter(rate)
        #This following if statement removes what the util class in meter will not process 
        # if data.shape[0] < rate * 0.4:
        #The following if statement accounts for below 2 second threshold
        #71280 is 2 seconds
        # if data.shape[0] < 50000:
        #     #print(files)
        #     #Removes the txt files and wav files that don't meet threshold
        #     txt_files = os.path.dirname(files) + "/" + os.path.basename(files).split(".")[0] + '.txt'
        #     rmtree(os.path.dirname(files))
            #json_files = os.path.join(os.path.dirname(files), 'label.json')
            # if os.path.exists(files):
            #     os.unlink(files)
        # else:
        #     #Cuts down the volume on all wav files
        #     loudness = meter.integrated_loudness(data)
        #     loudness_normalized_audio = pyln.normalize.loudness(data, loudness, -27.0)
        #     wavfile.write(files, rate, loudness_normalized_audio)

#Created the directory of each character with respective wav file copied in each folder
#Steps:
#   1: get the destination and source targets
#   2: create colab folder directory in location of the destination target
#   3: create the folders of each character with respective episode within the colab folders
#   4: if the folder with the respective character already exists, don't override just add the "2222..." to the end to differentiate
def create_outer_directory(directory, wav_ext = '.wav', txt_ext = '.txt'):
    wav_path = sorted([os.path.abspath(wav_files) for wav_files in glob.glob(os.path.join(directory, f'**/*{wav_ext}'), recursive = True)])
    # txt_path = sorted([os.path.abspath(txt_files) for txt_files in glob.glob(os.path.join(directory, f'**/*{txt_ext}'), recursive = True)])
    destination_target = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(wav_path[0]))))
    
    
    # fileList = [file for file in txt_path if file.endswith(".txt")]
    for wav_files in tqdm.tqdm(wav_path):
        one_up_folder = os.path.dirname(wav_files)
        basename = os.path.basename(wav_files)
        first_part = '-'.join(basename.split("_")[:3])
        character_name = basename.split("_")[3]
        txt_label = os.path.splitext(basename.split("_")[6])[0]
        if not os.path.exists(os.path.join(destination_target, "Colab Folder")):
            os.mkdir(os.path.join(destination_target, "Colab Folder"))
        fpath = os.path.join(destination_target, "Colab Folder")
        if not os.path.exists(os.path.join(fpath, character_name)):
            os.mkdir(os.path.join(fpath, character_name))
        outer_directory = os.path.join(fpath, character_name)
        destination_file_name= character_name + "-" + EPISODES[os.path.basename(one_up_folder)] + "-" + first_part + "-" + txt_label
        destination_directory = os.path.join(outer_directory, destination_file_name)
        if not os.path.exists(destination_directory):
            os.mkdir(destination_directory)
            copy(wav_files, destination_directory)
            txt_files = wav_files.replace(wav_ext, txt_ext)
            copy(txt_files, destination_directory)


#cleans up the extra label.json (not sure why have to find out)
def cleanup(directory, ext = '.wav'):
    abs_path = sorted([os.path.abspath(wav_files) for wav_files in glob.glob(os.path.join(directory, f'**/*{ext}'), recursive = True)])
    for files in abs_path:
        if not os.path.exists(os.path.join(os.path.dirname(files), 'label.json')):
            print(os.path.dirname(files))
            rmtree(os.path.dirname(files))

#fixes the sentence of the label json file
def fix_sentence(str):
    if str == "":                    # Don't change empty strings.
        return str
    if str[-1] in ["?", ".", "!"]:   # Don't change if already okay.
        return str
    if str[-1] == ",":               # Change trailing ',' to '.'.
        return str[:-1] + "."
    return str + "."                 # Otherwise, add '.'.




#Removes clips less than 1.5 seconds
def remove_short_clips(directory, ext = '.wav'):
    wav_path = sorted([os.path.abspath(path) for path in glob.glob(os.path.join(directory, f'**/*{ext}') , recursive = True)])
    short_files = []
    for files in tqdm.tqdm(wav_path):
        f = sf.SoundFile(files)
        seconds = f.frames / f.samplerate
        if seconds < 1.5:
            rmtree(os.path.dirname(files))
    print("the length of the clip length less than 1.5 seconds is: " + str(len(short_files)))

def strip_accents(text):
    text = unidecode.unidecode('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")

    return str(text)




#creates the metadata.csv in the very outer directory. 
#after completing this make sure to redo the entire process because i accidentally triggered trimsilence twice
def create_transcript_per_speaker(directory, txt_ext = '.txt'):
    label_path = sorted([os.path.abspath(path) for path in glob.glob(os.path.join(directory, f'**/*{txt_ext}') , recursive = True)])
    # metadata_location = os.path.dirname(os.path.dirname(label_path[0]))
        
    metadata_array = []
    for files in tqdm.tqdm(label_path):
        both_files = os.listdir(os.path.dirname(files).strip('"'))
        fileList = [file for file in both_files if file.endswith(".wav")]
        with open(files, "r") as input:
            for line, wav_file in zip(input, fileList):
                metadata_array.append(wav_file + "|" + unidecode.unidecode(line))
                if not os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(files))), 'metadata.csv')):
                    file_write = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(files))), 'metadata.csv'), "w")
                if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(files))), 'metadata.csv')):
                    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(files))), 'metadata.csv'), 'w') as filehandle:
                        for listitem in metadata_array:
                            filehandle.write('%s\n' % listitem)
                    
                

#copy all the wav files into a wav folder. delete the rest of the folders but keep except metadata.csv and wav folder
def create_wav_folder(directory, wav_ext = '.wav'):
    wav_path = sorted([os.path.abspath(path) for path in glob.glob(os.path.join(directory, f'**/*{wav_ext}') , recursive = True)])
    os.makedirs(os.path.join(directory, 'wavs/'), exist_ok=True)

    waves_folder = os.path.join(directory, 'wavs/')
    for files in wav_path:
        if files not in os.path.join(waves_folder, os.path.basename(files)):
            shutil.move(files, waves_folder)

    subdirectory = [shutil.rmtree(os.path.dirname(dirpath)) for dirpath, dirname, files in os.walk('MEGAsync Imports/Master file/Colab Folder') for random_file in files if (random_file.endswith('.txt'))]
    remove_empty_folder = [shutil.rmtree(dirpath) for dirpath, dirname, files in os.walk('MEGAsync Imports/Master file/Colab Folder') if not files]
    #print(configfiles)




if __name__ == '__main__':
    #STEP 1 (Only trigger if starting from bare scratch):
    #The three following commands come from soundfilemaniuplation file
    #soundfilemanipulation.remove_extra_period(source_directory, '.flac')
    #soundfilemanipulation.convert_flac_to_wav(source_directory, ext = '.flac')
    #soundfilemanipulation.delete_noisy_files(source_directory)

    #STEP 1:s
    #Creates the directories in the colab folder 
    # create_outer_directory(source_directory, wav_ext='.wav', txt_ext='.txt')

    # #STEP 2: 
    # #Removes the short clips < 1.5 seconds and the tree
    # remove_short_clips(colab_files)

    # #STEP 3: 
    # # Trim silences on both ends for data normalization
    # preprocessor = Preprocessor()
    # preprocessor.build_from_path()

    #Creates the overall transcript with speaker , quote, and phonemes (metadata.csv)
    create_transcript_per_speaker(colab_files)

    #puts all the wav into one folder and deletes the rest of the folders that only have text files
    create_wav_folder(colab_files)




#normalize_volume(colab_files, ext = '.wav')
#convert_wav_to_json(colab_files, ext_wav = ".wav", ext_json='.json')
#create_alignment_json(colab_files, ext1 = '.wav', ext2 = '.json')
#cleanup(colab_files)

#Step 0?: Downsample to 44k?
#Step 0?: Might be able to use noisy/very noisy files?
#Step 0?: Might have to use custom alignment dictionary?


#Step 1: create the outer directory with the wav file
#Step 2: Create the JSON of text from speaker
#Step 3: Run the aligner over those folders containing JSON and wav files
#Step 4: Look at which ones did not get aligned
#Step 5: Remove those that were not aligned properly from 48k -> 11050

#Step 6: Cut out the silence in beginning and end of clips
#Right now structure is wav, json, alignment.json
#Have to read in the alignment.json --> if words[0].alignedword == 'sp' --> get the start and end. cut out this chunk
                                        #if words.alignedword[0] != sp --> continue
                                        #if words.alignedword[-1] == sp --> get the start and end. Cut out this chunk
#Step 7: Cut out silence at end of clips
#Step 8: Cut out the less than 1.5 second clips
#Step 9: Remove the original alignment.json and replace with alignment2.json (corrected version with 1.5 seconds removed and silence removed)
#Step 10: put alignment and label json into one file with following structure: #wav/00_54_39_Spike_Neutral__So what's the good news_.wav | So what's the good news
                                                                               #wav/blah.wav | {S OW1} {W AH T S} {DH AH0} {G UH1 D} {N UW1 Z}
#Step 11: Create the file structure such as:[wav folder with name wav]
                                           #wav file:
                                           #wav/00_54_39_Spike_Neutral__So what's the good news_.wav | So what's the good news
                                           #wav/blah.wav | {S OW1} {W AH T S} {DH AH0} {G UH1 D} {N UW1 Z}


#Step 12: Copy the files into an outer directory of wav's. so structure would be like
                                                                    #wav 
                                                                    #-> 00_16_09_Zesty Gourmand_Neutral__The barest hint of a sensation.wav
                                                                    #-> 00_15_53_Zesty Gourmand_Smug__Anypony can throw ingredients together.wav
#final structure would be a folder with every single wav file not split up by each speaker and an outer metadata.csv with every single speaker