import os
import glob
import json
import numpy as np
#from scripts.audio_preprocess import normalize_volume

# load preprocessing config file
with open("../config.json") as f:
    conf = json.loads(f.read())

DELETE_NOISY = conf["DELETE_NOISY"]
DELETE_VERY_NOISY = conf["DELETE_VERY_NOISY"]

label_file = 'MEGAsync Imports/Master file/Sliced Dialogue/'

#Removes the extra period at the end of the file like "blah..wav" -> "blah.wav"
def remove_extra_period(directory, ext='.flac'):
    file_array = sorted([os.path.abspath(file_path) for file_path in glob.glob(os.path.join(directory, f"**/*{ext}"), recursive = True)])

    if not len(file_array):
        print(f'[info] There are no "{ext}" files found inside {directory} dataset. Please put a correct file extension')

    file_dict = {x: (os.path.splitext(x)[0].rstrip('.')+os.path.splitext(x)[-1]) for x in file_array if x != (os.path.splitext(x)[0].rstrip('.')+os.path.splitext(x)[-1])}
    for src, dst in file_dict.items():
        os.rename(src,dst)


#Convert all flac files to wav files
def convert_flac_to_wav(directory, ext = '.flac'):
    file_array = sorted([os.path.abspath(file_path) for file_path in glob.glob(os.path.join(directory, f"**/*{ext}"), recursive = True)])

    if not len(file_array):
        print(f'[info] There are no "{ext}" files found inside {directory} dataset. Please put a correct file extension')

    file_dict = {x: (os.path.splitext(x)[0] + '.wav') for x in file_array if x != (os.path.splitext(x)[0] + '.wav')}
    
    for src, dst in file_dict.items():
        os.rename(src, dst)
    
#Deletes all noisy and very noisy files
def delete_noisy_files(directory):
    if os.path.exists(directory):
        if DELETE_NOISY:
            for files in glob.glob(os.path.join(directory, '**', '*_Noisy_*'), recursive=True):
                os.remove(files)
        if DELETE_VERY_NOISY:
             for files in glob.glob(os.path.join(directory, '**', '*_Very Noisy_*'), recursive=True):
                os.remove(files)

##################################################################################
### for all audio                                                              ###
###   Equalize volumes/amplitudes (avoid clipped samples for later sections)   ###
##################################################################################
#normalize_volume(label_file)


##################################################################################
### for all audio                                                              ###
###  - High-pass filter                                                        ###
###  - Low-Pass filter                                                         ###
###  - Resample to target sample rate. # note, need to save sr info somewhere. ###
###  - Trim                                                                    ###
##################################################################################

##################################################
### Collect all metadata into central object   ###
###  - audio paths                             ###
###  - transcripts                             ###
###  - speaker names                           ###
###  - emotions                                ###
###  - noise levels                            ###
###  - source                                  ###
###  - source type                             ###
###  - native sample rate                      ###
##################################################
def collect_metadata(directory):
    #collect metadata in this dict object
    meta = {}

    for file_path in glob.glob(directory + '/**/*wav', recursive=True):
        print(file_path)
    



remove_extra_period(label_file, '.flac')
convert_flac_to_wav(label_file, ext = '.flac')
delete_noisy_files(label_file)

#collect_metadata(label_file)