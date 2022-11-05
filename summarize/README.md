# Playground

The fine-tuned model is `davinci:ft-ccb-lab-members-2022-06-24-04-30-17`. The
input format depends on whether you're using zero-shot (summarizing the first
part of the lecture) or not.

## Zero-shot

Playground example [here](https://beta.openai.com/playground/p/r12w2TWcU6TGCdrKpx8lsgai?model=davinci:ft-ccb-lab-members-2022-06-24-04-30-17)

```
Text:

[raw transcript text to be summarized, no line breaks]

Summary:
```

## Previous context

Playground example [here](https://beta.openai.com/playground/p/IxLDGo6pW8mAdDO0wzKtb0oe?model=davinci:ft-ccb-lab-members-2022-06-24-04-30-17)

```
Previous summaries:

[previous summary 1]
[previous summary 2]
...
[previous summary n]

Text:

[raw transcript text to be summarized, no line breaks]

Summary:
```

Previous summaries should be in chronological order (the `n` summaries
immediately preceding the section to be summarized)

# Environment setup

Create a `config.txt` in the repo root. It should have one line of text
(your API key). Then follow the instructions for one of the virtual environment
setups below.

## venv

1. `python -m venv ./senior-design-venv`
2. Activate the venv with instructions in the table [here](https://docs.python.org/3/library/venv.html)
   ("The invocation of the script is platform-specific..."). Your shell input
   should now be preceded by `(senior-design-venv)` or whatever the name of your
   particular venv is.
3. ```bash
   pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
   pip install transformers
   pip install openai
   ```

## Conda

Use conda ([miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation)
if you want something lightweight <sup>[why conda?](#why-conda)</sup>).

```bash
conda create --name senior-design python=3.9 -y
conda activate senior-design
conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
conda install -c huggingface transformers -y
conda install -c conda-forge openai -y
```

## Notes

1. The environment can be named whatever you want - `senior-design-venv` and
   `senior-design` are just working examples.
2. The Pytorch install will vary based on your architecture. Refer
   to [this page](https://pytorch.org/get-started/locally/) for specific
   instructions (note that torch conda binaries don't work on M1)
3. Transformers install instructions [here](https://huggingface.co/docs/transformers/installation)
   for reference
4. OpenAI Python API repo [here](https://github.com/openai/openai-python)

# Running the summarizer

If you want to see intermediate prompts/summaries, go to the 
`summarize_file` call in `backend/summarizer-cli.py` and set `verbose=True`.

## PyCharm

1. Make sure your interpreter is the virtual environment you set up previously 
2. Open `summarizer-cli.py`
3. Change `input_path` to the path to the transcript text
4. Run the script

## CLI

1. Make sure you're at the repo root.
2. `python -m backend.summarizer-cli <INPUT_PATH>`

   `INPUT_PATH` is the path to the transcript text.

# Why conda?

Transcription is a work in progress - I'm hoping to find something that's
accurate, splits content into sentences, and can be run locally. So ideally
that's something that runs on Pytorch with CUDA enabled, and conda lets that
happen in a reproducible virtual environment (it's not the only way,
[venv](https://docs.python.org/3/library/venv.html) would probably work too).
