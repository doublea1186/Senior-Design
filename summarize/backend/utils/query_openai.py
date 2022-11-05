import openai
from getpass import getpass
from summarize.backend.utils.constants import MODEL, TEMPERATURE, RETURNED_TOKENS, \
    FREQUENCY_PENALTY, PRESENCE_PENALTY


def ask_openai(prompt: str, verbose=False, **kwargs) -> str:
    engine = kwargs.get('engine', MODEL)
    temperature = kwargs.get('temperature', TEMPERATURE)
    max_tokens = kwargs.get('max_tokens', RETURNED_TOKENS)
    top_p = kwargs.get('top_p', 1)
    frequency_penalty = kwargs.get('frequency_penalty', FREQUENCY_PENALTY)
    presence_penalty = kwargs.get('presence_penalty', PRESENCE_PENALTY)
    stop = kwargs.get('stop', None)

    # print(engine)
    response = openai.Completion.create(
        model=engine, prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens, top_p=top_p, frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty, stop=stop
    )

    if verbose:
        print(f'Prompt:\n'
              f'{prompt}\n'
              f'Full response JSON:\n'
              f'{response}')
    return response['choices'][0]['text'].strip()


def interactive_test() -> None:
    openai.api_key = getpass("Enter OpenAI API key:")
    # print(openai.Engine.list())
    model_prompt = input("Enter model prompt:")
    returned = ask_openai(model_prompt, verbose=True)
    print(returned)


if __name__ == '__main__':
    interactive_test()
