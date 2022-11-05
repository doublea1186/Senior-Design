import pyperclip
import json


def review(input_jsonl: str, out_jsonl: str):
    with open(input_jsonl) as in_file, open(out_jsonl, 'w') as out_file:
        for line in in_file:
            json_obj = json.loads(line)
            clipped = json_obj['completion'].split('\n')[0]
            pyperclip.copy(clipped)
            corrected = input(f'{clipped}\n')
            json_obj['completion'] = f'{corrected}\n\n###'
            out_file.write(json.dumps(json_obj))
            out_file.write('\n')
            print('---')


if __name__ == '__main__':
    review('../../resources/cached-full-run/updated-fine-tune.jsonl',
           '../../resources/cached-full-run/manually-tweaked.jsonl')
