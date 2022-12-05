import argparse
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utility import transcribe 
from summarize.backend import summarizer
from qa import qa

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
    summary_path = './resources/' + wav_file_path[:-4] + '_summary.txt'
    summarizer.summarize_file(transcript_path=output_file_txt,
                #    summary_path='./resources/CIS521_L1_summary_2.txt',
                   summary_path= summary_path,
                   out_csv_path='./resources/io_pairs_test.csv',
                   out_finetune_path='./resources/fine-tune_test.jsonl',
                   config_path='./config.txt',
                   verbose=True, fine_tuned=True)
    
    output_file_qa = wav_file_path[:-4] + "_question_answer.csv"

    text_lines = qa.read_file(summary_path)
    chunked_for_qa = qa.split_sentence_chunks(500, text_lines)
    cleaned_for_qa = qa.removing_new_lines(chunked_for_qa)
    class_name = "AI and Philosophy"
    lecture_number = 1
    qa.generate_questions_in_csv(output_file_qa, cleaned_for_qa, class_name, lecture_number)


