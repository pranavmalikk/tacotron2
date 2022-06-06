   
#processes the rest of the MFA values. skips stereo files (data.shape != 2)
# def skip_dimension_alignments(directory, alignment_file = 'alignment.json'):
#     wav_path = sorted([os.path.abspath(path) for path in glob.glob(os.path.join(directory, '**/*.wav'), recursive = True)])
#     missing_files_wav = [files for files in wav_path if not os.path.exists(os.path.join(os.path.dirname(files), alignment_file))]
#     missing_volume_wav_files = []
#     missing_volume_json_files = []
#     missing_volume_alignment_files = []
#     for file in missing_files_wav:
#         data, rate = sf.read(file)
#         print(str(file) + " " + str(data.shape))
#         if len(data.shape) != 2:
#             missing_volume_wav_files.append(file)
#             missing_volume_json_files.append(os.path.join(os.path.dirname(file), 'label.json'))
#             missing_volume_alignment_files.append(os.path.join(os.path.dirname(file), alignment_file))
#         else:
#             # print(len(data.shape))
#             rmtree(os.path.dirname(file))

#     print(len(missing_files_wav))
#     pyfoal.from_files_to_files(missing_volume_json_files, missing_volume_wav_files, missing_volume_alignment_files)


#Creates a wav copy inside the folder so that the "original" wav gets retained (dont think it's necessary)
# def create_wav_copy(directory, ext = '.wav'):
#     wav_path = sorted([os.path.abspath(path) for path in glob.glob(os.path.join(directory, '**/*{ext}'), recursive = True)])
#     missing_files_wav = [files for files in wav_path if not os.path.exists(os.path.join(os.path.dirname(files), 'alignment.json'))]
#     print(missing_files_wav)
#     create_new_directory = [os.mkdir(os.path.join(os.path.dirname(path), 'original_wav')) for path in missing_files_wav if not os.path.exists(os.path.join(os.path.dirname(path), 'original_wav'))]
#     for files in wav_path:
#         destination_location = os.path.join(os.path.dirname(files), 'original_wav', os.path.basename(files))
#         print(destination_location)
#         if not os.path.exists(destination_location):
#              copy(files, os.path.join(os.path.dirname(files), 'original_wav'))

#Removes the silence in the beginning and end of file
# def remove_silence(directory, ext = '.wav', json_file = 'alignment2.json'):
#     wav_path = sorted([os.path.abspath(path) for path in glob.glob(os.path.join(directory, f'**/*{ext}') , recursive = True)])
#     json_path = sorted([os.path.abspath(path) for path in glob.glob(os.path.join(directory, f'**/*{json_file}'), recursive = True)])

#     for json_file, wav_file in zip(json_path, wav_path):
#         f = open(json_file)
#         json_object = json.load(f)
#         first_value = [value for key,value in json_object['words'][0].items()]
#         last_value = [value for key, value in json_object['words'][-1].items()]
#         final_sound = AudioSegment.from_file(wav_file)
#         if first_value[0] == 'sp' and last_value[0] == 'sp':
#             print(len(final_sound))
#             print(wav_file)
#             ending_time_first_silence = first_value[2]
#             print("Beginning frame end sp " + str(ending_time_first_silence))
#             starting_time_last_silence = last_value[1]
#             print("Last frame start " + str(starting_time_last_silence))
#             new_starting_time = ending_time_first_silence * 1000
#             new_ending_time = starting_time_last_silence * 1000
#             final_sound = final_sound[new_starting_time:new_ending_time]
#             final_sound.export(wav_file, format = 'wav')
            
#         elif first_value[0] == 'sp' and last_value[0] != 'sp':
#             print(len(final_sound))
#             print(wav_file)
#             ending_time_first_silence = first_value[2]
#             print("Beginning frame end sp " + str(ending_time_first_silence))
#             new_starting_time = ending_time_first_silence* 1000
#             final_sound = final_sound[new_starting_time:]
#             final_sound.export(wav_file, format = 'wav')
        
#         elif first_value[0] != 'sp' and last_value[0] == 'sp':
#             print(len(final_sound))
#             print(wav_file)
#             starting_time_last_silence = last_value[1]
#             print("Last frame start " + str(starting_time_last_silence))
#             new_ending_time = starting_time_last_silence * 1000
#             final_sound = final_sound[:new_ending_time]
#             final_sound.export(wav_file, format = 'wav')



# def clean_adjusted_alignment(directory, wav_ext = '.wav',  json_ext = 'label.json', alignment_ext = 'alignment2.json'):
#     wav_path = sorted([os.path.abspath(path) for path in glob.glob(os.path.join(directory, f'**/*{wav_ext}'), recursive = True)])
    
#     missing_wav_files = []
#     missing_json_files = []
#     missing_alignment_files = []

#     for files in wav_path:
#         data, rate = sf.read(files)
#         if not os.path.exists(os.path.join(os.path.dirname(files), "alignment2.json")):
#             print(data.shape[0])
#             missing_wav_files.append(files)
#             missing_json_files.append(os.path.join(os.path.dirname(files), 'label.json'))
#             missing_alignment_files.append(os.path.join(os.path.dirname(files), 'alignment2.json'))

#     print(missing_wav_files)

#     pyfoal.from_files_to_files(missing_json_files, missing_wav_files, missing_alignment_files)

######ARPABET#########


#Custom dictionary lookup
# def load_arpadict(sentence, dict_path = '../merged_dictionary.txt'):
#         # load dictionary as lookup table
#         final_dict = {}
#         with open(dict_path) as f:
#             for index, line in enumerate(f):
#                 if sentence in line:
#                     final_dict[sentence] = unidecode(' '.join(line.split()[1:]).strip())
#         return final_dict

# def convert_to_arpa(text, punc="!?,.;:␤#-_'\"()[]\n"):
#     out = []
#     for word in text.split(" "):
#         end_chars = ''; start_chars = ''
#         while any(elem in word for elem in punc) and len(word) > 1:
#             if word[-1] in punc:
#                 end_chars = word[-1] + end_chars
#                 word = word[:-1]
#             elif word[0] in punc:
#                 start_chars = start_chars + word[0]
#                 word = word[1:]
#             else:
#                 break
#         try:
#             word = str(load_arpadict(word.upper()))
#         except KeyError:
#             pass
#         out.append((start_chars + (word or '') + end_chars).rstrip())
#     return ' '.join(out)

#Create the JSON document transcription of each wav file
#Also creates the alignment JSON
# def convert_wav_to_json(directory, ext_wav = ".wav", ext_json = ".json"):
#     wav_path = sorted([os.path.abspath(path) for path in glob.glob(os.path.join(directory, f'**/*{ext_wav}'), recursive = True)])
#     json_path = sorted([os.path.abspath(path) for path in glob.glob(os.path.join(directory, f'**/*{ext_json}'), recursive = True)])
#     #directory_path = sorted([os.path.join(os.path.dirname(files), "alignment.json") for files in json_path])
#     characters = {}
#     content = {}
#     for files in wav_path:
#         print(files)
#         #creates the character object
#         characters['character'] = os.path.basename(files.split("_")[3])
#         characters['emotion'] = os.path.basename(files.split("_")[4])
#         #creates the content (txt) object -> joins the value from beyond the 6th split, removes all "_" and replaces the end with nothing
#         content['content'] = "_".join(os.path.basename(files).split("_")[6:]).replace("_", "?").replace('.wav', '').replace('-', '').replace("'", '').lower()
#         for key, value in content.items():
#             content[key] = fix_sentence(value)
#         character_object = {
#             #'speaker': characters['character'],
#             #'emotions': characters['emotion'],
#             'quote': content['content'] 
#         }
#         # print(convert_to_arpa(character_object['quote']))
#         if not os.path.exists(os.path.join(os.path.dirname(files), 'label.json')):
#             file_write = open(os.path.join(os.path.dirname(files), 'label.json'), "w")
#         if os.path.exists(os.path.join(os.path.dirname(files), 'label.json')):
#             file_write = open(os.path.join(os.path.dirname(files), 'label.json'), "w")
#             json.dump(character_object['quote'], file_write)
    #pyfoal.from_files_to_files(json_path, wav_path, directory_path)

##after removing silence have to re-align the label.json with the wav file
    #clean_adjusted_alignment(colab_files)
    #post_remove_silence_MFA(colab_files, ext_wav = ".wav", ext_json = "label.json")
    #post_remove_silence_MFA('A. K./', ext_wav = ".wav", ext_json = "label.json")