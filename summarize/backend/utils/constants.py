# change this to change choice of model and associated constants
CURRENT_MODEL = "fine-tune-05-06-22-ccb"

# set this to True if you have an NVIDIA GPU
CUDA = True


class Model:
    def __init__(self, name: str, max_tokens: int, price_per_1k: float):
        self.name = name
        self.max_tokens = max_tokens
        self.price_per_1k = price_per_1k


models = {
    'ada': Model('text-ada-001', 2048, .0008),
    'babbage': Model('text-babbage-001', 2048, .0012),
    'curie': Model('text-curie-001', 2048, .006),
    'davinci': Model('text-davinci-002', 4000, .06),
    'fine-tune-05-06-22': Model("davinci:ft-upenn-senior-design-projects-2022-05-06-05-21-51", 2048, .12),
    'fine-tune-05-06-22-ccb': Model("davinci:ft-ccb-lab-members-2022-06-24-04-30-17", 2048, .12)
}


MAX_ALLOWED_TOKENS = models[CURRENT_MODEL].max_tokens
MODEL = models[CURRENT_MODEL].name
PRICE_PER_1K = models[CURRENT_MODEL].price_per_1k

# default model parameters
TEMPERATURE = .6
RETURNED_TOKENS = 128
FREQUENCY_PENALTY = .7
PRESENCE_PENALTY = .7

# higher = more aggressive summarization/compression
# lower = more granular
MAX_WORDS_PER_CHUNK = 100

# number of tokens to reserve to summarize the current chunk
SUMMARY_TOKEN_TARGET = 200
TARGET_FEW_SHOT_EXAMPLES = 10
