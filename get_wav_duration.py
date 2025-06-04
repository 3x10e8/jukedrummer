# Wazzabeee/get_wav_duration.py
#   https://gist.github.com/Wazzabeee/5dc05b11b8529457cde7b3fea0c0a45e
import os
import sys
import wave

# Get the path to the directory from the command-line argument
if len(sys.argv) < 2:
    print("Usage: python script.py <directory>")
    sys.exit(1)
root_dir = sys.argv[1]

total_duration = 0  # Initialize total duration to 0

# Recursively traverse through the directory tree
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        # Check if the file is a WAV file
        if filename.endswith('.wav'):
            file_path = os.path.join(dirpath, filename)
            with wave.open(file_path, 'r') as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                duration = frames / float(rate)  # Calculate duration in seconds
                total_duration += duration

# Convert total duration to hours, minutes, and seconds
hours, remainder = divmod(total_duration, 3600)
minutes, seconds = divmod(remainder, 60)

print(f"Total duration of all WAV files: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")