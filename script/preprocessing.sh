#!/bin/bash

#python3 utils/preprocess.py --audio_dir data/audio --segment_audio_dir data/segment_audio --mel_dir data/mel --beat_dir data/token --cuda 0
python3 utils/preprocess.py --audio_dir data/audio --segment_audio_dir data/segment_audio --mel_dir data/mel --beat_dir data/beats --cuda 0
#python3 utils/preprocess.py --audio_dir DrumCovers/data/audio --segment_audio_dir DrumCovers/data/segment_audio --mel_dir DrumCovers/data/mel --beat_dir DrumCovers/data/token --cuda 0