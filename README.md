# Senior Design Project

###### Ahmed Ahmed, Hannah Gonzalez

## Set up

Run: 
```
pip install SpeechRecognition 
```
```
pip install moviepy 
```
```
pip install pydub 
```
```
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
```
```
pip install transformers
```
```
pip install openai
```

## Transcription
```
python3 utility/transcribe.py 
```

## Summarization
```
python -m summarize.backend.summarizer-cli input_file_name_of_lecture_transcript
```
Example: python -m summarize.backend.summarizer-cli ./summarize/resources/CIS521_L1.txt

