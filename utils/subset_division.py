from email import parser
import pickle
import numpy as np
import os
import argparse
import random

def write_subset(segments, pkl_path, valid_precentage=0.2):
    # divide dataset into training set and validation set by Mels of complete songs from segemented clips
    # Note: this means that segments of the same song won't get split between train and val, which is good
    nfile = len(os.listdir('data/audio/target/'))
    segments = sorted(segments)
    fns = {}
    train_set = []
    valid_set = []
    for s in segments:
        if s not in fns:
            fns[s.rsplit('_', 1)[0]] = 'valid' if len(fns) < round(nfile * valid_precentage) else 'train'
        if fns[s.rsplit('_', 1)[0]] == 'train':
            train_set += [s]
        elif fns[s.rsplit('_', 1)[0]] == 'valid':
            valid_set += [s]
    #print(len(fns), fns)
    with open(os.path.join(pkl_path, 'dataset.pkl'), 'wb') as f:
        pickle.dump([sorted(train_set), sorted(valid_set)], f)

def comparing(data_dir):
    # comparation between 2 dataset

    segments = os.listdir(os.path.join(data_dir, 'target'))
    fns = []
    for s in segments:
        if os.path.isfile(os.path.join(data_dir, 'others', s)) and \
            np.load(os.path.join(data_dir, 'target', s)).shape[1]==4096 and \
            np.load(os.path.join(data_dir, 'others', s)).shape[1]==4096:
            fns.append(s)
        else:
            print(f'{s} is not of size 4096?')
    return fns

def inference(mel_dir, pkl_path):
    print('step 3: divide into subsets')
    fns = comparing(mel_dir)
    #print(fns) # these are all the segments
    write_subset(fns, pkl_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio_dir', type=str, default=None)
    parser.add_argument('--mel_dir', type=str, default=None)
    parser.add_argument('--pkl_path', type=str, default=None)

    args = parser.parse_args()
    fns = comparing(args.mel_dir)
    write_subset(fns, args.pkl_path)
    