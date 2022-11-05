from summarize.backend.utils.text_utils import num_tokens
from summarize.backend.utils.constants import PRICE_PER_1K


class Chunk:
    """
    A small class to link text to the number of tokens it takes for GPT-2
    to process.
    """

    def __init__(self, text: str):
        self.text = text
        self.tokens = num_tokens(text)

    def __hash__(self):
        return hash(self.text)


class ResultChunk(Chunk):
    def __init__(self, to_summarize: str, prompt: Chunk, response: Chunk):
        self.to_summarize = to_summarize
        self.prompt = prompt
        self.response = response
        self.transcript = to_summarize
        # in this class, the text and tokens no longer correspond
        # "text" is the stuff that was unique to this query
        # "tokens" includes context that was used to aid generation
        super().__init__(f'Text:\n\n'
                         f'{to_summarize}\n\n'
                         f'Summary:\n\n'
                         f'{response.text}')
        self.tokens = prompt.tokens + response.tokens

    def __hash__(self):
        return hash(self.response.text)


class Document:
    def __init__(self, results: list[ResultChunk]):
        self.results = results
        self.summary = results_to_summary(results)
        self.tokens = results_to_tokens(results)
        self.cost = results_to_cost(results)


def results_to_summary(results: list[ResultChunk]) -> str:
    # TODO: improve this with headers (this is currently chronological)
    return '\n'.join([r.response.text for r in results])


def results_to_tokens(results: list[ResultChunk]) -> int:
    return sum(r.tokens for r in results)


def results_to_cost(results: list[ResultChunk]) -> float:
    return results_to_tokens(results) / 1000 * PRICE_PER_1K
