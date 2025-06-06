# JukeDrummer
## Updates
For training JukeDrummer model using your own datasets, see [recipe.ipynb](./recipe.ipynb)

For using pre-trained JukeDrummer weights, these are the steps I followed to get the model weights provided in the original repo to work:
1. (if using VS code) create a conda environment. I used Python 3.8 to stay close to library versions provided in [requirements.txt](requirements.txt)
2. download model weight checkpoints from the Google Drive links in [get_ckpt.sh](./script/get_ckpt.sh). The `wget` commands may not work on some linux systems but directly downloading the files from Google Drive worked, use the same URLs as the `wget` calls.
3. some variables and paths had to be edited from the original repo, hence this fork. See commit history for all changes made.
4. copy some drumless WAV file to the ./input_drumless directory. Note that the models here expect a ~24s input as noted in the ISMIR paper. With some trial and error truncating your WAV to 23.78 seconds at 44.1kHz should work, see [truncate.py](./input_drumless/truncate_to_24s/truncate.py) 
5. generating drum WAVs. Note, this generates solo drum tracks (each sample_iters corresponds to a separate track) -- these would have to be mereged again with the drumless WAV to hear the final render.
```
python inference.py --exp_idx=1 --cuda=0 --input_dir=input_drumless --output_dir=output_with_drums --sample_iters=10
```
- [debug.py](./debug.py) could be used for stepping through the code in a python debugger.

## Source Repo's readme.md:
### Demo video 
[![Watch the video](https://img.youtube.com/vi/kfsN_46Rwq0/maxresdefault.jpg)](https://www.youtube.com/watch?v=kfsN_46Rwq0)

- Author: [Yueh-Kao Wu](), [Ching-Yu Chiu](https://github.com/SunnyCYC), [Yi-Hsuan Yang](http://mac.citi.sinica.edu.tw/~yang/)
- This repository contains the official implementation of the following paper: **JukeDrummer: Conditional Beat-aware Audio-domain Drum Accompaniment Generation via Transformer VQ-VA** [[arxiv](https://arxiv.org/abs/2210.06007)] [[demo](https://legoodmanner.github.io/jukedrummer-demo/)]
- Jukedrummer is a project on drum accopaniment generation given songs in which percussion instruments are completely absent (drumless songs) as input. The generated drum accompaniments should not only sound consistent with input but also sound similar to real drums.
- We use joined dataset consiting 3 different multi-track dataset: [MUSDB18](https://sigsep.github.io/datasets/musdb.html), [MedleyDB](https://medleydb.weebly.com
), [MixingSecret](https://musicinformatics.gatech.edu/conferences/mixing-secrets-a-multi-track-dataset-for-instrument-recognition/) after delete several duplicated songs in the joined dataset.
- We put our results in our [demo page](https://legoodmanner.github.io/jukedrummer-demo/). For further demonstration, please visit the site.

<!-- <img src="src/img/flowchart.jpg" width="500"> -->

---

## Prerequisites
- Python version >= 3.6
- Install dependencies
    ```bash 
    pip3 install -r requirements.txt
    ```
- GPU with >10 GB RAM (optional, but recommended)


---

## Inference
### Get pre-trained parameters
The script below would download the checkpoints to `ckpt/` folder.
```bash
bash script/get_ckpt.sh
```
### Generating
The model would load pre-trained parameters in `\ckpt` when inference.
```bash
python3 inference.py \
    --exp_idx \ # Determine the checkpoint id to load the pre-trained parameters
    --cuda \ # Determine the cuda id
    --input_dir \ # input drumless audio directory
    --output_dir \ # output audio directory
    --sample_iters \ # iterations of sampling
```
Note that `exp_id` could be choiced from `1, 2, 11, 12`:
- `1`: Tranformer encoder/decoder + Low-level beat information 
- `2`: Transformer encoder/decoder 
- `11`: Tranformer encoder + Low-level beat information
- `12`: Tranformer encoder

According to our experiment, model with checkpoint `exp_id=1` is the **best** in both subjective and objective metrics. 

(For more configuration setting, please refer `hparams.py`)


---

## Training
### Preprocessing
1. Run the script below to establish the directories. In order to expedite the training processes, several intermediate data would be generated and stored in this directories.
    ```bash 
    bash script/build_folder.sh
    ```
2. Every Raw wave should be separated into a **drum track** and a **drumless track**. Then, put drum tracks into `audio/target` folder and put drumless tracks into `audio/others` folder
3. The preprocessing has 4 stages:
    1. Segmentation by either downbeats or hop window
    2. Extract Mel spectrograms from segemented audio waves
    3. Divide dataset into train & valid subset
    4. Beat Information Extraction


4. Users can run our script below to accomplish the whole preprocessing directly:
    ```bash 
    bash script/preprocessing.sh
    ```

### Train

- For complete training process, there are 5 stages:
    1. Train drum VQ-VAE
    2. Train drumless VQ-VAE
    3. Using VQ-VAEs to extract drum tokens and drumless tokens from Mel-spectrogram respectively.
    4. Train lanuguage model (Transformer) with those extracted tokens.
- Users can either take advantage of our script below to train the model or separately run those commands in script.
    ```bash
    bash script/train.sh
    ```
---

## Limitation
However, there are several problems still remaining to be solved in future works:  
- **Generalizability**: Generated accompaniments are worse when using recordings outside our joined dataset
- **Stability**: The model struggles to change its tempo going through different sections of a song.
- **Dependency**: Insufficient clues for locating beats and tempo would lead to bad accompaniment generation.

## Reference:
- [Jukebox](https://github.com/openai/jukebox)
- [HifiGAN](https://github.com/jik876/hifi-gan)
    - The contents in the directory, "hifi_gan", are cloned and revised from this repo. 
- [madmom](https://github.com/CPJKU/madmom)
- [drum-aware4beat](https://github.com/SunnyCYC/drum-aware4beat)
    - The contents in the directory, "DrumAware4Beat", are cloned and revised from this repo. 

## Contact:
Feel free to email me: yk.lego09@gmail.com if you have any problem.

## Citation:
```
@inproceedings{wu2022jukedrummer, 
	title={JukeDrummer: Conditional Beat-aware Audio-domain Drum Accompaniment Generation via Transformer VQ-VA},
	author={Yueh-Kao Wu, Ching-Yu Chiu, Yi-Hsuan Yang},
	booktitle = {Proc. Int. Society for Music Information Retrieval Conf.},
	year={2022},
}
```
