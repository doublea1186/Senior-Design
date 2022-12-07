import sys
from summarize.backend.summarizer import summarize_file


# if __name__ == '__main__':
#     # index 0 arg is always name of script
#     input_path = sys.argv[1]
#     summarize_file(transcript_path=input_path,
#                    summary_path='./resources/CIS521_L1_summary_2.txt',
#                    out_csv_path='./resources/io_pairs_test.csv',
#                    out_finetune_path='./resources/fine-tune_test.jsonl',
#                    config_path='./config.txt',
#                    verbose=True, fine_tuned=True)
