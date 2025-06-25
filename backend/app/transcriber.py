# import whisper
# # from faster_whisper import WhisperModel
# import tempfile

# model = whisper.load_model("base")
# def transcribe_audio(audio_path):
#     result = model.transcribe(audio_path)
#     return result["text"].strip()
import assemblyai as aai


def transcribe_audio(audio_path):
    api_key="842dd84554cb4ab59e084cebc4762666"
    aai.settings.api_key = api_key
    # audio_file = "https://assembly.ai/wildfires.mp3"

    config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)

    transcript = aai.Transcriber(config=config).transcribe(audio_path)

    if transcript.status == "error":
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    return(transcript.text)

