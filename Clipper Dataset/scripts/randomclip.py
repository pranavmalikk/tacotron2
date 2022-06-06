import random
from numpy import clip
import torchaudio

#waveform, sample_rate = torchaudio.load('Igneous-fim:s5e20-00-06-05/00_06_05_Igneous_Neutral__I am called igneous rock pie, son of thelmspar granite pie.wav')
#waveform, sample_rate = torchaudio.load('Igneous-fim:s5e20-00-06-02/00_06_02_Igneous_Neutral__Surely thy name is not but granny smith.wav')
waveform, sample_rate = torchaudio.load('Igneous-fim:s5e20-00-14-25/00_14_25_Igneous_Neutral__Oh my.wav')

print(waveform)
# class RandomClip:
#     def __init__(self, sample_rate, waveform):
#         self.vad = torchaudio.functional.vad(waveform,
#             sample_rate=sample_rate, trigger_level=7.0)

#     def __len__(self):
#         return len(self.vad)

#     def __call__(self, audio_data):

#         return self.vad(audio_data) # remove silences at the beggining/end

upgraded_wave = torchaudio.functional.vad(waveform, sample_rate)
torchaudio.save('Igneous-fim:s5e20-00-14-25/something.wav', upgraded_wave, sample_rate) 
