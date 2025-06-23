import whisper
import tempfile

model = whisper.load_model("base")

# def transcribe_audio(audio_bytes):
#     with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
#         tmp.write(audio_bytes)
#         tmp.flush()
#         result = model.transcribe(tmp.name)
#         return result["text"].strip()

def transcribe_audio(audio_path):
    result = model.transcribe(audio_path)
    return result["text"].strip()