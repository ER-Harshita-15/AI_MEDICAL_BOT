#Step1a: Setup Text to Speech–TTS–model with gTTS
import os
from gtts import gTTS

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)


input_text="Hi this is Medical Agent developed by Harshita!"
#text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")

#this has created a file gtts_testing.mp3 in the current directory pronouncing the input text

#Step1b: Setup Text to Speech–TTS–model with ElevenLabs
import elevenlabs
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY=os.environ.get("ELEVENLABS_API_KEY")


def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio=client.generate(
        text= input_text,
        voice= "Alice",
        output_format= "mp3_22050_32",
        model= "eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)

#text_to_speech_with_elevenlabs_old(input_text, output_filepath="elevenlabs_testing.mp3") 


#Step2: Use Model for Text output to Voice

import subprocess
import platform
"""""
def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


input_text="Hi this is Ai with Harshita, autoplay testing!"
text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")
"""""
from gtts import gTTS
from pydub import AudioSegment
import subprocess
import platform
import os

def text_to_speech_with_gtts(input_text, mp3_filepath="gtts_audio.mp3", wav_filepath="gtts_audio.wav"):
    language = "en"

    # Step 1: Generate the MP3 audio using gTTS
    tts = gTTS(text=input_text, lang=language, slow=False)
    tts.save(mp3_filepath)

    # Step 2: Convert MP3 to WAV using pydub
    try:
        audio = AudioSegment.from_mp3(mp3_filepath)
        audio.export(wav_filepath, format="wav")
    except Exception as e:
        print(f"Error converting MP3 to WAV: {e}")
        return

    # Step 3: Play the WAV file
    os_name = platform.system()
    try:
        if os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();'])
        elif os_name == "Darwin":  # macOS
            subprocess.run(['afplay', wav_filepath])
        elif os_name == "Linux":
            subprocess.run(['aplay', wav_filepath])  # May need ffplay or mpg123 based on system
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio:\n{e}")

# Run the function
input_text = "Hi this is AI with Harshita, testing MP3 to WAV conversion and playback!"
#text_to_speech_with_gtts(input_text)


import os
import platform
import subprocess
from pydub import AudioSegment
from elevenlabs import ElevenLabs, save

def text_to_speech_with_elevenlabs(input_text, mp3_filepath="elevenlabs_audio.mp3", wav_filepath="elevenlabs_audio.wav"):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    # Step 1: Generate MP3 from ElevenLabs
    audio = client.generate(
        text=input_text,
        voice="Alice",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    save(audio, mp3_filepath)

    # Step 2: Convert MP3 to WAV using pydub
    try:
        sound = AudioSegment.from_mp3(mp3_filepath)
        sound.export(wav_filepath, format="wav")
    except Exception as e:
        print(f"Error converting MP3 to WAV: {e}")
        return

    # Step 3: Play the WAV audio
    os_name = platform.system()
    try:
        if os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();'])
        elif os_name == "Darwin":  # macOS
            subprocess.run(['afplay', wav_filepath])
        elif os_name == "Linux":
            subprocess.run(['aplay', wav_filepath])  # Or try mpg123, ffplay
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio:\n{e}")

    return wav_filepath


    # Optional: Cleanup mp3 if not needed
    # os.remove(mp3_filepath)

# Example usage:
#text_to_speech_with_elevenlabs(input_text)
