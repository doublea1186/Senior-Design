import json
from transformers import GPT2TokenizerFast
from summarize.backend.utils.sentence_splitter import split_into_sentences
from summarize.backend.utils.constants import MAX_WORDS_PER_CHUNK


tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')


def json_from_file(path: str):
    """
    :param path: The location of a json
    :return: The Python representation of the json
    """
    with open(path) as json_file:
        return json.load(json_file)


def raw_dict_to_transcript(raw_dict) -> str:
    """
    Returns the raw transcript resulting from calling json_to_file
    on an AWS Transcribe output json.
    :param raw_dict: The Python object form of the AWS Transcribe output
    :return: The complete raw text from the json
    """
    return raw_dict['results']['transcripts'][0]['transcript']


def num_tokens(text: str) -> int:
    """
    Computes the number of GPT-2 tokens for a particular block of text.
    No GPT-3-specific solution is available without adding a node dependency,
    and I'd really rather not do that.
    :param text: A block of text
    :return: The number of tokens in the given text
    """
    tokenized = tokenizer(text)
    return len(tokenized['input_ids'])


def text_to_chunks(text: str, verbose=False) -> list[str]:
    sentences = split_into_sentences(text)
    if verbose:
        print(f'Number of sentences: {len(sentences)}')
        print(f'Sentence lengths: {[len(s) for s in sentences]}')
    chunks = []
    curr_block = []
    block_words = 0
    for s in sentences:
        curr_words = len(s.split())
        if block_words + curr_words > MAX_WORDS_PER_CHUNK:
            # 1 sentence minimum (enter this if curr_words > MAX but block is 0)
            if block_words == 0:
                chunks.append([s])
            else:
                chunks.append(curr_block)
            curr_block = []
            block_words = 0
        curr_block.append(s)
        block_words += curr_words
    if len(curr_block) > 0:
        chunks.append(curr_block)
    chunks = [' '.join(s) for s in chunks]
    if verbose:
        print(f'Number of chunks: {len(chunks)}')
        print(f"max chunk length: {max(len(x.split()) for x in chunks)} words")
    return chunks


def load_chunks_from_file(path: str) -> list[str]:
    return text_to_chunks(raw_dict_to_transcript(json_from_file(path)))


if __name__ == '__main__':
    tokens = 0
    with open('../../resources/cached-full-run/manually-tweaked.jsonl') \
            as file:
        for line in file:
            example = json.loads(line)
            tokens += num_tokens(example['prompt'])
            tokens += num_tokens(example['completion'])
    print(tokens)
    print(tokens / 1000 * .12)
