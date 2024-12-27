import whisper

model = whisper.load_model("base")
def analyze_text(audio):
  result = model.transcribe(audio, fp16=False, language='pt', temperature=0)
  return result['text']