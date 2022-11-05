import json
import re


if __name__ == '__main__':
    outputs = []
    with open('../../resources/cached-full-run/521-fine-tune.jsonl') as jsonl:
        for example in jsonl:
            obj = json.loads(example)
            obj['completion'] = f"{obj['completion']}\n\n###"
            init_prompt = obj['prompt']
            prompt_items = re.split('\n\n|\n', init_prompt)
            curr_prompt = prompt_items[-2]

            if len(prompt_items) > 5:
                prev_summaries = '\n'.join(prompt_items[5::5])
                new_prompt = (f'Previous summaries:\n\n'
                              f'{prev_summaries}\n\n'
                              f'Text:\n\n'
                              f'{curr_prompt}\n\n'
                              f'Summary:')
            else:
                new_prompt = (f'Text:\n\n'
                              f'{curr_prompt}\n\n'
                              f'Summary:')
            obj['prompt'] = new_prompt
            outputs.append(obj)
    with open('../../resources/cached-full-run/updated-fine-tune.jsonl',
              'w') as out_file:
        for o in outputs:
            out_file.write(json.dumps(o))
            out_file.write('\n')
