import argparse
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utility import transcribe 

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description="A script for Question Answer Generation")
    parser.add_argument("--path", type=str)
    args = parser.parse_args()


    # wav file will be contained in wav_file_path
    wav_file_path = transcribe.convert_from_video(args.path)

    # transcribed text file will be contained in output_file_txt
    output_file_txt = wav_file_path[:-4] + '.txt'
    
    # this function transcribes wav file to text
    transcribe.get_large_audio_transcription(wav_file_path, output_file_txt)

    # you can now use output_file_txt as the filepath to summarize


