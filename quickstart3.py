import re
from google.cloud import speech
from pydub import AudioSegment
import wave

def get_wav_sample_rate(file_path):
    with wave.open(file_path, 'rb') as wf:
        sample_rate = wf.getframerate()
    return sample_rate

def convert_to_mono(input_path, output_path):
    stereo_audio = AudioSegment.from_wav(input_path)
    mono_audio = stereo_audio.set_channels(1)
    mono_audio.export(output_path, format="wav")

def analyze_transcript(transcript):
    # 습관어 선언
    habit_words = ['어', '그']

    # 습관어 등장 횟수 초기화
    habit_counts = {word: transcript.count(word) for word in habit_words}
    
    return habit_counts

def run_quickstart():
    file_path = "C:/Users/yimkj/speech/mono_audio.wav"
    convert_to_mono("C:/Users/yimkj/speech/sga2.wav", file_path)

    client = speech.SpeechClient()

    # WAV 파일의 샘플링 속도 확인
    sample_rate = get_wav_sample_rate(file_path)

    audio_content = None
    with open(file_path, "rb") as audio_file:
        audio_content = audio_file.read()
    
    audio = speech.RecognitionAudio(content=audio_content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,  # WAV 파일의 실제 샘플링 속도로 설정
        language_code="ko-KR",
    )

    response = client.recognize(config=config, audio=audio)

    transcript = response.results[0].alternatives[0].transcript
    print(f"Transcript: {transcript}")

    # 습관어 분석
    habit_counts = analyze_transcript(transcript)
    for word, count in habit_counts.items():
        print(f"'{word}': {count}번")

if __name__ == "__main__":
    run_quickstart()
