#%% Trucate WAVs to 24s as that's the max sample len for JukeDrummer
# Actually 24s didn't work, but 23.78s at 44.1kHz does fit the size expected by the LanguageModel
from scipy.io import wavfile
from glob import glob
import numpy as np

MAX_DURATION_s = 23.78

wav_file_paths = glob('input_drumless/truncate_to_24s/sounds/*.wav')
print(wav_file_paths)

for file_path in wav_file_paths:
    sr, data = wavfile.read(file_path)
    
    # scale to 32b float or VS code won't play it
    # https://stackoverflow.com/a/51085663
    max_sample = np.max(np.abs(data))
    data_f32 = (data/max_sample).astype(np.float32)
    print(data_f32.shape, sr)

    N_24 = int(sr*MAX_DURATION_s)
    data_24s = data_f32[:N_24, :]

    # assume we can only work with mono audio
    data_24s_mono = np.mean(data_24s, axis=-1)

    wav_out_path = file_path.split('.wav')[0] + f"_{str(MAX_DURATION_s).replace('.', 'p')}s.wav"
    wavfile.write(wav_out_path, sr, data_24s_mono)
    
# %%
