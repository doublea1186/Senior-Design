import speech_recognition as sr 
import sys
from moviepy.editor import * 
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence


def get_large_audio_transcription(audio_file: str, output_file: str):
    """
    Transcribe a long audio file.

    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks.

    Args:
        audio_file: Path to audio file.
        output_file: Path to transcribed output file.
    """
    r = sr.Recognizer()
    sound = AudioSegment.from_wav(audio_file)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 1500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text

        # delete created chunk
        os.remove(chunk_filename)
    
    text_file = open(output_file, "w")
    text_file.write(whole_text)
    text_file.close()
    os.remove(folder_name)

def convert_from_video(video_file):
    '''
    Convert a video file to an audio file.

    The supported formats are mp3 and mp4.

    Args:
        video_file: Path to video file.
    '''
    format = video_file[-4:]

    if format == '.mp4' or format == '.mp3':
        clip = VideoFileClip(video_file)
        clip.audio.write_audiofile(video_file[:-4] + '.wav')
    else:
        raise ValueError(
            'Unsupported format. Only mp3 and mp4 are supported. \n'
            f'Got {format}'
            )

if __name__ == '__main__':
    file_name = 'testing/cis521_lecture_1.wav'
    output_file = 'testing/cis521_lecture_1.txt'
    get_large_audio_transcription(file_name, output_file)