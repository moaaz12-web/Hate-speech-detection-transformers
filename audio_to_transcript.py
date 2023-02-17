import whisper
from googletrans import Translator

audio_to_text_model = whisper.load_model("medium")

def audio_to_transcript(audio_path, output_language):
  try:
    result = audio_to_text_model.transcribe(audio_path)
  except Exception as e:
    print("Error transcribing audio file: ", e)
    return e

  try:
    translator = Translator()
    translated_transcript = translator.translate(result['text'], dest=output_language).text
  except Exception as e:
    print("Error translating transcript: ", e)
    return {"error": "An error occurred while translating the transcrip. Please try again later."}, 400

  return translated_transcript


# transcript = audio_to_trasncript('/content/Espanol.mp3', 'English')