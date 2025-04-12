import os
import subprocess
import platform
from dotenv import load_dotenv
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs

load_dotenv()

# Get API key
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    raise ValueError("Missing ELEVENLABS_API_KEY! Set it in your environment variables.")

# Step 1a: Text-to-Speech using gTTS
def text_to_speech_with_gtts(input_text, output_filepath):
    try:
        language = "en"
        audioobj = gTTS(text=input_text, lang=language, slow=False)
        audioobj.save(output_filepath)
        play_audio(output_filepath)
    except Exception as e:
        print(f"Error in gTTS: {e}")

# Step 1b: Text-to-Speech using ElevenLabs
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio = client.generate(
            text=input_text,
            voice="Aria",
            output_format="mp3_22050_32",
            model="eleven_turbo_v2"
        )
        elevenlabs.save(audio, output_filepath)
        play_audio(output_filepath)
    except Exception as e:
        print(f"Error in ElevenLabs API: {e}")

# Step 2: Cross-platform audio playback
def play_audio(file_path):
    os_name = platform.system()
    try:
        if os_name == "Windows":  
            subprocess.run(["start", "", file_path], shell=True)  # Opens in default media player
        elif os_name == "Darwin":  
            subprocess.run(['afplay', file_path])  # macOS
        elif os_name == "Linux":  
            subprocess.run(['mpg123', file_path])  # Use mpg123 or ffplay
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"Error playing audio: {e}")

# Run tests
if __name__ == "__main__":
    input_text = "Hello, this is AI with Hassan!"
    
    print("Testing gTTS...")
    text_to_speech_with_gtts(input_text, "gtts_testing.mp3")

    print("Testing ElevenLabs...")
    text_to_speech_with_elevenlabs(input_text, "elevenlabs_testing.mp3")
