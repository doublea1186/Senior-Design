from summarize.backend.utils.embeddings import sims_from_sentences
from summarize.backend.utils.query_openai import ask_openai
import re
from torch import Tensor


num_list_pattern = re.compile(r'\n[0-9]\. ')


def split_topic_list(response: str) -> list[str]:
    return re.split(num_list_pattern, response)


def topics_zero_shot(text: str) -> list[str]:
    # create prompt
    # ask openai and strip response
    # split based on regex
    # TODO: is there a functional difference between numbers and bullets?
    prompt = (f'What are the main topics in this text?\n\n'
              f'{text}\n\n'
              f'Topics:\n\n'
              f'1.')
    raw_response = ask_openai(prompt).strip()
    return split_topic_list(raw_response)


def topic_similarities(text1: str, text2: str) -> Tensor:
    topics1 = topics_zero_shot(text1)
    topics2 = topics_zero_shot(text2)
    return sims_from_sentences(topics1, topics2)


def max_topic_similarity(sims: Tensor) -> ...:
    # TODO: should this be a singular value or multiple?
    #  Single value could be more straightforward
    #  Multiple values could serve as a good tiebreaker?
    ...


if __name__ == '__main__':
    print(split_topic_list(f'first\n'
                           f'2. second\n'
                           f'3. third\n'
                           f'4. fourth'))
